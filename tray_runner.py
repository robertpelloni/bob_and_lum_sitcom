#!/usr/bin/env python3
"""Desktop System Tray Controller for Bob & Lum Sitcom Dashboard & Services.

Features:
  - Generates custom system tray icon with Bob & Lum brand colors.
  - Controls local dashboard HTTP server (Start / Stop / Restart).
  - Open Dashboard directly in the default web browser.
  - Run automated corpus verification check.
  - Safely quit all backend processes.

Usage:
  python3 tray_runner.py [--port 8080] [--headless]
"""
import argparse
import os
import signal
import subprocess
import sys
import threading
import time
import webbrowser
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent
DASHBOARD_SCRIPT = REPO_ROOT / "dashboard.py"
MANAGE_SCRIPT = REPO_ROOT / "transcribeme" / "manage_corpus.py"

dashboard_process = None
server_lock = threading.Lock()


def create_tray_image():
    """Dynamically generate a 64x64 icon for the system tray."""
    try:
        from PIL import Image, ImageDraw
        img = Image.new("RGBA", (64, 64), color=(0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        # Background circle
        draw.ellipse([4, 4, 60, 60], fill=(22, 27, 34), outline=(88, 166, 255), width=3)
        # 'B' & 'L' in gold and blue
        draw.text((14, 18), "B", fill=(88, 166, 255))
        draw.text((36, 18), "L", fill=(227, 179, 65))
        return img
    except Exception:
        return None


def start_server(port=8080):
    global dashboard_process
    with server_lock:
        if dashboard_process and dashboard_process.poll() is None:
            print(f"Dashboard server is already running (PID: {dashboard_process.pid})")
            return
        cmd = [sys.executable, str(DASHBOARD_SCRIPT), "--port", str(port)]
        dashboard_process = subprocess.Popen(cmd, cwd=str(REPO_ROOT))
        print(f"Started Bob & Lum Dashboard on http://localhost:{port} (PID: {dashboard_process.pid})")


def stop_server():
    global dashboard_process
    with server_lock:
        if dashboard_process and dashboard_process.poll() is None:
            print(f"Stopping dashboard server (PID: {dashboard_process.pid})...")
            dashboard_process.terminate()
            try:
                dashboard_process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                dashboard_process.kill()
            dashboard_process = None
            print("Dashboard server stopped.")
        else:
            print("Dashboard server is not running.")


def restart_server(port=8080):
    stop_server()
    time.sleep(0.5)
    start_server(port)


def open_browser(port=8080):
    url = f"http://localhost:{port}"
    print(f"Opening browser to {url}...")
    webbrowser.open(url)


def run_integrity_check():
    print("Running corpus integrity check...")
    subprocess.run([sys.executable, str(MANAGE_SCRIPT), "--check"], cwd=str(REPO_ROOT))


def quit_all(icon=None):
    print("Shutting down all Bob & Lum services...")
    stop_server()
    if icon:
        icon.stop()
    sys.exit(0)


def setup_tray(port=8080):
    try:
        import pystray
        from pystray import MenuItem as item
    except ImportError:
        print("pystray is not installed. Running in CLI mode.")
        return False

    image = create_tray_image()
    if not image:
        return False

    def on_open(icon, _):
        open_browser(port)

    def on_start(icon, _):
        start_server(port)

    def on_stop(icon, _):
        stop_server()

    def on_restart(icon, _):
        restart_server(port)

    def on_check(icon, _):
        run_integrity_check()

    def on_quit(icon, _):
        quit_all(icon)

    menu = (
        item("Open Sitcom Dashboard", on_open, default=True),
        item("Start Dashboard Server", on_start),
        item("Stop Dashboard Server", on_stop),
        item("Restart Dashboard Server", on_restart),
        item("Check Corpus Integrity", on_check),
        item("Quit All", on_quit),
    )

    icon = pystray.Icon("bob_and_lum", image, "Bob & Lum Sitcom", menu)
    return icon


def main():
    parser = argparse.ArgumentParser(description="Bob & Lum Sitcom System Tray Controller")
    parser.add_argument("--port", type=int, default=8080, help="Dashboard server port (default: 8080)")
    parser.add_argument("--headless", action="store_true", help="Run without graphical system tray (CLI mode)")
    args = parser.parse_args()

    # Automatically start dashboard server on launch
    start_server(args.port)

    if args.headless or not os.environ.get("DISPLAY"):
        print("Graphical display not detected or --headless specified. Running in CLI daemon mode.")
        print("Press Ctrl+C to stop services and exit.")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            quit_all()
    else:
        icon = setup_tray(args.port)
        if icon:
            print("System tray icon running. Right click for options.")
            icon.run()
        else:
            print("Could not initialize system tray. Running in fallback mode.")
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                quit_all()


if __name__ == "__main__":
    main()
