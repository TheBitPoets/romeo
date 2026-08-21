from fastapi import FastAPI

def create_status_app():
    """Crea un'app FastAPI con GET /status."""
    app = FastAPI()
    @app.get("/status")
    def status():
        return {"robot": "romeo", "ready": True}
    return app
