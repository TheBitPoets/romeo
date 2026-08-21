import json
import urllib.request

def fetch_status(url):
    """Esegue GET e restituisce il body JSON di una risposta 200."""
    with urllib.request.urlopen(url, timeout=2.0) as response:
        if response.status != 200:
            raise ValueError("status HTTP inatteso")
        return json.load(response)
