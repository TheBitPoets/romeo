# Secondo anno 17. Stream MJPEG

## Obiettivo

In questa unità imparerai a riconoscere frame e boundary.

## Che cosa sai già

Sai leggere byte JPEG e una response HTTP; conosci iteratori e `next` grazie a uno scaffold guidato.

## Modello mentale

MJPEG invia una sequenza di immagini JPEG dentro una response HTTP multipart. Un boundary separa i frame, come un divisore etichettato. Lo scaffold costruisce server e generatore: lo studente osserva due parti e verifica la struttura, senza implementare streaming o concorrenza da zero.

## Esempio minimo commentato

```text
--frame
Content-Type: image/jpeg

<byte JPEG>
--frame
Content-Type: image/jpeg

<byte JPEG>
```

```python
primo = next(camera.frames(frames_per_second=10))
assert primo.startswith(b"ÿØ")
```

Il secondo frammento controlla il JPEG; il boundary appartiene al livello HTTP multipart.

## Prova guidata

1. Evidenzia testualmente i due boundary nell'esempio.
2. Distingui header della parte e byte del frame.
3. Leggi due frame dal generatore mock fornito.
4. Verifica marker JPEG per entrambi.
5. Ispeziona una response MJPEG scaffolded e controlla il parametro boundary.

## Esercizio base

Leggi e valida due frame consecutivi dal mock.

## Esercizio intermedio

Verifica Content-Type multipart e presenza del boundary in una response fornita.

## Mini-sfida

Interrompi la lettura dopo tre frame e dimostra che camera e stream vengono chiusi.

## Consegna valutata

Leggi il primo frame del mock e verifica i marker JPEG.

## Errori tipici

- Chiamare MJPEG un singolo byte array JPEG.
- Confondere boundary e marker interni JPEG.
- Creare un ciclo infinito senza condizione di arresto o cleanup.

## Autoverifica

- So spiegare perché MJPEG contiene più JPEG?
- So trovare il boundary?
- Il mio lettore può terminare in modo pulito?

## Accessibilità

Fornisci frame campione e struttura testuale; il risultato può essere verificato con contatori e status senza dover vedere il video.

## Parole nuove

| Termine | Significato in questa lezione |
| --- | --- |
| `MJPEG` | stream formato da immagini JPEG successive |
| `multipart` | body HTTP composto da più parti |
| `boundary` | sequenza che separa le parti |
| `frame` | una singola immagine dello stream |
