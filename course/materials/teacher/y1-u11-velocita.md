# Guida docente — 11. Scegli la velocità

Durata prevista: 55 minuti. Difficoltà: A.

## Evidenze osservabili

Lo studente sa confrontare valori normalizzati tra 0 e 1, anticipa l'effetto delle istruzioni e interpreta almeno un
risultato del grader. La consegna è: Raggiungi il target a x=1.0 usando velocità 0.5 per due secondi.

## Sequenza proposta

- 0–10 min: richiamo della lezione precedente e previsione collettiva.
- 10–20 min: dimostrazione minima nel simulatore, mostrando stato e arresto.
- 20–40 min: lavoro a coppie con ruoli pilota/osservatore, scambiati a metà.
- 40–55 min: verifica automatica, spiegazione orale e exit ticket.

Non fornire subito la soluzione. Chiedere prima: “quale riga cambia lo stato?”, “quale prova lo
dimostra?” e “Romeo è fermo alla fine?”. Usare gli hint in ordine e mostrare l'event log solo dopo
che lo studente ha scritto una previsione.

## Idee errate frequenti

Le chiamate non sono descrizioni ma azioni; `sleep` non ferma i motori; una velocità doppia non
garantisce precisione doppia; superare un target non equivale a raggiungerlo. Sul robot fisico il
watchdog è una rete di sicurezza, non sostituisce `stop()`.

## Inclusione e valutazione formativa

Fornire una scheda con i nomi delle funzioni e consentire di descrivere prima l'algoritmo con
frecce. Per chi procede rapidamente, richiedere una variante con una funzione nominata bene.
Raccogliere come evidenze: previsione, sorgente, esito dei check e una frase di spiegazione. Nel
debrief collegare float, intervallo, limite alla prossima unità, evitando dettagli interni del backend.
