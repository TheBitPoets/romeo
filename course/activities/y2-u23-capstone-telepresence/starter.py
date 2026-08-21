"""Verifica foto, stato, controllo WebSocket e stop alla fine della sessione."""

from fastapi.testclient import TestClient
from romeo.camera.mock import MockCameraService
from romeo.web import create_app

# 1. Prepara gli endpoint o i dati.
# 2. Esegui l'operazione e valida la risposta con assert.
# 3. Stampa il marker richiesto solo dopo le verifiche.
