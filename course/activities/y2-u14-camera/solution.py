def capture_photo(camera):
    """Acquisisce una foto usando il servizio ricevuto."""
    photo = camera.capture_photo()
    if not isinstance(photo, bytes):
        raise ValueError("la foto deve essere bytes")
    return photo
