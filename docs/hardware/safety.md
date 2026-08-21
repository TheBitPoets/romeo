# Safety del robot fisico

Questa checklist è obbligatoria prima di impostare `ROMEO_BACKEND=crickit`. Il
watchdog software riduce il rischio, ma non corregge cablaggio, alimentazione o
parti meccaniche errate.

## Prima dell'alimentazione

- solleva le ruote dal tavolo per il primo test e libera l'area nelle prove a terra;
- verifica motore destro su CRICKIT motor 1 e sinistro su motor 2;
- verifica tensione, polarità, massa comune e limiti di corrente rispetto alle
  schede e ai motori effettivamente montati;
- fissa cavi, camera e batteria lontano da ruote e ingranaggi;
- prepara un arresto fisico accessibile e non lasciare il robot incustodito;
- non attivare camera o rete senza autorizzazioni e informativa adeguate.

## Collaudo progressivo

1. Installa l'extra con `python -m pip install -e ".[hardware]"` nel virtualenv
   Raspberry Pi.
2. Avvia con `ROMEO_MAX_SPEED=0.2` e `ROMEO_COMMAND_TIMEOUT=0.5`.
3. Prova `forward(0.1)` per meno di mezzo secondo con le ruote sollevate.
4. Se una ruota gira al contrario, modifica la configurazione
   `CrickitConfig`; non compensare nel programma dello studente.
5. Verifica che eccezione, `Ctrl+C`, perdita del client e timeout portino entrambi
   i throttle a zero.
6. Calibra pan/tilt partendo dal centro e restringi i limiti prima di raggiungere
   battute meccaniche.
7. Ripeti a terra in un'area delimitata aumentando gradualmente il limite.

## Invarianti software

Il backend reale è sempre avvolto da `SafetyBackend`: velocità limitata, watchdog,
timeout dei comandi, controller remoto esclusivo, stop su disconnessione e stop
durante shutdown/errori. I server devono essere avviati attraverso gli adapter
Romeo; evitare accesso diretto a `adafruit_crickit` nel codice applicativo.

La verifica CI del backend CRICKIT usa un test double. Cablaggio, direzione motori,
range servo, latenza e comportamento in caso di brownout restano prove hardware
da firmare sulla checklist dell'esemplare reale.
