# Preparare l'ambiente studente

Esistono due situazioni diverse: **laboratorio scolastico gestito** e **PC personale**. Non mischiarle.

## Laboratorio scolastico gestito

Nella configurazione consigliata lo studente non deve installare manualmente il plugin Romeo, Docker o scegliere il digest del runtime. Queste operazioni appartengono al docente/amministratore.

Lo studente deve trovare:

- TheBitLab funzionante;
- la propria consegna;
- un workspace personale;
- il comando di esecuzione/test;
- il simulatore richiesto dall'Activity.

Se `romeo-sim` o la sandbox non sono disponibili, non cercare di "ripararli" installando package dentro il workspace: segnala l'errore al docente.

## Che cos'è un virtual environment?

Sul tuo PC Python può essere usato da molti progetti. Un **virtual environment** (`venv`) crea una cartella con un ambiente isolato per il progetto corrente. I package installati lì non vanno a modificare inutilmente l'installazione Python globale.

Puoi immaginarlo così:

```text
Python del computer
   ├── progetto A / .venv / dipendenze A
   └── Romeo     / .venv / dipendenze Romeo
```

Non è una macchina virtuale e non è una sandbox di sicurezza: è soprattutto isolamento delle dipendenze Python.

## Ambiente personale o di esercitazione

Da una copia del repository Romeo:

```console
python -m venv .venv
```

La cartella `.venv` viene creata nella directory corrente e non va committata nel repository.

### Attivare su Windows PowerShell

```powershell
.\.venv\Scripts\Activate.ps1
```

### Attivare su Linux/macOS

```console
source .venv/bin/activate
```

Dopo l'attivazione il prompt normalmente mostra `(.venv)`.

## Verifica quale Python stai usando

```console
python --version
python -c "import sys; print(sys.executable)"
python -m pip --version
```

Il path di `sys.executable` dovrebbe puntare dentro `.venv`. Usa preferibilmente `python -m pip` invece di un `pip` generico: in questo modo package e interprete sono chiaramente collegati.

## Installare Romeo per esercitarsi

```console
python -m pip install --upgrade pip
python -m pip install -e ".[web]"
```

`-e` è comodo in un checkout di sviluppo/esercitazione perché le modifiche al sorgente vengono viste senza reinstallare il package. Non è il modello preferito per un deployment amministrativo di produzione.

## Avviare il viewer locale

```console
python -m uvicorn romeo.web.app:create_app --factory --host 127.0.0.1 --port 8000
```

Apri `http://127.0.0.1:8000/` nel browser.

## Uscire dal venv

```console
deactivate
```

La cartella `.venv` resta sul disco e potrai riattivarla la volta successiva.

```{warning}
L'ambiente personale è utile per imparare e fare prove, ma non sostituisce il grading autorevole configurato dal laboratorio TheBitLab. Un venv isola package Python; non rende sicuro l'esecuzione di codice ostile.
```
