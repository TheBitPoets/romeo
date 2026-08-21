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
| 2 | U21–U23 | Lezioni riscritte: safety, integrazione e telepresenza; grading comportamentale e scaffold restano un gate aperto. |

Ogni materiale studente ora contiene: prerequisiti, modello mentale, esempio
minimo commentato, prova guidata, esercizio base, esercizio intermedio,
mini-sfida, errori tipici, autoverifica, supporto accessibile e glossario locale.
Hint, worksheet, rubriche ed exit ticket derivano dal contenuto specifico, non
rivelano la soluzione e chiedono una previsione e un'evidenza osservabile.

## Divergenza starter-lezione ancora aperta

I 23 starter del secondo anno contengono solo import e commenti generici, mentre
alcune lezioni descrivono server, thread, listener o harness come già forniti.
Adeguare gli starter richiede scegliere quale contratto didattico dovranno
implementare e importare gli hidden test; è quindi una decisione sull'esperienza
pubblica dello studente, non un refactoring silenzioso. La PR non è pronta
pedagogicamente finché questa scelta non viene presa e applicata.

## Limite valutativo

Gli scenari geometrici verificano comportamento del robot per submission
collaborative. I marker stdout del secondo anno sono soltanto feedback
trasparente e possono essere stampati senza acquisire la competenza. Hidden
behavioural test autorevoli richiedono prima il boundary sandbox deciso nel
threat model e un contratto di esercizio osservabile. Le activity Y2 dichiarano
quindi `test: false`: il plugin continua a mostrare i marker durante la pratica,
ma non vengono presentati come valutazione automatica.
