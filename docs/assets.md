# Inventario degli asset

Inventario verificato il 21 agosto 2026.

| Percorso | Quantità | Provenienza | Licenza / diritti |
| --- | ---: | --- | --- |
| `images/*.png` | 53 | Fotografie originali e catture documentali realizzate dal maintainer; attestazione in `images/PROVENANCE.md` | Escluse da Apache-2.0 e CC BY-SA 4.0; copyright delle fotografie mantenuto dall'autore, elementi di terzi soggetti ai rispettivi diritti |
| `src/romeo/web/static/*` | 3 | HTML, CSS e JavaScript originali del progetto | Apache-2.0 |
| `course/activities/*/scenario.json` | 43 | Scenari originali generati per il corso | CC BY-SA 4.0 |

Le immagini sono raggruppate per funzione:

- installazione del sistema operativo e Raspberry Pi Imager: `1`–`16`;
- installazione di Romeo: `17`–`23`, inclusa la variante `19_romeo_installation2.png`;
- installazione CRICKIT: `24`–`28`;
- costruzione del robot e pan/tilt: `29`–`52`.

Il file storico `images/_` contiene soltanto una riga vuota, non è un asset.

## Provenienza confermata

Il maintainer ha attestato nel corso dell'audit di essere l'autore delle
fotografie originali usate nella guida di assemblaggio storica del README. La
dichiarazione persistente e le relative limitazioni sono registrate in
`images/PROVENANCE.md` e `images/LICENSE.md`.

I metadati disponibili restano evidenza tecnica accessoria: cinque file
(`19_romeo_installation.png`, `19_romeo_installation2.png`,
`26_crickit_installation.png`, `27_crickit_installation.png`,
`30_build_robot.png`) conservano modello `Redmi Note 13 5G` e timestamp coerente.
L'attestazione del maintainer risolve la precedente incertezza sulla provenienza
delle fotografie senza trasformare automaticamente questi asset in contenuto
CC BY-SA.

## Screenshot e diritti di terzi

I file che mostrano Raspberry Pi Imager, Raspberry Pi OS, terminali,
documentazione, marchi, loghi o prodotti di terzi sono catture documentali del
maintainer. La loro presenza non implica proprietà o rilicenza del software,
dell'interfaccia, della documentazione, dei marchi o del design rappresentato;
i relativi diritti restano ai rispettivi titolari.

## Vincolo di conservazione

Le 53 immagini PNG sono parte intenzionale della guida di assemblaggio storica e
non devono essere eliminate in seguito a questo audit. Eventuali release o
bundle che desiderino redistribuirle con una licenza esplicita separata devono
prima registrare quella concessione; il Course Bundle continua a non dipendere
da questi file.
