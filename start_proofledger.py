"""
ProofLedger One-Click Launcher
Launches the FastAPI backend and opens the pre-built React dashboard in your browser.
"""
import sys
import webbrowser
import threading
import time
from pathlib import Path
import uvicorn

backend_dir = Path(__file__).resolve().parent / "backend"
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

def open_browser():
    time.sleep(1.5)
    webbrowser.open("http://localhost:8000")

if __name__ == "__main__":
    print("=" * 65)
    print("  ProofLedger: Autonomous AI Escrow & Milestone Verification via PayPal")
    print("  Target Categories: Agentic Commerce, PayPal + AI, Most Impactful")
    print("=" * 65)
    print("  Backend & Web Dashboard: http://localhost:8000")
    print("  Swagger API Docs:        http://localhost:8000/docs")
    print("=" * 65)
    
    # Auto-open browser in background thread
    threading.Thread(target=open_browser, daemon=True).start()
    
    # Run server
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=False)
