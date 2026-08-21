# Secondo anno 6. Il protocollo Romeo/1

## Obiettivo

In questa unità imparerai a analizzare comandi testuali con una whitelist.

## Che cosa sai già

Sai scambiare righe di byte e usare `split`, condizioni e conversioni numeriche.

## Modello mentale

Un protocollo è un accordo preciso sul significato dei messaggi. Romeo/1 usa una riga per comando: prima una parola ammessa, poi gli eventuali argomenti. Una whitelist elenca ciò che è valido; tutto il resto viene rifiutato senza eseguire azioni.

## Esempio minimo commentato

```python
riga = "FORWARD 0.4"
parti = riga.split()
comando = parti[0]

if comando not in {"FORWARD", "STOP"}:
    raise ValueError("comando sconosciuto")
```

Il parser Romeo completo è fornito dalla libreria; prima ne osserviamo le regole con codice semplice.

## Prova guidata

1. Compila una tabella con `FORWARD velocità` e `STOP`.
2. Separa tre righe valide con `split`.
3. Prova un comando sconosciuto e controlla che venga rifiutato.
4. Usa `parse_command` e osserva nome e argomenti.
5. Verifica anche argomento mancante e velocità fuori limite.

## Esercizio base

Analizza `FORWARD 0.4` e `STOP` verificando nome e argomenti.

## Esercizio intermedio

Costruisci una tabella di almeno quattro input invalidi e del motivo del rifiuto.

## Mini-sfida

Produci risposte testuali coerenti `OK` o `ERROR motivo` senza muovere il robot per input invalidi.

## Consegna valutata

Analizza FORWARD e STOP e controlla nome e argomenti.

## Errori tipici

- Accettare qualsiasi parola e passarla direttamente al robot.
- Dimenticare di convertire e limitare la velocità.
- Ignorare il fine riga e unire due comandi ricevuti insieme.

## Autoverifica

- So scrivere la grammatica dei due comandi?
- So spiegare perché serve una whitelist?
- Il mio codice rifiuta dati invalidi prima dell'azione?

## Accessibilità

La tabella del protocollo usa testo e non colori. Leggi gli errori con una motivazione breve e stabile.

## Parole nuove

| Termine | Significato in questa lezione |
| --- | --- |
| `protocollo` | regole condivise per interpretare messaggi |
| `whitelist` | elenco esplicito dei valori ammessi |
| `argomento` | valore che completa un comando |
