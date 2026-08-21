# 11. Scegli la velocità

## Obiettivo

In questo laboratorio imparerai a confrontare valori normalizzati tra 0 e 1.

## Che cosa sai già

Saper usare `forward`, `sleep` e `stop` e leggere posizione e tempo finali.

## Modello mentale

La velocità richiesta è un numero tra 0 e 1: zero significa fermo, uno è il limite configurato, e 0.5 è metà comando. A parità di scenario, distanza significa velocità per tempo. Cambiamo un solo valore alla volta per confrontare due prove.

## Esempio minimo commentato

```python
from time import sleep
from romeo.easy import forward, stop

forward(0.25)  # Un quarto del comando massimo.
sleep(2)       # Mantienilo per due secondi.
stop()
```

## Prova guidata

1. Annota posizione iniziale e durata prima del primo run.
2. Esegui l'esempio con velocità 0.25 e annota la posizione finale.
3. Ripeti con 0.5 senza cambiare la durata.
4. Confronta le due distanze e formula una frase, senza pretendere precisione dell'hardware reale.
5. Usa 0.5 per due secondi e verifica il target della consegna.

## Esercizio base

Raggiungi x=1.0 con velocità 0.5 per due secondi e fermati.

## Esercizio intermedio

Raggiungi la stessa posizione con una velocità più bassa e una durata adeguata.

## Mini-sfida

Prevedi una terza coppia velocità/durata equivalente e verifica la tolleranza finale.

## Consegna valutata

Raggiungi il target a x=1.0 usando velocità 0.5 per due secondi.

## Errori tipici

- Usare un valore fuori dall'intervallo da 0 a 1.
- Dimenticare che la partenza è x=0.5 e calcolare tutta la coordinata come distanza.
- Cambiare contemporaneamente velocità e target senza poter confrontare i run.

## Autoverifica

- So spiegare il significato di 0, 0.5 e 1?
- So distinguere coordinata iniziale, distanza percorsa e coordinata finale?
- So trovare due coppie velocità/durata che producono una distanza simile?

## Accessibilità

Mostra valori e distanze in una tabella testuale; accompagna la traiettoria con coordinate numeriche e unità di misura.

## Parole nuove

| Termine | Significato in questa lezione |
| --- | --- |
| `float` | numero che può avere una parte decimale |
| `normalizzato` | espresso nell'intervallo da 0 a 1 |
| `limite` | massimo valore consentito dalla configurazione |
