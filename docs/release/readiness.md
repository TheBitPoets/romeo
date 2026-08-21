# Readiness della piattaforma Romeo

Audit finale eseguito il 21 agosto 2026 sul branch `feat/platform-foundation`.

## Stato pre-merge

Le due decisioni pre-merge sono state applicate: broker sandbox ufficiale
TheBitLab e funzioni nominate con behavioural test per Y2. La PR resta draft
finché la modifica coordinata `2cornot2c`, l'immagine Romeo firmata per digest e
la review finale non sono disponibili. I marker stdout sono solo feedback.

## Evidenze automatiche

- API `romeo.easy` e `Robot` esercitate con mock, simulatore e backend override;
- mock CRICKIT e adapter reale testati senza import hardware in CI;
- safety testata per speed limit, watchdog, timeout, lease, disconnessione,
  eccezioni e shutdown;
- fisica 2D, collisioni, scenari, traiettorie e grader deterministici testati;
- viewer, REST, WebSocket, protocollo TCP, client, tastiera, camera mock e
  gamepad verificati automaticamente;
- runtime `romeo-sim` scoperto dall'entry point ufficiale e conforme alla suite
  mirata `2cornot2c` (33 test upstream);
- Course Bundle 1.0.0 e 43 Activity validati anche con i validator upstream;
- tutte le 43 soluzioni docente eseguite; i 23 lab Y2 hanno starter importabili,
  soluzioni coerenti e hidden behavioural test senza marker valutativi;
- lint Ruff, typing mypy strict e suite pytest eseguiti su Python locale; la CI
  replica i gate su Python 3.10 e 3.12.

## Verifiche fisiche ancora necessarie

CI non può provare polarità e verso dei motori, limiti servo, camera Picamera2,
latenza effettiva del watchdog, alimentazione e brownout. Seguire
`docs/hardware/safety.md` su un esemplare reale e registrare modello/revisione e
risultato. Queste prove non impediscono simulazione, corso o grading headless.

## Licenze e provenienza degli asset

Il software è Apache-2.0 e il Course Bundle è CC BY-SA 4.0. La provenienza delle
53 immagini storiche è stata chiarita con un'attestazione persistente del
maintainer in `images/PROVENANCE.md`: le fotografie originali sono dell'autore
della guida e devono essere conservate perché fanno parte della guida di
assemblaggio storica del README.

Le immagini non vengono però assorbite automaticamente nella licenza del
software o del corso. `images/LICENSE.md` mantiene separati i diritti sulle
fotografie e preserva i diritti di terzi per screenshot, interfacce software,
documentazione, marchi, loghi e design di prodotto. Il manifest del Course
Bundle continua a non dipendere dai PNG storici.

## M12

3D, sensori aggiuntivi, computer vision, navigazione autonoma e Webots restano
fuori dalla baseline. Lo stato/event protocol e i backend sostituibili preparano
l'evoluzione senza imporla. Ogni estensione richiede un caso didattico, budget di
dipendenze e verifica di privacy/hardware prima dell'implementazione.
