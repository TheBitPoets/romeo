# 10. Stop e sicurezza

## Obiettivo

In questo laboratorio imparerai a garantire l'arresto anche al termine di una sequenza.

## Che cosa sai già

Saper costruire una breve sequenza temporizzata e terminarla con `stop()`.

## Modello mentale

Lo stop scritto nel programma è la regola principale. Il watchdog è una seconda rete di sicurezza: se per troppo tempo non arrivano comandi validi, ordina lo stop. Non sostituisce il nostro `stop()`; protegge da un programma o collegamento interrotto.

## Esempio minimo commentato

```python
from romeo.easy import forward, stop

forward(0.2)
# Anche una prova brevissima dichiara esplicitamente lo stato sicuro.
stop()
```

## Prova guidata

1. Individua l'ultima istruzione motore dello starter.
2. Prevedi lo stato finale se il programma terminasse in quel punto.
3. Aggiungi `stop()` e verifica che entrambe le ruote valgano zero.
4. Spiega a un compagno la differenza tra stop esplicito e watchdog.
5. Compila la scheda di sicurezza prima di provare lo stesso codice sul robot fisico.

## Esercizio base

Invia un comando motore e lascia Romeo esplicitamente fermo.

## Esercizio intermedio

Confronta l'event log di un programma con e senza stop esplicito, usando solo il simulatore.

## Mini-sfida

Scrivi in tre passi la procedura umana da seguire se il robot fisico non risponde ai comandi.

## Consegna valutata

Invia almeno un comando motore e lascia Romeo fermo.

## Errori tipici

- Credere che la fine del file equivalga sempre a uno stop immediato.
- Usare il watchdog come scusa per omettere `stop()`.
- Provare un caso di errore direttamente sull'hardware prima del simulatore.

## Autoverifica

- So mostrare nel codice lo stop esplicito?
- So spiegare il ruolo di riserva del watchdog?
- So indicare un'evidenza che entrambe le ruote siano a zero?

## Accessibilità

La checklist di sicurezza deve essere disponibile in testo ad alta leggibilità e letta ad alta voce prima della prova fisica.

## Parole nuove

| Termine | Significato in questa lezione |
| --- | --- |
| `watchdog` | controllo che ferma il robot quando i comandi non arrivano in tempo |
| `fail-safe` | comportamento che porta il sistema in uno stato sicuro |
| `stop esplicito` | istruzione `stop()` scritta nel programma |
