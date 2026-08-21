# 12. Crea una funzione

## Obiettivo

In questo laboratorio imparerai a racchiudere una sequenza in una funzione con parametro.

## Che cosa sai già

Saper scrivere e verificare una sequenza con movimento, durata e stop.

## Modello mentale

Definire una funzione significa dare un nome a una piccola ricetta. Le righe rientrate sono il corpo della ricetta e non partono finché la funzione non viene chiamata. Un parametro è un posto vuoto che riceve un valore diverso a ogni chiamata.

## Esempio minimo commentato

```python
from romeo.easy import stop

def arresta():       # Definiamo la ricetta.
    stop()            # Corpo: è rientrato di quattro spazi.

arresta()             # Ora eseguiamo la ricetta.
```

## Prova guidata

1. Cerchia il nome `arresta` nella definizione e nella chiamata.
2. Esegui il file senza la chiamata finale e osserva che il corpo non viene eseguito.
3. Ripristina la chiamata e verifica l'evento di stop.
4. Completa il corpo di `avanza_per(secondi)` con movimento, `sleep(secondi)` e stop.
5. Chiama `avanza_per(2)` e verifica posizione e stato finali.

## Esercizio base

Definisci `avanza_per(secondi)` e usala con il valore 2.

## Esercizio intermedio

Chiama la stessa funzione prima con 1 e poi con 2; confronta le distanze in due run separati.

## Mini-sfida

Definisci una seconda funzione senza parametri che accenda un LED e lasci Romeo fermo.

## Consegna valutata

Definisci avanza_per(secondi), chiamala con 2 e raggiungi il target.

## Errori tipici

- Dimenticare i due punti dopo la riga `def`.
- Non rientrare il corpo di quattro spazi.
- Definire la funzione ma non chiamarla.

## Autoverifica

- So distinguere definizione e chiamata?
- So indicare quali righe appartengono al corpo?
- So spiegare quale valore riceve il parametro `secondi`?

## Accessibilità

Evidenzia il rientro anche con una guida verticale e descrivilo come «quattro spazi»; non comunicarlo soltanto con il colore dell'editor.

## Parole nuove

| Termine | Significato in questa lezione |
| --- | --- |
| `def` | parola che avvia la definizione di una funzione |
| `corpo` | righe rientrate eseguite dalla funzione |
| `parametro` | nome che riceve il valore fornito alla chiamata |
