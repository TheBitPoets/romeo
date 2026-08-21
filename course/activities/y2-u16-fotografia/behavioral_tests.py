import pytest
from main import download_photo

class Response:
    status_code=200; headers={"content-type":"image/jpeg"}; content=b"jpeg-variable"
class Client:
    def __init__(self): self.paths=[]
    def get(self,path): self.paths.append(path); return Response()

def test_path_media_type_e_contenuto():
    client=Client(); assert download_photo(client) == b"jpeg-variable"
    assert client.paths == ["/api/camera/photo"]
