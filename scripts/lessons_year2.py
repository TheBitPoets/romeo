"""Unit-specific lessons for the networking-focused second year."""

# ruff: noqa: E501, I001 -- complete lesson prose is intentionally kept near its unit.

from __future__ import annotations

from pedagogy_content import LessonContent


LESSONS_Y2: dict[str, LessonContent] = {
    "rete": LessonContent(
        prerequisites="Sai eseguire un programma Python, usare variabili e leggere un semplice diagramma con frecce.",
        mental_model=(
            "Una rete è un insieme di dispositivi che possono scambiarsi dati. Immagina una scuola: "
            "l'host è una persona, la rete è il sistema di corridoi e il servizio è lo sportello a cui "
            "la persona si rivolge. L'analogia aiuta a separare i ruoli, ma i dati viaggiano in piccoli "
            "blocchi e non come persone intere. `127.0.0.1` è il percorso speciale con cui un host parla a sé stesso."
        ),
        example="""Il primo esperimento non usa Internet: riconosce il percorso locale.

```python
from ipaddress import ip_address

indirizzo = ip_address("127.0.0.1")
print(indirizzo.is_loopback)  # True: il messaggio resta su questo computer
```

Lo scaffold importa `ip_address`: in questa unità non dobbiamo ancora conoscere i socket.""",
        guided_practice=(
            "Disegna due host come rettangoli e una rete come linea fra loro; aggiungi un servizio dentro ogni host.",
            "Esegui l'esempio e osserva che il risultato è un valore booleano.",
            "Scrivi accanto a ogni elemento del disegno se è host, rete o servizio.",
            "Sostituisci l'indirizzo con `192.0.2.10` e prevedi il risultato prima di eseguire.",
            "Ripristina il loopback e usa un `assert` prima del messaggio finale.",
        ),
        base_exercise="Riconosci `127.0.0.1` come loopback e stampa il risultato soltanto dopo la verifica.",
        intermediate_exercise="Classifica sei esempi dati dal docente come host, collegamento di rete o servizio e motiva due risposte.",
        challenge="Disegna il percorso concettuale computer studente → rete locale → Romeo → servizio di controllo, senza indicare ancora porte.",
        common_errors=(
            "Confondere la rete con Internet: una rete può esistere anche senza accesso esterno.",
            "Chiamare servizio l'intero Raspberry Pi: il Raspberry Pi è l'host che ospita uno o più servizi.",
            "Pensare che loopback indichi Romeo: indica sempre il computer che esegue il programma.",
        ),
        self_check=(
            "So indicare host, rete e servizio in un disegno?",
            "So spiegare dove resta un messaggio inviato a loopback?",
            "Il mio programma verifica il dato prima di dichiarare successo?",
        ),
        accessibility="Usa etichette e forme oltre ai colori nel diagramma. È possibile descrivere a voce il percorso come elenco ordinato.",
        glossary=(("host", "dispositivo collegato alla rete"), ("servizio", "funzione offerta da un programma"), ("loopback", "percorso con cui un host comunica con sé stesso")),
    ),
    "indirizzi-ip": LessonContent(
        prerequisites="Sai distinguere host, rete e servizio e sai usare stringhe e confronti in Python.",
        mental_model=(
            "Un indirizzo IP identifica un'interfaccia di rete, come un numero civico identifica una destinazione. "
            "Un nome come `localhost` è più facile da ricordare e viene risolto in un indirizzo. Il paragone postale "
            "non è perfetto: un host può avere più indirizzi e un indirizzo può cambiare."
        ),
        example="""Risolviamo un nome e poi controlliamo il risultato.

```python
import socket
from ipaddress import ip_address

testo = socket.gethostbyname("localhost")  # nome → testo IPv4
indirizzo = ip_address(testo)              # testo → oggetto verificabile
print(testo, indirizzo.version)
```

`gethostbyname` è fornita da Python: in questa lezione osserviamo la risoluzione, non la implementiamo.""",
        guided_practice=(
            "Prevedi se `localhost` è un nome o un indirizzo.",
            "Esegui l'esempio e annota il testo restituito.",
            "Stampa `type(testo)` e `type(indirizzo)` per distinguere rappresentazione e oggetto.",
            "Verifica che la versione sia 4 e che `indirizzo.is_loopback` sia vero.",
            "Simula un errore passando a `ip_address` un testo non valido e leggi il messaggio senza nasconderlo.",
        ),
        base_exercise="Risolvi `localhost` e verifica che produca un IPv4 di loopback.",
        intermediate_exercise="Confronta `127.0.0.1` e il risultato della risoluzione spiegando perché rappresentano lo stesso percorso locale.",
        challenge="Scrivi una funzione `descrivi(indirizzo)` che restituisce `locale` oppure `non locale` usando `is_loopback`.",
        common_errors=(
            "Confondere il nome `localhost` con il suo indirizzo numerico.",
            "Controllare soltanto che il testo contenga punti invece di validarlo.",
            "Usare l'indirizzo locale pensando di raggiungere il Raspberry Pi remoto.",
        ),
        self_check=("So descrivere il passaggio nome → indirizzo?", "So distinguere stringa e oggetto `IPv4Address`?", "So verificare che un indirizzo sia loopback?"),
        accessibility="Leggi gli indirizzi anche cifra per cifra; non affidarti alla sola posizione in un diagramma e lascia il risultato testuale copiabile.",
        glossary=(("indirizzo IP", "identificatore numerico di un'interfaccia di rete"), ("DNS", "sistema che risolve nomi in indirizzi"), ("IPv4", "formato di indirizzo composto da quattro numeri")),
    ),
    "porte": LessonContent(
        prerequisites="Sai cos'è un host e sai usare tuple e `with` in Python.",
        mental_model=(
            "L'indirizzo porta il messaggio all'host; la porta lo consegna al servizio corretto. Un endpoint è quindi "
            "la coppia `(indirizzo, porta)`. La porta `0` non è la porta del servizio: durante `bind` chiede al sistema "
            "di scegliere temporaneamente una porta disponibile."
        ),
        example="""Lo scaffold crea e chiude il socket; osserviamo solo l'assegnazione della porta.

```python
import socket

with socket.socket() as listener:
    listener.bind(("127.0.0.1", 0))
    endpoint = listener.getsockname()
    print(endpoint)  # per esempio ('127.0.0.1', 53124)
```

Il socket è una risorsa del sistema: `with` lo chiude anche in caso di errore.""",
        guided_practice=(
            "Cerchia separatamente indirizzo e porta nell'endpoint dell'esempio.",
            "Prevedi quale parte resta stabile e quale può cambiare fra due esecuzioni.",
            "Esegui due volte e registra le porte scelte.",
            "Estrai la porta con `listener.getsockname()[1]`.",
            "Verifica che sia compresa fra 1 e 65535 prima di stampare il marker.",
        ),
        base_exercise="Chiedi una porta effimera al sistema e verifica che sia positiva.",
        intermediate_exercise="Crea due listener contemporanei sulla porta `0` e verifica che abbiano endpoint diversi.",
        challenge="Spiega perché salvare una porta trovata chiudendo subito il socket non garantisce che resti libera.",
        common_errors=("Usare soltanto la porta e dimenticare l'indirizzo.", "Pensare che `0` sia la porta finale assegnata.", "Dimenticare di chiudere il socket dopo l'esperimento."),
        self_check=("So costruire un endpoint?", "So spiegare che cosa fa `bind`?", "So trovare la porta realmente assegnata?"),
        accessibility="Rappresenta l'endpoint sia come coppia scritta sia come diagramma. Pronuncia separatamente indirizzo e porta.",
        glossary=(("porta", "numero che seleziona un servizio su un host"), ("endpoint", "coppia indirizzo e porta"), ("bind", "associazione di un socket a un endpoint locale")),
    ),
    "client-server": LessonContent(
        prerequisites="Sai distinguere host e servizio, conosci gli endpoint e sai usare byte letterali come `b\"PING\"`.",
        mental_model=(
            "Il client avvia una richiesta; il server attende e risponde. In questa prima prova `socketpair` crea due "
            "estremità locali già collegate: nasconde indirizzi, porte e apertura della connessione per farci osservare "
            "soltanto lo scambio di byte. Non è ancora un server TCP reale."
        ),
        example="""```python
import socket

client, server = socket.socketpair()  # coppia locale già collegata
with client, server:
    client.sendall(b"PING\n")
    ricevuto = server.recv(16)
    print(ricevuto)                    # b'PING\n'
```

`recv(16)` può ricevere fino a 16 byte; una rete reale non promette un messaggio intero per ogni `recv`.""",
        guided_practice=(
            "Disegna due estremità e una freccia PING dal client al server.",
            "Esegui l'esempio e osserva la `b` davanti al dato stampato.",
            "Aggiungi la risposta `PONG` nella direzione opposta.",
            "Verifica entrambi i byte ricevuti con `assert`.",
            "Rimuovi temporaneamente l'invio di PONG e prevedi perché il client rimarrebbe in attesa.",
        ),
        base_exercise="Completa uno scambio PING/PONG sulla coppia locale.",
        intermediate_exercise="Invia due parole in un unico blocco e separale usando il carattere di fine riga.",
        challenge="Disegna che cosa dovrà essere aggiunto per trasformare la coppia locale in client e server TCP su loopback.",
        common_errors=("Inviare una stringa invece di byte.", "Leggere prima che l'altra estremità abbia inviato.", "Credere che `recv(16)` restituisca sempre esattamente 16 byte."),
        self_check=("So indicare chi avvia ogni messaggio?", "So distinguere stringhe e byte?", "So chiudere entrambe le estremità?"),
        accessibility="Affianca alle frecce parole `invia` e `riceve`; recita la sequenza in ordine per chi non usa il diagramma.",
        glossary=(("client", "programma che avvia una richiesta"), ("server", "programma che attende e risponde"), ("byte", "unità di dati trasmessa dal socket")),
    ),
    "socket": LessonContent(
        prerequisites="Sai scambiare byte su una coppia locale e conosci indirizzo, porta, client e server.",
        mental_model=(
            "Un server TCP prepara un punto di ascolto con `bind` e `listen`; `accept` crea un nuovo socket dedicato "
            "a un client. Il client usa `connect`. Per far avanzare server e client nello stesso programma lo scaffold "
            "avvia il server in un thread: la concorrenza è fornita, non è l'obiettivo da implementare oggi."
        ),
        example="""Lo scaffold contiene `serve_once` e il thread. Tu completi il client.

```python
with socket.create_connection(("127.0.0.1", porta), timeout=2) as client:
    client.sendall(b"HELLO\n")
    risposta = client.recv(32)
    assert risposta == b"WELCOME\n"
```

Il timeout impedisce un'attesa infinita; non garantisce che la rete risponda in tempo.""",
        guided_practice=(
            "Ordina le tessere bind, listen, connect, accept, send, recv.",
            "Segui nel diagramma il socket di ascolto e il nuovo socket restituito da `accept`.",
            "Avvia lo scaffold e completa soltanto il blocco client.",
            "Aggiungi timeout e verifica la risposta prima del marker.",
            "Esegui due volte e controlla che thread e socket vengano sempre chiusi.",
        ),
        base_exercise="Completa il client che saluta il server fornito e valida `WELCOME`.",
        intermediate_exercise="Completa il corpo di `serve_once` nello scaffold, mantenendo timeout e context manager.",
        challenge="Gestisci un saluto errato restituendo `ERROR` senza lasciare thread o socket aperti.",
        common_errors=("Chiamare `connect` prima che il listener sia pronto.", "Confondere il socket listener con quello della connessione accettata.", "Usare `recv` senza timeout durante il debug."),
        self_check=("So raccontare l'ordine di apertura della connessione?", "So indicare i due socket lato server?", "Il programma termina anche con input errato?"),
        accessibility="Fornisci anche una sequenza numerata testuale del diagramma temporale. Lo scaffold evita che difficoltà con i thread oscurino il concetto di TCP.",
        glossary=(("listen", "mette il socket in attesa di connessioni"), ("accept", "accetta un client e restituisce il socket della connessione"), ("thread", "flusso concorrente fornito qui dallo scaffold")),
    ),
    "protocollo-testuale": LessonContent(
        prerequisites="Sai scambiare righe di byte e usare `split`, condizioni e conversioni numeriche.",
        mental_model=(
            "Un protocollo è un accordo preciso sul significato dei messaggi. Romeo/1 usa una riga per comando: "
            "prima una parola ammessa, poi gli eventuali argomenti. Una whitelist elenca ciò che è valido; tutto il "
            "resto viene rifiutato senza eseguire azioni."
        ),
        example="""```python
riga = "FORWARD 0.4"
parti = riga.split()
comando = parti[0]

if comando not in {"FORWARD", "STOP"}:
    raise ValueError("comando sconosciuto")
```

Il parser Romeo completo è fornito dalla libreria; prima ne osserviamo le regole con codice semplice.""",
        guided_practice=("Compila una tabella con `FORWARD velocità` e `STOP`.", "Separa tre righe valide con `split`.", "Prova un comando sconosciuto e controlla che venga rifiutato.", "Usa `parse_command` e osserva nome e argomenti.", "Verifica anche argomento mancante e velocità fuori limite."),
        base_exercise="Analizza `FORWARD 0.4` e `STOP` verificando nome e argomenti.",
        intermediate_exercise="Costruisci una tabella di almeno quattro input invalidi e del motivo del rifiuto.",
        challenge="Produci risposte testuali coerenti `OK` o `ERROR motivo` senza muovere il robot per input invalidi.",
        common_errors=("Accettare qualsiasi parola e passarla direttamente al robot.", "Dimenticare di convertire e limitare la velocità.", "Ignorare il fine riga e unire due comandi ricevuti insieme."),
        self_check=("So scrivere la grammatica dei due comandi?", "So spiegare perché serve una whitelist?", "Il mio codice rifiuta dati invalidi prima dell'azione?"),
        accessibility="La tabella del protocollo usa testo e non colori. Leggi gli errori con una motivazione breve e stabile.",
        glossary=(("protocollo", "regole condivise per interpretare messaggi"), ("whitelist", "elenco esplicito dei valori ammessi"), ("argomento", "valore che completa un comando")),
    ),
    "json": LessonContent(
        prerequisites="Sai usare dizionari, liste, stringhe, numeri e booleani Python.",
        mental_model=(
            "JSON è testo con una struttura condivisa. `json.dumps` trasforma un oggetto Python in testo da inviare; "
            "`json.loads` ricostruisce dati Python dal testo. JSON non apre connessioni e non esegue comandi."
        ),
        example="""```python
import json

stato = {"moving": True, "motors": [0.3, 0.3]}
testo = json.dumps(stato)   # dict → str
copia = json.loads(testo)  # str → dict
print(type(testo), type(copia))
```

Controllare i tipi dopo la decodifica evita di fidarsi soltanto dell'aspetto del testo.""",
        guided_practice=("Prevedi i tipi di `stato`, `testo` e `copia`.", "Esegui e verifica le previsioni.", "Aggiungi il campo stringa `type`.", "Modifica il testo rendendolo invalido e osserva `JSONDecodeError`.", "Verifica campi e tipi prima di usare i valori."),
        base_exercise="Serializza e decodifica lo stato di Romeo mantenendo tipo e valori.",
        intermediate_exercise="Valida un messaggio richiedendo `type`, due velocità numeriche e `moving` booleano.",
        challenge="Restituisci un errore leggibile per JSON malformato o con schema incompleto.",
        common_errors=("Confondere un dizionario con il testo JSON che lo rappresenta.", "Scrivere `True` a mano nel JSON, dove il valore è `true`.", "Usare campi ricevuti senza verificarne presenza e tipo."),
        self_check=("So descrivere serializzazione e deserializzazione?", "So indicare il tipo prima e dopo?", "So gestire un messaggio malformato?"),
        accessibility="Mostra dict e JSON su righe separate con etichette; non segnalare le differenze solo con colori.",
        glossary=(("serializzazione", "trasformazione dei dati in un formato trasmissibile"), ("schema", "insieme dei campi e tipi attesi"), ("JSON", "formato testuale strutturato")),
    ),
    "http": LessonContent(
        prerequisites="Conosci client/server, endpoint, protocollo testuale e JSON.",
        mental_model=(
            "HTTP organizza uno scambio in request e response. La request contiene metodo e risorsa; la response "
            "contiene status, header e body. Il server e il thread sono già nello scaffold: oggi leggiamo il protocollo, "
            "non implementiamo ancora un server web."
        ),
        example="""```text
GET /status HTTP/1.1       ← metodo e risorsa

HTTP/1.1 200 OK           ← status
Content-Type: application/json

{"status": "ok"}          ← body
```

```python
with urllib.request.urlopen(url, timeout=2) as risposta:
    print(risposta.status, risposta.headers["Content-Type"])
```
""",
        guided_practice=("Etichetta metodo, path, status, header e body nell'esempio.", "Prevedi il significato di 200 e 404.", "Interroga il server locale fornito dallo scaffold.", "Verifica status e Content-Type prima di leggere il JSON.", "Richiedi un path inesistente e osserva la risposta d'errore."),
        base_exercise="Esegui GET sul server locale fornito e valida status 200 e body JSON.",
        intermediate_exercise="Gestisci separatamente una risposta 404 senza dichiarare successo.",
        challenge="Confronta due response con lo stesso body ma Content-Type diversi e spiega quale rispetta il contratto.",
        common_errors=("Guardare soltanto il body e ignorare lo status.", "Confondere metodo HTTP e nome della funzione Python.", "Costruire subito server, thread e handler senza isolare il concetto HTTP."),
        self_check=("So scomporre una request?", "So scomporre una response?", "So verificare status e media type prima del body?"),
        accessibility="Presenta request e response come testo copiabile oltre al diagramma; pronuncia i codici cifra per cifra e spiegane il significato.",
        glossary=(("request", "messaggio inviato dal client HTTP"), ("response", "risposta del server HTTP"), ("header", "metadato della richiesta o risposta"), ("body", "contenuto del messaggio")),
    ),
    "rest": LessonContent(
        prerequisites="Sai leggere request e response HTTP e decodificare JSON.",
        mental_model=(
            "REST tratta gli elementi del sistema come risorse con indirizzi stabili. `GET /api/status` chiede una "
            "rappresentazione dello stato; non significa 'esegui una funzione chiamata status'. TestClient sostituisce "
            "la rete esterna ma conserva metodo, path, status e body. FastAPI è nascosto nello scaffold fino alla prossima unità."
        ),
        example="""```python
with TestClient(create_app()) as client:  # app già fornita
    response = client.get("/api/status")
    assert response.status_code == 200
    stato = response.json()
    print(stato["status"])
```

Il client consuma la risorsa; non ha bisogno di conoscere come il server la costruisce.""",
        guided_practice=("Individua la risorsa nel path `/api/status`.", "Prevedi quali parti della response vanno validate.", "Esegui il client sul servizio fornito.", "Controlla status, Content-Type e campi JSON.", "Richiedi una risorsa inesistente e confronta il risultato."),
        base_exercise="Leggi `/api/status` e verifica il contratto minimo.",
        intermediate_exercise="Scrivi una funzione client che restituisce `moving` soltanto per una response valida.",
        challenge="Progetta path e rappresentazione JSON per una risorsa `info` senza implementare il server.",
        common_errors=("Chiamare REST qualsiasi risposta JSON.", "Inserire verbi come `getStatus` nel path senza ragionare sulla risorsa.", "Fidarsi del JSON senza controllare lo status."),
        self_check=("So spiegare che cosa rappresenta una risorsa?", "So distinguere HTTP da stile REST?", "Il mio client rifiuta response incomplete?"),
        accessibility="Scrivi sempre metodo e path insieme (`GET /api/status`) e accompagna ogni icona con un'etichetta testuale.",
        glossary=(("REST", "stile per organizzare risorse e operazioni HTTP"), ("risorsa", "elemento identificato da un path"), ("rappresentazione", "dati che descrivono una risorsa")),
    ),
    "fastapi": LessonContent(
        prerequisites="Sai definire funzioni Python e conosci route REST, status e JSON.",
        mental_model=(
            "FastAPI collega una coppia metodo+path a una normale funzione Python. Il decorator `@app.get` registra "
            "la route: non cambia il ragionamento dentro la funzione. TestClient avvia l'app in memoria; nasconde socket "
            "e thread per farci concentrare sulla route."
        ),
        example="""```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/status")          # registra GET /status
def status() -> dict[str, object]:
    return {"ready": True}  # FastAPI lo converte in JSON
```

La firma tipizzata documenta il valore restituito; OpenAPI descrive automaticamente le route registrate.""",
        guided_practice=("Leggi decorator, firma e return separatamente.", "Completa il solo dizionario restituito dalla route fornita.", "Usa TestClient per verificare status e JSON.", "Apri `/openapi.json` e trova il path registrato.", "Aggiungi una seconda route semplice senza copiare tutta l'app."),
        base_exercise="Implementa `GET /status` con risposta tipizzata e testala.",
        intermediate_exercise="Aggiungi `GET /info` con nome e versione e verifica entrambe le route.",
        challenge="Aggiungi un parametro di path semplice e verifica anche il caso non valido restituito dal framework.",
        common_errors=("Dimenticare `@` davanti al decorator.", "Restituire testo che sembra JSON invece di un dizionario Python.", "Confondere il path della route con il nome della funzione."),
        self_check=("So indicare quale riga registra la route?", "So spiegare chi converte il dizionario in JSON?", "So trovare la route nello schema OpenAPI?"),
        accessibility="Mostra il codice con annotazioni testuali, non solo evidenziazione sintattica; fornisci una tabella route→funzione.",
        glossary=(("route", "associazione fra metodo, path e funzione"), ("decorator", "riga con `@` che registra la funzione nel framework"), ("OpenAPI", "descrizione strutturata dell'API")),
    ),
    "websocket": LessonContent(
        prerequisites="Conosci HTTP, JSON e FastAPI; sai usare un context manager.",
        mental_model=(
            "HTTP normale apre uno scambio request/response; WebSocket mantiene un canale aperto in cui entrambe le "
            "parti possono inviare messaggi. Lo scaffold fornisce server e gestione asincrona: il client didattico usa "
            "TestClient sincrono, così il nuovo concetto è soltanto la conversazione persistente."
        ),
        example="""```python
with client.websocket_connect("/ws/control") as ws:
    pronto = ws.receive_json()
    ws.send_json({"command": "STOP"})
    risposta = ws.receive_json()
```

```text
server → ready
client → STOP
server → ack
```

L'ordine fa parte del protocollo; la chiusura del `with` termina la connessione.""",
        guided_practice=("Confronta una timeline HTTP con quella WebSocket.", "Numera ready, comando e ack.", "Collegati al server fornito e verifica `ready`.", "Invia STOP e valida l'ack completo.", "Chiudi senza inviare altri dati e verifica che il robot resti fermo."),
        base_exercise="Completa la conversazione ready→STOP→ack.",
        intermediate_exercise="Invia un comando invalido e verifica una risposta error senza perdere la connessione.",
        challenge="Disegna come heartbeat o timeout rileverebbero un client scomparso, senza implementarli qui.",
        common_errors=("Inviare prima di leggere il messaggio ready previsto.", "Confondere WebSocket con una serie di GET HTTP.", "Uscire senza verificare lo STOP alla disconnessione."),
        self_check=("So spiegare perché la connessione resta aperta?", "So indicare chi invia ogni messaggio?", "So descrivere cosa deve accadere alla chiusura?"),
        accessibility="La sequenza dei messaggi è disponibile come elenco testuale oltre alle frecce; gli ack sono leggibili e non dipendono da animazioni.",
        glossary=(("WebSocket", "canale persistente e bidirezionale"), ("frame", "unità trasmessa sul WebSocket"), ("ack", "risposta che conferma la gestione del messaggio")),
    ),
    "web-controller": LessonContent(
        prerequisites="Conosci eventi semplici, payload JSON e conversazione WebSocket ready/comando/ack.",
        mental_model=(
            "Il controller web ha due responsabilità separate: un evento dell'interfaccia sceglie un comando; il "
            "trasporto lo invia. Lo scaffold fornisce pagina, connessione e listener del browser. Tu completi una "
            "funzione pura che traduce azione in payload, così puoi testarla senza clic reali."
        ),
        example="""```javascript
function payloadFor(action) {
  if (action === "forward") {
    return {command: "FORWARD", speed: 0.25};
  }
  return {command: "STOP"};
}
```

Il pulsante e la tastiera possono chiamare la stessa funzione; il feedback mostra l'ultimo ack anche come testo.""",
        guided_practice=("Associa ogni pulsante a un'azione scritta.", "Prevedi il payload di avanti e stop.", "Completa la funzione di traduzione nello scaffold.", "Verifica i payload senza rete.", "Collega la funzione al WebSocket fornito e osserva ack ed errore."),
        base_exercise="Traduci pulsanti avanti e stop in payload validi.",
        intermediate_exercise="Aggiungi indietro, sinistra e destra mantenendo una sola funzione di mapping.",
        challenge="Disabilita i comandi di movimento quando la connessione non è pronta e lascia STOP sempre disponibile.",
        common_errors=("Mescolare selezione del comando e dettagli del WebSocket in ogni pulsante.", "Inviare stringhe diverse dal protocollo documentato.", "Mostrare stato soltanto tramite colore senza testo."),
        self_check=("So testare il mapping senza browser?", "Tutti i controlli producono payload validi?", "L'interfaccia mostra connessione e ack in testo?"),
        accessibility="Ogni pulsante ha etichetta, focus da tastiera e stato testuale; non usare soltanto colore, hover o posizione per comunicare il comando.",
        glossary=(("evento UI", "azione prodotta da pulsante o tastiera"), ("payload", "dati contenuti nel messaggio"), ("feedback", "informazione visibile sul risultato del comando")),
    ),
    "tastiera-remota": LessonContent(
        prerequisites="Sai gestire un evento con una funzione e conosci il protocollo testuale e lo STOP WebSocket.",
        mental_model=(
            "La tastiera produce tasti, ma il robot accetta comandi. Una funzione pura converte W/A/S/D/SPACE; un "
            "client separato trasporta il comando. Lo scaffold gestisce le differenze del terminale e la connessione: "
            "lo studente non deve leggere direttamente caratteri grezzi dal sistema operativo."
        ),
        example="""```python
from romeo.network.keyboard import command_for_key

comando = command_for_key("w")
print(comando.name)  # FORWARD
```

Lo STOP va inviato anche in `finally`, perché un errore o la chiusura non devono lasciare Romeo in movimento.""",
        guided_practice=("Compila la tabella W/A/S/D/SPACE.", "Prova ogni tasto con la funzione pura.", "Verifica maiuscole, minuscole e tasto sconosciuto.", "Collega il mapping al client fornito.", "Simula un errore e osserva lo STOP nel blocco `finally`."),
        base_exercise="Trasforma W e SPACE in FORWARD e STOP.",
        intermediate_exercise="Gestisci tutti i tasti previsti e ignora in modo esplicito quelli sconosciuti.",
        challenge="Crea una sequenza controllata che invia STOP dopo un periodo senza nuovi tasti.",
        common_errors=("Inviare il tasto grezzo invece del comando di protocollo.", "Dimenticare SPACE o lo STOP finale.", "Dipendere da una API terminal-specific non presente sul computer dello studente."),
        self_check=("So separare mapping e trasporto?", "Ogni uscita dal programma invia STOP?", "Esiste un'alternativa ai tasti per chi non può usarli?"),
        accessibility="Mantieni anche pulsanti cliccabili e rimappabili; stampa il comando riconosciuto e non richiedere pressioni simultanee.",
        glossary=(("mapping", "corrispondenza fra tasto e comando"), ("timeout", "tempo massimo senza un nuovo evento"), ("finally", "blocco eseguito anche quando avviene un errore")),
    ),
    "camera": LessonContent(
        prerequisites="Sai usare oggetti, chiamare metodi e chiudere risorse con `try/finally`.",
        mental_model=(
            "CameraService è una presa comune: il codice chiede una foto senza sapere se dietro c'è Picamera2 o un "
            "mock. Il mock restituisce dati prevedibili in classe e CI. La camera reale richiede hardware, permesso e "
            "segnalazione chiara; questi dettagli restano nell'implementazione del servizio."
        ),
        example="""```python
camera = MockCameraService()
try:
    foto = camera.capture_photo()
    assert foto.startswith(b"\xff\xd8")
finally:
    camera.close()
```

I byte non vengono visualizzati: controlliamo soltanto il contratto minimo del servizio.""",
        guided_practice=("Individua chiamante, interfaccia e implementazione nel diagramma.", "Cattura una foto dal mock.", "Osserva tipo e lunghezza senza stampare tutti i byte.", "Sposta `close` in `finally`.", "Simula camera non disponibile e produci un messaggio comprensibile."),
        base_exercise="Acquisisci e valida una foto dal mock senza importare Picamera2.",
        intermediate_exercise="Scrivi una funzione che riceve un CameraService come parametro e restituisce la dimensione della foto.",
        challenge="Gestisci `available == False` senza tentare la cattura e garantendo cleanup.",
        common_errors=("Importare direttamente Picamera2 nel programma applicativo.", "Stampare migliaia di byte della foto.", "Dimenticare privacy e chiusura della camera su errore."),
        self_check=("Il mio codice funziona con un mock?", "La camera viene sempre chiusa?", "So spiegare perché l'hardware è isolato?"),
        accessibility="Descrivi testualmente stato camera e risultato; prevedi attività completa col mock per chi non può usare o essere ripreso dalla camera.",
        glossary=(("CameraService", "contratto comune per le operazioni della camera"), ("mock", "sostituto prevedibile usato nei test"), ("JPEG", "formato compresso dei byte della foto")),
    ),
    "pan-tilt": LessonContent(
        prerequisites="Conosci la API Robot, i numeri decimali e il CameraService.",
        mental_model=(
            "Pan ruota lo sguardo a sinistra/destra; tilt lo inclina su/giù. Gli angoli sono gradi entro limiti sicuri. "
            "Robot inoltra la richiesta al backend: il mock registra gli angoli, mentre il backend reale muove i servo."
        ),
        example="""```python
backend = MockBackend()
robot = Robot(backend)
try:
    robot.look(pan=60, tilt=120)
    print(backend.pan_angle, backend.tilt_angle)
finally:
    robot.close()
```

Lo scaffold mostra gli assi con etichette e fornisce limiti sicuri; non forzare manualmente i servo.""",
        guided_practice=("Indica pan e tilt su un disegno etichettato.", "Porta prima la camera nella posizione centrale fornita.", "Cambia un asse alla volta e prevedi il risultato.", "Verifica i valori registrati dal mock.", "Prova un valore fuori limite senza collegare hardware reale."),
        base_exercise="Imposta pan 60 e tilt 120 sul backend mock.",
        intermediate_exercise="Scrivi `centra_camera(robot)` usando gli angoli centrali documentati.",
        challenge="Limita in modo esplicito due valori ricevuti prima di passarli a `look` e spiega la scelta.",
        common_errors=("Scambiare pan e tilt.", "Assumere che qualsiasi angolo sia fisicamente sicuro.", "Dimenticare `close` quando un assert fallisce."),
        self_check=("So indicare i due assi?", "Conosco unità e limiti?", "Il test usa il mock prima dell'hardware?"),
        accessibility="Accompagna le frecce con parole sinistra/destra/su/giù e valori numerici; consenti controllo tramite pulsanti grandi oltre agli assi analogici.",
        glossary=(("pan", "rotazione orizzontale della camera"), ("tilt", "inclinazione verticale della camera"), ("servo", "motore comandato verso una posizione angolare")),
    ),
    "fotografia": LessonContent(
        prerequisites="Conosci REST, TestClient, JSON, byte JPEG e CameraService mock.",
        mental_model=(
            "Una foto REST è una risorsa binaria: la response contiene byte JPEG invece di JSON. Status e Content-Type "
            "dicono al client se e come interpretarla. `create_app(camera=mock)` passa alla app una camera prevedibile; "
            "questa iniezione evita hardware reale durante il test."
        ),
        example="""```python
with TestClient(create_app(camera=MockCameraService())) as client:
    response = client.get("/api/camera/photo")
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/jpeg"
```

Solo dopo questi controlli usiamo `response.content` come JPEG.""",
        guided_practice=("Confronta una response JSON e una JPEG.", "Individua dove il mock viene passato alla app.", "Richiedi la foto e controlla lo status.", "Controlla Content-Type e marker JPEG.", "Simula camera indisponibile e verifica una risposta d'errore."),
        base_exercise="Valida status, media type e contenuto della foto mock.",
        intermediate_exercise="Salva i byte soltanto dopo la validazione e verifica che il file non sia vuoto.",
        challenge="Definisci il comportamento REST per camera non disponibile, motivando status e body d'errore.",
        common_errors=("Chiamare `.json()` su una foto.", "Accettare qualsiasi contenuto con status 200.", "Usare la camera reale nei test automatici."),
        self_check=("So distinguere response JSON e binaria?", "Controllo il Content-Type?", "Il test è ripetibile senza hardware?"),
        accessibility="L'esito della foto è descritto anche con testo, dimensione e status; nessuno deve essere ripreso per completare il laboratorio.",
        glossary=(("Content-Type", "header che descrive il formato del body"), ("iniezione", "passaggio esplicito di un collaboratore alla app"), ("binario", "dati composti da byte, non testo JSON")),
    ),
    "video": LessonContent(
        prerequisites="Sai leggere byte JPEG e una response HTTP; conosci iteratori e `next` grazie a uno scaffold guidato.",
        mental_model=(
            "MJPEG invia una sequenza di immagini JPEG dentro una response HTTP multipart. Un boundary separa i frame, "
            "come un divisore etichettato. Lo scaffold costruisce server e generatore: lo studente osserva due parti e "
            "verifica la struttura, senza implementare streaming o concorrenza da zero."
        ),
        example="""```text
--frame
Content-Type: image/jpeg

<byte JPEG>
--frame
Content-Type: image/jpeg

<byte JPEG>
```

```python
primo = next(camera.frames(frames_per_second=10))
assert primo.startswith(b"\xff\xd8")
```

Il secondo frammento controlla il JPEG; il boundary appartiene al livello HTTP multipart.""",
        guided_practice=("Evidenzia testualmente i due boundary nell'esempio.", "Distingui header della parte e byte del frame.", "Leggi due frame dal generatore mock fornito.", "Verifica marker JPEG per entrambi.", "Ispeziona una response MJPEG scaffolded e controlla il parametro boundary."),
        base_exercise="Leggi e valida due frame consecutivi dal mock.",
        intermediate_exercise="Verifica Content-Type multipart e presenza del boundary in una response fornita.",
        challenge="Interrompi la lettura dopo tre frame e dimostra che camera e stream vengono chiusi.",
        common_errors=("Chiamare MJPEG un singolo byte array JPEG.", "Confondere boundary e marker interni JPEG.", "Creare un ciclo infinito senza condizione di arresto o cleanup."),
        self_check=("So spiegare perché MJPEG contiene più JPEG?", "So trovare il boundary?", "Il mio lettore può terminare in modo pulito?"),
        accessibility="Fornisci frame campione e struttura testuale; il risultato può essere verificato con contatori e status senza dover vedere il video.",
        glossary=(("MJPEG", "stream formato da immagini JPEG successive"), ("multipart", "body HTTP composto da più parti"), ("boundary", "sequenza che separa le parti"), ("frame", "una singola immagine dello stream")),
    ),
    "eventi": LessonContent(
        prerequisites="Sai definire funzioni, usare condizioni, liste e cicli brevi.",
        mental_model=(
            "Un evento descrive qualcosa che è accaduto; un handler è una funzione che decide come reagire. Il dispatcher "
            "consegna ogni evento all'handler. Lo scaffold contiene il ciclo della coda: oggi scriviamo reazioni semplici, "
            "non callback, async o event loop complessi. Questa unità va studiata prima dei controller interattivi."
        ),
        example="""```python
def handle_event(evento):
    if evento["type"] == "key":
        return evento["value"]
    return None

risultato = handle_event({"type": "key", "value": "w"})
```

La funzione è testabile senza tastiera, browser o gamepad.""",
        guided_practice=("Separa evento, dispatcher e handler nel diagramma.", "Prevedi il risultato di due eventi.", "Completa l'handler con un solo tipo.", "Usa la coda scaffolded per consegnare gli eventi in ordine.", "Aggiungi un evento sconosciuto che non deve causare movimento."),
        base_exercise="Gestisci due eventi di tasto mantenendo l'ordine.",
        intermediate_exercise="Mappa eventi press/release in comando e STOP con una funzione pura.",
        challenge="Gestisci tre tipi di evento mantenendo handler piccoli e un comportamento sicuro per tipi ignoti.",
        common_errors=("Mettere tutta la logica nel ciclo invece che nell'handler testabile.", "Eseguire movimento per eventi sconosciuti.", "Confondere ordine della coda e priorità degli eventi."),
        self_check=("So definire evento, handler e dispatcher?", "Posso testare l'handler senza dispositivo?", "Un evento ignoto lascia Romeo fermo?"),
        accessibility="Gli eventi possono provenire da pulsante, tastiera o dati simulati; mostra sempre una traccia testuale ordinata.",
        glossary=(("evento", "dato che descrive qualcosa accaduto"), ("handler", "funzione che reagisce a un evento"), ("coda", "struttura che conserva l'ordine degli eventi")),
    ),
    "gamepad": LessonContent(
        prerequisites="Conosci eventi, velocità delle due ruote, funzioni e numeri fra -1 e 1.",
        mental_model=(
            "Lo stick produce due assi. Prima applichiamo una dead-zone per ignorare piccoli tremolii, poi mescoliamo "
            "avanti e sterzo nelle velocità sinistra/destra e infine limitiamo il risultato. pygame e il dispositivo "
            "sono nello scaffold: la funzione matematica resta testabile con numeri simulati."
        ),
        example="""```python
mapping = GamepadMapping(max_speed=0.6)
sinistra, destra = wheel_speeds(0.0, -1.0, mapping)
print(sinistra, destra)  # 0.6 0.6: stick avanti
```

Molti controller riportano avanti come Y negativo; il mapping isola questa convenzione.""",
        guided_practice=("Segna centro e direzioni sugli assi etichettati.", "Prevedi le ruote per centro, avanti e destra.", "Verifica le previsioni con input simulati.", "Prova valori dentro e fuori la dead-zone.", "Collega infine la funzione agli eventi pygame forniti."),
        base_exercise="Calcola le ruote per centro e avanti rispettando velocità massima.",
        intermediate_exercise="Verifica una curva a destra e una a sinistra con proprietà simmetriche.",
        challenge="Crea una configurazione con dead-zone e max speed diverse senza modificare la funzione di mapping.",
        common_errors=("Dimenticare che l'asse Y può essere invertito.", "Inviare il rumore vicino allo zero ai motori.", "Mescolare lettura pygame e matematica rendendo impossibili i test senza gamepad."),
        self_check=("So spiegare la dead-zone?", "Le velocità rispettano sempre i limiti?", "Posso testare tutto senza controller fisico?"),
        accessibility="Offri tastiera e pulsanti come input equivalenti; mostra numericamente assi e ruote e consenti rimappatura.",
        glossary=(("asse", "valore continuo prodotto dallo stick"), ("dead-zone", "zona vicino allo zero trattata come ferma"), ("differential drive", "movimento ottenuto combinando due velocità ruota")),
    ),
    "telemetria": LessonContent(
        prerequisites="Conosci JSON, schema, coordinate del simulatore e WebSocket.",
        mental_model=(
            "La telemetria è una fotografia strutturata dello stato inviata nel tempo. `schema_version` dice al client "
            "come leggere i campi; pose, motori, camera e tempo hanno nomi e unità documentati. Il renderer è soltanto "
            "un consumatore: il test può leggere gli stessi dati senza browser."
        ),
        example="""```python
state = engine.state()
assert state["schema_version"] == "romeo.simulation.state.v1"
pose = state["pose"]
print(pose["x"], pose["y"], state["time"])
```

Prima si controlla la versione, poi i campi; lo scaffold fornisce scenario ed engine.""",
        guided_practice=("Annota versione, pose, motori, camera e tempo in uno snapshot.", "Controlla schema_version prima degli altri campi.", "Leggi pose e unità documentate.", "Confronta due snapshot dopo un passo simulato.", "Simula una versione sconosciuta e rifiutala con un errore chiaro."),
        base_exercise="Valida versione e campi principali di uno snapshot.",
        intermediate_exercise="Calcola se Romeo è in movimento usando le due velocità motore dello snapshot.",
        challenge="Scrivi un consumer che ignora campi aggiuntivi ma rifiuta versioni incompatibili e campi obbligatori mancanti.",
        common_errors=("Leggere campi prima di controllare la versione.", "Confondere tempo simulato e ora del computer.", "Dipendere da coordinate o elementi HTML del viewer."),
        self_check=("So spiegare perché lo schema è versionato?", "Conosco unità e significato dei campi usati?", "Il mio consumer funziona senza renderer?"),
        accessibility="Presenta la telemetria come tabella e JSON copiabile; non affidarti soltanto all'animazione del viewer.",
        glossary=(("telemetria", "stato misurato e comunicato nel tempo"), ("pose", "posizione e orientamento"), ("schema_version", "versione del contratto dei dati")),
    ),
    "safety": LessonContent(
        prerequisites="Conosci controllo remoto, timeout, mock backend e test deterministici.",
        mental_model=(
            "Il controllo è un permesso temporaneo: un solo controller possiede il lease. Ogni comando valido rinnova "
            "il tempo; il watchdog ferma i motori quando scade. Release, disconnect, eccezione e shutdown devono tutti "
            "portare allo stesso stato sicuro: velocità zero. Il test usa clock e watchdog controllati dallo scaffold."
        ),
        example="""```python
safety.claim_controller("client-a")
try:
    safety.set_motor_speeds_for("client-a", 0.4, 0.4)
finally:
    safety.release_controller("client-a")

assert (backend.left_speed, backend.right_speed) == (0.0, 0.0)
```

Il `finally` copre l'uscita normale e l'errore; un test separato fa avanzare il clock oltre il timeout.""",
        guided_practice=("Disegna una timeline claim→command→renew→expire→stop.", "Prendi il controllo e verifica il movimento sul mock.", "Tenta il claim da un secondo controller e osserva il rifiuto.", "Rilascia nel `finally` e verifica zero.", "Avanza il clock scaffolded senza comandi e verifica lo stop del watchdog."),
        base_exercise="Dimostra che release azzera entrambi i motori.",
        intermediate_exercise="Dimostra ownership esclusiva e stop alla scadenza con clock controllato.",
        challenge="Simula una disconnessione durante il movimento e raccogli una traccia che dimostri lo stop automatico.",
        common_errors=("Disattivare il watchdog proprio nel test che dovrebbe verificarlo.", "Fermare solo un motore.", "Affidarsi allo STOP manuale come unico percorso sicuro."),
        self_check=("Un secondo controller viene rifiutato?", "Timeout, disconnect ed errore portano a zero?", "I test non dipendono da attese reali fragili?"),
        accessibility="La timeline è anche un elenco numerato; stato owner, tempo residuo e motori sono disponibili come testo.",
        glossary=(("lease", "permesso di controllo con durata limitata"), ("watchdog", "controllo che ferma il sistema quando i comandi cessano"), ("ownership", "regola che consente un solo controller attivo")),
    ),
    "integrazione": LessonContent(
        prerequisites="Hai completato WebSocket control, telemetria versionata e safety con disconnect.",
        mental_model=(
            "L'integrazione collega due flussi senza confonderli: `/ws/control` riceve intenzioni e restituisce ack; "
            "`/ws/state` pubblica telemetria. Entrambi usano la stessa API Robot e lo stesso safety boundary. Lo scaffold "
            "fornisce app e connessioni; lo studente completa la sequenza e le verifiche end-to-end."
        ),
        example="""```text
controller → /ws/control → ack
                         ↓
                     Robot API
                         ↓
viewer     ← /ws/state ← state versionato
```

Il diagramma mostra dipendenze, non ordine temporale; la prova guidata aggiunge la timeline.""",
        guided_practice=("Etichetta control, ack, Robot API e state.", "Apri i due canali scaffolded e verifica i messaggi ready.", "Invia FORWARD e attendi ack.", "Leggi uno state e verifica movimento e versione.", "Chiudi il controller e verifica uno state successivo con motori a zero."),
        base_exercise="Collega un comando a un aggiornamento di stato osservabile.",
        intermediate_exercise="Verifica che payload invalido produca errore e non modifichi lo stato.",
        challenge="Interrompi il canale control senza STOP esplicito e dimostra il fail-safe tramite il canale state.",
        common_errors=("Usare REST polling e chiamarlo telemetria realtime.", "Considerare l'ack prova sufficiente del movimento.", "Chiudere il viewer ma lasciare vivo il controller senza timeout."),
        self_check=("So distinguere i due canali?", "Verifico sia ack sia stato?", "La perdita del control porta a motori zero?"),
        accessibility="Ack e telemetria sono disponibili come log testuale; il controller include pulsanti oltre a tastiera e gamepad.",
        glossary=(("integrazione", "verifica congiunta di componenti già testati separatamente"), ("end-to-end", "prova dal comando fino allo stato osservato"), ("canale", "connessione con una responsabilità definita")),
    ),
    "capstone-telepresence": LessonContent(
        prerequisites="Hai completato foto/video, controller, telemetria, safety e integrazione e sai documentare test e failure.",
        mental_model=(
            "La telepresenza è un sistema a strati: input → controllo sicuro → Robot API → backend, mentre camera e "
            "telemetria riportano ciò che accade. Il capstone non richiede di riscrivere server o framework: lo scaffold "
            "fornisce infrastruttura, e il gruppo integra, verifica e spiega i confini. Ogni incremento deve lasciare Romeo fermo."
        ),
        example="""```text
1. status e foto funzionano con mock
2. controllo produce ack e stato coerente
3. stream può essere aperto e chiuso
4. timeout/disconnect producono STOP
5. demo ripetibile e log registrato
```

Questo è un piano di verifica, non codice da copiare: ogni riga diventa un checkpoint osservabile.""",
        guided_practice=("Disegna l'architettura con API, protocolli e backend separati.", "Completa checkpoint status+camera con mock.", "Aggiungi controllo e telemetria senza hardware.", "Inietta payload invalido, timeout e disconnect e registra l'esito.", "Esegui la demo completa due volte lasciando motori a zero.", "Solo dopo la checklist docente, ripeti una prova breve sull'hardware reale."),
        base_exercise="Integra foto, un comando WebSocket, ack, stato versionato e STOP finale nel simulatore.",
        intermediate_exercise="Aggiungi stream e input accessibile, mantenendo separati UI, trasporto e Robot API.",
        challenge="Dimostra con log automatico che disconnect, timeout e camera indisponibile degradano in modo sicuro e comprensibile.",
        common_errors=("Assemblare componenti senza verificare ogni incremento.", "Mostrare movimento e video ma non i failure mode.", "Usare il robot reale prima di superare mock, simulazione e checklist safety."),
        self_check=("Ogni requisito ha un'evidenza osservabile?", "La stessa logica funziona con simulatore e backend reale?", "Ogni uscita o errore lascia i motori a zero e chiude camera/connessioni?"),
        accessibility="La demo offre pulsanti, tastiera rimappabile e log testuale; video e colore non sono l'unica evidenza. Definire ruoli di gruppo ruotabili e consenso camera.",
        glossary=(("telepresenza", "controllo remoto accompagnato da percezione e stato"), ("fail-safe", "comportamento che porta a uno stato sicuro in caso di guasto"), ("checkpoint", "risultato intermedio verificabile")),
    ),
}
