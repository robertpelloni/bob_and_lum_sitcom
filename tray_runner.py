#!/usr/bin/env python3
"""Desktop System Tray Controller for Bob & Lum Sitcom Dashboard.

Tray menu: Open Dashboard / Start / Stop / Restart / Check Corpus Integrity /
View Log / Quit All (stops dashboard + tray). Dashboard child runs hidden,
BelowNormal, bound to 127.0.0.1, logging to dashboard.log.

Usage: python tray_runner.py [--port 8765] [--headless]
Windows: tray mode by default (DISPLAY is a Unix concept - do not gate on it).
"""
import argparse, json, os, subprocess, sys, threading, time, urllib.request, webbrowser
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parent
DASHBOARD_SCRIPT = REPO_ROOT / "dashboard.py"
MANAGE_SCRIPT = REPO_ROOT / "transcribeme" / "manage_corpus.py"
LOG_PATH = REPO_ROOT / "dashboard.log"
DEFAULT_PORT = 8765
dashboard_process = None
server_lock = threading.Lock()

def dashboard_alive(port):
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/api/status", timeout=2) as r:
            return json.loads(r.read().decode()).get("app") == "bob-and-lum-dashboard"
    except Exception:
        return False

def create_tray_image():
    try:
        from PIL import Image, ImageDraw
        img = Image.new("RGBA", (64, 64), color=(0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        d.ellipse([4, 4, 60, 60], fill=(22, 27, 34), outline=(88, 166, 255), width=3)
        d.text((14, 20), "B", fill=(88, 166, 255)); d.text((36, 20), "L", fill=(227, 179, 65))
        return img
    except Exception:
        return None

def start_server(port=DEFAULT_PORT):
    global dashboard_process
    with server_lock:
        if dashboard_process and dashboard_process.poll() is None:
            print(f"Dashboard already running (PID {dashboard_process.pid})"); return
        if dashboard_alive(port):
            print(f"Dashboard already answering on http://127.0.0.1:{port} (external process)"); return
        flags = 0
        if os.name == "nt":
            flags = getattr(subprocess, "CREATE_NO_WINDOW", 0x08000000) | 0x00004000  # no window + BELOW_NORMAL
        log = open(LOG_PATH, "a", encoding="utf-8")
        dashboard_process = subprocess.Popen([sys.executable, str(DASHBOARD_SCRIPT), "--port", str(port), "--host", "127.0.0.1"],
            cwd=str(REPO_ROOT), stdout=log, stderr=log, creationflags=flags)
        print(f"Started dashboard http://127.0.0.1:{port} (PID {dashboard_process.pid}, BelowNormal, log dashboard.log)")

def stop_server():
    global dashboard_process
    with server_lock:
        if dashboard_process and dashboard_process.poll() is None:
            dashboard_process.terminate()
            try: dashboard_process.wait(timeout=3)
            except subprocess.TimeoutExpired: dashboard_process.kill()
            print("Dashboard stopped."); dashboard_process = None
        else:
            print("Dashboard child not running (external instances are left alone - use Quit on their page).")

def restart_server(port=DEFAULT_PORT):
    stop_server(); time.sleep(0.5); start_server(port)

def run_integrity_check():
    print("Running corpus integrity check (BelowNormal child)...")
    flags = 0x00004000 if os.name == "nt" else 0
    try: subprocess.run([sys.executable, str(MANAGE_SCRIPT), "--check"], cwd=str(REPO_ROOT), creationflags=flags)
    except Exception as e: print(f"check failed: {e}")

def view_log():
    try:
        if os.name == "nt": os.startfile(str(LOG_PATH))  # type: ignore[attr-defined]
        else: subprocess.Popen(["xdg-open", str(LOG_PATH)])
    except Exception: print(f"Log: {LOG_PATH}")

def quit_all(icon=None):
    print("Shutting down Bob & Lum dashboard + tray...")
    stop_server()
    if icon: icon.stop()
    os._exit(0)

def setup_tray(port):
    try:
        import pystray
        from pystray import MenuItem as item
    except ImportError:
        print("pystray not installed. Run: pip install pystray pillow"); return None
    image = create_tray_image()
    if not image:
        print("Pillow not installed / icon failed. Run: pip install pillow"); return None
    menu = (
        item("Open Sitcom Dashboard", lambda i, _: webbrowser.open(f"http://127.0.0.1:{port}"), default=True),
        item("Start Dashboard Server", lambda i, _: start_server(port)),
        item("Stop Dashboard Server", lambda i, _: stop_server()),
        item("Restart Dashboard Server", lambda i, _: restart_server(port)),
        item("Check Corpus Integrity", lambda i, _: threading.Thread(target=run_integrity_check, daemon=True).start()),
        item("View dashboard.log", lambda i, _: view_log()),
        item("Quit All", lambda i, _: quit_all(i)),
    )
    return pystray.Icon("bob_and_lum", image, f"Bob & Lum Sitcom (:{port})", menu)

def main():
    ap = argparse.ArgumentParser(description="Bob & Lum Sitcom System Tray Controller")
    ap.add_argument("--port", type=int, default=DEFAULT_PORT)
    ap.add_argument("--headless", action="store_true", help="CLI daemon mode, no tray icon")
    a = ap.parse_args()
    start_server(a.port)
    # BUGFIX (v1.5.0): old code required $DISPLAY, which never exists on Windows -> tray never appeared.
    want_tray = not a.headless and (sys.platform == "win32" or bool(os.environ.get("DISPLAY")) or sys.platform == "darwin")
    if not want_tray:
        print("Headless/CLI mode. Ctrl+C to stop.")
        try:
            while True: time.sleep(1)
        except KeyboardInterrupt: quit_all()
    else:
        icon = setup_tray(a.port)
        if icon:
            print(f"System tray icon running (dashboard :{a.port}). Right-click for Open/Start/Stop/Restart/Check/Log/Quit.")
            icon.run()
        else:
            print("Tray init failed; CLI mode. Ctrl+C to stop.")
            try:
                while True: time.sleep(1)
            except KeyboardInterrupt: quit_all()
if __name__ == "__main__": main()
