def download_photo(client):
    """Scarica e valida una foto JPEG dalla REST API."""
    response = client.get("/api/camera/photo")
    if response.status_code != 200:
        raise ValueError("foto non disponibile")
    if not response.headers.get("content-type", "").startswith("image/jpeg"):
        raise ValueError("media type inatteso")
    return response.content
