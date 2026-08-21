---
marp: true
paginate: true
size: 16:9
title: 04 — Romeo Y1: simulatore e missioni
---

# 04 — Simulatore, coordinate e missioni

Unità Y1 17–20

---

# Richiamo

Finora il simulatore era un luogo sicuro in cui eseguire il codice.

Ora diventa anche un **microscopio**:

```text
traiettoria + clock + eventi + stato finale
```

---

# Obiettivi

- leggere traiettoria ed event log;
- usare coordinate e orientamento;
- scomporre una missione in segmenti verificabili;
- confrontare previsione e risultato;
- usare report e tentativi per il debug;
- costruire il capstone del primo anno.

---

# Stato 2D

Una posa minima può essere pensata come:

```text
(x, y, orientamento)
```

Il robot non “sa andare al punto” per magia: i comandi nel tempo trasformano progressivamente questo stato.

---

# Previsione → osservazione

Prima di eseguire annota:

```text
posizione iniziale
segmento previsto
rotazione prevista
posizione finale attesa
```

Poi confronta con la traiettoria simulata.

---

# Event log

L'event log risponde a domande che l'animazione da sola può nascondere:

- quale comando è partito?
- quando?
- con quali parametri?
- quando è avvenuto lo stop?
- quale stato finale è stato registrato?

---

# Missione = segmenti verificabili

```text
Missione
├─ segmento A
├─ rotazione
├─ segmento B
└─ arresto finale
```

Debugga prima il segmento che non rispetta il contratto, non riscrivere tutta la missione.

---

# Tolleranza

Nel mondo robotico un risultato può essere corretto entro una tolleranza.

```text
|x_observed - x_target| <= epsilon
```

Tolleranza non significa “va bene più o meno”: deve essere definita e coerente col problema.

---

# Errore tipico

> Guardare soltanto l'animazione e correggere “a occhio”.

L'animazione aiuta l'intuizione, ma report, eventi e stato numerico rendono il debug ripetibile.

---

# Checkpoint

Una missione termina 20 cm a destra del target.

Quali evidenze controlleresti per prime?

1. traiettoria;
2. event log;
3. durate/velocità;
4. orientamento dopo le rotazioni;
5. stato finale.

Ordinale e motiva.

---

# Capstone Y1

La consegna completa dovrebbe includere:

```text
obiettivo
→ piano/segmenti
→ codice
→ tentativi
→ report finale
→ spiegazione degli errori corretti
```

Il risultato è una missione **spiegabile**, non soltanto riuscita.

---

# Simulatore e robot reale

Il capstone può preparare una futura prova fisica, ma non la autorizza automaticamente.

Il passaggio reale richiede:

- robot commissionato;
- preflight valido;
- area/STOP/supervisione;
- confronto tra stessa missione simulata e fisica.

---

# Recap

- simulatore = ambiente + misura + debug;
- coordinate rendono esplicito lo stato;
- missioni si scompongono;
- report ed eventi sono evidenze;
- capstone = progetto + verifica + spiegazione.

---

# Ponte verso il secondo anno

Nel secondo anno Romeo non è più solo un robot che esegue codice locale.

Diventa un **nodo di rete**.