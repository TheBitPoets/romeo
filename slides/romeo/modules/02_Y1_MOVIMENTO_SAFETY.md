---
marp: true
paginate: true
size: 16:9
title: 02 — Romeo Y1: movimento e safety
---

# 02 — Movimento e safety

Unità Y1 6–11

---

# Richiamo

Finora abbiamo prodotto effetti semplici.

Con i motori entra una nuova responsabilità:

> il programma modifica la posizione fisica del robot.

Per questo movimento e safety vanno insegnati insieme.

---

# Obiettivi

- controllare una ruota e poi due;
- distinguere avanti/indietro, curva e rotazione;
- ragionare su velocità normalizzate;
- prevedere una sequenza prima di eseguirla;
- garantire uno stop finale;
- usare il simulatore per debug di movimento.

---

# Una ruota alla volta

Prima di coordinare due motori osserva separatamente:

```text
comando → ruota sinistra
comando → ruota destra
```

Nel robot reale questo concetto sarà anche parte del commissioning della polarità.

---

# Due ruote = cinematica osservabile

```text
L = R > 0     → avanti
L = R < 0     → indietro
L ≠ R         → curva
L = -R        → rotazione sul posto
```

Prima di memorizzare funzioni, prevedi la conseguenza delle velocità relative.

---

# Il tempo è parte del programma

Una missione può essere vista come:

```text
azione + durata
azione + durata
stop
```

Il simulatore permette di osservare traiettoria e clock senza usare il pavimento come debugger.

---

# Velocità normalizzata

Valori tra 0 e 1 rendono esplicito il rapporto rispetto al massimo configurato.

Non confondere:

- comando software;
- velocità fisica reale;
- calibrazione/trim del singolo robot.

Sono livelli diversi.

---

# Stop come invariante

Una sequenza di movimento deve avere un comportamento di arresto comprensibile anche in caso di uscita anticipata.

Modello mentale:

```text
start movement
   ↓
work
   ↓
STOP known state
```

La safety non è una “lezione finale”: attraversa tutto il corso.

---

# Errore tipico

> Provare direttamente sul robot reale una sequenza non verificata perché “dura solo due secondi”.

Due secondi sono sufficienti per urtare un ostacolo o cadere da un banco.

Prima simulatore, poi area libera e gate fisico.

---

# Checkpoint

Prevedi il movimento qualitativo per:

```text
L = 0.8, R = 0.8
L = 0.8, R = 0.3
L = 0.6, R = -0.6
L = 0.0, R = 0.0
```

Poi confronta la previsione con il simulatore.

---

# Activity e report

Per ogni esercizio di movimento conserva almeno:

- codice;
- traiettoria prevista;
- traiettoria osservata;
- event log quando utile;
- stato finale;
- spiegazione dell'eventuale differenza.

---

# Collegamento al robot fisico

Nel commissioning il tecnico/docente verifica:

- verso delle ruote con conferma umana;
- speed limit;
- trim sinistra/destra;
- STOP e watchdog.

Lo studente non deve rifare il commissioning a ogni Activity.

---

# Recap

- due ruote producono comportamento emergente;
- velocità relative contano più del nome del comando;
- tempo e stato finale sono parte della missione;
- stop/safety sono requisiti, non optional;
- simulatore prima del robot reale.

---

# Prossimo blocco

Ora rendiamo il codice meno ripetitivo e più generale:

**funzioni, sequenze, condizioni e cicli**.