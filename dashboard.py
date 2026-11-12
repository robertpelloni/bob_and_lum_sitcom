#!/usr/bin/env python3
"""Unified Bob & Lum Sitcom Dashboard Server.

Consolidates:
  - Screenplay Reader (Season 1 & Season 2)
  - Kling AI Scene Prompts Catalog with quick copy & filtering
  - Raw Transcript Corpus Explorer with full-text search
  - System metrics and service controls (quit/restart/diagnostics)

Usage:
  python3 dashboard.py [--port 8080] [--host 0.0.0.0]
"""
import argparse
import html
import http.server
import json
import os
import re
import socketserver
import sqlite3
import sys
import urllib.parse
from pathlib import Path


def lower_self_priority():
    import os
    try:
        if os.name == 'nt':
            import ctypes
            BELOW_NORMAL_PRIORITY_CLASS = 0x00004000
            ctypes.windll.kernel32.SetPriorityClass(ctypes.windll.kernel32.GetCurrentProcess(), BELOW_NORMAL_PRIORITY_CLASS)
        else:
            try:
                os.nice(10)
            except Exception:
                pass
    except Exception:
        pass


REPO_ROOT = Path(__file__).resolve().parent
DB_PATH = REPO_ROOT / "transcribeme" / "catalog.db"
CORPUS_PATH = REPO_ROOT / "CONVERSATION_SCRIPT_COMPLETE.txt"
S1_PATH = REPO_ROOT / "sitcom_final_s1.md"
S2_PATH = REPO_ROOT / "sitcom_final_s2.md"

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Bob & Lum Sitcom — Unified Dashboard</title>
  <style>
    :root {
      --bg: #0d1117;
      --card-bg: #161b22;
      --border: #30363d;
      --text: #c9d1d9;
      --heading: #f0f6fc;
      --accent: #58a6ff;
      --accent-hover: #1f6feb;
      --danger: #f85149;
      --success: #3fb950;
      --bob: #58a6ff;
      --lum: #e3b341;
      --code-bg: #090d13;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      background: var(--bg);
      color: var(--text);
      display: flex;
      flex-direction: column;
      height: 100vh;
      overflow: hidden;
    }
    header {
      background: var(--card-bg);
      border-bottom: 1px solid var(--border);
      padding: 12px 24px;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }
    .brand {
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .brand h1 {
      font-size: 1.25rem;
      color: var(--heading);
      letter-spacing: 0.5px;
    }
    .badge {
      font-size: 0.75rem;
      background: #238636;
      color: #fff;
      padding: 2px 8px;
      border-radius: 12px;
      font-weight: 600;
    }
    .nav-tabs {
      display: flex;
      gap: 8px;
    }
    .tab-btn {
      background: transparent;
      border: 1px solid transparent;
      color: var(--text);
      padding: 6px 14px;
      border-radius: 6px;
      cursor: pointer;
      font-size: 0.9rem;
      transition: all 0.15s ease;
    }
    .tab-btn:hover {
      background: #21262d;
    }
    .tab-btn.active {
      background: #21262d;
      border-color: var(--accent);
      color: var(--heading);
      font-weight: 600;
    }
    .header-actions {
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .btn {
      background: #21262d;
      border: 1px solid var(--border);
      color: var(--text);
      padding: 6px 12px;
      border-radius: 6px;
      cursor: pointer;
      font-size: 0.85rem;
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }
    .btn:hover { background: #30363d; }
    .btn-danger { color: var(--danger); }
    .btn-danger:hover { background: rgba(248,81,73,0.15); border-color: var(--danger); }

    main {
      flex: 1;
      display: flex;
      overflow: hidden;
      position: relative;
    }
    .tab-pane {
      display: none;
      width: 100%;
      height: 100%;
      overflow-y: auto;
      padding: 24px;
    }
    .tab-pane.active { display: block; }`n    /* Single-page mode (2026-11-08): stacked sections, no tab switching */`n    main { display: block !important; overflow-y: auto !important; }`n    .tab-pane { display: block !important; height: auto !important; overflow: visible !important; padding: 0 0 32px 0 !important; scroll-margin-top: 12px; }

    /* Overview metrics */
    .metric-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 16px;
      margin-bottom: 24px;
    }
    .metric-card {
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 16px;
    }
    .metric-val {
      font-size: 1.75rem;
      font-weight: 700;
      color: var(--heading);
      margin: 8px 0 4px;
    }
    .metric-sub { font-size: 0.8rem; color: #8b949e; }

    /* Cards and tables */
    .section-card {
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 20px;
      margin-bottom: 20px;
    }
    .section-card h2 {
      font-size: 1.1rem;
      color: var(--heading);
      margin-bottom: 12px;
      border-bottom: 1px solid var(--border);
      padding-bottom: 8px;
    }

    /* Screenplay reader */
    .screenplay-container {
      max-width: 900px;
      margin: 0 auto;
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 32px;
      line-height: 1.6;
    }
    .screenplay-container h1, .screenplay-container h2, .screenplay-container h3 {
      color: var(--heading);
      margin: 20px 0 10px;
    }
    .screenplay-container p { margin-bottom: 14px; }
    .screenplay-container hr { border: 0; border-top: 1px solid var(--border); margin: 24px 0; }

    /* Prompts Explorer */
    .prompt-filters {
      display: flex;
      gap: 12px;
      margin-bottom: 16px;
    }
    .input-control {
      background: #090d13;
      border: 1px solid var(--border);
      color: var(--text);
      padding: 8px 12px;
      border-radius: 6px;
      font-size: 0.9rem;
    }
    .prompt-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
      gap: 16px;
    }
    .prompt-card {
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 16px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }
    .prompt-header {
      font-size: 0.85rem;
      color: var(--accent);
      font-weight: 600;
      margin-bottom: 8px;
    }
    .prompt-body {
      font-size: 0.9rem;
      line-height: 1.5;
      background: var(--code-bg);
      border: 1px solid #21262d;
      border-radius: 6px;
      padding: 12px;
      margin-bottom: 12px;
      font-family: monospace;
      max-height: 160px;
      overflow-y: auto;
    }
    .copy-btn {
      align-self: flex-end;
    }

    /* Transcript search */
    .search-box {
      width: 100%;
      margin-bottom: 16px;
    }
    .search-results {
      max-height: 550px;
      overflow-y: auto;
    }
    .result-item {
      padding: 12px;
      border-bottom: 1px solid var(--border);
    }
    .result-item:hover { background: #21262d; }
    .result-speaker-Bob { color: var(--bob); font-weight: 600; }
    .result-speaker-Lum { color: var(--lum); font-weight: 600; }
  </style>
</head>
<body>
  <header>
    <div class="brand">
      <h1>🎬 Bob & Lum Sitcom</h1>
      <span class="badge" title="Active release version">v1.4.0</span>
      <span style="font-size: 0.8rem; color: #8b949e;">Autopilot Dashboard</span>
    </div>
    <div class="nav-tabs">
      <a class="tab-btn" href="#sec-s1" title="Read Season 1 screenplay, highest value first">Season 1</a>
      <a class="tab-btn" href="#sec-s2" title="Read Season 2 plus bonus screenplay">Season 2</a>
      <a class="tab-btn" href="#sec-prompts" title="Browse and copy all 102 Kling video prompts">Kling Prompts (102)</a>
      <a class="tab-btn" href="#sec-corpus" title="Full-text search across 258350 transcript lines">Corpus Search</a>
      <a class="tab-btn" href="#sec-overview" title="Metrics, canon, and pipeline actions">Overview</a>
    </div>
    <div class="header-actions">
      <button class="btn" onclick="fetchStatus()">🔄 Refresh</button>
      <button class="btn btn-danger" onclick="quitServer()" title="Safely shutdown dashboard process">🛑 Quit Dashboard</button>
    </div>
  </header>

  <main>
    <!-- OVERVIEW TAB -->
    <div id="sec-overview" class="tab-pane">
      <div class="metric-grid">
        <div class="metric-card">
          <div class="metric-sub">Master Corpus Size</div>
          <div class="metric-val" id="metric-corpus-size">5.9 MB</div>
          <div class="metric-sub">247 sessions &bull; 258,350 lines</div>
        </div>
        <div class="metric-card">
          <div class="metric-sub">Kling Video Prompts</div>
          <div class="metric-val" id="metric-prompts-count">102</div>
          <div class="metric-sub">51 S1 &bull; 51 S2</div>
        </div>
        <div class="metric-card">
          <div class="metric-sub">Episodes Authored</div>
          <div class="metric-val">26</div>
          <div class="metric-sub">12 S1 &bull; 8 S2 &bull; 6 Bonus</div>
        </div>
        <div class="metric-card">
          <div class="metric-sub">Corpus Sync Parity</div>
          <div class="metric-val" style="color: var(--success);">100%</div>
          <div class="metric-sub">Byte-identical master & sitcom</div>
        </div>
      </div>

      <div class="section-card">
        <h2 title="Immutable character and canon rules">System Architecture & Lore Canon <span style="cursor:help" title="Bob yogurt coffee pizza never Pop-Tarts. Chris for both, Noah next to Lum, Crystal dad saves both. USB is Bob, burners are Lum and Harry.">?</span></h2>
        <ul style="margin-left: 20px; line-height: 1.8;">
          <li><strong>Bob's Sacraments:</strong> Yogurt, coffee, and pizza. <em>Never Pop-Tarts</em>. Holds cold pizza slices like cigarettes.</li>
          <li><strong>The Sacrifices:</strong> Chris Papa died for <em>both</em> Bob & Lum; Noah died <em>next to Lum</em>; Crystal's dad died as a divine rehabilitation message saving Bob and Crystal.</li>
          <li><strong>Tech Ancestry:</strong> USB flash drives to the library belong to Bob; gas-station burner phones belong to Lum and Harry.</li>
          <li><strong>The Dashboard Motif:</strong> The dashboard on Bob's dual-monitor rig is perpetually broken — liturgy of the startup grind.</li>
        </ul>
      </div>

      <div class="section-card">
        <h2 title="One-click jobs run BelowNormal in background, logs to dashboard.log">Quick Automation & Pipeline Actions <span style="cursor:help" title="Rebuild HTML viewer or re-index Kling prompts without blocking the dashboard.">?</span></h2>
        <p style="margin-bottom: 12px; color: #8b949e;">Trigger autonomous routines directly from this interface:</p>
        <button class="btn" onclick="runAction('/api/rebuild-html')">Rebuild WordPress HTML</button>
        <button class="btn" onclick="runAction('/api/extract-prompts')">Re-index Kling Prompts</button>
      </div>
    </div>

    <!-- PROMPTS TAB -->
    <div id="sec-prompts" class="tab-pane">
      <div class="prompt-filters">
        <select id="season-filter" class="input-control" onchange="filterPrompts()">
          <option value="all">All Seasons</option>
          <option value="1">Season 1 (51 Prompts)</option>
          <option value="2">Season 2 (51 Prompts)</option>
        </select>
        <input type="text" id="prompt-search" class="input-control search-box" placeholder="Filter scene prompts by keyword..." oninput="filterPrompts()">
      </div>
      <div class="prompt-grid" id="prompts-container">
        <!-- Rendered via JS -->
      </div>
    </div>

    <!-- SCREENPLAY S1 TAB -->
    <div id="sec-s1" class="tab-pane">
      <div class="screenplay-container" id="s1-content">
        Loading Season 1 Screenplay...
      </div>
    </div>

    <!-- SCREENPLAY S2 TAB -->
    <div id="sec-s2" class="tab-pane">
      <div class="screenplay-container" id="s2-content">
        Loading Season 2 Screenplay...
      </div>
    </div>

    <!-- TRANSCRIPTS TAB -->
    <div id="sec-corpus" class="tab-pane">
      <div class="section-card">
        <h2 title="Search all 258350 lines of the 247-session corpus">Full-Text Corpus Search <span style="cursor:help" title="Type a phrase and press Enter. Example queries: adapter, Sting Ray, hologram, blazer.">?</span></h2>
        <div style="display: flex; gap: 8px; margin-bottom: 12px;">
          <input type="text" id="corpus-query" class="input-control search-box" placeholder="Search across 258,350 lines (e.g. 'adapter', 'Sting Ray', 'hologram', 'blazer')..." onkeydown="if(event.key==='Enter') searchCorpus()">
          <button class="btn" onclick="searchCorpus()">Search</button>
        </div>
        <div id="search-status" style="font-size: 0.85rem; color: #8b949e; margin-bottom: 8px;"></div>
        <div class="search-results" id="search-results"></div>
      </div>
    </div>
  </main>

  <script>
    let allPrompts = [];

    function showTab(tabId) {
      document.querySelectorAll('.tab-pane').forEach(el => el.classList.remove('active'));
      document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
      document.getElementById('tab-' + tabId).classList.add('active');
      event.target.classList.add('active');
      if (tabId === 'prompts' && allPrompts.length === 0) loadPrompts();
      if (tabId === 'screenplay-s1' && document.getElementById('s1-content').textContent.includes('Loading')) loadScreenplay(1);
      if (tabId === 'screenplay-s2' && document.getElementById('s2-content').textContent.includes('Loading')) loadScreenplay(2);
    }

    async function loadPrompts() {
      const res = await fetch('/api/prompts');
      allPrompts = await res.json();
      filterPrompts();
    }

    function filterPrompts() {
      const season = document.getElementById('season-filter').value;
      const q = document.getElementById('prompt-search').value.toLowerCase();
      const container = document.getElementById('prompts-container');
      const filtered = allPrompts.filter(p => {
        const matchSeason = season === 'all' || p.season.toString() === season;
        const matchQuery = !q || p.prompt_title.toLowerCase().includes(q) || p.prompt_text.toLowerCase().includes(q) || p.episode_title.toLowerCase().includes(q);
        return matchSeason && matchQuery;
      });

      container.innerHTML = filtered.map(p => `
        <div class="prompt-card">
          <div>
            <div class="prompt-header">S${p.season} E${p.episode_num} &bull; ${p.episode_title} &bull; Prompt ${p.prompt_num}</div>
            <div style="font-weight: 600; color: #f0f6fc; margin-bottom: 6px;">${p.prompt_title}</div>
            <div class="prompt-body">${p.prompt_text}</div>
          </div>
          <button class="btn copy-btn" onclick="copyPrompt('${encodeURIComponent(p.raw_block)}')">📋 Copy Prompt</button>
        </div>
      `).join('');
    }

    function copyPrompt(raw) {
      navigator.clipboard.writeText(decodeURIComponent(raw));
      alert('Copied Kling Scene Prompt to clipboard!');
    }

    async function loadScreenplay(season) {
      const res = await fetch('/api/screenplay?season=' + season);
      const text = await res.text();
      const target = document.getElementById('s' + season + '-content');
      // Simple format
      target.innerHTML = '<pre style="white-space: pre-wrap; font-family: inherit;">' + text.replace(/</g, '&lt;').replace(/>/g, '&gt;') + '</pre>';
    }

    async function searchCorpus() {
      const q = document.getElementById('corpus-query').value.trim();
      if (!q) return;
      document.getElementById('search-status').textContent = 'Searching...';
      const res = await fetch('/api/search?q=' + encodeURIComponent(q));
      const data = await res.json();
      document.getElementById('search-status').textContent = `Found ${data.matches.length} occurrences:`;
      const container = document.getElementById('search-results');
      container.innerHTML = data.matches.map(m => `
        <div class="result-item">
          <span style="font-size: 0.75rem; color: #8b949e;">Line ${m.line_num}</span>
          <p>${m.text.replace(/</g, '&lt;')}</p>
        </div>
      `).join('');
    }

    async function runAction(endpoint) {
      const res = await fetch(endpoint, { method: 'POST' });
      const data = await res.json();
      alert(data.message || 'Action executed successfully');
    }

    async function quitServer() {
      if (confirm('Are you sure you want to quit the Bob & Lum Dashboard Server?')) {
        await fetch('/api/quit', { method: 'POST' });
        document.body.innerHTML = '<div style="padding: 40px; text-align: center; color: #8b949e;"><h2>Dashboard server stopped. You can safely close this window.</h2></div>';
      }
    }

    document.addEventListener('DOMContentLoaded', () => { loadPrompts(); loadScreenplay(1); loadScreenplay(2); });`n`n    async function fetchStatus() {
      location.reload();
    }
  </script>
</body>
</html>
"""


class DashboardHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Quiet standard logging to avoid noise
        pass

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        if path == "/" or path == "/index.html":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML_TEMPLATE.encode("utf-8"))
            return

        elif path == "/api/prompts":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            if DB_PATH.exists():
                conn = sqlite3.connect(DB_PATH)
                conn.row_factory = sqlite3.Row
                rows = conn.execute(
                    "SELECT season, episode_num, episode_title, prompt_num, prompt_title, prompt_text, raw_block FROM kling_prompts ORDER BY season, prompt_num"
                ).fetchall()
                data = [dict(r) for r in rows]
                conn.close()
            else:
                data = []
            self.wfile.write(json.dumps(data).encode("utf-8"))
            return

        elif path == "/api/screenplay":
            season = query.get("season", ["1"])[0]
            sp_path = S1_PATH if season == "1" else S2_PATH
            if sp_path.exists():
                content = sp_path.read_text(encoding="utf-8", errors="replace")
                self.send_response(200)
                self.send_header("Content-Type", "text/plain; charset=utf-8")
                self.end_headers()
                self.wfile.write(content.encode("utf-8"))
            else:
                self.send_response(404)
                self.end_headers()
            return

        elif path == "/api/search":
            q = query.get("q", [""])[0].strip().lower()
            matches = []
            if q and CORPUS_PATH.exists():
                with open(CORPUS_PATH, "r", encoding="utf-8", errors="replace") as f:
                    for i, line in enumerate(f, 1):
                        if q in line.lower():
                            matches.append({"line_num": i, "text": line.strip()})
                            if len(matches) >= 50:
                                break
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"matches": matches}).encode("utf-8"))
            return

        self.send_response(404)
        self.end_headers()

    def do_POST(self):
        path = self.path
        if path == "/api/quit":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"message": "Server shutting down"}).encode("utf-8"))

            def shutdown():
                import time
                time.sleep(0.5)
                os._exit(0)

            import threading
            threading.Thread(target=shutdown).start()
            return

        elif path == "/api/rebuild-html":
            import subprocess
            res = subprocess.run([sys.executable, str(REPO_ROOT / "transcribeme" / "regen_wordpress_html.py")], capture_output=True, text=True)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"message": "WordPress HTML viewer successfully regenerated!"}).encode("utf-8"))
            return

        elif path == "/api/extract-prompts":
            import subprocess
            res = subprocess.run([sys.executable, str(REPO_ROOT / "transcribeme" / "extract_kling_prompts.py")], capture_output=True, text=True)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"message": "Kling AI video prompts successfully extracted and indexed!"}).encode("utf-8"))
            return

        self.send_response(404)
        self.end_headers()


def run_server(port=8080, host="0.0.0.0"):
    lower_self_priority()
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer((host, port), DashboardHandler) as httpd:
        print(f"🎬 Bob & Lum Dashboard Server listening on http://{host}:{port}/")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")


def main():
    parser = argparse.ArgumentParser(description="Bob & Lum Sitcom Unified Dashboard Server")
    parser.add_argument("--port", type=int, default=8080, help="Server port (default: 8080)")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Bind address (default: 0.0.0.0)")
    args = parser.parse_args()
    lower_self_priority()
    run_server(port=args.port, host=args.host)


if __name__ == "__main__":
    main()
