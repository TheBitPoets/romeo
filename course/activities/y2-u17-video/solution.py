def first_video_frame(camera, fps=10):
    """Legge e valida il primo frame JPEG dello stream."""
    frame = next(camera.frames(frames_per_second=fps))
    if not frame.startswith(b"\xff\xd8") or not frame.endswith(b"\xff\xd9"):
        raise ValueError("frame JPEG non valido")
    return frame
