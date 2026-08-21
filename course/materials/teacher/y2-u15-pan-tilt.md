# Guida docente — secondo anno 15. Pan e tilt

Durata: 60 minuti. Difficoltà: B. Obiettivo osservabile: lo studente sa
orientare la camera attraverso Robot e giustifica protocollo, validazione e cleanup.

## Prerequisiti e modello mentale

Conosci la API Robot, i numeri decimali e il CameraService.

Pan ruota lo sguardo a sinistra/destra; tilt lo inclina su/giù. Gli angoli sono gradi entro limiti sicuri. Robot inoltra la richiesta al backend: il mock registra gli angoli, mentre il backend reale muove i servo.

## Conduzione

- 0–10 min: mappa alla lavagna di client, server, request e response.
- 10–25 min: dimostrazione su loopback, prima con previsione e poi con trace.
- 25–50 min: pair programming; un ruolo cura il protocollo, l'altro failure e risorse.
- 50–60 min: run TheBitLab, revisione dell'evidenza ed exit ticket.

Il marker di output offre soltanto feedback formativo ed è banalmente riproducibile. Non usarlo
come prova sommativa. Finché il runtime non viene eseguito dentro il boundary ufficiale TheBitLab,
anche gli assert e i check comportamentali presuppongono una submission collaborativa.

## Misconcezioni e safety

- Scambiare pan e tilt.
- Assumere che qualsiasi angolo sia fisicamente sicuro.
- Dimenticare `close` quando un assert fallisce.

## Inclusione ed evidenze

Accompagna le frecce con parole sinistra/destra/su/giù e valori numerici; consenti controllo tramite pulsanti grandi oltre agli assi analogici.

Le evidenze sono sorgente, comportamento osservato, gestione degli errori, cleanup e spiegazione
orale. Il marker, da solo, non dimostra la competenza.
