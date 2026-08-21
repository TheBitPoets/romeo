---
marp: true
paginate: true
size: 16:9
title: 03 — Romeo Y1: astrazione e controllo
---

# 03 — Astrazione e controllo del flusso

Unità Y1 12–16

---

# Richiamo

Una missione scritta come lunga sequenza di comandi funziona, ma diventa difficile da capire e modificare.

Ora impariamo a rappresentare **idee**, non solo passi.

---

# Obiettivi

- racchiudere sequenze in funzioni;
- usare parametri per generalizzare;
- progettare missioni come passi nominati;
- scegliere con `if`;
- ripetere con `for` e `while`;
- riconoscere il rischio di cicli non terminanti;
- mantenere lo stop/safety anche dopo il refactor.

---

# Funzione = nome a un comportamento

```python
def avanti_per(secondi):
    forward()
    sleep(secondi)
    stop()
```

La funzione crea un'astrazione: chi la usa ragiona su **avanti_per**, non su ogni dettaglio interno.

---

# Parametri

Un parametro rende riutilizzabile una struttura:

```python
avanti_per(1.0)
avanti_per(2.5)
```

Domanda didattica:

> che cosa resta uguale e che cosa varia?

---

# Missione come composizione

```text
parti
→ vai al punto A
→ ruota
→ vai al punto B
→ stop
```

Prima assegna nomi ai pezzi; poi implementali.

La decomposizione prepara il debugging e il test per segmenti.

---

# `if`: comportamento condizionale

```python
if distanza < soglia:
    stop()
else:
    forward()
```

Il punto non è la sintassi: è esplicitare **quale dato controlla quale decisione**.

---

# `for`: ripetizione nota

```python
for _ in range(4):
    lato_quadrato()
```

Quando il numero di ripetizioni è noto, `for` rende visibile la struttura.

---

# `while`: ripetizione condizionata

```python
while not missione_finita:
    aggiorna()
```

Ogni `while` deve far nascere una domanda:

> che cosa rende falsa la condizione?

Un robot con ciclo infinito può diventare un problema fisico.

---

# Invariante di safety

Dopo ogni refactor chiedi:

```text
esiste ancora un percorso affidabile verso stop()?
```

Funzioni e cicli non devono nascondere il requisito di arresto.

---

# Errore tipico

> Copiare quattro volte lo stesso blocco e poi correggerne solo tre.

La duplicazione crea divergenza. Una funzione ben scelta concentra il comportamento e riduce i punti da correggere.

---

# Checkpoint

Quale struttura useresti?

1. percorri quattro lati uguali;
2. continua finché non raggiungi una condizione;
3. scegli tra due comportamenti in base a un valore;
4. riusa “ruota di 90°” con durate calibrabili.

Motiva prima di scrivere codice.

---

# Activity

Nelle unità 12–16 confronta sempre:

```text
versione esplicita
→ refactor
→ stesso comportamento osservabile
```

Il simulatore serve a verificare che l'astrazione non abbia cambiato la missione per errore.

---

# Recap

- funzione = astrazione riusabile;
- parametro = variazione controllata;
- `if` = decisione;
- `for` = ripetizione nota;
- `while` = ripetizione con condizione e obbligo di terminazione;
- safety deve sopravvivere ai refactor.

---

# Prossimo blocco

Usiamo il simulatore non solo per “vedere il robot”, ma come **strumento di misura, debug e grading**.