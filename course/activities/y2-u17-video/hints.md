# Hint progressivi

1. Leggi due frame dal generatore mock fornito.
2. Verifica marker JPEG per entrambi.
3. Ispeziona una response MJPEG scaffolded e controlla il parametro boundary.

## Se qualcosa non funziona

- Chiamare MJPEG un singolo byte array JPEG.
- Confondere boundary e marker interni JPEG.
- Creare un ciclo infinito senza condizione di arresto o cleanup.
