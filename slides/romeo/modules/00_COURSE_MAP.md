---
marp: true
paginate: true
size: 16:9
title: 00 — Romeo: mappa del corso
---

# Romeo
## Python, robotica e servizi con un solo modello mentale

20 unità primo anno + 23 unità secondo anno

---

# Idea centrale

Lo studente scrive **lo stesso programma** contro una API stabile.

```text
codice studente
      ↓
Romeo API
      ↓
mock | simulatore | hardware CRICKIT
```

Cambiamo backend, non il modo di ragionare sul programma.

---

# Obiettivi del percorso

- imparare Python attraverso azioni osservabili;
- passare da comandi semplici a missioni verificabili;
- usare il simulatore come debugger ripetibile;
- introdurre rete, API e realtime nel secondo anno;
- arrivare al robot reale solo dopo gate tecnici e di safety.

---

# Primo anno

```text
primo programma
→ movimento e safety
→ funzioni / if / cicli
→ simulatore e coordinate
→ missione capstone
```

La robotica rende visibili tempo, stato, errore e conseguenze del codice.

---

# Secondo anno

```text
rete / TCP / JSON
→ HTTP / REST / FastAPI
→ WebSocket / controller
→ camera / eventi / telemetria
→ safety di rete / telepresenza
```

Il robot diventa un nodo di un sistema distribuito.

---

# Workflow studente

```text
scrivi
→ simula
→ osserva report/traiettoria/event log
→ correggi
→ consegna tentativo
→ robot reale solo se autorizzato
```

Il robot fisico non è il primo posto in cui scoprire un bug.

---

# TheBitLab

Il runtime `romeo-sim` permette alle Activity di produrre evidenze headless:

- risultato;
- traiettoria;
- event log;
- stato finale;
- grading previsto dall'Activity.

---

# Safety come requisito software

Ogni sequenza di movimento deve avere un arresto comprensibile.

Nel mondo reale aggiungiamo:

- limiti;
- watchdog;
- ownership/controller lease;
- preflight;
- commissioning del singolo robot.

---

# Fonti e manuali

Non duplicare ciò che esiste:

- `docs/student/` → workflow studente;
- `docs/teacher/` → conduzione e grading;
- `docs/operations/` → installazione/deploy;
- `docs/hardware/` → safety e collaudo;
- `course/` → curriculum e Activity.

---

# Checkpoint

Classifica ciascuna azione:

1. provare una curva per la prima volta;
2. verificare la polarità di una ruota appena assemblata;
3. eseguire una Activity assegnata;
4. controllare un Romeo già collaudato prima della sessione reale.

Scelte: simulatore, commissioning, TheBitLab, preflight.

---

# Evidenza

Durante il corso non basta dire “ha funzionato”.

Conserviamo, quando rilevante:

```text
codice + report + traiettoria/eventi + test + spiegazione
```

Sul robot reale aggiungiamo versione/configurazione e misure di commissioning.

---

# Prossimo passo

Primo anno: **scrivere il primo programma e capire che cosa significa comandare Romeo senza dipendere dall'hardware fisico**.