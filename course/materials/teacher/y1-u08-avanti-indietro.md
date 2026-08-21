# Guida docente — 8. Avanti e indietro

Durata prevista: 55 minuti. Difficoltà: A.

## Punto di partenza e modello mentale

Prerequisiti: Saper prevedere il movimento da una coppia di velocità.

Un comando motore resta attivo finché un altro comando lo cambia. `sleep(1)` non ferma Romeo: lascia trascorrere un secondo con il comando corrente. `backward` imposta entrambe le ruote all'indietro; `stop` le porta infine a zero.

## Evidenze osservabili

Lo studente sa comporre due movimenti opposti nel tempo. Raccogliere il sorgente, la previsione, il risultato dei check e
le risposte di autoverifica. La consegna valutata è: Avanza per un secondo, torna indietro per un secondo e fermati.

## Sequenza proposta

- 0–10 min: richiamo della lezione precedente e previsione collettiva.
- 10–20 min: dimostrazione minima nel simulatore, mostrando stato e arresto.
- 20–40 min: lavoro a coppie con ruoli pilota/osservatore, scambiati a metà.
- 40–55 min: verifica automatica, spiegazione orale e exit ticket.

Non fornire subito la soluzione. Chiedere prima: “quale riga cambia lo stato?”, “quale prova lo
dimostra?” e “Romeo è fermo alla fine?”. Usare gli hint in ordine e mostrare l'event log solo dopo
che lo studente ha scritto una previsione.

## Idee errate frequenti e diagnosi

- Pensare che `sleep` significhi stop: i motori mantengono l'ultimo comando.
- Usare durate diverse senza aggiornare la previsione della posa finale.
- Mettere `stop()` tra il comando e il relativo `sleep`, annullando il movimento.

## Inclusione e valutazione formativa

Usa una linea del tempo testuale con stato e durata; l'animazione può essere rallentata o sostituita dalla lettura della traiettoria numerica.

Usare l'esercizio base come pratica comune, l'intermedio per consolidare e la mini-sfida soltanto
dopo una spiegazione corretta. Nel debrief introdurre solo il lessico elencato nella lezione.
