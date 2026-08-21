"""Collegati a /ws/control, invia STOP e verifica l'ack."""

from fastapi.testclient import TestClient
from romeo.web import create_app

# 1. Prepara gli endpoint o i dati.
# 2. Esegui l'operazione e valida la risposta con assert.
# 3. Stampa il marker richiesto solo dopo le verifiche.
