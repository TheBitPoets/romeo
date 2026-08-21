# Hint progressivi

1. Tenta il claim da un secondo controller e osserva il rifiuto.
2. Rilascia nel `finally` e verifica zero.
3. Avanza il clock scaffolded senza comandi e verifica lo stop del watchdog.

## Se qualcosa non funziona

- Disattivare il watchdog proprio nel test che dovrebbe verificarlo.
- Fermare solo un motore.
- Affidarsi allo STOP manuale come unico percorso sicuro.
