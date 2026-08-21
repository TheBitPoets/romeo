# Guida docente — 16. Controlla un ciclo while

Durata prevista: 60 minuti. Difficoltà: B.

## Punto di partenza e modello mentale

Prerequisiti: Saper leggere `if`, un confronto semplice e un blocco ripetuto con `for`.

`while` ripete il corpo finché la sua domanda resta vera. Servono un contatore iniziale, un limite e un aggiornamento: senza aggiornamento la domanda non cambia e il ciclo può non finire. Prima del run simuliamo ogni giro in una tabella.

## Evidenze osservabili

Lo studente sa usare una condizione e assicurare la terminazione. Raccogliere il sorgente, la previsione, il risultato dei check e
le risposte di autoverifica. La consegna valutata è: Invia tre comandi con while e termina con stop.

## Sequenza proposta

- 0–10 min: richiamo della lezione precedente e previsione collettiva.
- 10–20 min: dimostrazione minima nel simulatore, mostrando stato e arresto.
- 20–40 min: lavoro a coppie con ruoli pilota/osservatore, scambiati a metà.
- 40–60 min: verifica automatica, spiegazione orale e exit ticket.

Non fornire subito la soluzione. Chiedere prima: “quale riga cambia lo stato?”, “quale prova lo
dimostra?” e “Romeo è fermo alla fine?”. Usare gli hint in ordine e mostrare l'event log solo dopo
che lo studente ha scritto una previsione.

## Idee errate frequenti e diagnosi

- Dimenticare l'incremento e creare un ciclo che non termina.
- Rientrare `stop()` nel corpo quando deve essere eseguito una volta sola.
- Confondere `< 3` con `<= 3` e ottenere un giro in più.

## Inclusione e valutazione formativa

La tabella testuale rende espliciti i cambiamenti del contatore; fornisci una procedura scritta e raggiungibile da tastiera per interrompere l'esecuzione.

Usare l'esercizio base come pratica comune, l'intermedio per consolidare e la mini-sfida soltanto
dopo una spiegazione corretta. Nel debrief introdurre solo il lessico elencato nella lezione.
