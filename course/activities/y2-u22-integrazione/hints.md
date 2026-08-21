# Hint progressivi

1. Invia FORWARD e attendi ack.
2. Leggi uno state e verifica movimento e versione.
3. Chiudi il controller e verifica uno state successivo con motori a zero.

## Se qualcosa non funziona

- Usare REST polling e chiamarlo telemetria realtime.
- Considerare l'ack prova sufficiente del movimento.
- Chiudere il viewer ma lasciare vivo il controller senza timeout.
