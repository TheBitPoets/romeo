# Secondo anno 8. Una richiesta HTTP

## Obiettivo

In questa unità imparerai a riconoscere metodo, status e body.

## Che cosa sai già

Conosci client/server, endpoint, protocollo testuale e JSON.

## Modello mentale

HTTP organizza uno scambio in request e response. La request contiene metodo e risorsa; la response contiene status, header e body. Il server e il thread sono già nello scaffold: oggi leggiamo il protocollo, non implementiamo ancora un server web.

## Esempio minimo commentato

```text
GET /status HTTP/1.1       ← metodo e risorsa

HTTP/1.1 200 OK           ← status
Content-Type: application/json

{"status": "ok"}          ← body
```

```python
with urllib.request.urlopen(url, timeout=2) as risposta:
    print(risposta.status, risposta.headers["Content-Type"])
```


## Prova guidata

1. Etichetta metodo, path, status, header e body nell'esempio.
2. Prevedi il significato di 200 e 404.
3. Interroga il server locale fornito dallo scaffold.
4. Verifica status e Content-Type prima di leggere il JSON.
5. Richiedi un path inesistente e osserva la risposta d'errore.

## Esercizio base

Esegui GET sul server locale fornito e valida status 200 e body JSON.

## Esercizio intermedio

Gestisci separatamente una risposta 404 senza dichiarare successo.

## Mini-sfida

Confronta due response con lo stesso body ma Content-Type diversi e spiega quale rispetta il contratto.

## Consegna valutata

Completa `fetch_status` nello starter senza rinominare le funzioni. Rispetta parametri, valore restituito e cleanup descritti nella docstring: TheBitLab importerà le funzioni e le proverà con input diversi. Obiettivo: riconoscere metodo, status e body.

## Errori tipici

- Guardare soltanto il body e ignorare lo status.
- Confondere metodo HTTP e nome della funzione Python.
- Costruire subito server, thread e handler senza isolare il concetto HTTP.

## Autoverifica

- So scomporre una request?
- So scomporre una response?
- So verificare status e media type prima del body?

## Accessibilità

Presenta request e response come testo copiabile oltre al diagramma; pronuncia i codici cifra per cifra e spiegane il significato.

## Parole nuove

| Termine | Significato in questa lezione |
| --- | --- |
| `request` | messaggio inviato dal client HTTP |
| `response` | risposta del server HTTP |
| `header` | metadato della richiesta o risposta |
| `body` | contenuto del messaggio |
