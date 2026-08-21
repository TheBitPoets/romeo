# Guida docente — 10. Stop e sicurezza

Durata prevista: 50 minuti. Difficoltà: A.

## Punto di partenza e modello mentale

Prerequisiti: Saper costruire una breve sequenza temporizzata e terminarla con `stop()`.

Lo stop scritto nel programma è la regola principale. Il watchdog è una seconda rete di sicurezza: se per troppo tempo non arrivano comandi validi, ordina lo stop. Non sostituisce il nostro `stop()`; protegge da un programma o collegamento interrotto.

## Evidenze osservabili

Lo studente sa garantire l'arresto anche al termine di una sequenza. Raccogliere il sorgente, la previsione, il risultato dei check e
le risposte di autoverifica. La consegna valutata è: Invia almeno un comando motore e lascia Romeo fermo.

## Sequenza proposta

- 0–10 min: richiamo della lezione precedente e previsione collettiva.
- 10–20 min: dimostrazione minima nel simulatore, mostrando stato e arresto.
- 20–40 min: lavoro a coppie con ruoli pilota/osservatore, scambiati a metà.
- 40–50 min: verifica automatica, spiegazione orale e exit ticket.

Non fornire subito la soluzione. Chiedere prima: “quale riga cambia lo stato?”, “quale prova lo
dimostra?” e “Romeo è fermo alla fine?”. Usare gli hint in ordine e mostrare l'event log solo dopo
che lo studente ha scritto una previsione.

## Idee errate frequenti e diagnosi

- Credere che la fine del file equivalga sempre a uno stop immediato.
- Usare il watchdog come scusa per omettere `stop()`.
- Provare un caso di errore direttamente sull'hardware prima del simulatore.

## Inclusione e valutazione formativa

La checklist di sicurezza deve essere disponibile in testo ad alta leggibilità e letta ad alta voce prima della prova fisica.

Usare l'esercizio base come pratica comune, l'intermedio per consolidare e la mini-sfida soltanto
dopo una spiegazione corretta. Nel debrief introdurre solo il lessico elencato nella lezione.
