# Preparare l'ambiente studente

## Laboratorio scolastico gestito

Nella configurazione consigliata lo studente non deve installare manualmente il plugin Romeo né scegliere il digest Docker. Queste operazioni appartengono al docente/amministratore. Lo studente deve trovare TheBitLab già funzionante e una consegna con il proprio workspace.

Verifiche minime:

- Python è disponibile se l'attività richiede un terminale locale;
- il workspace della consegna si apre correttamente;
- il comando **Esegui test** produce un report;
- per le Activity Romeo il report autorevole viene prodotto dal runtime configurato dal laboratorio.

## Ambiente personale o di esercitazione

Se vuoi studiare Romeo fuori dal laboratorio puoi creare un virtual environment dedicato. Da una copia del repository Romeo:

```console
python -m venv .venv
```

Attivazione su Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Attivazione su Linux/macOS:

```console
source .venv/bin/activate
```

Poi:

```console
python -m pip install --upgrade pip
python -m pip install -e ".[web]"
```

Per avviare il viewer del simulatore:

```console
python -m uvicorn romeo.web.app:create_app --factory --host 127.0.0.1 --port 8000
```

Apri `http://127.0.0.1:8000/` nel browser.

```{warning}
L'ambiente personale è utile per imparare e fare prove, ma non sostituisce il grading autorevole configurato dal laboratorio TheBitLab.
```
