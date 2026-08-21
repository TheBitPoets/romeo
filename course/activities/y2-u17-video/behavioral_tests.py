import pytest
from main import first_video_frame

class Camera:
    def __init__(self, frame): self.frame=frame; self.fps=[]
    def frames(self, frames_per_second): self.fps.append(frames_per_second); yield self.frame; raise AssertionError("consumato più di un frame")

def test_un_solo_frame_e_fps_inoltrato():
    camera=Camera(b"\xff\xd8body\xff\xd9")
    assert first_video_frame(camera, 7) == b"\xff\xd8body\xff\xd9"
    assert camera.fps == [7]

def test_rifiuta_frame_non_jpeg():
    with pytest.raises(ValueError): first_video_frame(Camera(b"png"))
