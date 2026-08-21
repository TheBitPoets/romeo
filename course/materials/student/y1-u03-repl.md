# 3. Esplora con il REPL

## Obiettivo

In questo laboratorio imparerai a provare una chiamata alla volta e leggere gli errori.

## Che cosa sai già

Aver completato U02 e saper eseguire un file con Run.

## Modello mentale

Il REPL è un banco prova: mostra `>>>`, riceve una sola istruzione e risponde subito. Un file conserva invece una sequenza da rieseguire. Prima proviamo un comando nel REPL, poi trasferiamo la sequenza riuscita in `main.py`.

## Esempio minimo commentato

```text
>>> from romeo.easy import stop
>>> stop()
>>> fermati()
NameError: name 'fermati' is not defined
```

L'ultima risposta non è un giudizio: indica che Python non conosce il nome `fermati`.

## Prova guidata

1. Apri il REPL e trova il prompt `>>>`.
2. Digita l'import dell'esempio e premi Invio una sola volta.
3. Digita `stop()` e osserva la risposta e lo stato dei motori.
4. Prova volontariamente `Stop()` e leggi l'ultima riga dell'errore.
5. Chiudi la prova e trasferisci in `main.py` la sequenza LED rosso, movimento, stop.

## Esercizio base

Prova `led("red")` nel REPL dopo l'import fornito e verifica il nome testuale del colore.

## Esercizio intermedio

Causa un `NameError`, correggi soltanto il nome e ripeti la chiamata.

## Mini-sfida

Prevedi la differenza tra eseguire tre righe nel REPL e salvarle nello stesso ordine in `main.py`.

## Consegna valutata

Trasferisci in main.py la sequenza provata nel REPL: LED rosso, movimento, stop.

## Errori tipici

- Copiare anche i caratteri `>>>`: sono il prompt, non parte del codice.
- Dimenticare l'import prima della chiamata e ricevere `NameError`.
- Leggere tutto il traceback insieme invece di partire dall'ultima riga.

## Autoverifica

- So distinguere il prompt da ciò che devo digitare?
- So trovare il nome sconosciuto in un `NameError`?
- So spiegare quando usare il REPL e quando usare `main.py`?

## Accessibilità

La trascrizione testuale accompagna ogni cambiamento visivo; chi usa uno screen reader può seguire prompt, comando e risposta in ordine lineare.

## Parole nuove

| Termine | Significato in questa lezione |
| --- | --- |
| `REPL` | ambiente che legge ed esegue una istruzione alla volta |
| `prompt` | i caratteri `>>>` che indicano che Python è pronto |
| `NameError` | errore che segnala un nome non conosciuto |
