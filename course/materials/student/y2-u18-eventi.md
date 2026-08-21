# Secondo anno 18. Programmazione a eventi

## Obiettivo

In questa unità imparerai a reagire a eventi senza polling fragile.

## Che cosa sai già

Sai definire funzioni, usare condizioni, liste e cicli brevi.

## Modello mentale

Un evento descrive qualcosa che è accaduto; un handler è una funzione che decide come reagire. Il dispatcher consegna ogni evento all'handler. Lo scaffold contiene il ciclo della coda: oggi scriviamo reazioni semplici, non callback, async o event loop complessi. Questa unità va studiata prima dei controller interattivi.

## Esempio minimo commentato

```python
def handle_event(evento):
    if evento["type"] == "key":
        return evento["value"]
    return None

risultato = handle_event({"type": "key", "value": "w"})
```

La funzione è testabile senza tastiera, browser o gamepad.

## Prova guidata

1. Separa evento, dispatcher e handler nel diagramma.
2. Prevedi il risultato di due eventi.
3. Completa l'handler con un solo tipo.
4. Usa la coda scaffolded per consegnare gli eventi in ordine.
5. Aggiungi un evento sconosciuto che non deve causare movimento.

## Esercizio base

Gestisci due eventi di tasto mantenendo l'ordine.

## Esercizio intermedio

Mappa eventi press/release in comando e STOP con una funzione pura.

## Mini-sfida

Gestisci tre tipi di evento mantenendo handler piccoli e un comportamento sicuro per tipi ignoti.

## Consegna valutata

Inserisci due eventi in una coda e gestiscili nell'ordine.

## Errori tipici

- Mettere tutta la logica nel ciclo invece che nell'handler testabile.
- Eseguire movimento per eventi sconosciuti.
- Confondere ordine della coda e priorità degli eventi.

## Autoverifica

- So definire evento, handler e dispatcher?
- Posso testare l'handler senza dispositivo?
- Un evento ignoto lascia Romeo fermo?

## Accessibilità

Gli eventi possono provenire da pulsante, tastiera o dati simulati; mostra sempre una traccia testuale ordinata.

## Parole nuove

| Termine | Significato in questa lezione |
| --- | --- |
| `evento` | dato che descrive qualcosa accaduto |
| `handler` | funzione che reagisce a un evento |
| `coda` | struttura che conserva l'ordine degli eventi |
