# Problemi comuni

Usa questa pagina per capire **dove** cercare prima di cambiare codice a caso.

## `SyntaxError`

Python non riesce a leggere il programma. Controlla la riga indicata e quella precedente: parentesi, due punti, virgolette e indentazione sono le cause più comuni.

## `NameError`

Hai usato un nome che Python non conosce. Controlla spelling e `import`.

## Il programma parte ma Romeo non si muove nel simulatore

Controlla che il comando di movimento sia realmente eseguito e che non venga subito annullato da `stop()`. Guarda la sequenza degli eventi e il report.

## Romeo si muove nella direzione sbagliata nel simulatore

Verifica prima il programma: `forward`, `backward`, `left`, `right` e l'ordine delle istruzioni. Il simulatore è deterministico, quindi una direzione errata è normalmente riproducibile.

## Il simulatore è corretto ma il robot reale devia

Non modificare subito la logica. Ferma il robot e segnala il problema al docente: può dipendere da calibrazione, attrito, ruote, motori o alimentazione.

## La camera non è disponibile sul robot

Non smontare o riconnettere componenti a robot alimentato senza autorizzazione. Il docente/diagnostica hardware controllerà camera, collegamento, configurazione Picamera2 e disponibilità del device.

## Il runtime non è disponibile

Se TheBitLab segnala che `romeo-sim` non è disponibile, il problema è normalmente dell'ambiente, del plugin o del backend, non del tuo `main.py`. Conserva il messaggio e avvisa il docente.

## Il grading autorevole non parte

TheBitLab è progettato per fallire chiuso quando la sandbox sicura non è disponibile. Non cercare di aggirare l'errore eseguendo codice riservato fuori dalla piattaforma. Il docente o l'amministratore deve ripristinare il servizio.

## Regola di debug

Riduci il problema. Prova una sequenza minima, per esempio `forward` seguito da `stop`, prima di analizzare una missione lunga. Quando il caso minimo funziona, reintroduci un elemento alla volta.
