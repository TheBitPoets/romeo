---
marp: true
paginate: true
size: 16:9
title: 09 — Romeo: dal simulatore al robot reale
---

# 09 — Dal simulatore al robot reale
## Gate operativo e safety

Deck trasversale

---

# Principio

Il robot reale non sostituisce il simulatore.

Il flusso corretto è:

```text
missione verificata in simulazione
→ robot fisico già commissionato
→ preflight
→ sessione supervisionata/autorizzata
→ confronto simulato vs reale
```

---

# Obiettivi

- distinguere commissioning e preflight;
- capire che cosa può essere verificato automaticamente;
- sapere dove serve conferma umana;
- preparare una prova fisica a velocità/limiti conservativi;
- raccogliere evidenze senza usare il robot come debugger primario;
- verificare la capability `romeo-doctor` contro lo SHA/versione realmente installato.

---

# Commissioning

È il collaudo completo del **singolo esemplare** Romeo.

Può includere movimenti attivi supervisionati:

- motore sinistro/destra a velocità minima;
- polarità;
- watchdog;
- forward/backward/turn;
- servo pan/tilt;
- camera;
- brownout/carico;
- trim e speed limit.

Autorità: `docs/hardware/commissioning.md`.

---

# Feedback umano necessario

Senza encoder/IMU sufficienti il software non può sapere da solo se una ruota gira nel **verso meccanico corretto**.

Quindi:

```text
comando software
→ movimento osservato
→ conferma umana
→ configurazione/calibrazione
```

Non inventare una misura che l'hardware non possiede.

---

# Preflight

Il preflight risponde a una domanda più piccola:

> questo Romeo, già collaudato, è pronto **adesso** per eseguire il programma studente?

Deve essere rapido, ripetibile, prevalentemente passivo e fail-safe.

---

# Check preflight tipici

Quando disponibili:

- package/versione;
- backend hardware;
- I2C/CRICKIT;
- calibrazione;
- limiti servo;
- camera;
- rete/servizi;
- watchdog;
- stato valido del commissioning.

Non è necessario muovere motori ogni volta.

---

# `romeo-doctor`: capability versionata

Non assumere il comando dalla documentazione o dalla memoria della chat.

```text
SHA/versione installato
→ il doctor è presente e validato?
   sì → usa i check passivi previsti
   no → usa le checklist hardware
```

La disponibilità è una proprietà dell'installazione reale, non del piano futuro.

---

# Doctor ≠ commissioning

Anche quando `romeo-doctor` è disponibile:

- il preflight resta prevalentemente passivo;
- il doctor non certifica da solo il verso meccanico delle ruote;
- il commissioning supervisionato conserva i test di movimento attivo;
- calibrazioni e misure fisiche devono restare associate al singolo esemplare.

Automatizzare un check non elimina il boundary fisico.

---

# Prima del movimento reale

- area libera;
- possibilità immediata di togliere alimentazione;
- velocità conservativa;
- ruote sollevate quando il test lo richiede;
- operatore/docente consapevole del prossimo comando;
- STOP verificabile.

---

# Stessa missione

Il confronto utile è:

```text
stesso codice / stessa missione
simulatore ↔ robot reale
```

Le differenze possono derivare da:

- attrito;
- batteria/alimentazione;
- tolleranze meccaniche;
- trim;
- superficie;
- sensori/camera;
- timing reale.

---

# Evidenza fisica

Il commissioning deve produrre un record come:

`physical-validation-YYYY-MM-DD.md`

con:

- hardware/versioni;
- misure;
- calibrazioni;
- test eseguiti;
- limiti;
- problemi aperti.

Mai credenziali o dati sensibili.

---

# Errore tipico

> “Il simulatore passa, quindi posso eseguire subito sul robot.”

No: il simulatore verifica programma/scenario; commissioning e preflight verificano **l'esemplare fisico e la sessione reale**.

Sono evidenze complementari.

---

# Checkpoint

Classifica ogni operazione:

1. confermare che throttle positivo faccia girare la ruota nel verso corretto;
2. controllare che la calibrazione valida sia presente prima della lezione;
3. provare una missione nuova;
4. misurare latenza watchdog;
5. verificare la logica di stop su disconnect.

Scelte: simulatore, commissioning, preflight/doctor, test software.

---

# Regola per gli studenti

```text
prima simula
poi spiega
poi mostra evidenza
solo dopo usa il robot reale quando autorizzato
```

La velocità di apprendimento viene dalla ripetibilità del simulatore; il robot reale serve a confrontare modello e mondo fisico.

---

# Recap

- commissioning = collaudo dell'esemplare;
- preflight = prontezza della sessione;
- parte della verifica fisica richiede feedback umano;
- `romeo-doctor` si usa solo se presente e validato nello SHA/versione installato;
- le checklist restano il fallback autorevole;
- stessa missione simulata→reale è il confronto didattico corretto;
- safety e STOP precedono ogni movimento.