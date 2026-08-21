import io
import main
import pytest

class Response(io.BytesIO):
    def __init__(self, body, status=200): super().__init__(body); self.status=status; self.closed_by_context=False
    def __enter__(self): return self
    def __exit__(self, *args): self.closed_by_context=True; self.close()

def test_get_json_e_cleanup(monkeypatch):
    response = Response(b'{"status":"ready"}')
    monkeypatch.setattr(main.urllib.request, "urlopen", lambda url, timeout: response)
    assert main.fetch_status("http://127.0.0.1/status") == {"status":"ready"}
    assert response.closed_by_context

def test_rifiuta_status_non_200(monkeypatch):
    monkeypatch.setattr(main.urllib.request, "urlopen", lambda url, timeout: Response(b'{}', 503))
    with pytest.raises(ValueError): main.fetch_status("http://local/status")
