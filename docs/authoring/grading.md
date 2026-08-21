# Progettare il grading

Il grader deve misurare la competenza dichiarata dalla lezione, non una scorciatoia facile da imitare.

## Parti dal comportamento osservabile

Scrivi prima una frase verificabile, per esempio:

- "Romeo si ferma nella zona target";
- "la funzione restituisce JSON valido con i campi richiesti";
- "la connessione viene chiusa in sicurezza";
- "il messaggio WebSocket viene validato prima del comando".

Solo dopo scegli il tipo di test.

## Missioni di movimento

Per la robotica spaziale preferisci stato finale, traiettoria, collisioni, checkpoint e command trace validata. Il processo trusted può riprodurre la trace su un nuovo simulation engine e calcolare il risultato senza fidarsi del voto prodotto dalla submission.

## Networking e servizi

Per socket, HTTP, REST, FastAPI, WebSocket, camera e gamepad usa contratti importabili e test comportamentali. Evita che `print("OK")` possa sostituire l'implementazione richiesta.

## Test pubblici e riservati

I test pubblici servono a insegnare. I behavioral test non devono necessariamente mostrare ogni fixture allo studente. Tuttavia un file montato nello stesso container del codice non è un segreto crittografico: non inserirvi credenziali o dati sensibili.

## Trusted finalize

Considera il risultato del worker sandbox come input non trusted. La finalizzazione sul processo host deve validare schema, limiti e contenuto prima di trasformarlo in `runtime_execution.v1` autorevole.

## Rubrica

La rubrica può includere aspetti automatici e aspetti docente. Mantieni chiaro quali punti derivano da checks deterministici e quali richiedono osservazione/argomentazione.

## Anti-pattern

Evita:

- pass/fail basato solo su stdout quando il comportamento è testabile;
- expected outcome sensibili montati inutilmente nel container;
- test che dipendono da timing fragile del computer host;
- grader che accetta lo starter non modificato;
- grader che richiede un dettaglio non dichiarato nella consegna;
- fallback dal sandbox autorevole al processo locale.

## Test del grader

Prima di pubblicare una Activity prova almeno:

- starter originale → fallisce l'obiettivo;
- soluzione docente → passa;
- soluzione parzialmente corretta → fallisce il check appropriato;
- input/payload malformato → errore stabile;
- timeout → fallimento controllato;
- output eccessivo o schema inatteso → rifiuto.
