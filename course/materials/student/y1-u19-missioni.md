# 19. Completa una missione

## Obiettivo

In questo laboratorio imparerai a scomporre un percorso in segmenti verificabili.

## Che cosa sai già

Saper leggere coordinate, pianificare segmenti e usare traiettoria ed eventi per correggerli.

## Modello mentale

Una missione lunga diventa gestibile dividendola in checkpoint ordinati. Ogni checkpoint è una prova intermedia: prima raggiungiamo il primo, poi aggiungiamo il tratto successivo. Passare vicino ai punti nell'ordine conta più che indovinare subito l'intero programma.

## Esempio minimo commentato

```text
Partenza → checkpoint 1 → checkpoint 2 → checkpoint 3/parcheggio

Per ogni freccia annota:
1. posa di partenza; 2. rotazione; 3. tratto; 4. prova osservabile.
```

## Prova guidata

1. Leggi lo scenario e trascrivi nell'ordine tutti i checkpoint, contando quelli effettivamente presenti.
2. Disegna un segmento tra partenza e primo checkpoint e prevedi la posa raggiunta.
3. Implementa soltanto il primo segmento e verifica la traiettoria.
4. Aggiungi un checkpoint alla volta, conservando una versione funzionante.
5. Esegui la missione completa e controlla ordine, parcheggio finale, collisioni e stop.

## Esercizio base

Attraversa nell'ordine i checkpoint dello scenario e fermati sul target finale.

## Esercizio intermedio

Raggruppa almeno un tratto in una funzione con un nome che descriva lo scopo.

## Mini-sfida

Ottieni lo stesso percorso con una seconda combinazione di velocità e durate, mantenendo tutti i check verdi.

## Consegna valutata

Attraversa nell'ordine due checkpoint e fermati sul target finale.

## Errori tipici

- Saltare direttamente al target finale senza attraversare i checkpoint in ordine.
- Aggiungere tutti i segmenti prima di aver verificato il primo.
- Contare checkpoint diversi da quelli realmente dichiarati nello scenario.

## Autoverifica

- So elencare i checkpoint nell'ordine corretto?
- So mostrare sulla traiettoria dove viene superato ciascun punto?
- So indicare quale segmento correggere quando un checkpoint fallisce?

## Accessibilità

Fornisci la sequenza dei checkpoint come elenco numerato con coordinate, non soltanto come marcatori sulla mappa.

## Parole nuove

| Termine | Significato in questa lezione |
| --- | --- |
| `checkpoint` | punto intermedio da raggiungere nell'ordine stabilito |
| `collisione` | contatto del robot con ostacolo o bordo |
| `missione` | insieme completo di obiettivi e vincoli |
