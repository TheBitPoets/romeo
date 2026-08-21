import pytest
from main import capture_photo

class Camera:
    def __init__(self, photo): self.photo=photo; self.calls=0
    def capture_photo(self): self.calls+=1; return self.photo

def test_usa_il_servizio_iniettato_una_volta():
    camera=Camera(b"photo-17")
    assert capture_photo(camera) == b"photo-17" and camera.calls == 1

def test_rifiuta_un_risultato_non_bytes():
    with pytest.raises(ValueError): capture_photo(Camera("photo"))
