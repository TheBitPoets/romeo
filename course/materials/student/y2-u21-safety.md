# Secondo anno 21. Safety di rete

## Obiettivo

In questa unità imparerai a applicare ownership, timeout e stop.

## Che cosa sai già

Conosci controllo remoto, timeout, mock backend e test deterministici.

## Modello mentale

Il controllo è un permesso temporaneo: un solo controller possiede il lease. Ogni comando valido rinnova il tempo; il watchdog ferma i motori quando scade. Release, disconnect, eccezione e shutdown devono tutti portare allo stesso stato sicuro: velocità zero. Il test usa clock e watchdog controllati dallo scaffold.

## Esempio minimo commentato

```python
safety.claim_controller("client-a")
try:
    safety.set_motor_speeds_for("client-a", 0.4, 0.4)
finally:
    safety.release_controller("client-a")

assert (backend.left_speed, backend.right_speed) == (0.0, 0.0)
```

Il `finally` copre l'uscita normale e l'errore; un test separato fa avanzare il clock oltre il timeout.

## Prova guidata

1. Disegna una timeline claim→command→renew→expire→stop.
2. Prendi il controllo e verifica il movimento sul mock.
3. Tenta il claim da un secondo controller e osserva il rifiuto.
4. Rilascia nel `finally` e verifica zero.
5. Avanza il clock scaffolded senza comandi e verifica lo stop del watchdog.

## Esercizio base

Dimostra che release azzera entrambi i motori.

## Esercizio intermedio

Dimostra ownership esclusiva e stop alla scadenza con clock controllato.

## Mini-sfida

Simula una disconnessione durante il movimento e raccogli una traccia che dimostri lo stop automatico.

## Consegna valutata

Prendi il controllo, muovi, rilascia e verifica motori a zero.

## Errori tipici

- Disattivare il watchdog proprio nel test che dovrebbe verificarlo.
- Fermare solo un motore.
- Affidarsi allo STOP manuale come unico percorso sicuro.

## Autoverifica

- Un secondo controller viene rifiutato?
- Timeout, disconnect ed errore portano a zero?
- I test non dipendono da attese reali fragili?

## Accessibilità

La timeline è anche un elenco numerato; stato owner, tempo residuo e motori sono disponibili come testo.

## Parole nuove

| Termine | Significato in questa lezione |
| --- | --- |
| `lease` | permesso di controllo con durata limitata |
| `watchdog` | controllo che ferma il sistema quando i comandi cessano |
| `ownership` | regola che consente un solo controller attivo |
