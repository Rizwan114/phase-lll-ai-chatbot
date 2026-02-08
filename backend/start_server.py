import uvicorn
import os
from src.main import app

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    reload = os.getenv("RELOAD", "True").lower() == "true"

    print(f"Starting Todo Backend API on {host}:{port}")
    print(f"Reload mode: {reload}")

    uvicorn.run(
        "src.main:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )