# Hint progressivi

1. Interroga il server locale fornito dallo scaffold.
2. Verifica status e Content-Type prima di leggere il JSON.
3. Richiedi un path inesistente e osserva la risposta d'errore.

## Se qualcosa non funziona

- Guardare soltanto il body e ignorare lo status.
- Confondere metodo HTTP e nome della funzione Python.
- Costruire subito server, thread e handler senza isolare il concetto HTTP.
