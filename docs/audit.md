# Audit iniziale

Audit eseguito il 21 agosto 2026. I riferimenti sono fissati per rendere ripetibili
le conclusioni; l'implementazione dovrà riesaminare il contratto upstream prima di
ogni integrazione incompatibile.

## TheBitPoets/romeo

- Riferimento: `main` a `17760b692759b4db87cdf21cf0fa32606d920bd2`.
- Stato iniziale: repository hardware/documentale, senza package Python, test o CI
  applicativa. La documentazione descrive Raspberry Pi, CRICKIT, due motori DC,
  camera e supporto pan/tilt.
- Conseguenza: il repository può diventare la sorgente unica di API, backend,
  simulatore e corso senza dover migrare codice applicativo preesistente.
- Convenzione adottata: sviluppo su `feat/platform-foundation`, non su `main`.

## marwano/robo

- Riferimento verificato: `main` a
  `d5effda54837e51cff640d65e002c4576ec9a92f` (audit 2026-08-21).
- Licenza: MIT, copyright 2023 Marwan Alsabbagh.
- Parti riutilizzabili come riferimento: separazione tra controllo motori e
  periferiche, test double di CRICKIT, comandi di movimento, controllo remoto e
  camera.
- Parti da modernizzare: isolamento più netto dell'hardware, Picamera2/libcamera,
  safety fail-safe, typing e test deterministici.
- Vincolo: il testo Manning non è una sorgente del corso. Ogni materiale didattico
  Romeo sarà originale. Qualunque codice adattato in modo sostanziale conserverà
  avviso di copyright e licenza MIT.

## TheBitPoets/2cornot2c

- Riferimento: `main` a `5472eef86568a4e7ce59ad34ba937220df27efd7`.
- Standard da riusare: estensione attività `extensions.thebitlab.runtime`, schema
  `runtime_activity.v1`, discovery mediante entry point
  `thebitlab.runtimes` e lifecycle `describe()`, `probe()`, `launch()`,
  `run()`, `close()`.
- Il runtime è un processo/plugin separato: Romeo non deve importare moduli interni
  di TheBitLab. Richieste e risultati devono restare serializzabili. Gli artefatti
  della submission sono dichiarati dal contratto; per gli output la v1 non offre
  ancora un collector standard, quindi Romeo userà path workspace validati e
  metadata documentati senza inventare campi ABI.
- Il runtime previsto è `romeo-sim`, con capability iniziali
  `interactive-launch`, `headless-run`, `deterministic-grade` e
  `artifact-collect`.

## TheBitPoets/thebitlab-hardware

- Riferimento: `d8d3c22615405297d490c14338a6263e9eae30b2`.
- Convenzioni da riusare: radice del Course Bundle con `bundle.json` e
  `curriculum.json`; contenuti separati in `activities/`, `materials/student/`,
  `materials/teacher/`, `handouts/`, `docs/`, `optional/` e `scripts/`.
- Ogni attività deve dichiarare obiettivo, prerequisiti, consegna, starter, hint
  progressivi, grading, rubrica, soluzione docente, durata, difficoltà, metriche e
  scenario quando applicabile.
- Il bundle Romeo sarà validato con gli strumenti TheBitLab esistenti: non verrà
  introdotto un secondo formato.

## Rischi e verifiche aperte

- Hardware: polarità, canali CRICKIT, escursione servo, latenza del watchdog e
  comportamento al brownout richiedono una prova su un esemplare reale. In CI si
  usano mock; i test fisici restano marcati e separati.
- Safety: valori conservativi non sostituiscono la verifica meccanica del robot.
- Camera: Picamera2 dipende da Raspberry Pi OS e libcamera; import e avvio devono
  essere differiti per mantenere installabile il package altrove.
- Licenze: prima della distribuzione va mantenuto un inventario delle dipendenze e
  degli eventuali file derivati da `marwano/robo`.
- Determinismo: il clock simulato deve essere esplicito; browser e tempo reale non
  devono entrare nel calcolo del voto.

Non sono emerse decisioni di prodotto bloccanti per M0-M3. La scelta 2D,
l'esperienza pubblica proposta e l'ABI TheBitLab sono già definite dai requisiti.
