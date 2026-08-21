# Corso Romeo

Il Course Bundle contiene **43 unità**: 20 per il primo anno e 23 per il secondo. Il catalogo pubblico viene generato da `course/curriculum.json` e dagli `activity.json`, così obiettivi, prerequisiti, durata, difficoltà e runtime non vengono duplicati manualmente.

```{toctree}
:maxdepth: 2

methodology
pedagogical-audit
generated/index
```

## Primo anno

Focus: Python, programmazione procedurale, safety e robotica 2D. L'API deve rimanere lineare e leggibile; i concetti avanzati vengono introdotti soltanto quando servono.

## Secondo anno

Focus: networking, socket, HTTP/REST, FastAPI, WebSocket, camera, eventi, tastiera/gamepad e telepresenza. Le unità usano contratti comportamentali importabili quando il grading deve verificare il comportamento e non semplici marker testuali.

## Cosa non viene pubblicato nel catalogo

Il generatore filtra gli asset in base alla visibilità. Soluzioni docente, hidden test e fixture di grading non vengono incorporati nelle pagine pubbliche del sito, anche quando esistono nel repository/course bundle.

## Rigenerare localmente

```console
python scripts/generate_course_docs.py
python -m sphinx -W --keep-going -b html docs docs/_build/html
```

La CI esegue la stessa generazione prima del build Sphinx.
