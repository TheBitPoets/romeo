# Guida docente — 6. Controlla una ruota

Durata prevista: 50 minuti. Difficoltà: A.

## Punto di partenza e modello mentale

Prerequisiti: Saper chiamare funzioni con argomenti numerici e leggere lo stato di un'uscita.

`robot` è il nome della plancia di comando di Romeo. Il punto in `robot.drive(...)` sceglie il comando `drive` di quella plancia. I due numeri indicano nell'ordine ruota sinistra e ruota destra; zero significa ruota ferma. Non occorre ancora studiare le classi.

## Evidenze osservabili

Lo studente sa comandare separatamente la ruota sinistra. Raccogliere il sorgente, la previsione, il risultato dei check e
le risposte di autoverifica. La consegna valutata è: Con Robot.drive fai girare solo la ruota sinistra, poi ferma Romeo.

## Sequenza proposta

- 0–10 min: richiamo della lezione precedente e previsione collettiva.
- 10–20 min: dimostrazione minima nel simulatore, mostrando stato e arresto.
- 20–40 min: lavoro a coppie con ruoli pilota/osservatore, scambiati a metà.
- 40–50 min: verifica automatica, spiegazione orale e exit ticket.

Non fornire subito la soluzione. Chiedere prima: “quale riga cambia lo stato?”, “quale prova lo
dimostra?” e “Romeo è fermo alla fine?”. Usare gli hint in ordine e mostrare l'event log solo dopo
che lo studente ha scritto una previsione.

## Idee errate frequenti e diagnosi

- Invertire l'ordine sinistra/destra degli argomenti.
- Scrivere `Robot.drive(...)` invece di usare il nome `robot` preparato.
- Dimenticare `robot.stop()` perché l'animazione sembra già terminata.

## Inclusione e valutazione formativa

Affianca ai valori le parole sinistra/destra e usa lo stato numerico; non richiedere di dedurre la ruota attiva soltanto dall'animazione.

Usare l'esercizio base come pratica comune, l'intermedio per consolidare e la mini-sfida soltanto
dopo una spiegazione corretta. Nel debrief introdurre solo il lessico elencato nella lezione.
