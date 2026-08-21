# Secondo anno 9. REST: leggere lo stato

## Obiettivo

In questa unità imparerai a consumare una risorsa JSON.

## Che cosa sai già

Sai leggere request e response HTTP e decodificare JSON.

## Modello mentale

REST tratta gli elementi del sistema come risorse con indirizzi stabili. `GET /api/status` chiede una rappresentazione dello stato; non significa 'esegui una funzione chiamata status'. TestClient sostituisce la rete esterna ma conserva metodo, path, status e body. FastAPI è nascosto nello scaffold fino alla prossima unità.

## Esempio minimo commentato

```python
with TestClient(create_app()) as client:  # app già fornita
    response = client.get("/api/status")
    assert response.status_code == 200
    stato = response.json()
    print(stato["status"])
```

Il client consuma la risorsa; non ha bisogno di conoscere come il server la costruisce.

## Prova guidata

1. Individua la risorsa nel path `/api/status`.
2. Prevedi quali parti della response vanno validate.
3. Esegui il client sul servizio fornito.
4. Controlla status, Content-Type e campi JSON.
5. Richiedi una risorsa inesistente e confronta il risultato.

## Esercizio base

Leggi `/api/status` e verifica il contratto minimo.

## Esercizio intermedio

Scrivi una funzione client che restituisce `moving` soltanto per una response valida.

## Mini-sfida

Progetta path e rappresentazione JSON per una risorsa `info` senza implementare il server.

## Consegna valutata

Interroga /api/status con TestClient e verifica il contratto.

## Errori tipici

- Chiamare REST qualsiasi risposta JSON.
- Inserire verbi come `getStatus` nel path senza ragionare sulla risorsa.
- Fidarsi del JSON senza controllare lo status.

## Autoverifica

- So spiegare che cosa rappresenta una risorsa?
- So distinguere HTTP da stile REST?
- Il mio client rifiuta response incomplete?

## Accessibilità

Scrivi sempre metodo e path insieme (`GET /api/status`) e accompagna ogni icona con un'etichetta testuale.

## Parole nuove

| Termine | Significato in questa lezione |
| --- | --- |
| `REST` | stile per organizzare risorse e operazioni HTTP |
| `risorsa` | elemento identificato da un path |
| `rappresentazione` | dati che descrivono una risorsa |
