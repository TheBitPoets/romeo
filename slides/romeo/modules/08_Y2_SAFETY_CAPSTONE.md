---
marp: true
paginate: true
size: 16:9
title: 08 — Romeo Y2: safety e capstone
---

# 08 — Safety di rete, integrazione e capstone

Unità Y2 21–23

---

# Richiamo

Nel controllo remoto abbiamo più componenti:

```text
controller → rete → server → robot
                 ← telemetria/video
```

Ogni boundary può fallire.

Il capstone deve quindi dimostrare **safety e recovery**, non soltanto una demo riuscita.

---

# Obiettivi

- spiegare ownership/controller lease;
- usare timeout e stop su perdita di controllo;
- distinguere command path e telemetry path;
- integrare controllo, stato e video;
- testare failure modes in simulazione;
- produrre il capstone telepresenza con evidenze.

---

# Ownership del controllo

Domanda fondamentale:

> Chi ha il diritto di comandare Romeo in questo momento?

Una sessione deve avere una regola esplicita per acquisizione, rinnovo e perdita del controller.

---

# Timeout

Il controller non può essere considerato vivo per sempre.

```text
ultimo segnale valido
      ↓ tempo
timeout
      ↓
revoca controllo + STOP
```

Il timeout è parte del contratto di safety.

---

# Fail-safe

Un fallimento deve portare verso uno stato noto e conservativo.

Esempi:

- client disconnesso → stop;
- comando invalido → rifiuto, non movimento imprevedibile;
- controller lease scaduta → revoca;
- backend non pronto → fail closed.

---

# Comando e telemetria

Separare i due flussi aiuta a verificare il sistema:

```text
command path     controller → robot
telemetry path   controller ← robot
```

Il renderer non deve inventare lo stato che il backend non ha confermato.

---

# Testare i failure mode

Nel simulatore possiamo iniettare condizioni come:

- messaggio malformato;
- disconnect;
- timeout;
- controller concorrente;
- sequenza di movimento senza rinnovo;
- stato non coerente.

Queste prove devono precedere la sessione fisica.

---

# Capstone telepresenza

Una consegna completa integra:

```text
video
+ controllo realtime
+ telemetria
+ ownership
+ timeout/stop
+ report/test
```

Non serve aggiungere feature non richieste: serve dimostrare i contratti.

---

# Evidenza

Il report finale dovrebbe permettere di rispondere:

- quale controller era owner?
- che cosa succede a disconnect?
- quali messaggi vengono rifiutati?
- come osserviamo lo stato?
- quali test sono passati?
- quali limiti rimangono?

---

# Errore tipico

> Testare soltanto l'happy path con browser e robot entrambi funzionanti.

La safety si vede soprattutto quando **qualcosa smette di funzionare**.

---

# Checkpoint

Per ciascun evento definisci il comportamento atteso:

1. WebSocket chiusa durante `forward`;
2. secondo controller tenta di comandare;
3. payload con velocità fuori range;
4. camera non disponibile;
5. telemetria temporaneamente assente.

Quali devono causare STOP? Quali possono degradare senza movimento?

---

# Recap

- ownership evita controller concorrenti impliciti;
- timeout rende finita l'autorità di controllo;
- fail-safe porta a stato conservativo;
- il capstone integra canali diversi senza confonderne le responsabilità;
- failure testing è parte della consegna.

---

# Ultimo passaggio

Il sistema può essere corretto in simulazione e ancora non essere pronto per **quel robot fisico**.

→ commissioning, preflight e simulatore→reale.