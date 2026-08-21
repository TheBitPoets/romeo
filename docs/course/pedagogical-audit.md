# Audit pedagogico delle 43 unità

Audit pre-merge del 21 agosto 2026. La prima versione generava venti lezioni di
primo anno e ventitré di secondo anno da due testi quasi identici: i file
esistevano, ma mancavano spiegazione specifica, pratica graduata e prerequisiti
reali.

## Esito per unità

| Anno | Unità | Esito e intervento |
| --- | --- | --- |
| 1 | U01–U05 | Riscritte: ordine di esecuzione, componenti, REPL, chiamata e LED introdotti uno alla volta. |
| 1 | U06–U11 | Riscritte: ruota singola, coppia, direzione, rotazione, stop e velocità con esempi minimi e safety. |
| 1 | U12–U16 | Riscritte: funzioni, sequenze, `if`, `for`, `while`; ogni costrutto richiama solo prerequisiti già spiegati. |
| 1 | U17–U20 | Riscritte: simulazione, coordinate, missioni e capstone con evidenze e decomposizione progressiva. |
| 2 | U01–U07 | Riscritte: rete, IP, porte, ruoli, socket, protocollo testuale e JSON con modelli mentali separati. |
| 2 | U08–U13 | Riscritte: HTTP, REST, FastAPI, WebSocket, controller e tastiera con request/response e cleanup espliciti. |
| 2 | U14–U20 | Riscritte: camera, pan/tilt, foto, video, eventi, gamepad e telemetria includendo privacy e failure mode. |
| 2 | U21–U23 | Riscritte e riallineate: safety, integrazione e telepresenza con contratti osservabili e STOP verificato. |

Ogni materiale studente ora contiene: prerequisiti, modello mentale, esempio
minimo commentato, prova guidata, esercizio base, esercizio intermedio,
mini-sfida, errori tipici, autoverifica, supporto accessibile e glossario locale.
Hint, worksheet, rubriche ed exit ticket derivano dal contenuto specifico, non
rivelano la soluzione e chiedono una previsione e un'evidenza osservabile.

## Contratti osservabili del secondo anno

Le 23 unità espongono ora una funzione nominata e importabile. Starter,
consegna, soluzione e fixture usano la stessa firma; gli starter non aprono
socket, thread, camera o server durante l'import. Le astrazioni restano ordinarie:
funzioni pure dove possibile, dipendenze passate come parametri e cleanup
esplicito dove serve. I test provano input differenti, errori e lifecycle senza
chiedere agli studenti di conoscere fixture o framework di grading.

## Limite valutativo

I marker stdout restano soltanto feedback trasparente e non assegnano punti.
Le activity Y2 dichiarano `test: true`, `sandbox: true` e richiedono
`sandbox-plan.v1`; il voto deriva dai behavioural test nel broker ufficiale.
Il run locale è diagnostico e viene marcato non autorevole.
