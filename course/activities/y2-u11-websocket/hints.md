# Hint progressivi

1. Collegati al server fornito e verifica `ready`.
2. Invia STOP e valida l'ack completo.
3. Chiudi senza inviare altri dati e verifica che il robot resti fermo.

## Se qualcosa non funziona

- Inviare prima di leggere il messaggio ready previsto.
- Confondere WebSocket con una serie di GET HTTP.
- Uscire senza verificare lo STOP alla disconnessione.
