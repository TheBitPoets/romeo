# Guida docente — 2. Dai componenti ai comandi

Durata prevista: 50 minuti. Difficoltà: A.

## Punto di partenza e modello mentale

Prerequisiti: Aver eseguito U01 e saper riconoscere un'istruzione e lo stato finale fermo.

Pensa a una catena di messaggi: il programma chiede un'azione, il Raspberry Pi la interpreta, la scheda CRICKIT fornisce energia ai motori e le ruote si muovono. Il LED è un'uscita separata: comunica uno stato senza muovere il robot.

## Evidenze osservabili

Lo studente sa collegare API, motori, ruote e LED. Raccogliere il sorgente, la previsione, il risultato dei check e
le risposte di autoverifica. La consegna valutata è: Usa il LED verde come segnale di pronto, aziona entrambi i motori e fermati.

## Sequenza proposta

- 0–10 min: richiamo della lezione precedente e previsione collettiva.
- 10–20 min: dimostrazione minima nel simulatore, mostrando stato e arresto.
- 20–40 min: lavoro a coppie con ruoli pilota/osservatore, scambiati a metà.
- 40–50 min: verifica automatica, spiegazione orale e exit ticket.

Non fornire subito la soluzione. Chiedere prima: “quale riga cambia lo stato?”, “quale prova lo
dimostra?” e “Romeo è fermo alla fine?”. Usare gli hint in ordine e mostrare l'event log solo dopo
che lo studente ha scritto una previsione.

## Idee errate frequenti e diagnosi

- Confondere Raspberry Pi e CRICKIT: il primo esegue il programma, la seconda pilota i carichi elettrici.
- Pensare che cambiare il LED fermi i motori: sono due uscite indipendenti.
- Osservare solo l'animazione e non lo stato numerico delle ruote.

## Inclusione e valutazione formativa

Affianca ai componenti reali etichette grandi e numerate; descrivi sempre a parole LED e velocità, senza affidarti soltanto a colori o animazioni.

Usare l'esercizio base come pratica comune, l'intermedio per consolidare e la mini-sfida soltanto
dopo una spiegazione corretta. Nel debrief introdurre solo il lessico elencato nella lezione.
