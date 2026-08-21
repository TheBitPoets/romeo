"""Servi JSON su loopback, esegui GET e verifica status 200."""

import json
import threading
import urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer

# 1. Prepara gli endpoint o i dati.
# 2. Esegui l'operazione e valida la risposta con assert.
# 3. Stampa il marker richiesto solo dopo le verifiche.
