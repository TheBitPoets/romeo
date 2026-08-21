# 2. Dai componenti ai comandi

## Obiettivo

In questo laboratorio imparerai a collegare API, motori, ruote e LED.

## Che cosa sai già

Aver eseguito U01 e saper riconoscere un'istruzione e lo stato finale fermo.

## Modello mentale

Pensa a una catena di messaggi: il programma chiede un'azione, il Raspberry Pi la interpreta, la scheda CRICKIT fornisce energia ai motori e le ruote si muovono. Il LED è un'uscita separata: comunica uno stato senza muovere il robot.

## Esempio minimo commentato

```python
from romeo.easy import led, stop

# Il messaggio "pronto" usa il LED, non i motori.
led("green")
stop()
```

Nel pannello di stato cerca sia il nome del colore sia le due velocità delle ruote.

## Prova guidata

1. Ordina le quattro schede: programma, Raspberry Pi, CRICKIT, motori.
2. Indica quale componente calcola e quale componente fornisce energia ai motori.
3. Esegui l'esempio e controlla separatamente LED, ruota sinistra e ruota destra.
4. Completa lo starter con il segnale verde, un comando avanti e lo stop finale.
5. Racconta il viaggio del comando dal codice alle ruote senza usare abbreviazioni.

## Esercizio base

Associa ciascun comando della consegna al componente che cambia stato.

## Esercizio intermedio

Esegui LED verde, movimento e stop; annota tre eventi nell'ordine osservato.

## Mini-sfida

Disegna la catena dei componenti e aggiungi una freccia di ritorno per il feedback del simulatore.

## Consegna valutata

Usa il LED verde come segnale di pronto, aziona entrambi i motori e fermati.

## Errori tipici

- Confondere Raspberry Pi e CRICKIT: il primo esegue il programma, la seconda pilota i carichi elettrici.
- Pensare che cambiare il LED fermi i motori: sono due uscite indipendenti.
- Osservare solo l'animazione e non lo stato numerico delle ruote.

## Autoverifica

- So descrivere il ruolo di Raspberry Pi, CRICKIT e motori con una frase ciascuno?
- So dire quale istruzione cambia il LED?
- So verificare che entrambe le ruote siano ferme alla fine?

## Accessibilità

Affianca ai componenti reali etichette grandi e numerate; descrivi sempre a parole LED e velocità, senza affidarti soltanto a colori o animazioni.

## Parole nuove

| Termine | Significato in questa lezione |
| --- | --- |
| `Raspberry Pi` | il piccolo computer che esegue Python |
| `CRICKIT` | la scheda che comanda motori, servo e LED |
| `uscita` | una parte del robot che il programma può modificare |
