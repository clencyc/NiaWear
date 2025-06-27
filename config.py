from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

def configure_app(app):
    # Load environment variables
    load_dotenv()

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:8080"],
        allow_methods=["*"],
        allow_headers=["*"],
    )
