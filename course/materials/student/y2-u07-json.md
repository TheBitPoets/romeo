# Secondo anno 7. Dati JSON

## Obiettivo

In questa unità imparerai a serializzare e validare un messaggio.

## Che cosa sai già

Sai usare dizionari, liste, stringhe, numeri e booleani Python.

## Modello mentale

JSON è testo con una struttura condivisa. `json.dumps` trasforma un oggetto Python in testo da inviare; `json.loads` ricostruisce dati Python dal testo. JSON non apre connessioni e non esegue comandi.

## Esempio minimo commentato

```python
import json

stato = {"moving": True, "motors": [0.3, 0.3]}
testo = json.dumps(stato)   # dict → str
copia = json.loads(testo)  # str → dict
print(type(testo), type(copia))
```

Controllare i tipi dopo la decodifica evita di fidarsi soltanto dell'aspetto del testo.

## Prova guidata

1. Prevedi i tipi di `stato`, `testo` e `copia`.
2. Esegui e verifica le previsioni.
3. Aggiungi il campo stringa `type`.
4. Modifica il testo rendendolo invalido e osserva `JSONDecodeError`.
5. Verifica campi e tipi prima di usare i valori.

## Esercizio base

Serializza e decodifica lo stato di Romeo mantenendo tipo e valori.

## Esercizio intermedio

Valida un messaggio richiedendo `type`, due velocità numeriche e `moving` booleano.

## Mini-sfida

Restituisci un errore leggibile per JSON malformato o con schema incompleto.

## Consegna valutata

Completa `encode_state`, `decode_state` nello starter senza rinominare le funzioni. Rispetta parametri, valore restituito e cleanup descritti nella docstring: TheBitLab importerà le funzioni e le proverà con input diversi. Obiettivo: serializzare e validare un messaggio.

## Errori tipici

- Confondere un dizionario con il testo JSON che lo rappresenta.
- Scrivere `True` a mano nel JSON, dove il valore è `true`.
- Usare campi ricevuti senza verificarne presenza e tipo.

## Autoverifica

- So descrivere serializzazione e deserializzazione?
- So indicare il tipo prima e dopo?
- So gestire un messaggio malformato?

## Accessibilità

Mostra dict e JSON su righe separate con etichette; non segnalare le differenze solo con colori.

## Parole nuove

| Termine | Significato in questa lezione |
| --- | --- |
| `serializzazione` | trasformazione dei dati in un formato trasmissibile |
| `schema` | insieme dei campi e tipi attesi |
| `JSON` | formato testuale strutturato |
