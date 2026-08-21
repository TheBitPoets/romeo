# Aggiornamento e rollback

Romeo ha due artefatti da coordinare: package Python trusted e immagine OCI del worker sandbox.

## Aggiornamento sicuro

1. identifica SHA/versione correnti;
2. verifica CI e release candidate;
3. installa il nuovo package in ambiente controllato;
4. configura il nuovo digest OCI immutabile;
5. esegui `list` e `probe`;
6. esegui smoke Y1 e Y2 attraverso il normale percorso studente;
7. verifica fail-closed;
8. solo dopo promuovi la configurazione al servizio usato dalla classe.

## Non aggiornare "a metà"

Evitare di cambiare casualmente solo il package o solo l'immagine senza verificare la compatibilità. Registra sempre la terna:

```text
TheBitLab SHA
Romeo package SHA/version
Romeo runtime OCI digest
```

## Rollback

Il rollback deve ripristinare una combinazione già nota e verificata, non ricostruire un'immagine "simile".

Passi consigliati:

1. ripristina package/versione precedente;
2. ripristina esatto digest OCI precedente;
3. ricarica il servizio;
4. `probe romeo-sim`;
5. smoke di una Activity breve;
6. registra il motivo del rollback.

## Durante una lezione

Se il runtime autorevole si rompe durante la classe, il fallback operativo è continuare la parte didattica nel simulatore/formazione prevista, non trasformare automaticamente il grading locale process-only in voto autorevole. La distinzione di sicurezza deve restare visibile.

## Evidenze

Conserva changelog, PR/commit, digest e risultati smoke. Non registrare segreti di registry o token di servizio.
