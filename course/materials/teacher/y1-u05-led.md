# Guida docente — 5. Comunica con il LED

Durata prevista: 50 minuti. Difficoltà: A.

## Punto di partenza e modello mentale

Prerequisiti: Saper chiamare una funzione con un argomento e distinguere numero e testo.

Il LED è un'uscita immediata: `led(...)` cambia il suo stato ma non muove le ruote. Il nome del colore è testo, quindi va scritto tra virgolette. Il pannello di stato riporta anche il nome o i valori del colore per non dipendere soltanto dalla vista.

## Evidenze osservabili

Lo studente sa usare un output immediato per mostrare lo stato. Raccogliere il sorgente, la previsione, il risultato dei check e
le risposte di autoverifica. La consegna valutata è: Imposta il LED su blu; il grader controllerà il colore finale.

## Sequenza proposta

- 0–10 min: richiamo della lezione precedente e previsione collettiva.
- 10–20 min: dimostrazione minima nel simulatore, mostrando stato e arresto.
- 20–40 min: lavoro a coppie con ruoli pilota/osservatore, scambiati a metà.
- 40–50 min: verifica automatica, spiegazione orale e exit ticket.

Non fornire subito la soluzione. Chiedere prima: “quale riga cambia lo stato?”, “quale prova lo
dimostra?” e “Romeo è fermo alla fine?”. Usare gli hint in ordine e mostrare l'event log solo dopo
che lo studente ha scritto una previsione.

## Idee errate frequenti e diagnosi

- Scrivere `led(blue)` senza virgolette e ricevere `NameError`.
- Usare un nome non previsto, per esempio `azzurro`, invece dei valori documentati.
- Pensare che il primo colore resti quello finale dopo una seconda chiamata.

## Inclusione e valutazione formativa

Nomina sempre il colore nel testo e leggi i valori di stato; non usare rosso/verde come unico modo per comunicare errore o successo.

Usare l'esercizio base come pratica comune, l'intermedio per consolidare e la mini-sfida soltanto
dopo una spiegazione corretta. Nel debrief introdurre solo il lessico elencato nella lezione.
