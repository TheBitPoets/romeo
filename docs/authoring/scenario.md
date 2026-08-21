# Creare uno scenario simulato

Gli scenari spaziali usano `romeo.scenario.v1`. Il file descrive il mondo e i checks; non contiene codice studente.

## Esempio

```json
{
  "schema_version": "romeo.scenario.v1",
  "id": "esempio-target",
  "world_width": 3.0,
  "world_height": 2.0,
  "start_x": 0.5,
  "start_y": 0.5,
  "start_heading_degrees": 0,
  "robot_radius": 0.1,
  "wheel_base": 0.18,
  "max_wheel_speed": 0.5,
  "obstacles": [],
  "checks": [
    {
      "id": "target",
      "name": "Raggiunge il target",
      "type": "stop_in_zone",
      "parameters": {
        "x": 1.0,
        "y": 0.5,
        "tolerance": 0.04,
        "points": 3
      }
    }
  ]
}
```

## Coordinate e unità

Il mondo simulato usa grandezze coerenti con il simulation engine. Mantieni dimensioni semplici per le unità introduttive: lo studente deve ragionare sul concetto della lezione, non combattere con una geometria inutilmente complessa.

## Pose iniziale

`start_x`, `start_y` e `start_heading_degrees` definiscono la condizione iniziale. Una missione deve essere comprensibile anche da un disegno sul quaderno.

## Robot e velocità

`robot_radius`, `wheel_base` e `max_wheel_speed` appartengono al modello simulato. Non inserire in ogni Activity la calibrazione accidentale del singolo esemplare fisico: quella resta configurazione hardware.

## Ostacoli

Aggiungili solo quando servono all'obiettivo didattico. Un ostacolo può trasformare una semplice lezione sui cicli in una lezione implicita di geometria/path planning.

## Checks

Ogni check dovrebbe corrispondere a una frase della consegna. Esempi tipici includono target, collisioni, checkpoint, orientamento, tempo o stato finale.

Evita checks che premiano dettagli implementativi non richiesti. Se due programmi diversi raggiungono correttamente lo stesso obiettivo, il grader dovrebbe accettarli salvo che la tecnica stessa sia l'obiettivo della lezione.

## Debug dello scenario

Prima di cambiare il programma studente:

1. valida il JSON;
2. esegui la soluzione docente;
3. osserva traiettoria e stato finale;
4. verifica ogni check separatamente;
5. prova almeno un caso volutamente errato.

Uno scenario che accetta la soluzione ma anche uno starter vuoto non è pronto.
