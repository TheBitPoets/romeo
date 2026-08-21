"""Unit-specific, beginner-friendly teaching content for Romeo year one."""

# ruff: noqa: E501 -- complete teaching sentences are easier to review without wrapping.

from __future__ import annotations

from pedagogy_content import LessonContent

LESSONS_Y1: dict[str, LessonContent] = {
    "introduzione": LessonContent(
        prerequisites="Nessuna esperienza di programmazione. È sufficiente saper usare mouse e tastiera.",
        mental_model=(
            "Un programma è una lista di istruzioni che Romeo esegue dall'alto verso il basso. "
            "Il pulsante Run avvia la lista; `stop()` lascia le ruote ferme alla fine. Oggi non serve "
            "capire ogni simbolo: prima osserviamo che una riga di codice produce un effetto."
        ),
        example="""```python
# Questa riga rende disponibile il comando stop.
from romeo.easy import stop

# Questa istruzione ferma entrambe le ruote.
stop()
```

Premendo Run, la riga con `stop()` viene eseguita e lo stato finale mostra entrambe le ruote ferme.""",
        guided_practice=(
            "Apri lo starter e individua le righe che iniziano con `from` e quelle che terminano con le parentesi `()`.",
            "Indica con il dito la prima istruzione che Romeo eseguirà e poi la seconda.",
            "Prima di premere Run, scrivi: «alla fine le ruote saranno ferme».",
            "Premi Run e cerca nel feedback lo stato finale dei motori.",
            "Aggiungi i comandi richiesti dalla consegna, uno per riga, mantenendo `stop()` come ultima azione.",
        ),
        base_exercise="Esegui un programma che accende il LED blu e termina con `stop()`.",
        intermediate_exercise="Inserisci un breve comando `forward(0.2)` prima di `stop()` e prevedi l'ordine degli eventi mostrati dal simulatore.",
        challenge="Scambia due istruzioni, prevedi cosa cambia e poi verifica. Ripristina `stop()` come ultima azione.",
        common_errors=(
            "Scrivere `stop` senza parentesi: il comando viene nominato ma non eseguito.",
            "Scrivere `Stop()` con la maiuscola: Python distingue maiuscole e minuscole.",
            "Eliminare `stop()` finale: lo stato sicuro non è più espresso chiaramente dal programma.",
        ),
        self_check=(
            "So indicare l'ordine in cui vengono eseguite tre istruzioni?",
            "So trovare nel feedback se le ruote sono ferme?",
            "So spiegare perché `stop()` deve restare alla fine?",
        ),
        accessibility="Leggi ad alta voce l'ordine delle istruzioni e usa anche lo stato testuale dei motori: il colore e il movimento sullo schermo non sono le sole evidenze.",
        glossary=(
            ("programma", "una lista ordinata di istruzioni"),
            ("istruzione", "un'azione scritta su una riga"),
            ("Run", "il comando che avvia il programma"),
        ),
    ),
    "componenti": LessonContent(
        prerequisites="Aver eseguito U01 e saper riconoscere un'istruzione e lo stato finale fermo.",
        mental_model=(
            "Pensa a una catena di messaggi: il programma chiede un'azione, il Raspberry Pi la "
            "interpreta, la scheda CRICKIT fornisce energia ai motori e le ruote si muovono. Il LED "
            "è un'uscita separata: comunica uno stato senza muovere il robot."
        ),
        example="""```python
from romeo.easy import led, stop

# Il messaggio "pronto" usa il LED, non i motori.
led("green")
stop()
```

Nel pannello di stato cerca sia il nome del colore sia le due velocità delle ruote.""",
        guided_practice=(
            "Ordina le quattro schede: programma, Raspberry Pi, CRICKIT, motori.",
            "Indica quale componente calcola e quale componente fornisce energia ai motori.",
            "Esegui l'esempio e controlla separatamente LED, ruota sinistra e ruota destra.",
            "Completa lo starter con il segnale verde, un comando avanti e lo stop finale.",
            "Racconta il viaggio del comando dal codice alle ruote senza usare abbreviazioni.",
        ),
        base_exercise="Associa ciascun comando della consegna al componente che cambia stato.",
        intermediate_exercise="Esegui LED verde, movimento e stop; annota tre eventi nell'ordine osservato.",
        challenge="Disegna la catena dei componenti e aggiungi una freccia di ritorno per il feedback del simulatore.",
        common_errors=(
            "Confondere Raspberry Pi e CRICKIT: il primo esegue il programma, la seconda pilota i carichi elettrici.",
            "Pensare che cambiare il LED fermi i motori: sono due uscite indipendenti.",
            "Osservare solo l'animazione e non lo stato numerico delle ruote.",
        ),
        self_check=(
            "So descrivere il ruolo di Raspberry Pi, CRICKIT e motori con una frase ciascuno?",
            "So dire quale istruzione cambia il LED?",
            "So verificare che entrambe le ruote siano ferme alla fine?",
        ),
        accessibility="Affianca ai componenti reali etichette grandi e numerate; descrivi sempre a parole LED e velocità, senza affidarti soltanto a colori o animazioni.",
        glossary=(
            ("Raspberry Pi", "il piccolo computer che esegue Python"),
            ("CRICKIT", "la scheda che comanda motori, servo e LED"),
            ("uscita", "una parte del robot che il programma può modificare"),
        ),
    ),
    "repl": LessonContent(
        prerequisites="Aver completato U02 e saper eseguire un file con Run.",
        mental_model=(
            "Il REPL è un banco prova: mostra `>>>`, riceve una sola istruzione e risponde subito. "
            "Un file conserva invece una sequenza da rieseguire. Prima proviamo un comando nel REPL, "
            "poi trasferiamo la sequenza riuscita in `main.py`."
        ),
        example="""```text
>>> from romeo.easy import stop
>>> stop()
>>> fermati()
NameError: name 'fermati' is not defined
```

L'ultima risposta non è un giudizio: indica che Python non conosce il nome `fermati`.""",
        guided_practice=(
            "Apri il REPL e trova il prompt `>>>`.",
            "Digita l'import dell'esempio e premi Invio una sola volta.",
            "Digita `stop()` e osserva la risposta e lo stato dei motori.",
            "Prova volontariamente `Stop()` e leggi l'ultima riga dell'errore.",
            "Chiudi la prova e trasferisci in `main.py` la sequenza LED rosso, movimento, stop.",
        ),
        base_exercise='Prova `led("red")` nel REPL dopo l\'import fornito e verifica il nome testuale del colore.',
        intermediate_exercise="Causa un `NameError`, correggi soltanto il nome e ripeti la chiamata.",
        challenge="Prevedi la differenza tra eseguire tre righe nel REPL e salvarle nello stesso ordine in `main.py`.",
        common_errors=(
            "Copiare anche i caratteri `>>>`: sono il prompt, non parte del codice.",
            "Dimenticare l'import prima della chiamata e ricevere `NameError`.",
            "Leggere tutto il traceback insieme invece di partire dall'ultima riga.",
        ),
        self_check=(
            "So distinguere il prompt da ciò che devo digitare?",
            "So trovare il nome sconosciuto in un `NameError`?",
            "So spiegare quando usare il REPL e quando usare `main.py`?",
        ),
        accessibility="La trascrizione testuale accompagna ogni cambiamento visivo; chi usa uno screen reader può seguire prompt, comando e risposta in ordine lineare.",
        glossary=(
            ("REPL", "ambiente che legge ed esegue una istruzione alla volta"),
            ("prompt", "i caratteri `>>>` che indicano che Python è pronto"),
            ("NameError", "errore che segnala un nome non conosciuto"),
        ),
    ),
    "chiamate-funzione": LessonContent(
        prerequisites="Saper provare una riga nel REPL e riconoscere un `NameError`.",
        mental_model=(
            "Una funzione è un comando con un nome. Le parentesi chiedono a Python di eseguirlo; "
            "il valore dentro le parentesi è un argomento che precisa come eseguirlo. `forward(0.3)` "
            "significa quindi: esegui `forward` usando velocità 0.3."
        ),
        example="""```python
from romeo.easy import forward, stop

# Nome: forward; parentesi: esegui; argomento: 0.3.
forward(0.3)
stop()
```""",
        guided_practice=(
            "Sottolinea il nome `forward` nell'esempio.",
            "Cerchia le parentesi e racchiudi in un quadrato l'argomento `0.3`.",
            "Prevedi quale evento motore apparirà per primo.",
            "Esegui il programma e confronta il valore mostrato con `0.3`.",
            "Cambia soltanto l'argomento in `0.2`, ripeti e poi ripristina la consegna.",
        ),
        base_exercise="Scrivi la chiamata richiesta `forward(0.3)` e termina con `stop()`.",
        intermediate_exercise="Confronta gli eventi prodotti da `forward()` e `forward(0.3)` senza cambiare altre righe.",
        challenge='Trova e correggi tre chiamate errate: `Forward(0.3)`, `forward 0.3`, `forward("0.3")`.',
        common_errors=(
            "Omettere le parentesi e quindi non eseguire la funzione.",
            "Usare la virgola al posto del punto in `0.3`.",
            "Mettere il numero tra virgolette e trasformarlo in testo.",
        ),
        self_check=(
            "So indicare nome, parentesi e argomento in una chiamata?",
            "So spiegare che cosa cambia modificando soltanto l'argomento?",
            "So riconoscere un numero e una stringa?",
        ),
        accessibility="Usa marcatori diversi anche nel testo — «nome», «parentesi», «argomento» — senza affidare le tre parti soltanto a colori.",
        glossary=(
            ("funzione", "un comando Python che può essere eseguito"),
            ("chiamata", "il nome della funzione seguito dalle parentesi"),
            ("argomento", "un valore fornito alla funzione"),
        ),
    ),
    "led": LessonContent(
        prerequisites="Saper chiamare una funzione con un argomento e distinguere numero e testo.",
        mental_model=(
            "Il LED è un'uscita immediata: `led(...)` cambia il suo stato ma non muove le ruote. "
            "Il nome del colore è testo, quindi va scritto tra virgolette. Il pannello di stato "
            "riporta anche il nome o i valori del colore per non dipendere soltanto dalla vista."
        ),
        example="""```python
from romeo.easy import led

# Le virgolette indicano che blue è testo.
led("blue")
```""",
        guided_practice=(
            "Individua le due virgolette che racchiudono `blue`.",
            "Prevedi il nome del colore che apparirà nello stato.",
            "Esegui una volta con `red` e leggi il feedback testuale.",
            "Modifica soltanto la stringa in `blue` per la consegna.",
            "Controlla che nessun evento motore sia necessario per cambiare il LED.",
        ),
        base_exercise="Imposta il LED blu e verifica il valore testuale o RGB finale.",
        intermediate_exercise="Mostra in ordine `red`, `green`, `blue`; annota quale colore resta alla fine.",
        challenge='Prevedi e verifica che cosa accade con `led("off")` dopo un colore acceso.',
        common_errors=(
            "Scrivere `led(blue)` senza virgolette e ricevere `NameError`.",
            "Usare un nome non previsto, per esempio `azzurro`, invece dei valori documentati.",
            "Pensare che il primo colore resti quello finale dopo una seconda chiamata.",
        ),
        self_check=(
            "So spiegare perché il colore è tra virgolette?",
            "So trovare lo stato del LED anche senza distinguere il colore nell'immagine?",
            "So prevedere quale di più chiamate determina il colore finale?",
        ),
        accessibility="Nomina sempre il colore nel testo e leggi i valori di stato; non usare rosso/verde come unico modo per comunicare errore o successo.",
        glossary=(
            ("stringa", "testo racchiuso tra virgolette"),
            ("RGB", "tre quantità che descrivono rosso, verde e blu"),
            ("stato finale", "il valore rimasto dopo l'ultima istruzione"),
        ),
    ),
    "motore-singolo": LessonContent(
        prerequisites="Saper chiamare funzioni con argomenti numerici e leggere lo stato di un'uscita.",
        mental_model=(
            "`robot` è il nome della plancia di comando di Romeo. Il punto in `robot.drive(...)` "
            "sceglie il comando `drive` di quella plancia. I due numeri indicano nell'ordine ruota "
            "sinistra e ruota destra; zero significa ruota ferma. Non occorre ancora studiare le classi."
        ),
        example="""```python
from romeo import Robot

robot = Robot()          # Prepariamo la plancia di comando.
robot.drive(0.3, 0.0)    # Sinistra attiva, destra ferma.
robot.stop()             # Entrambe ferme alla fine.
```""",
        guided_practice=(
            "Scrivi sopra i due argomenti le etichette «sinistra» e «destra».",
            "Prevedi la coppia di valori mostrata dopo `drive(0.3, 0.0)`.",
            "Esegui e cerca l'evento con sinistra 0.3 e destra 0.0.",
            "Scambia i due valori e osserva quale ruota cambia, poi annulla la modifica.",
            "Completa la consegna e controlla l'evento di stop finale.",
        ),
        base_exercise="Attiva soltanto la ruota sinistra a 0.35 e poi ferma Romeo.",
        intermediate_exercise="Esegui due prove separate: solo sinistra e solo destra; confronta gli eventi.",
        challenge="Prevedi il verso di rotazione del robot quando soltanto la ruota sinistra avanza.",
        common_errors=(
            "Invertire l'ordine sinistra/destra degli argomenti.",
            "Scrivere `Robot.drive(...)` invece di usare il nome `robot` preparato.",
            "Dimenticare `robot.stop()` perché l'animazione sembra già terminata.",
        ),
        self_check=(
            "So indicare quale argomento comanda ciascuna ruota?",
            "So spiegare il significato di zero?",
            "So verificare negli eventi che una sola ruota sia stata attivata?",
        ),
        accessibility="Affianca ai valori le parole sinistra/destra e usa lo stato numerico; non richiedere di dedurre la ruota attiva soltanto dall'animazione.",
        glossary=(
            ("robot", "il nome scelto per la plancia di comando"),
            ("drive", "il comando che imposta insieme le due ruote"),
            ("velocità con segno", "numero positivo per avanti, negativo per indietro"),
        ),
    ),
    "due-motori": LessonContent(
        prerequisites="Saper leggere i due argomenti di `robot.drive(sinistra, destra)`.",
        mental_model=(
            "Romeo usa una guida differenziale: decide il movimento confrontando le due ruote. "
            "Due valori positivi uguali lo fanno avanzare diritto; un valore zero fa perno su una "
            "ruota; valori diversi producono una curva."
        ),
        example="""```python
from romeo import Robot

robot = Robot()
robot.drive(0.3, 0.3)  # Stessa velocità: direzione diritta.
robot.stop()
```""",
        guided_practice=(
            "Disegna due ruote e scrivi 0.3 accanto a entrambe.",
            "Prevedi se il robot va diritto o gira.",
            "Esegui l'esempio e controlla che lo stesso evento contenga entrambi i valori 0.3.",
            "Prova temporaneamente `drive(0.2, 0.4)` e descrivi la curva senza misurarla.",
            "Ripristina due valori 0.3 e termina con lo stop richiesto.",
        ),
        base_exercise="Imposta entrambe le ruote a 0.3 e termina in sicurezza.",
        intermediate_exercise="Compila una tabella di previsione per `(0.3, 0.3)`, `(0.0, 0.3)` e `(0.2, 0.4)`.",
        challenge="Trova due coppie diverse che facciano curvare Romeo in direzioni opposte.",
        common_errors=(
            "Credere che due numeri uguali facciano girare il robot.",
            "Confondere la coppia di velocità con due comandi eseguiti in tempi diversi.",
            "Controllare soltanto una ruota nel feedback.",
        ),
        self_check=(
            "So prevedere l'effetto di due valori uguali?",
            "So distinguere una curva da un movimento diritto usando i numeri?",
            "So verificare che entrambe le ruote siano state comandate nello stesso evento?",
        ),
        accessibility="Rappresenta ogni coppia sia con frecce sia con una tabella testuale sinistra/destra; le frecce da sole non sono necessarie per capire.",
        glossary=(
            ("guida differenziale", "movimento ottenuto confrontando le velocità delle due ruote"),
            ("coppia", "i due valori sinistra e destra considerati insieme"),
            ("curva", "movimento con velocità delle ruote diverse"),
        ),
    ),
    "avanti-indietro": LessonContent(
        prerequisites="Saper prevedere il movimento da una coppia di velocità.",
        mental_model=(
            "Un comando motore resta attivo finché un altro comando lo cambia. `sleep(1)` non ferma "
            "Romeo: lascia trascorrere un secondo con il comando corrente. `backward` imposta entrambe "
            "le ruote all'indietro; `stop` le porta infine a zero."
        ),
        example="""```python
from time import sleep
from romeo.easy import forward, stop

forward(0.2)  # Inizia il movimento.
sleep(1)      # Continua per un secondo.
stop()        # Termina il movimento.
```""",
        guided_practice=(
            "Segna sulla carta tre istanti: inizio, dopo un secondo, fine.",
            "Scrivi lo stato delle ruote in ciascun istante dell'esempio.",
            "Esegui e osserva come cambia il tempo simulato durante `sleep`.",
            "Aggiungi dopo il primo secondo `backward(0.4)` e un secondo `sleep(1)`.",
            "Termina con `stop()` e confronta posizione iniziale e finale.",
        ),
        base_exercise="Avanza per un secondo, torna indietro per un secondo e fermati.",
        intermediate_exercise="Usa la stessa velocità nei due versi e spiega perché Romeo dovrebbe tornare vicino alla partenza.",
        challenge="Cambia soltanto la durata del ritorno; prevedi da quale lato della partenza finirà.",
        common_errors=(
            "Pensare che `sleep` significhi stop: i motori mantengono l'ultimo comando.",
            "Usare durate diverse senza aggiornare la previsione della posa finale.",
            "Mettere `stop()` tra il comando e il relativo `sleep`, annullando il movimento.",
        ),
        self_check=(
            "So dire quale comando resta attivo durante ogni `sleep`?",
            "So prevedere il verso del movimento?",
            "So confrontare posa iniziale e finale usando numeri, non solo l'animazione?",
        ),
        accessibility="Usa una linea del tempo testuale con stato e durata; l'animazione può essere rallentata o sostituita dalla lettura della traiettoria numerica.",
        glossary=(
            ("sleep", "attesa durante la quale resta attivo il comando corrente"),
            ("durata", "tempo per cui continua un movimento"),
            ("backward", "comando che muove entrambe le ruote all'indietro"),
        ),
    ),
    "curve-rotazioni": LessonContent(
        prerequisites="Saper usare una durata e conoscere l'effetto di velocità uguali o diverse.",
        mental_model=(
            "In una curva il centro di Romeo cambia posizione; in una rotazione sul posto le ruote "
            "vanno in versi opposti e il centro resta quasi fermo. L'angolo ottenuto dipende da velocità, "
            "durata e distanza tra le ruote: perciò si calibra una durata con prove piccole."
        ),
        example="""```python
from time import sleep
from romeo.easy import left, stop

left(0.5)       # Le ruote girano in versi opposti.
sleep(0.5)      # Una prima prova breve, non ancora "90 gradi".
stop()
```""",
        guided_practice=(
            "Disegna la posa iniziale con una freccia orientata verso destra.",
            "Esegui una prova breve di 0.5 s e leggi l'orientamento finale.",
            "Confronta l'angolo osservato con 90 gradi e calcola soltanto se serve più o meno tempo.",
            "Modifica la durata di un piccolo passo e ripeti, senza cambiare anche la velocità.",
            "Quando sei nella tolleranza, termina con `stop()` e annota la durata calibrata.",
        ),
        base_exercise="Ruota a sinistra fino a circa 90 gradi e fermati.",
        intermediate_exercise="Confronta una curva ottenuta con ruote diverse e una rotazione sul posto, descrivendo posizione e orientamento.",
        challenge="Trova una durata per circa 45 gradi mantenendo la stessa velocità e spiega la tua previsione.",
        common_errors=(
            "Copiare una durata precisa senza verificarla nel proprio scenario.",
            "Cambiare velocità e durata insieme, rendendo difficile capire quale modifica ha avuto effetto.",
            "Confondere coordinate finali e orientamento finale.",
        ),
        self_check=(
            "So distinguere curva e rotazione usando il movimento del centro?",
            "So leggere l'errore di orientamento in gradi?",
            "So descrivere una calibrazione cambiando una variabile alla volta?",
        ),
        accessibility="Fornisci orientamento iniziale/finale e errore in gradi come testo; non richiedere di stimare l'angolo soltanto dalla figura.",
        glossary=(
            ("orientamento", "direzione verso cui punta Romeo"),
            ("grado", "unità usata per misurare un angolo"),
            ("calibrazione", "serie di piccole prove per trovare un valore adatto"),
        ),
    ),
    "stop-safety": LessonContent(
        prerequisites="Saper costruire una breve sequenza temporizzata e terminarla con `stop()`.",
        mental_model=(
            "Lo stop scritto nel programma è la regola principale. Il watchdog è una seconda rete di "
            "sicurezza: se per troppo tempo non arrivano comandi validi, ordina lo stop. Non sostituisce "
            "il nostro `stop()`; protegge da un programma o collegamento interrotto."
        ),
        example="""```python
from romeo.easy import forward, stop

forward(0.2)
# Anche una prova brevissima dichiara esplicitamente lo stato sicuro.
stop()
```""",
        guided_practice=(
            "Individua l'ultima istruzione motore dello starter.",
            "Prevedi lo stato finale se il programma terminasse in quel punto.",
            "Aggiungi `stop()` e verifica che entrambe le ruote valgano zero.",
            "Spiega a un compagno la differenza tra stop esplicito e watchdog.",
            "Compila la scheda di sicurezza prima di provare lo stesso codice sul robot fisico.",
        ),
        base_exercise="Invia un comando motore e lascia Romeo esplicitamente fermo.",
        intermediate_exercise="Confronta l'event log di un programma con e senza stop esplicito, usando solo il simulatore.",
        challenge="Scrivi in tre passi la procedura umana da seguire se il robot fisico non risponde ai comandi.",
        common_errors=(
            "Credere che la fine del file equivalga sempre a uno stop immediato.",
            "Usare il watchdog come scusa per omettere `stop()`.",
            "Provare un caso di errore direttamente sull'hardware prima del simulatore.",
        ),
        self_check=(
            "So mostrare nel codice lo stop esplicito?",
            "So spiegare il ruolo di riserva del watchdog?",
            "So indicare un'evidenza che entrambe le ruote siano a zero?",
        ),
        accessibility="La checklist di sicurezza deve essere disponibile in testo ad alta leggibilità e letta ad alta voce prima della prova fisica.",
        glossary=(
            ("watchdog", "controllo che ferma il robot quando i comandi non arrivano in tempo"),
            ("fail-safe", "comportamento che porta il sistema in uno stato sicuro"),
            ("stop esplicito", "istruzione `stop()` scritta nel programma"),
        ),
    ),
    "velocita": LessonContent(
        prerequisites="Saper usare `forward`, `sleep` e `stop` e leggere posizione e tempo finali.",
        mental_model=(
            "La velocità richiesta è un numero tra 0 e 1: zero significa fermo, uno è il limite "
            "configurato, e 0.5 è metà comando. A parità di scenario, distanza significa velocità per "
            "tempo. Cambiamo un solo valore alla volta per confrontare due prove."
        ),
        example="""```python
from time import sleep
from romeo.easy import forward, stop

forward(0.25)  # Un quarto del comando massimo.
sleep(2)       # Mantienilo per due secondi.
stop()
```""",
        guided_practice=(
            "Annota posizione iniziale e durata prima del primo run.",
            "Esegui l'esempio con velocità 0.25 e annota la posizione finale.",
            "Ripeti con 0.5 senza cambiare la durata.",
            "Confronta le due distanze e formula una frase, senza pretendere precisione dell'hardware reale.",
            "Usa 0.5 per due secondi e verifica il target della consegna.",
        ),
        base_exercise="Raggiungi x=1.0 con velocità 0.5 per due secondi e fermati.",
        intermediate_exercise="Raggiungi la stessa posizione con una velocità più bassa e una durata adeguata.",
        challenge="Prevedi una terza coppia velocità/durata equivalente e verifica la tolleranza finale.",
        common_errors=(
            "Usare un valore fuori dall'intervallo da 0 a 1.",
            "Dimenticare che la partenza è x=0.5 e calcolare tutta la coordinata come distanza.",
            "Cambiare contemporaneamente velocità e target senza poter confrontare i run.",
        ),
        self_check=(
            "So spiegare il significato di 0, 0.5 e 1?",
            "So distinguere coordinata iniziale, distanza percorsa e coordinata finale?",
            "So trovare due coppie velocità/durata che producono una distanza simile?",
        ),
        accessibility="Mostra valori e distanze in una tabella testuale; accompagna la traiettoria con coordinate numeriche e unità di misura.",
        glossary=(
            ("float", "numero che può avere una parte decimale"),
            ("normalizzato", "espresso nell'intervallo da 0 a 1"),
            ("limite", "massimo valore consentito dalla configurazione"),
        ),
    ),
    "funzioni": LessonContent(
        prerequisites="Saper scrivere e verificare una sequenza con movimento, durata e stop.",
        mental_model=(
            "Definire una funzione significa dare un nome a una piccola ricetta. Le righe rientrate "
            "sono il corpo della ricetta e non partono finché la funzione non viene chiamata. Un "
            "parametro è un posto vuoto che riceve un valore diverso a ogni chiamata."
        ),
        example="""```python
from romeo.easy import stop

def arresta():       # Definiamo la ricetta.
    stop()            # Corpo: è rientrato di quattro spazi.

arresta()             # Ora eseguiamo la ricetta.
```""",
        guided_practice=(
            "Cerchia il nome `arresta` nella definizione e nella chiamata.",
            "Esegui il file senza la chiamata finale e osserva che il corpo non viene eseguito.",
            "Ripristina la chiamata e verifica l'evento di stop.",
            "Completa il corpo di `avanza_per(secondi)` con movimento, `sleep(secondi)` e stop.",
            "Chiama `avanza_per(2)` e verifica posizione e stato finali.",
        ),
        base_exercise="Definisci `avanza_per(secondi)` e usala con il valore 2.",
        intermediate_exercise="Chiama la stessa funzione prima con 1 e poi con 2; confronta le distanze in due run separati.",
        challenge="Definisci una seconda funzione senza parametri che accenda un LED e lasci Romeo fermo.",
        common_errors=(
            "Dimenticare i due punti dopo la riga `def`.",
            "Non rientrare il corpo di quattro spazi.",
            "Definire la funzione ma non chiamarla.",
        ),
        self_check=(
            "So distinguere definizione e chiamata?",
            "So indicare quali righe appartengono al corpo?",
            "So spiegare quale valore riceve il parametro `secondi`?",
        ),
        accessibility="Evidenzia il rientro anche con una guida verticale e descrivilo come «quattro spazi»; non comunicarlo soltanto con il colore dell'editor.",
        glossary=(
            ("def", "parola che avvia la definizione di una funzione"),
            ("corpo", "righe rientrate eseguite dalla funzione"),
            ("parametro", "nome che riceve il valore fornito alla chiamata"),
        ),
    ),
    "sequenze": LessonContent(
        prerequisites="Saper costruire movimenti temporizzati e racchiudere una piccola ricetta in una funzione.",
        mental_model=(
            "Una sequenza è un algoritmo espresso come passi ordinati. Ogni movimento ha tre parti: "
            "avvio, durata, cambiamento successivo. Prima di scrivere Python possiamo disegnare frecce "
            "e numerare i segmenti; poi traduciamo un segmento alla volta."
        ),
        example="""```python
from time import sleep
from romeo.easy import forward, left, stop

forward(0.4)  # Segmento 1: avanza.
sleep(1)
left(0.5)     # Segmento 2: cambia orientamento.
sleep(0.5)
stop()
```""",
        guided_practice=(
            "Disegna la missione con tre frecce numerate: avanti, sinistra, avanti.",
            "Per ogni freccia scrivi comando e durata previsti.",
            "Implementa ed esegui soltanto il primo segmento, terminando temporaneamente con stop.",
            "Aggiungi la rotazione e confronta posa prevista e osservata.",
            "Aggiungi l'ultimo avanzamento e lascia un solo stop finale.",
        ),
        base_exercise="Esegui avanti, rotazione a sinistra, avanti e stop nell'ordine richiesto.",
        intermediate_exercise="Racchiudi il tratto rettilineo in una funzione già nota e usala due volte.",
        challenge="Inverti l'ordine dei primi due segmenti, prevedi la posa diversa e poi verifica.",
        common_errors=(
            "Scrivere tutti i comandi prima di aggiungere le durate.",
            "Correggere più segmenti insieme e non sapere quale modifica ha funzionato.",
            "Confondere ordine del disegno e ordine delle righe Python.",
        ),
        self_check=(
            "So numerare e descrivere i segmenti prima di programmare?",
            "So collegare ogni `sleep` al comando che resta attivo?",
            "So testare un segmento alla volta?",
        ),
        accessibility="Offri sia una mappa a frecce sia una lista numerata equivalente; la missione deve essere comprensibile senza interpretare solo il disegno.",
        glossary=(
            ("algoritmo", "serie ordinata di passi per ottenere un risultato"),
            ("segmento", "una parte della missione verificabile da sola"),
            ("sequenza", "azioni eseguite in un ordine preciso"),
        ),
    ),
    "condizioni": LessonContent(
        prerequisites="Saper chiamare una funzione e comprendere un nome che riceve un valore, come un parametro.",
        mental_model=(
            "Una condizione è una domanda con risposta `True` o `False`. `if` esegue il blocco "
            "rientrato soltanto quando la risposta è `True`; `else` descrive l'altra strada. Seguiamo "
            "una strada per volta con il dito prima di eseguire."
        ),
        example="""```python
from romeo.easy import forward

modalita_sicura = True
if modalita_sicura:
    forward(0.3)  # Eseguita perché la condizione è True.
```""",
        guided_practice=(
            "Leggi la condizione come domanda: «modalità sicura è attiva?».",
            "Segna quale riga rientrata verrà eseguita con `True`.",
            "Esegui e controlla la velocità 0.3 nell'evento motore.",
            "Aggiungi un ramo `else` con velocità 0.5 e ripeti temporaneamente con `False`.",
            "Ripristina `True`, usa la durata adatta al target e termina con stop fuori dai due rami.",
        ),
        base_exercise="Con `modalita_sicura = True`, scegli velocità 0.3 e fermati sul target.",
        intermediate_exercise="Completa anche `else` e verifica separatamente sia `True` sia `False`.",
        challenge="Scrivi una funzione `scegli_velocita(modalita_sicura)` che esegua una delle due velocità e provala con entrambi i valori.",
        common_errors=(
            "Dimenticare i due punti dopo `if` o `else`.",
            "Allineare il corpo con `if` invece di rientrarlo.",
            "Provare soltanto il caso `True` e credere che anche l'altra strada funzioni.",
        ),
        self_check=(
            "So dire quale blocco viene eseguito con `True` e con `False`?",
            "So spiegare perché lo stop comune può stare dopo i due rami?",
            "Ho verificato entrambe le strade cambiando un solo valore?",
        ),
        accessibility="Rappresenta i due rami con le etichette testuali VERO/FALSO oltre alle frecce; leggi l'indentazione come «dentro if» o «dentro else».",
        glossary=(
            ("booleano", "valore che può essere soltanto `True` o `False`"),
            ("if", "esegue un blocco quando la condizione è vera"),
            ("else", "esegue il blocco alternativo quando la condizione è falsa"),
        ),
    ),
    "ciclo-for": LessonContent(
        prerequisites="Saper riconoscere un blocco rientrato e chiamare più volte la stessa funzione.",
        mental_model=(
            "Un ciclo `for` ripete un blocco un numero già noto di volte. `range(4)` fornisce quattro "
            "giri; a ogni giro il nome `passo` riceve il numero corrente. Le righe fuori dal rientro, "
            "come lo stop finale, vengono eseguite una sola volta."
        ),
        example="""```python
from romeo.easy import forward, stop

for passo in range(4):
    forward(0.2)  # Questa riga viene chiamata quattro volte.

stop()            # Questa riga viene chiamata una volta.
```""",
        guided_practice=(
            "Scrivi su carta i quattro valori prodotti da `range(4)`: 0, 1, 2, 3.",
            "Evidenzia la sola riga che appartiene al corpo del ciclo.",
            "Prevedi il numero di eventi motore prima del run.",
            "Esegui e conta gli eventi, non la distanza percorsa: senza `sleep` i comandi sono immediati.",
            "Cambia temporaneamente `range(2)`, verifica due eventi e ripristina quattro.",
        ),
        base_exercise="Usa `for` e `range(4)` per inviare quattro comandi, poi fermati.",
        intermediate_exercise="Aggiungi una breve durata nel corpo per rendere osservabile ogni ripetizione e prevedi il tempo totale.",
        challenge="Definisci una funzione con parametro `ripetizioni` e usa `range(ripetizioni)`; provala con 2 e 4.",
        common_errors=(
            "Credere che `range(4)` produca cinque valori da 0 a 4.",
            "Non rientrare il comando da ripetere.",
            "Rientrare anche `stop()` e fermare Romeo a ogni giro senza averlo previsto.",
        ),
        self_check=(
            "So prevedere quanti giri produce `range(4)`?",
            "So indicare quali righe sono dentro e fuori dal ciclo?",
            "So verificare il numero di ripetizioni negli eventi?",
        ),
        accessibility="Accompagna il blocco rientrato con una lista dei quattro giri; usa il nome esplicito `passo` invece di simboli convenzionali non spiegati.",
        glossary=(
            ("for", "ciclo che visita una sequenza di valori"),
            ("range", "funzione che produce un numero stabilito di valori interi"),
            ("iterazione", "un singolo giro del ciclo"),
        ),
    ),
    "ciclo-while": LessonContent(
        prerequisites="Saper leggere `if`, un confronto semplice e un blocco ripetuto con `for`.",
        mental_model=(
            "`while` ripete il corpo finché la sua domanda resta vera. Servono un contatore iniziale, "
            "un limite e un aggiornamento: senza aggiornamento la domanda non cambia e il ciclo può non "
            "finire. Prima del run simuliamo ogni giro in una tabella."
        ),
        example="""```python
contatore = 0
while contatore < 3:
    # Il contatore deve cambiare a ogni giro.
    contatore = contatore + 1
```

La tabella dei valori è 0 → 1 → 2 → 3; quando vale 3, `3 < 3` è falso e il ciclo termina.""",
        guided_practice=(
            "Crea una tabella con colonne `contatore` e `contatore < 3`.",
            "Compila a mano le righe per 0, 1, 2 e 3.",
            "Individua nel codice l'istruzione che avvicina il ciclo alla fine.",
            "Aggiungi `forward(0.2)` nel corpo e prevedi tre eventi motore.",
            "Esegui nel simulatore, verifica tre eventi e lascia `stop()` fuori dal ciclo.",
        ),
        base_exercise="Usa `while` e un contatore per inviare tre comandi, poi fermati.",
        intermediate_exercise="Modifica il limite a 2 e poi a 4, compilando prima la tabella di previsione.",
        challenge="Trova il difetto in una copia senza incremento, senza eseguirla; spiega come interrompere una prova che non termina.",
        common_errors=(
            "Dimenticare l'incremento e creare un ciclo che non termina.",
            "Rientrare `stop()` nel corpo quando deve essere eseguito una volta sola.",
            "Confondere `< 3` con `<= 3` e ottenere un giro in più.",
        ),
        self_check=(
            "So elencare i valori del contatore a ogni giro?",
            "So indicare perché la condizione diventa falsa?",
            "So riconoscere un ciclo potenzialmente infinito prima di eseguirlo?",
        ),
        accessibility="La tabella testuale rende espliciti i cambiamenti del contatore; fornisci una procedura scritta e raggiungibile da tastiera per interrompere l'esecuzione.",
        glossary=(
            ("while", "ciclo che continua mentre una condizione è vera"),
            ("contatore", "numero aggiornato a ogni iterazione"),
            ("terminazione", "momento in cui la condizione diventa falsa e il ciclo finisce"),
        ),
    ),
    "simulazione": LessonContent(
        prerequisites="Saper prevedere una sequenza, eseguirla e leggere posizione, orientamento e tempo finali.",
        mental_model=(
            "Il simulatore è un quaderno di laboratorio ripetibile. Lo stato è una fotografia di un "
            "istante; la traiettoria unisce molte pose; l'event log elenca i comandi. Con lo stesso "
            "scenario e lo stesso programma otteniamo gli stessi numeri: questo rende il debug verificabile."
        ),
        example="""```python
from time import sleep
from romeo.easy import forward, stop

forward(0.5)  # Nell'event log appare il cambio dei motori.
sleep(1)      # La traiettoria registra pose nel tempo.
stop()        # Lo stato finale mostra motori a zero.
```""",
        guided_practice=(
            "Prima del run scrivi una previsione per tempo, x, y, orientamento e stato motori.",
            "Esegui una volta e leggi prima lo stato finale, senza guardare l'animazione.",
            "Trova nell'event log il primo cambio motori e lo stop.",
            "Leggi tre punti della traiettoria: iniziale, intermedio e finale.",
            "Ripeti senza modifiche e verifica che gli stessi valori coincidano.",
        ),
        base_exercise="Avanza per due secondi, fermati e confronta previsione e traiettoria.",
        intermediate_exercise="Inserisci intenzionalmente una durata errata, usa le evidenze per individuarla e correggi una sola riga.",
        challenge="Spiega con una frase quale evidenza useresti per distinguere velocità errata, durata errata e stop mancante.",
        common_errors=(
            "Guardare soltanto l'animazione e ignorare i valori numerici.",
            "Cambiare più righe dopo un fallimento e perdere la causa dell'errore.",
            "Confondere un evento di comando con una posa della traiettoria.",
        ),
        self_check=(
            "So distinguere stato, evento e punto di traiettoria?",
            "So confrontare previsione e misura con numeri?",
            "So mostrare che due run identici producono lo stesso risultato?",
        ),
        accessibility="Ogni elemento visivo deve avere un equivalente testuale ordinato per tempo; traiettoria e colori non devono essere le sole fonti di feedback.",
        glossary=(
            ("stato", "valori del simulatore in un singolo istante"),
            ("evento", "registrazione di un comando o fatto significativo"),
            ("determinismo", "stesso input e stesso scenario producono lo stesso risultato"),
        ),
    ),
    "coordinate": LessonContent(
        prerequisites="Saper leggere una posa del simulatore e costruire una sequenza di tratti e rotazioni.",
        mental_model=(
            "La posa di Romeo contiene posizione `(x, y)` e orientamento. `x` cresce andando verso "
            "destra nella mappa, `y` cresce andando verso l'alto; l'orientamento dice dove punta il "
            "robot. Per raggiungere un punto, confrontiamo partenza e target e pianifichiamo i segmenti."
        ),
        example="""```text
Partenza: (0.5, 0.5), orientamento 0°
Target:   (1.0, 0.5)

La y non cambia e Romeo punta già verso x crescente:
serve un solo tratto diritto lungo 0.5 m.
```""",
        guided_practice=(
            "Copia partenza e target in una tabella con colonne x e y.",
            "Calcola separatamente quanto cambia x e quanto cambia y.",
            "Controlla se l'orientamento iniziale punta già verso la prima direzione utile.",
            "Traduci il piano in rotazione eventuale, avanzamento e stop.",
            "Esegui e confronta distanza dal target e tolleranza, poi correggi un solo segmento.",
        ),
        base_exercise="Dalla posa iniziale raggiungi `(1.0, 0.5)` e fermati.",
        intermediate_exercise="Disegna il piano per un target con la stessa x ma y maggiore, indicando prima la rotazione necessaria.",
        challenge="Pianifica su carta un target in cui cambiano sia x sia y usando due tratti e una rotazione.",
        common_errors=(
            "Confondere distanza da percorrere con coordinata finale.",
            "Ignorare l'orientamento iniziale e avanzare nella direzione sbagliata.",
            "Scambiare x e y leggendo la posa.",
        ),
        self_check=(
            "So indicare il verso positivo degli assi x e y?",
            "So calcolare la differenza tra partenza e target?",
            "So spiegare quando serve una rotazione prima di avanzare?",
        ),
        accessibility="Descrivi la mappa anche come coordinate e direzioni testuali; una griglia tattile o una tabella può sostituire la sola rappresentazione grafica.",
        glossary=(
            ("coordinata", "numero che indica una posizione lungo un asse"),
            ("posa", "posizione x/y più orientamento"),
            ("tolleranza", "distanza massima dal target ancora accettata"),
        ),
    ),
    "missioni": LessonContent(
        prerequisites="Saper leggere coordinate, pianificare segmenti e usare traiettoria ed eventi per correggerli.",
        mental_model=(
            "Una missione lunga diventa gestibile dividendola in checkpoint ordinati. Ogni checkpoint "
            "è una prova intermedia: prima raggiungiamo il primo, poi aggiungiamo il tratto successivo. "
            "Passare vicino ai punti nell'ordine conta più che indovinare subito l'intero programma."
        ),
        example="""```text
Partenza → checkpoint 1 → checkpoint 2 → checkpoint 3/parcheggio

Per ogni freccia annota:
1. posa di partenza; 2. rotazione; 3. tratto; 4. prova osservabile.
```""",
        guided_practice=(
            "Leggi lo scenario e trascrivi nell'ordine tutti i checkpoint, contando quelli effettivamente presenti.",
            "Disegna un segmento tra partenza e primo checkpoint e prevedi la posa raggiunta.",
            "Implementa soltanto il primo segmento e verifica la traiettoria.",
            "Aggiungi un checkpoint alla volta, conservando una versione funzionante.",
            "Esegui la missione completa e controlla ordine, parcheggio finale, collisioni e stop.",
        ),
        base_exercise="Attraversa nell'ordine i checkpoint dello scenario e fermati sul target finale.",
        intermediate_exercise="Raggruppa almeno un tratto in una funzione con un nome che descriva lo scopo.",
        challenge="Ottieni lo stesso percorso con una seconda combinazione di velocità e durate, mantenendo tutti i check verdi.",
        common_errors=(
            "Saltare direttamente al target finale senza attraversare i checkpoint in ordine.",
            "Aggiungere tutti i segmenti prima di aver verificato il primo.",
            "Contare checkpoint diversi da quelli realmente dichiarati nello scenario.",
        ),
        self_check=(
            "So elencare i checkpoint nell'ordine corretto?",
            "So mostrare sulla traiettoria dove viene superato ciascun punto?",
            "So indicare quale segmento correggere quando un checkpoint fallisce?",
        ),
        accessibility="Fornisci la sequenza dei checkpoint come elenco numerato con coordinate, non soltanto come marcatori sulla mappa.",
        glossary=(
            ("checkpoint", "punto intermedio da raggiungere nell'ordine stabilito"),
            ("collisione", "contatto del robot con ostacolo o bordo"),
            ("missione", "insieme completo di obiettivi e vincoli"),
        ),
    ),
    "capstone": LessonContent(
        prerequisites="Aver completato U01–U19 e saper usare funzioni, condizioni, cicli, coordinate, grading e stop sicuro.",
        mental_model=(
            "Il capstone è un piccolo progetto, non un unico tentativo. Prima definiamo criteri di "
            "successo, poi dividiamo la missione in funzioni, proviamo segmenti, leggiamo le evidenze e "
            "documentiamo una correzione. Il grader misura il comportamento; la spiegazione mostra il metodo."
        ),
        example="""```python
from romeo.easy import stop

def parcheggia():
    # Aggiungi qui soltanto i passi del parcheggio finale.
    stop()

# Le altre funzioni della missione verranno chiamate prima.
parcheggia()
```

L'esempio mostra la struttura, non rivela il percorso o i valori della soluzione.""",
        guided_practice=(
            "Trascrivi i criteri: checkpoint, collisioni, parcheggio, orientamento, tempo e stop presenti nello scenario.",
            "Disegna il percorso e assegna un nome a ogni segmento o fase.",
            "Implementa funzioni piccole e verifica ciascuna fase con una posa attesa.",
            "Usa una condizione o un ciclo soltanto dove rende il piano più chiaro, poi prova entrambi i casi necessari.",
            "Esegui il grader completo e correggi un check alla volta.",
            "Consegna codice, previsione, una correzione documentata e una breve spiegazione della safety.",
        ),
        base_exercise="Completa la missione con funzioni nominate e stop finale, superando tutti i check comportamentali.",
        intermediate_exercise="Riduci una ripetizione con un ciclo già conosciuto e dimostra che la traiettoria resta corretta.",
        challenge="Trova una seconda strategia valida e confrontala con la prima per chiarezza, tempo simulato e margine dagli ostacoli.",
        common_errors=(
            "Scrivere l'intera missione come una lunga sequenza prima di provare i segmenti.",
            "Aggiungere funzioni o cicli decorativi che non rendono il piano più chiaro.",
            "Considerare sufficiente il punteggio automatico senza consegnare spiegazione ed evidenze di debug.",
        ),
        self_check=(
            "Ogni funzione ha un nome che descrive una fase della missione?",
            "Posso mostrare un'evidenza per ogni criterio della rubrica?",
            "Romeo resta fermo anche alla conclusione dell'ultima fase?",
        ),
        accessibility="La consegna e la rubrica devono essere disponibili come checklist testuale; coordinate, eventi e risultati accompagnano sempre la mappa visiva.",
        glossary=(
            ("capstone", "progetto finale che combina le competenze del corso"),
            ("rubrica", "criteri trasparenti usati per valutare il lavoro"),
            ("evidenza", "dato, evento o spiegazione che dimostra un risultato"),
        ),
    ),
}
