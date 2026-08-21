# Inventario degli asset

Inventario verificato il 21 agosto 2026.

| Percorso | Quantità | Provenienza | Licenza |
| --- | ---: | --- | --- |
| `images/*.png` | 53 | Presenti nei commit iniziali; autore dichiarato in chat ma non attestato nel repository | Non determinata; esclusi dalla distribuzione |
| `src/romeo/web/static/*` | 3 | HTML, CSS e JavaScript originali del progetto | Apache-2.0 |
| `course/activities/*/scenario.json` | 43 | Scenari originali generati per il corso | CC BY-SA 4.0 |

Le immagini sono raggruppate per funzione:

- installazione del sistema operativo e Raspberry Pi Imager: `1`–`16`;
- installazione di Romeo: `17`–`23`, inclusa la variante `19_romeo_installation2.png`;
- installazione CRICKIT: `24`–`28`;
- costruzione del robot e pan/tilt: `29`–`52`.

Il file storico `images/_` contiene soltanto una riga vuota, non è un asset e
non viene distribuito come contenuto del corso.

La verifica ha considerato ciascuno dei 53 file: storia Git, nomi, contenuto e
metadati disponibili non forniscono una prova autonoma di paternità o licenza.
Il requisito resta aperto in issue #1. Prima della distribuzione il titolare deve
committare un'attestazione che identifichi tutti i file e la licenza scelta;
fino ad allora i PNG restano nel repository storico ma fuori dai release asset.
