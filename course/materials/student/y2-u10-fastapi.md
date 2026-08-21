# Secondo anno 10. Costruisci una API FastAPI

## Obiettivo

In questa unità imparerai a definire un endpoint tipizzato.

## Che cosa sai già

Sai definire funzioni Python e conosci route REST, status e JSON.

## Modello mentale

FastAPI collega una coppia metodo+path a una normale funzione Python. Il decorator `@app.get` registra la route: non cambia il ragionamento dentro la funzione. TestClient avvia l'app in memoria; nasconde socket e thread per farci concentrare sulla route.

## Esempio minimo commentato

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/status")          # registra GET /status
def status() -> dict[str, object]:
    return {"ready": True}  # FastAPI lo converte in JSON
```

La firma tipizzata documenta il valore restituito; OpenAPI descrive automaticamente le route registrate.

## Prova guidata

1. Leggi decorator, firma e return separatamente.
2. Completa il solo dizionario restituito dalla route fornita.
3. Usa TestClient per verificare status e JSON.
4. Apri `/openapi.json` e trova il path registrato.
5. Aggiungi una seconda route semplice senza copiare tutta l'app.

## Esercizio base

Implementa `GET /status` con risposta tipizzata e testala.

## Esercizio intermedio

Aggiungi `GET /info` con nome e versione e verifica entrambe le route.

## Mini-sfida

Aggiungi un parametro di path semplice e verifica anche il caso non valido restituito dal framework.

## Consegna valutata

Completa `create_status_app` nello starter senza rinominare le funzioni. Rispetta parametri, valore restituito e cleanup descritti nella docstring: TheBitLab importerà le funzioni e le proverà con input diversi. Obiettivo: definire un endpoint tipizzato.

## Errori tipici

- Dimenticare `@` davanti al decorator.
- Restituire testo che sembra JSON invece di un dizionario Python.
- Confondere il path della route con il nome della funzione.

## Autoverifica

- So indicare quale riga registra la route?
- So spiegare chi converte il dizionario in JSON?
- So trovare la route nello schema OpenAPI?

## Accessibilità

Mostra il codice con annotazioni testuali, non solo evidenziazione sintattica; fornisci una tabella route→funzione.

## Parole nuove

| Termine | Significato in questa lezione |
| --- | --- |
| `route` | associazione fra metodo, path e funzione |
| `decorator` | riga con `@` che registra la funzione nel framework |
| `OpenAPI` | descrizione strutturata dell'API |
