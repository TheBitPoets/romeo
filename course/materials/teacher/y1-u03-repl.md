# Guida docente — 3. Esplora con il REPL

Durata prevista: 50 minuti. Difficoltà: A.

## Punto di partenza e modello mentale

Prerequisiti: Aver completato U02 e saper eseguire un file con Run.

Il REPL è un banco prova: mostra `>>>`, riceve una sola istruzione e risponde subito. Un file conserva invece una sequenza da rieseguire. Prima proviamo un comando nel REPL, poi trasferiamo la sequenza riuscita in `main.py`.

## Evidenze osservabili

Lo studente sa provare una chiamata alla volta e leggere gli errori. Raccogliere il sorgente, la previsione, il risultato dei check e
le risposte di autoverifica. La consegna valutata è: Trasferisci in main.py la sequenza provata nel REPL: LED rosso, movimento, stop.

## Sequenza proposta

- 0–10 min: richiamo della lezione precedente e previsione collettiva.
- 10–20 min: dimostrazione minima nel simulatore, mostrando stato e arresto.
- 20–40 min: lavoro a coppie con ruoli pilota/osservatore, scambiati a metà.
- 40–50 min: verifica automatica, spiegazione orale e exit ticket.

Non fornire subito la soluzione. Chiedere prima: “quale riga cambia lo stato?”, “quale prova lo
dimostra?” e “Romeo è fermo alla fine?”. Usare gli hint in ordine e mostrare l'event log solo dopo
che lo studente ha scritto una previsione.

## Idee errate frequenti e diagnosi

- Copiare anche i caratteri `>>>`: sono il prompt, non parte del codice.
- Dimenticare l'import prima della chiamata e ricevere `NameError`.
- Leggere tutto il traceback insieme invece di partire dall'ultima riga.

## Inclusione e valutazione formativa

La trascrizione testuale accompagna ogni cambiamento visivo; chi usa uno screen reader può seguire prompt, comando e risposta in ordine lineare.

Usare l'esercizio base come pratica comune, l'intermedio per consolidare e la mini-sfida soltanto
dopo una spiegazione corretta. Nel debrief introdurre solo il lessico elencato nella lezione.
