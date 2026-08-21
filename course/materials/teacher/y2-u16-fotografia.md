# Guida docente — secondo anno 16. Fotografia REST

Durata: 70 minuti. Difficoltà: B. Obiettivo osservabile: lo studente sa
ricevere JPEG con media type corretto e giustifica protocollo, validazione e cleanup.

## Prerequisiti e modello mentale

Conosci REST, TestClient, JSON, byte JPEG e CameraService mock.

Una foto REST è una risorsa binaria: la response contiene byte JPEG invece di JSON. Status e Content-Type dicono al client se e come interpretarla. `create_app(camera=mock)` passa alla app una camera prevedibile; questa iniezione evita hardware reale durante il test.

## Conduzione

- 0–10 min: mappa alla lavagna di client, server, request e response.
- 10–25 min: dimostrazione su loopback, prima con previsione e poi con trace.
- 25–50 min: pair programming; un ruolo cura il protocollo, l'altro failure e risorse.
- 50–70 min: run TheBitLab, revisione dell'evidenza ed exit ticket.

Il marker di output offre soltanto feedback formativo ed è banalmente riproducibile. Non usarlo
come prova sommativa. Finché il runtime non viene eseguito dentro il boundary ufficiale TheBitLab,
anche gli assert e i check comportamentali presuppongono una submission collaborativa.

## Misconcezioni e safety

- Chiamare `.json()` su una foto.
- Accettare qualsiasi contenuto con status 200.
- Usare la camera reale nei test automatici.

## Inclusione ed evidenze

L'esito della foto è descritto anche con testo, dimensione e status; nessuno deve essere ripreso per completare il laboratorio.

Le evidenze sono sorgente, comportamento osservato, gestione degli errori, cleanup e spiegazione
orale. Il marker, da solo, non dimostra la competenza.
