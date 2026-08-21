# Readiness della piattaforma Romeo

Audit finale eseguito il 21 agosto 2026 sul branch `feat/platform-foundation`.

## Stato pre-merge

La baseline tecnica è verificata, ma la PR non è ancora pronta al merge. Due
decisioni di progetto restano aperte: boundary sandbox per runtime plugin e
contratto didattico osservabile degli esercizi di secondo anno. I marker stdout
sono stati declassati a feedback formativo (`test: false`); starter e solution Y2
devono essere riallineati dopo la scelta. Anche i grader Y1 che misurano soltanto
il risultato geometrico vanno distinti dalle evidenze sui costrutti Python.

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
- tutte le 43 soluzioni docente eseguite; i 23 lab di rete passano attraverso il
  plugin completo e i relativi check di output;
- lint Ruff, typing mypy strict e suite pytest eseguiti su Python locale; la CI
  replica i gate su Python 3.10 e 3.12.

## Verifiche fisiche ancora necessarie

CI non può provare polarità e verso dei motori, limiti servo, camera Picamera2,
latenza effettiva del watchdog, alimentazione e brownout. Seguire
`docs/hardware/safety.md` su un esemplare reale e registrare modello/revisione e
risultato. Queste prove non impediscono simulazione, corso o grading headless.

## Licenze e provenienza degli asset

Il Course Bundle è CC BY-SA 4.0, ma il blocco sulle 53 immagini resta aperto:
la history non dimostra paternità e concessione. I PNG sono esclusi dalla
distribuzione finché issue #1 non contiene un'attestazione committata. Il
manifest del bundle non include queste immagini.

## M12

3D, sensori aggiuntivi, computer vision, navigazione autonoma e Webots restano
fuori dalla baseline. Lo stato/event protocol e i backend sostituibili preparano
l'evoluzione senza imporla. Ogni estensione richiede un caso didattico, budget di
dipendenze e verifica di privacy/hardware prima dell'implementazione.
