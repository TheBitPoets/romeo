# Build delle slide Romeo

Le slide sorgente sono Markdown/Marp. HTML, PDF e PPTX sono derivati e non vanno modificati a mano.

## Controllo strutturale

```bash
python scripts/build_slides.py --check-only
```

Il controllo verifica:

- 10 macro-deck numerati `00..09`;
- curriculum autorevole `20 + 23` unità;
- front matter Marp e checkpoint;
- link dashboard/indice;
- presenza dei manuali studente/docente e delle autorità hardware;
- mantenimento esplicito del boundary `romeo-doctor` pending.

## Build completa

```bash
python scripts/build_slides.py --formats html,pdf,pptx --browser chrome
```

Output:

```text
build/romeo-slides/
  html/
  pdf/
  pptx/
  MANIFEST.json
  SHA256SUMS.txt
```

Il renderer è fissato a `@marp-team/marp-cli@4.5.0`. HTML/PDF usano rendering parallelo; PPTX è intenzionalmente seriale per evitare timeout Chrome/Puppeteer già osservati nel consumer TPSI5.

Il manifest conserva lo SHA sorgente effettivo e dichiara il curriculum `romeo.curriculum.v1` con 20 unità Y1 e 23 Y2.