# Secondo anno 20. Telemetria versionata

## Obiettivo e modello mentale

In questa unità imparerai a leggere stato senza dipendere dal renderer. Userai schema, pose, motors, clock. Separa sempre tre domande:
chi comunica, quale messaggio attraversa il confine e quale risposta prova che l'operazione è
riuscita. Il robot non deve conoscere i dettagli del trasporto: socket, REST e WebSocket arrivano
alla stessa API Romeo attraverso adapter distinti.

## Laboratorio

Genera uno snapshot simulato e verifica schema e campi.

1. Disegna endpoint e direzione dei messaggi.
2. Completa `starter.py` con la minima operazione osservabile.
3. Verifica dati e status prima di stampare il marker richiesto dal grader.
4. Chiudi socket, camera o sessioni anche in caso di errore.
5. Esegui due volte: un risultato deterministico deve essere ripetibile.

## Debug guidato

Un timeout suggerisce spesso che un endpoint attende dati o una chiusura. Una risposta ricevuta non
è automaticamente valida: controlla tipo, schema, status e valori. Per JSON distingui testo e
oggetto Python; per HTTP distingui trasporto, metodo e risorsa; per WebSocket considera la durata
della connessione e lo STOP alla disconnessione. Non esporre il server della classe su Internet.
Usa loopback durante gli esperimenti e non inserire segreti nel sorgente.

## Autoverifica

Sai spiegare perché questa tecnologia è adatta al compito? Quale failure hai gestito? Dove avviene
la validazione? Quale istruzione libera la risorsa? Mostra un'evidenza concreta: risposta, marker,
stato motori o test. Poi descrivi come cambierebbe solo l'adapter passando dal simulatore al Romeo
fisico.
