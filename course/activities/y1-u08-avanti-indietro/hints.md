# Hint progressivi

1. Esegui e osserva come cambia il tempo simulato durante `sleep`.
2. Aggiungi dopo il primo secondo `backward(0.4)` e un secondo `sleep(1)`.
3. Termina con `stop()` e confronta posizione iniziale e finale.

## Se qualcosa non funziona

- Pensare che `sleep` significhi stop: i motori mantengono l'ultimo comando.
- Usare durate diverse senza aggiornare la previsione della posa finale.
- Mettere `stop()` tra il comando e il relativo `sleep`, annullando il movimento.
