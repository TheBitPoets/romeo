# Creare contenuti Romeo

Questa sezione è per chi progetta nuove lezioni, Activity, scenari e rubriche.

```{toctree}
:maxdepth: 2

activity
scenario
grading
```

## Separazione delle responsabilità

Una nuova lezione può coinvolgere più artefatti, ma ognuno ha un ruolo distinto:

- **curriculum**: ordine, titolo, obiettivo, durata e difficoltà;
- **Activity**: consegna, prerequisiti, asset, runtime e policy di grading;
- **starter**: punto di partenza dello studente;
- **scenario**: mondo simulato e checks spaziali/comportamentali;
- **runtime config**: configurazione specifica del plugin;
- **hints/materiali**: supporto progressivo;
- **soluzione docente**: fixture di qualità, non materiale da pubblicare nel catalogo studente.

## Regola didattica

Non introdurre in un'Activity un concetto che la progressione non ha ancora spiegato. Se il grader richiede una struttura più avanzata dello starter/lezione, è il contratto didattico a essere incoerente.

## Regola tecnica

Preferisci contratti e generatori esistenti. Non creare un nuovo schema JSON per una singola lezione quando `activity.json`, `runtime-config.json` o `romeo.scenario.v1` esprimono già il concetto.
