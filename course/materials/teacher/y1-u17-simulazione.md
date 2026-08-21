# Guida docente — 17. Osserva il simulatore

Durata prevista: 65 minuti. Difficoltà: B.

## Punto di partenza e modello mentale

Prerequisiti: Saper prevedere una sequenza, eseguirla e leggere posizione, orientamento e tempo finali.

Il simulatore è un quaderno di laboratorio ripetibile. Lo stato è una fotografia di un istante; la traiettoria unisce molte pose; l'event log elenca i comandi. Con lo stesso scenario e lo stesso programma otteniamo gli stessi numeri: questo rende il debug verificabile.

## Evidenze osservabili

Lo studente sa usare traiettoria, clock ed eventi per il debug. Raccogliere il sorgente, la previsione, il risultato dei check e
le risposte di autoverifica. La consegna valutata è: Avanza per due secondi, fermati e confronta la traiettoria con la previsione.

## Sequenza proposta

- 0–10 min: richiamo della lezione precedente e previsione collettiva.
- 10–20 min: dimostrazione minima nel simulatore, mostrando stato e arresto.
- 20–40 min: lavoro a coppie con ruoli pilota/osservatore, scambiati a metà.
- 40–65 min: verifica automatica, spiegazione orale e exit ticket.

Non fornire subito la soluzione. Chiedere prima: “quale riga cambia lo stato?”, “quale prova lo
dimostra?” e “Romeo è fermo alla fine?”. Usare gli hint in ordine e mostrare l'event log solo dopo
che lo studente ha scritto una previsione.

## Idee errate frequenti e diagnosi

- Guardare soltanto l'animazione e ignorare i valori numerici.
- Cambiare più righe dopo un fallimento e perdere la causa dell'errore.
- Confondere un evento di comando con una posa della traiettoria.

## Inclusione e valutazione formativa

Ogni elemento visivo deve avere un equivalente testuale ordinato per tempo; traiettoria e colori non devono essere le sole fonti di feedback.

Usare l'esercizio base come pratica comune, l'intermedio per consolidare e la mini-sfida soltanto
dopo una spiegazione corretta. Nel debrief introdurre solo il lessico elencato nella lezione.
