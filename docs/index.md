# Romeo · documentazione

Romeo è la piattaforma didattica di Python e robotica integrata con TheBitLab. Questo sito raccoglie in un unico punto la documentazione per **studenti**, **docenti**, **amministratori** e **sviluppatori**, insieme alla reference API generata dal codice.

```{admonition} Regola operativa
:class: important
Nel lavoro quotidiano si sviluppa e si prova prima nel simulatore. Il robot fisico è un target successivo, usato solo dopo il collaudo e secondo la checklist di sicurezza.
```

## Percorsi consigliati

- **Studente**: prepara l'ambiente, apri una consegna TheBitLab, modifica `main.py`, prova nel simulatore, leggi il report, correggi e seleziona il tentativo finale.
- **Docente**: prepara la classe, verifica runtime e grading, assegna le Activity, controlla i report e decide quando autorizzare il passaggio al robot fisico.
- **Amministratore**: installa il plugin `romeo-sim`, configura il digest OCI approvato e verifica che il grading runtime sia autorevole e fail-closed.
- **Sviluppatore**: usa un virtual environment, esegue lint/type-check/test/docs e consulta la reference API.

```{toctree}
:maxdepth: 2
:caption: Inizia qui

getting-started
student/index
teacher/index
operations/index
development/index
```

```{toctree}
:maxdepth: 2
:caption: Progetto e sicurezza

architecture/target
architecture/decisions
integrations/thebitlab-runtime
security/submission-threat-model
hardware/safety
hardware/camera
network/gamepad
release/runtime-image
release/readiness
course/pedagogical-audit
requirements-traceability
roadmap
audit
assets
```

```{toctree}
:maxdepth: 2
:caption: API Python

api/index
```
