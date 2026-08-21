# 17. Osserva il simulatore

## Obiettivo

In questo laboratorio imparerai a usare traiettoria, clock ed eventi per il debug.

## Che cosa sai già

Saper prevedere una sequenza, eseguirla e leggere posizione, orientamento e tempo finali.

## Modello mentale

Il simulatore è un quaderno di laboratorio ripetibile. Lo stato è una fotografia di un istante; la traiettoria unisce molte pose; l'event log elenca i comandi. Con lo stesso scenario e lo stesso programma otteniamo gli stessi numeri: questo rende il debug verificabile.

## Esempio minimo commentato

```python
from time import sleep
from romeo.easy import forward, stop

forward(0.5)  # Nell'event log appare il cambio dei motori.
sleep(1)      # La traiettoria registra pose nel tempo.
stop()        # Lo stato finale mostra motori a zero.
```

## Prova guidata

1. Prima del run scrivi una previsione per tempo, x, y, orientamento e stato motori.
2. Esegui una volta e leggi prima lo stato finale, senza guardare l'animazione.
3. Trova nell'event log il primo cambio motori e lo stop.
4. Leggi tre punti della traiettoria: iniziale, intermedio e finale.
5. Ripeti senza modifiche e verifica che gli stessi valori coincidano.

## Esercizio base

Avanza per due secondi, fermati e confronta previsione e traiettoria.

## Esercizio intermedio

Inserisci intenzionalmente una durata errata, usa le evidenze per individuarla e correggi una sola riga.

## Mini-sfida

Spiega con una frase quale evidenza useresti per distinguere velocità errata, durata errata e stop mancante.

## Consegna valutata

Avanza per due secondi, fermati e confronta la traiettoria con la previsione.

## Errori tipici

- Guardare soltanto l'animazione e ignorare i valori numerici.
- Cambiare più righe dopo un fallimento e perdere la causa dell'errore.
- Confondere un evento di comando con una posa della traiettoria.

## Autoverifica

- So distinguere stato, evento e punto di traiettoria?
- So confrontare previsione e misura con numeri?
- So mostrare che due run identici producono lo stesso risultato?

## Accessibilità

Ogni elemento visivo deve avere un equivalente testuale ordinato per tempo; traiettoria e colori non devono essere le sole fonti di feedback.

## Parole nuove

| Termine | Significato in questa lezione |
| --- | --- |
| `stato` | valori del simulatore in un singolo istante |
| `evento` | registrazione di un comando o fatto significativo |
| `determinismo` | stesso input e stesso scenario producono lo stesso risultato |
