# Hint progressivi

1. Avvia lo scaffold e completa soltanto il blocco client.
2. Aggiungi timeout e verifica la risposta prima del marker.
3. Esegui due volte e controlla che thread e socket vengano sempre chiusi.

## Se qualcosa non funziona

- Chiamare `connect` prima che il listener sia pronto.
- Confondere il socket listener con quello della connessione accettata.
- Usare `recv` senza timeout durante il debug.
