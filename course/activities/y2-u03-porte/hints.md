# Hint progressivi

1. Esegui due volte e registra le porte scelte.
2. Estrai la porta con `listener.getsockname()[1]`.
3. Verifica che sia compresa fra 1 e 65535 prima di stampare il marker.

## Se qualcosa non funziona

- Usare soltanto la porta e dimenticare l'indirizzo.
- Pensare che `0` sia la porta finale assegnata.
- Dimenticare di chiudere il socket dopo l'esperimento.
