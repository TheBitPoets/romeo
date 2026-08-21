---
marp: true
paginate: true
size: 16:9
title: 01 — Romeo Y1: fondamenti
---

# 01 — Primo anno
## Primo programma, API, REPL e LED

Unità Y1 1–5

---

# Richiamo

Un programma Python è una sequenza di istruzioni.

Con Romeo ogni istruzione può produrre un effetto osservabile:

```python
from romeo.easy import forward, stop
forward()
stop()
```

---

# Obiettivi

- eseguire il primo programma in sicurezza;
- collegare API e componenti senza dipendere dai dettagli CRICKIT;
- usare il REPL per prove minime;
- riconoscere chiamate di funzione e argomenti;
- usare il LED come output di stato.

---

# API prima dell'hardware

```text
forward()
   ↓
Romeo API
   ↓
backend scelto
```

Lo studente impara l'intenzione del comando. Il backend decide come rappresentarla in simulazione o su hardware.

---

# Una chiamata di funzione

```python
led((0, 255, 0))
```

Riconosci:

- nome;
- parentesi;
- argomento;
- effetto osservabile.

Poi modifica **una cosa alla volta**.

---

# REPL come microscopio

Nel REPL puoi provare un'idea minima e leggere subito errori e risultato.

Buona domanda:

> Quale singola chiamata voglio osservare?

Non usare il REPL per costruire una missione lunga senza conservarne il codice.

---

# LED = stato visibile

Il LED può rappresentare:

```text
verde  → pronto
blu    → missione in corso
rosso  → errore / stop
```

È un primo esempio di **output che comunica stato**, concetto che tornerà in rete e telemetria.

---

# Errore tipico

> “Se non ho il robot fisico non posso programmare Romeo.”

Falso: il backend mock/simulatore è intenzionalmente il primo ambiente di lavoro.

Il programma può essere scritto, eseguito e testato senza CRICKIT.

---

# Checkpoint

Spiega senza eseguire:

```python
from romeo.easy import led
led((255, 0, 0))
```

1. che cosa viene importato?
2. qual è la chiamata?
3. qual è l'argomento?
4. quale evidenza potresti osservare in simulazione/mock?

---

# Activity

Per le unità 1–5 usa le Activity del Course Bundle.

Workflow:

```text
starter
→ modifica minima
→ run nel simulatore/runtime
→ report
→ self-check
```

---

# Recap

- API stabile sopra backend diversi;
- REPL per prove piccole;
- funzione = nome + argomenti + comportamento;
- output visibile aiuta il debugging;
- simulazione prima dell'hardware.

---

# Prossimo blocco

Dagli output passiamo agli attuatori:

**ruote, velocità, curve e soprattutto STOP/safety**.