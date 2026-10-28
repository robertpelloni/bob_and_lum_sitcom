// CDP helper for the muse.ai "Chat — Bobbi" page target only.
// modes: inspect                 -> rich input/button dump (read-only)
//        input-post <msgFile>    -> focus + Input.insertText + Enter (real key)
const mode = process.argv[2];
const url = process.argv[3];
const fs = require('fs');

function getWS() {
  let W = globalThis.WebSocket;
  if (!W) { try { W = require('ws'); } catch (e) { console.error('no ws'); process.exit(3); } }
  return new W(url);
}

function makeSender(ws) {
  let nextId = 0;
  const pending = {};
  ws.onmessage = (ev) => {
    let m; try { m = JSON.parse(ev.data); } catch (e) { return; }
    if (m.id && pending[m.id]) {
      const res = m.result;
      const val = res && res.result && ('value' in res.result) ? res.result.value : res;
      pending[m.id](val); delete pending[m.id];
    }
  };
  return (method, params) => new Promise((resolve, reject) => {
    const id = ++nextId;
    pending[id] = resolve;
    ws.send(JSON.stringify({ id, method, params }));
    setTimeout(() => { if (pending[id]) { delete pending[id]; reject(new Error('timeout ' + method)); } }, 15000);
  });
}

(async () => {
  const ws = getWS();
  await new Promise((res, rej) => { ws.onopen = res; ws.onerror = () => rej(new Error('ws open error')); });
  const send = makeSender(ws);

  if (mode === 'inspect') {
    const expr = `(() => {
      const ta = document.querySelector('textarea[placeholder="Message"], textarea[aria-label="Message"], textarea');
      const allBtns = Array.from(document.querySelectorAll('button, [role="button"], input[type="submit"]'));
      const info = allBtns.map((b,i)=>({i, tag:b.tagName, type:b.type||'', aria:b.getAttribute('aria-label')||'', txt:(b.innerText||'').trim().slice(0,20), title:b.getAttribute('title')||'', disabled:b.disabled||false, cls:(b.className||'').toString().slice(0,40)}));
      const sendish = info.filter(b=>/send|submit|arrow|paper|plane/i.test((b.aria||'')+' '+(b.txt||'')+' '+(b.title||'')));
      return JSON.stringify({
        taFound: !!ta, taPlaceholder: ta && ta.placeholder, taAria: ta && ta.getAttribute('aria-label'),
        taInForm: !!(ta && ta.closest('form')), taParentBtns: ta ? Array.from(ta.parentElement.parentElement.querySelectorAll('button')).map(b=>({aria:b.getAttribute('aria-label')||'', txt:(b.innerText||'').trim().slice(0,20), type:b.type||''})) : [],
        totalButtons: allBtns.length, sendish, last10: info.slice(-10)
      });
    })()`;
    const v = await send('Runtime.evaluate', { expression: expr, returnByValue: true });
    console.log(typeof v === 'string' ? v : JSON.stringify(v, null, 2));
  } else if (mode === 'input-post') {
    const MSG = fs.readFileSync(process.argv[4], 'utf8');
    // 1) focus the input
    const focusExpr = `(() => { const ta = document.querySelector('textarea[placeholder="Message"], textarea[aria-label="Message"], textarea'); if(!ta) return 'NO_INPUT'; ta.focus(); ta.click(); return 'FOCUSED'; })()`;
    const fval = await send('Runtime.evaluate', { expression: focusExpr, returnByValue: true });
    console.log('focus:', fval);
    // 2) insert text as real typing
    await send('Input.insertText', { text: MSG });
    console.log('insertText: done, len=' + MSG.length);
    // 3) press Enter to submit (real key events)
    await send('Input.dispatchKeyEvent', { type: 'rawKeyDown', windowsVirtualKeyCode: 13, code: 'Enter', key: 'Enter' });
    await send('Input.dispatchKeyEvent', { type: 'char', windowsVirtualKeyCode: 13, text: '\r', unmodifiedText: '\r' });
    await send('Input.dispatchKeyEvent', { type: 'keyUp', windowsVirtualKeyCode: 13, code: 'Enter', key: 'Enter' });
    console.log('enter: sent');
  } else if (mode === 'verify') {
    const expr = `(() => {
      const ta = document.querySelector('textarea[placeholder="Message"], textarea[aria-label="Message"], textarea');
      return JSON.stringify({ composerLen: ta ? ta.value.length : -1, composerText: ta ? ta.value.slice(0,140) : '', threadTail: document.body.innerText.slice(-1600) });
    })()`;
    const v = await send('Runtime.evaluate', { expression: expr, returnByValue: true });
    console.log(typeof v === 'string' ? v : JSON.stringify(v, null, 2));
  } else if (mode === 'search') {
    const needle = process.argv[4] || 'verification packet';
    const expr2 = "(() => { const t = document.body.innerText; const idx = t.lastIndexOf('" + needle.replace(/'/g, '') + "'); if (idx < 0) return JSON.stringify({found:false, len:t.length, tail:t.slice(-400)}); return JSON.stringify({found:true, len:t.length, after:t.slice(idx, idx+5000)}); })()";
    const v2 = await send('Runtime.evaluate', { expression: expr2, returnByValue: true });
    console.log(typeof v2 === 'string' ? v2 : JSON.stringify(v2, null, 2));
  }

  try { ws.close(); } catch (e) {}
  process.exit(0);
})().catch(e => { console.error('ERR', e.message); process.exit(1); });
