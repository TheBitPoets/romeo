# Guida docente — 1. Conosci Romeo

Durata prevista: 45 minuti. Difficoltà: A.

## Punto di partenza e modello mentale

Prerequisiti: Nessuna esperienza di programmazione. È sufficiente saper usare mouse e tastiera.

Un programma è una lista di istruzioni che Romeo esegue dall'alto verso il basso. Il pulsante Run avvia la lista; `stop()` lascia le ruote ferme alla fine. Oggi non serve capire ogni simbolo: prima osserviamo che una riga di codice produce un effetto.

## Evidenze osservabili

Lo studente sa eseguire il primo programma e fermare il robot. Raccogliere il sorgente, la previsione, il risultato dei check e
le risposte di autoverifica. La consegna valutata è: Accendi il LED blu, invia un breve comando avanti e termina con stop.

## Sequenza proposta

- 0–10 min: richiamo della lezione precedente e previsione collettiva.
- 10–20 min: dimostrazione minima nel simulatore, mostrando stato e arresto.
- 20–40 min: lavoro a coppie con ruoli pilota/osservatore, scambiati a metà.
- 40–45 min: verifica automatica, spiegazione orale e exit ticket.

Non fornire subito la soluzione. Chiedere prima: “quale riga cambia lo stato?”, “quale prova lo
dimostra?” e “Romeo è fermo alla fine?”. Usare gli hint in ordine e mostrare l'event log solo dopo
che lo studente ha scritto una previsione.

## Idee errate frequenti e diagnosi

- Scrivere `stop` senza parentesi: il comando viene nominato ma non eseguito.
- Scrivere `Stop()` con la maiuscola: Python distingue maiuscole e minuscole.
- Eliminare `stop()` finale: lo stato sicuro non è più espresso chiaramente dal programma.

## Inclusione e valutazione formativa

Leggi ad alta voce l'ordine delle istruzioni e usa anche lo stato testuale dei motori: il colore e il movimento sullo schermo non sono le sole evidenze.

Usare l'esercizio base come pratica comune, l'intermedio per consolidare e la mini-sfida soltanto
dopo una spiegazione corretta. Nel debrief introdurre solo il lessico elencato nella lezione.
