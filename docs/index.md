# Romeo · documentazione

Romeo è la piattaforma didattica di Python e robotica integrata con TheBitLab. Questo sito raccoglie in un unico punto la documentazione per **studenti**, **docenti**, **amministratori**, **autori di contenuti** e **sviluppatori**, insieme alla reference API generata dal codice.

```{admonition} Regola operativa
:class: important
Nel lavoro quotidiano si sviluppa e si prova prima nel simulatore. Il robot fisico è un target successivo, usato solo dopo commissioning/preflight e secondo la checklist di sicurezza.
```

## Percorsi consigliati

- **Studente**: prepara l'ambiente, scrivi `main.py`, prova nel simulatore, interpreta il report, correggi e passa al robot solo quando autorizzato.
- **Docente**: prepara la lezione, verifica runtime/grading, gestisci la classe in parallelo e usa il singolo robot come stazione finale condivisa.
- **Course Delivery**: usa il dashboard trasversale per collegare le 43 unità alle slide macro, ai manuali e al workflow simulatore → robot reale.
- **Amministratore**: identifica il deployment reale, installa `romeo-sim`, configura il digest OCI, esegui probe/smoke e conserva rollback riproducibili.
- **Autore di contenuti**: crea Activity, scenari e grader senza duplicare i contratti del Course Bundle.
- **Sviluppatore**: lavora in venv, preserva gli invarianti real/sim, esegue test/CI/docs e consulta la reference API.

```{toctree}
:maxdepth: 2
:caption: Percorsi

getting-started
architecture/system-map
student/index
teacher/index
course/delivery
operations/index
authoring/index
development/index
course/index
```

```{toctree}
:maxdepth: 2
:caption: Progetto, hardware e sicurezza

architecture/target
architecture/decisions
integrations/thebitlab-runtime
security/submission-threat-model
hardware/safety
hardware/commissioning
hardware/preflight
hardware/pre-merge-checklist
hardware/camera
network/gamepad
release/runtime-image
release/readiness
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
