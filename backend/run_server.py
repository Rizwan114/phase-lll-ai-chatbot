import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

if __name__ == "__main__":
    # Get host and port from environment variables, with defaults
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", 8000))
    debug = os.getenv("DEBUG", "false").lower() == "true"

    print(f"Starting server on {host}:{port}")
    print(f"Debug mode: {debug}")
    print(f"Database URL: {os.getenv('DATABASE_URL', 'Not set')[:50]}...")

    # Run the application
    uvicorn.run(
        "src.main:app",
        host=host,
        port=port,
        reload=debug,  # Enable auto-reload in debug mode
        log_level=os.getenv("LOG_LEVEL", "info")
    )