# Hint progressivi

1. Aggiungi la risposta `PONG` nella direzione opposta.
2. Verifica entrambi i byte ricevuti con `assert`.
3. Rimuovi temporaneamente l'invio di PONG e prevedi perché il client rimarrebbe in attesa.

## Se qualcosa non funziona

- Inviare una stringa invece di byte.
- Leggere prima che l'altra estremità abbia inviato.
- Credere che `recv(16)` restituisca sempre esattamente 16 byte.
