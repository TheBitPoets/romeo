# 18. Raggiungi una coordinata

## Obiettivo

In questo laboratorio imparerai a tradurre metri e orientamento in comandi.

## Che cosa sai già

Saper leggere una posa del simulatore e costruire una sequenza di tratti e rotazioni.

## Modello mentale

La posa di Romeo contiene posizione `(x, y)` e orientamento. `x` cresce andando verso destra nella mappa, `y` cresce andando verso l'alto; l'orientamento dice dove punta il robot. Per raggiungere un punto, confrontiamo partenza e target e pianifichiamo i segmenti.

## Esempio minimo commentato

```text
Partenza: (0.5, 0.5), orientamento 0°
Target:   (1.0, 0.5)

La y non cambia e Romeo punta già verso x crescente:
serve un solo tratto diritto lungo 0.5 m.
```

## Prova guidata

1. Copia partenza e target in una tabella con colonne x e y.
2. Calcola separatamente quanto cambia x e quanto cambia y.
3. Controlla se l'orientamento iniziale punta già verso la prima direzione utile.
4. Traduci il piano in rotazione eventuale, avanzamento e stop.
5. Esegui e confronta distanza dal target e tolleranza, poi correggi un solo segmento.

## Esercizio base

Dalla posa iniziale raggiungi `(1.0, 0.5)` e fermati.

## Esercizio intermedio

Disegna il piano per un target con la stessa x ma y maggiore, indicando prima la rotazione necessaria.

## Mini-sfida

Pianifica su carta un target in cui cambiano sia x sia y usando due tratti e una rotazione.

## Consegna valutata

Dalla posa iniziale raggiungi il target (1.0, 0.5) e fermati.

## Errori tipici

- Confondere distanza da percorrere con coordinata finale.
- Ignorare l'orientamento iniziale e avanzare nella direzione sbagliata.
- Scambiare x e y leggendo la posa.

## Autoverifica

- So indicare il verso positivo degli assi x e y?
- So calcolare la differenza tra partenza e target?
- So spiegare quando serve una rotazione prima di avanzare?

## Accessibilità

Descrivi la mappa anche come coordinate e direzioni testuali; una griglia tattile o una tabella può sostituire la sola rappresentazione grafica.

## Parole nuove

| Termine | Significato in questa lezione |
| --- | --- |
| `coordinata` | numero che indica una posizione lungo un asse |
| `posa` | posizione x/y più orientamento |
| `tolleranza` | distanza massima dal target ancora accettata |
