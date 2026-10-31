const fs = require('fs');
const wsUrl = process.argv[2];
const msgFile = process.argv[3];
function getWS(){ let W=globalThis.WebSocket; if(!W){ try{W=require('ws');}catch(e){console.error('no ws');process.exit(3);} } return new W(wsUrl); }
function makeSender(ws){ let n=0; const p={}; ws.onmessage=(ev)=>{ let m; try{m=JSON.parse(ev.data);}catch(e){return;} if(m.id&&p[m.id]){ const r=m.result; const v=r&&r.result&&('value' in r.result)?r.result.value:r; p[m.id](v); delete p[m.id]; } }; return (method,params)=>new Promise((res,rej)=>{ const id=++n; p[id]=res; ws.send(JSON.stringify({id,method,params})); setTimeout(()=>{ if(p[id]){delete p[id]; rej(new Error('timeout '+method));} },15000); }); }
(async()=>{
const ws=getWS(); await new Promise((res,rej)=>{ws.onopen=res; ws.onerror=()=>rej(new Error('ws open'));} );
const send=makeSender(ws);
const MSG=fs.readFileSync(msgFile,'utf8');
const f=await send('Runtime.evaluate',{expression:`(()=>{const ta=document.querySelector('textarea[placeholder="Message"]');if(!ta)return 'NO_INPUT';ta.focus();ta.click();return 'FOCUSED';})()`,returnByValue:true});
console.log('focus:',f);
await send('Input.insertText',{text:MSG});
console.log('inserted len='+MSG.length);
await new Promise(r=>setTimeout(r,800));
const clicked=await send('Runtime.evaluate',{expression:`(()=>{const btns=Array.from(document.querySelectorAll('button'));const s=btns.find(b=>(b.getAttribute('aria-label')||'')==='Send');if(!s)return 'NO_SEND_BTN';s.click();return 'CLICKED';})()`,returnByValue:true});
console.log('send:',clicked);
await new Promise(r=>setTimeout(r,4000));
const v=await send('Runtime.evaluate',{expression:`(()=>{const t=document.body.innerText;const k='rewrite_s2';const i=t.lastIndexOf(k);return JSON.stringify({found:i>=0,len:t.length,tail:t.slice(-600)});})()`,returnByValue:true});
console.log(typeof v==='string'?v.slice(0,1200):JSON.stringify(v).slice(0,1200));
try{ws.close();}catch(e){} process.exit(0);
})().catch(e=>{console.error('ERR',e.message);process.exit(1);});
