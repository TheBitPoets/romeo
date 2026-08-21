import pytest
from main import is_loopback

def test_classifica_indirizzi_diversi():
    assert is_loopback("127.0.0.1") is True
    assert is_loopback("127.2.3.4") is True
    assert is_loopback("192.0.2.4") is False

def test_rifiuta_testo_non_ip():
    with pytest.raises(ValueError):
        is_loopback("romeo.local")
