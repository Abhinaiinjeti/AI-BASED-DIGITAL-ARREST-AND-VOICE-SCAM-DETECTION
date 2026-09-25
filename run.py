"""
Single-Command Unified Launcher
AI-BASED DIGITAL ARREST AND VOICE SCAM DETECTION

Launches both the FastAPI backend server (:8000) and the Vite React frontend (:5173)
concurrently with a single command:
    python run.py
"""

import os
import sys
import subprocess
import time
import webbrowser
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR / "frontend"


def main():
    print("=" * 65)
    print("AI-BASED DIGITAL ARREST AND VOICE SCAM DETECTION")
    print("Starting Integrated Prototype (Backend + Frontend)...")
    print("=" * 65)

    # Detect npm command for Windows
    npm_cmd = "npm.cmd" if sys.platform == "win32" else "npm"

    # Start FastAPI Backend
    print("[1/2] Launching FastAPI Backend on http://127.0.0.1:8000 ...")
    backend_proc = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "backend.app.main:app",
            "--host",
            "127.0.0.1",
            "--port",
            "8000",
        ],
        cwd=str(BASE_DIR),
    )

    # Brief delay for backend startup
    time.sleep(2)

    # Start React Vite Frontend
    print("[2/2] Launching Vite Frontend on http://localhost:5173 ...")
    frontend_proc = subprocess.Popen(
        [npm_cmd, "run", "dev"],
        cwd=str(FRONTEND_DIR),
    )

    print("\n" + "=" * 65)
    print("[+] APPLICATION IS RUNNING!")
    print("    Frontend UI:  http://localhost:5173")
    print("    Backend API: http://127.0.0.1:8000")
    print("    API Docs:    http://127.0.0.1:8000/docs")
    print("=" * 65)
    print("Press Ctrl+C to terminate both servers.\n")

    # Open web browser automatically
    time.sleep(1.5)
    try:
        webbrowser.open("http://localhost:5173")
    except Exception:
        pass

    try:
        while True:
            time.sleep(1)
            # Check if any process terminated prematurely
            if backend_proc.poll() is not None:
                print("[-] Backend process terminated.")
                break
            if frontend_proc.poll() is not None:
                print("[-] Frontend process terminated.")
                break
    except KeyboardInterrupt:
        print("\n[*] Gracefully stopping servers...")
    finally:
        if backend_proc.poll() is None:
            backend_proc.terminate()
        if frontend_proc.poll() is None:
            frontend_proc.terminate()
        print("[+] All services stopped successfully.")


if __name__ == "__main__":
    main()
