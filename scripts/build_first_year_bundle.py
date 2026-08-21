"""Generate the original, deterministic Romeo first-year Course Bundle."""

# ruff: noqa: E501 -- lesson source and prose are kept readable as complete data strings.

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSE = ROOT / "course"


@dataclass(frozen=True)
class Unit:
    slug: str
    title: str
    objective: str
    concepts: str
    task: str
    starter: str
    solution: str
    minutes: int = 50
    difficulty: str = "A"


UNITS = (
    Unit(
        "introduzione",
        "Conosci Romeo",
        "eseguire il primo programma e fermare il robot",
        "programma, istruzione, simulatore",
        "Accendi il LED blu, invia un breve comando avanti e termina con stop.",
        "from romeo.easy import forward, led, stop\n\n# Completa qui\n",
        'from romeo.easy import forward, led, stop\n\nled("blue")\nforward(0.2)\nstop()\n',
        45,
    ),
    Unit(
        "componenti",
        "Dai componenti ai comandi",
        "collegare API, motori, ruote e LED",
        "Raspberry Pi, CRICKIT, backend",
        "Usa il LED verde come segnale di pronto, aziona entrambi i motori e fermati.",
        "from romeo.easy import forward, led, stop\n\n# Segnale di pronto\n",
        'from romeo.easy import forward, led, stop\n\nled("green")\nforward(0.25)\nstop()\n',
    ),
    Unit(
        "repl",
        "Esplora con il REPL",
        "provare una chiamata alla volta e leggere gli errori",
        "REPL, import, chiamata",
        "Trasferisci in main.py la sequenza provata nel REPL: LED rosso, movimento, stop.",
        "from romeo.easy import forward, led, stop\n\n",
        'from romeo.easy import forward, led, stop\n\nled("red")\nforward(0.2)\nstop()\n',
    ),
    Unit(
        "chiamate-funzione",
        "Chiama una funzione",
        "riconoscere nome, parentesi e argomento",
        "funzione, argomento, valore predefinito",
        "Chiama forward con velocità 0.3, quindi stop.",
        "from romeo.easy import forward, stop\n\n# forward riceve una velocità tra 0 e 1\n",
        "from romeo.easy import forward, stop\n\nforward(0.3)\nstop()\n",
    ),
    Unit(
        "led",
        "Comunica con il LED",
        "usare un output immediato per mostrare lo stato",
        "RGB, stringhe, output",
        "Imposta il LED su blu; il grader controllerà il colore finale.",
        "from romeo.easy import led\n\n# Scegli: red, green, blue, yellow, white oppure off\n",
        'from romeo.easy import led\n\nled("blue")\n',
    ),
    Unit(
        "motore-singolo",
        "Controlla una ruota",
        "comandare separatamente la ruota sinistra",
        "Robot, drive, velocità con segno",
        "Con Robot.drive fai girare solo la ruota sinistra, poi ferma Romeo.",
        "from romeo import Robot\n\nrobot = Robot()\n# robot.drive(sinistra, destra)\n",
        "from romeo import Robot\n\nrobot = Robot()\nrobot.drive(0.35, 0.0)\nrobot.stop()\n",
    ),
    Unit(
        "due-motori",
        "Coordina due ruote",
        "confrontare velocità delle due ruote",
        "coppia di velocità, direzione",
        "Imposta entrambe le ruote a 0.3 e termina in sicurezza.",
        "from romeo import Robot\n\nrobot = Robot()\n",
        "from romeo import Robot\n\nrobot = Robot()\nrobot.drive(0.3, 0.3)\nrobot.stop()\n",
    ),
    Unit(
        "avanti-indietro",
        "Avanti e indietro",
        "comporre due movimenti opposti nel tempo",
        "sleep, sequenza, segno",
        "Avanza per un secondo, torna indietro per un secondo e fermati.",
        "from time import sleep\nfrom romeo.easy import backward, forward, stop\n\n",
        "from time import sleep\nfrom romeo.easy import backward, forward, stop\n\nforward(0.4)\nsleep(1)\nbackward(0.4)\nsleep(1)\nstop()\n",
        55,
    ),
    Unit(
        "curve-rotazioni",
        "Curve e rotazioni",
        "distinguere curva e rotazione sul posto",
        "differential drive, orientamento",
        "Ruota Romeo di circa 90 gradi a sinistra e fermalo.",
        "from time import sleep\nfrom romeo.easy import left, stop\n\n",
        "from time import sleep\nfrom romeo.easy import left, stop\n\nleft(0.5)\nsleep(0.5655)\nstop()\n",
        60,
        "B",
    ),
    Unit(
        "stop-safety",
        "Stop e sicurezza",
        "garantire l'arresto anche al termine di una sequenza",
        "stop, watchdog, fail-safe",
        "Invia almeno un comando motore e lascia Romeo fermo.",
        "from romeo.easy import forward, stop\n\nforward(0.2)\n# Manca l'istruzione più importante\n",
        "from romeo.easy import forward, stop\n\nforward(0.2)\nstop()\n",
    ),
    Unit(
        "velocita",
        "Scegli la velocità",
        "confrontare valori normalizzati tra 0 e 1",
        "float, intervallo, limite",
        "Raggiungi il target a x=1.0 usando velocità 0.5 per due secondi.",
        "from time import sleep\nfrom romeo.easy import forward, stop\n\n",
        "from time import sleep\nfrom romeo.easy import forward, stop\n\nforward(0.5)\nsleep(2)\nstop()\n",
        55,
    ),
    Unit(
        "funzioni",
        "Crea una funzione",
        "racchiudere una sequenza in una funzione con parametro",
        "def, parametro, corpo",
        "Definisci avanza_per(secondi), chiamala con 2 e raggiungi il target.",
        "from time import sleep\nfrom romeo.easy import forward, stop\n\ndef avanza_per(secondi):\n    # completa il corpo\n    pass\n\n",
        "from time import sleep\nfrom romeo.easy import forward, stop\n\ndef avanza_per(secondi):\n    forward(0.5)\n    sleep(secondi)\n    stop()\n\navanza_per(2)\n",
        60,
        "B",
    ),
    Unit(
        "sequenze",
        "Progetta una sequenza",
        "ordinare azioni e durate per una missione",
        "algoritmo, ordine, stato",
        "Avanza, ruota a sinistra, avanza ancora e fermati.",
        "from time import sleep\nfrom romeo.easy import forward, left, stop\n\n",
        "from time import sleep\nfrom romeo.easy import forward, left, stop\n\nforward(0.4)\nsleep(1)\nleft(0.5)\nsleep(0.5655)\nforward(0.4)\nsleep(1)\nstop()\n",
        60,
        "B",
    ),
    Unit(
        "condizioni",
        "Decidi con if",
        "scegliere un comportamento in base a un dato",
        "booleano, if, confronto",
        "Se modalita_sicura è True usa velocità 0.3; raggiungi il target e fermati.",
        "from time import sleep\nfrom romeo.easy import forward, stop\n\nmodalita_sicura = True\n# usa if\n",
        "from time import sleep\nfrom romeo.easy import forward, stop\n\nmodalita_sicura = True\nif modalita_sicura:\n    forward(0.3)\n    sleep(10 / 3)\nelse:\n    forward(0.5)\n    sleep(2)\nstop()\n",
        60,
        "B",
    ),
    Unit(
        "ciclo-for",
        "Ripeti con for",
        "ripetere un numero noto di azioni",
        "for, range, iterazione",
        "Usa un ciclo for per inviare quattro comandi di movimento, poi stop.",
        "from romeo.easy import forward, stop\n\n# ripeti 4 volte\n",
        "from romeo.easy import forward, stop\n\nfor _ in range(4):\n    forward(0.2)\nstop()\n",
        55,
        "B",
    ),
    Unit(
        "ciclo-while",
        "Controlla un ciclo while",
        "usare una condizione e assicurare la terminazione",
        "while, contatore, terminazione",
        "Invia tre comandi con while e termina con stop.",
        "from romeo.easy import forward, stop\n\ncontatore = 0\n# completa il ciclo\n",
        "from romeo.easy import forward, stop\n\ncontatore = 0\nwhile contatore < 3:\n    forward(0.2)\n    contatore = contatore + 1\nstop()\n",
        60,
        "B",
    ),
    Unit(
        "simulazione",
        "Osserva il simulatore",
        "usare traiettoria, clock ed eventi per il debug",
        "stato, evento, determinismo",
        "Avanza per due secondi, fermati e confronta la traiettoria con la previsione.",
        "from time import sleep\nfrom romeo.easy import forward, stop\n\n",
        "from time import sleep\nfrom romeo.easy import forward, stop\n\nforward(0.5)\nsleep(2)\nstop()\n",
        65,
        "B",
    ),
    Unit(
        "coordinate",
        "Raggiungi una coordinata",
        "tradurre metri e orientamento in comandi",
        "x, y, angolo, tolleranza",
        "Dalla posa iniziale raggiungi il target (1.0, 0.5) e fermati.",
        "from time import sleep\nfrom romeo.easy import forward, stop\n\n",
        "from time import sleep\nfrom romeo.easy import forward, stop\n\nforward(0.5)\nsleep(2)\nstop()\n",
        70,
        "C",
    ),
    Unit(
        "missioni",
        "Completa una missione",
        "scomporre un percorso in segmenti verificabili",
        "checkpoint, collisione, debug",
        "Attraversa nell'ordine due checkpoint e fermati sul target finale.",
        "from time import sleep\nfrom romeo.easy import forward, left, stop\n\n# pianifica i segmenti\n",
        "from time import sleep\nfrom romeo.easy import forward, stop\n\nforward(0.5)\nsleep(3)\nstop()\n",
        80,
        "C",
    ),
    Unit(
        "capstone",
        "Capstone: consegna robotica",
        "progettare, testare e spiegare una missione completa",
        "funzioni, cicli, condizioni, grading",
        "Raggiungi i checkpoint, evita collisioni, fermati nel parcheggio e consegna una breve spiegazione.",
        "from time import sleep\nfrom romeo.easy import forward, left, right, stop\n\n# Scrivi funzioni piccole e prova un segmento alla volta.\n",
        "from time import sleep\nfrom romeo.easy import forward, stop\n\ndef tratto(durata):\n    forward(0.5)\n    sleep(durata)\n    stop()\n\ntratto(3)\n",
        120,
        "C",
    ),
)


def dump(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8")


def scenario(index: int, unit: Unit) -> dict[str, object]:
    checks: list[dict[str, object]]
    if index == 5:
        checks = [
            {
                "id": "led",
                "name": "LED blu",
                "type": "final_led_color",
                "parameters": {"red": 0, "green": 0, "blue": 255, "points": 2},
            }
        ]
    elif index == 9:
        checks = [
            {
                "id": "turn",
                "name": "Rotazione di 90 gradi",
                "type": "final_orientation",
                "parameters": {"degrees": 90, "tolerance_degrees": 4, "points": 2},
            },
            {
                "id": "stop",
                "name": "Arresto finale",
                "type": "is_stopped",
                "parameters": {"points": 1},
            },
        ]
    elif index in {11, 12, 14, 17, 18}:
        checks = [
            {
                "id": "target",
                "name": "Raggiunge il target",
                "type": "stop_in_zone",
                "parameters": {"x": 1.0, "y": 0.5, "tolerance": 0.04, "points": 3},
            },
            {
                "id": "safe",
                "name": "Nessuna collisione",
                "type": "avoid_collisions",
                "parameters": {"max_collisions": 0, "points": 1},
            },
        ]
    elif index in {19, 20}:
        checks = [
            {
                "id": "route",
                "name": "Checkpoint in ordine",
                "type": "checkpoints",
                "parameters": {
                    "checkpoints": [
                        {"x": 0.75, "y": 0.5},
                        {"x": 1.0, "y": 0.5},
                        {"x": 1.25, "y": 0.5},
                    ],
                    "tolerance": 0.04,
                    "points": 4,
                },
            },
            {
                "id": "park",
                "name": "Parcheggio finale",
                "type": "stop_in_zone",
                "parameters": {"x": 1.25, "y": 0.5, "tolerance": 0.04, "points": 3},
            },
            {
                "id": "safe",
                "name": "Nessuna collisione",
                "type": "avoid_collisions",
                "parameters": {"max_collisions": 0, "points": 2},
            },
        ]
    else:
        required = 4 if index == 15 else 3 if index == 16 else 1
        checks = [
            {
                "id": "commands",
                "name": "Comandi motore eseguiti",
                "type": "minimum_motor_commands",
                "parameters": {"count": required, "points": 2},
            },
            {
                "id": "stop",
                "name": "Arresto finale",
                "type": "is_stopped",
                "parameters": {"points": 1},
            },
        ]
    return {
        "schema_version": "romeo.scenario.v1",
        "id": f"y1-u{index:02d}-{unit.slug}",
        "world_width": 3.0,
        "world_height": 2.0,
        "start_x": 0.5,
        "start_y": 0.5,
        "start_heading_degrees": 0,
        "robot_radius": 0.1,
        "wheel_base": 0.18,
        "max_wheel_speed": 0.5,
        "obstacles": [],
        "checks": checks,
    }


def student_material(index: int, unit: Unit) -> str:
    return f"""# {index}. {unit.title}

## Obiettivo

In questo laboratorio imparerai a {unit.objective}. Le parole chiave sono: {unit.concepts}.
Lavora prima nel simulatore: puoi ripetere la prova senza rischiare il robot fisico e il clock
simulato rende ogni esecuzione confrontabile con la precedente.

## Procedura

1. Apri `starter.py` e individua import, istruzioni già presenti e commenti.
2. Prevedi su carta cosa dovrebbe accadere, compreso lo stato finale dei motori.
3. Modifica poche righe alla volta e premi Run in TheBitLab.
4. Leggi il feedback di ogni controllo; usa traiettoria ed event log se il risultato sorprende.
5. Termina sempre esplicitamente con `stop()` quando hai mosso Romeo.

## Consegna

{unit.task}

Le velocità sono numeri normalizzati: `0` significa fermo e `1` è il massimo consentito.
Valori negativi in `Robot.drive(sinistra, destra)` fanno girare una ruota all'indietro.
`sleep(secondi)` fa avanzare il tempo simulato; sul robot reale rappresenta tempo reale.

## Errori utili

- `NameError`: controlla di avere importato e scritto correttamente il nome.
- `TypeError`: verifica parentesi e tipo dell'argomento.
- Romeo non si ferma: aggiungi `stop()` e controlla il flusso del programma.
- La missione fallisce di poco: non cambiare tutto; osserva posa finale, tempo e tolleranza.

## Mini-sfida e autoverifica

Prima di eseguire, cambia un solo valore e annota la tua previsione. Poi ripristina la soluzione
della consegna. Sai spiegare quale backend riceve il comando? Sai indicare lo stato finale delle
ruote? Sapresti raccontare a un compagno perché la stessa API funziona nel simulatore e sul robot?
"""


def teacher_material(index: int, unit: Unit) -> str:
    return f"""# Guida docente — {index}. {unit.title}

Durata prevista: {unit.minutes} minuti. Difficoltà: {unit.difficulty}.

## Evidenze osservabili

Lo studente sa {unit.objective}, anticipa l'effetto delle istruzioni e interpreta almeno un
risultato del grader. La consegna è: {unit.task}

## Sequenza proposta

- 0–10 min: richiamo della lezione precedente e previsione collettiva.
- 10–20 min: dimostrazione minima nel simulatore, mostrando stato e arresto.
- 20–40 min: lavoro a coppie con ruoli pilota/osservatore, scambiati a metà.
- 40–{unit.minutes} min: verifica automatica, spiegazione orale e exit ticket.

Non fornire subito la soluzione. Chiedere prima: “quale riga cambia lo stato?”, “quale prova lo
dimostra?” e “Romeo è fermo alla fine?”. Usare gli hint in ordine e mostrare l'event log solo dopo
che lo studente ha scritto una previsione.

## Idee errate frequenti

Le chiamate non sono descrizioni ma azioni; `sleep` non ferma i motori; una velocità doppia non
garantisce precisione doppia; superare un target non equivale a raggiungerlo. Sul robot fisico il
watchdog è una rete di sicurezza, non sostituisce `stop()`.

## Inclusione e valutazione formativa

Fornire una scheda con i nomi delle funzioni e consentire di descrivere prima l'algoritmo con
frecce. Per chi procede rapidamente, richiedere una variante con una funzione nominata bene.
Raccogliere come evidenze: previsione, sorgente, esito dei check e una frase di spiegazione. Nel
debrief collegare {unit.concepts} alla prossima unità, evitando dettagli interni del backend.
"""


def activity(index: int, unit: Unit) -> dict[str, object]:
    identifier = f"romeo-y1-u{index:02d}-{unit.slug}"
    return {
        "schema_version": "1.0",
        "id": identifier,
        "title": unit.title,
        "titolo": unit.title,
        "kind": "laboratorio",
        "tipo": "laboratorio",
        "language": "python",
        "linguaggio": "python",
        "difficulty": unit.difficulty,
        "difficolta": unit.difficulty,
        "topics": [part.strip() for part in unit.concepts.split(",")],
        "argomenti": [part.strip() for part in unit.concepts.split(",")],
        "objective": unit.objective,
        "prerequisites": []
        if index == 1
        else [f"romeo-y1-u{index - 1:02d}-{UNITS[index - 2].slug}"],
        "instructions": unit.task,
        "consegna": unit.task,
        "student_support_mode": "hint-progressivi",
        "grading_policy": {"compila": True, "test": True, "sandbox": True, "ai_feedback": False},
        "correzione": {"compila": True, "test": True, "sandbox": True, "ai_feedback": False},
        "metriche": {
            "tempo_stimato_minuti": unit.minutes,
            "traccia_tempo_dichiarato": True,
            "traccia_sessioni_thebitlab": True,
            "traccia_eventi_didattici": True,
            "traccia_errori_compilazione": True,
        },
        "rubrica": [
            {"criterio": "Missione deterministica", "punti": 6},
            {"criterio": "Codice leggibile", "punti": 2},
            {"criterio": "Spiegazione e safety", "punti": 2},
        ],
        "assets": [
            {
                "type": "starter",
                "path": "starter.py",
                "target_path": "main.py",
                "visibility": "student",
                "description": "Codice iniziale",
            },
            {
                "type": "fixture",
                "path": "scenario.json",
                "visibility": "grading",
                "description": "Scenario deterministico",
            },
            {
                "type": "fixture",
                "path": "runtime-config.json",
                "visibility": "grading",
                "description": "Configurazione romeo-sim",
            },
            {
                "type": "teacher_only",
                "path": "solution.py",
                "visibility": "teacher",
                "description": "Soluzione commentata",
            },
            {
                "type": "example",
                "path": "hints.md",
                "visibility": "student",
                "description": "Hint progressivi",
            },
        ],
        "extensions": {
            "thebitlab.runtime": {
                "schema_version": "runtime_activity.v1",
                "runtime_id": "romeo-sim",
                "config": {"path": "runtime-config.json", "media_type": "application/json"},
                "required_capabilities": [
                    "headless-run",
                    "deterministic-grade",
                    "artifact-collect",
                ],
                "submission": {
                    "artifacts": [
                        {
                            "id": "main",
                            "path": "main.py",
                            "media_type": "text/x-python",
                            "required": True,
                        }
                    ]
                },
            }
        },
    }


def build() -> None:
    units_manifest = []
    curriculum_units = []
    for index, unit in enumerate(UNITS, start=1):
        unit_id = f"y1-u{index:02d}-{unit.slug}"
        base = COURSE / "activities" / unit_id
        dump(base / "activity.json", activity(index, unit))
        dump(base / "scenario.json", scenario(index, unit))
        dump(
            base / "runtime-config.json",
            {
                "schema_version": "romeo.thebitlab.v1",
                "scenario": "scenario.json",
                "submission_artifact_id": "main",
                "max_simulation_seconds": 30,
            },
        )
        write(base / "starter.py", unit.starter)
        write(base / "solution.py", unit.solution)
        write(
            base / "hints.md",
            f"# Hint progressivi\n\n1. Rileggi l'obiettivo: {unit.objective}.\n2. Controlla import, parentesi, indentazione e valori.\n3. Parti da questa idea senza copiarla interamente: `{unit.solution.splitlines()[-1]}`\n",
        )
        student = f"materials/student/{unit_id}.md"
        teacher = f"materials/teacher/{unit_id}.md"
        worksheet = f"handouts/{unit_id}-worksheet.md"
        assessment = f"handouts/{unit_id}-assessment.md"
        unit_handouts = [worksheet, assessment]
        if index == 20:
            unit_handouts.append("handouts/y1-u20-capstone-rubric.md")
        write(COURSE / student, student_material(index, unit))
        write(COURSE / teacher, teacher_material(index, unit))
        write(
            COURSE / worksheet,
            f"# Scheda operativa — {unit.title}\n\nPrevisione: ____________________\n\nComandi in ordine: ____________________\n\nStato finale atteso: ____________________\n\nEsito dei check e correzione effettuata: ____________________\n",
        )
        write(
            COURSE / assessment,
            f"# Exit ticket — {unit.title}\n\n1. Spiega con parole tue come {unit.objective}.\n2. Indica un errore che il simulatore ti ha aiutato a trovare.\n3. Cerchia: autonomo / con un hint / con guida. Motiva con un'evidenza del run.\n",
        )
        units_manifest.append(
            {
                "id": unit_id,
                "title": unit.title,
                "order": index,
                "activities": [f"activities/{unit_id}/activity.json"],
                "materials": [student, teacher],
                "handouts": unit_handouts,
            }
        )
        curriculum_units.append(
            {
                "id": unit_id,
                "year": 1,
                "order": index,
                "title": unit.title,
                "objective": unit.objective,
                "estimated_minutes": unit.minutes,
                "difficulty": unit.difficulty,
                "activity": f"activities/{unit_id}/activity.json",
            }
        )
    bundle = {
        "schema_version": "1.0.0",
        "id": "romeo-python-robotics",
        "version": "0.1.0",
        "title": "Romeo — Python e robotica",
        "school_year": "2026/2027",
        "target_class": "Primo e secondo anno della scuola secondaria di secondo grado",
        "language": "it",
        "platform_min_version": "2026.8.0",
        "authors": [{"name": "TheBitLab", "role": "author"}],
        "license": "TBD-before-public-release",
        "price": None,
        "content": {"units": units_manifest},
    }
    dump(COURSE / "bundle.json", bundle)
    dump(
        COURSE / "index.json",
        {
            "units": [
                {
                    "id": unit["id"],
                    "title": unit["title"],
                    "order": unit["order"],
                    "items": [
                        {"type": item_type, "path": path}
                        for field, item_type in (
                            ("activities", "activity"),
                            ("materials", "material"),
                            ("handouts", "handout"),
                        )
                        for path in unit.get(field, [])
                    ],
                }
                for unit in units_manifest
            ]
        },
    )
    dump(
        COURSE / "curriculum.json",
        {
            "schema_version": "romeo.curriculum.v1",
            "course_id": "romeo-python-robotics",
            "language": "it",
            "years": [
                {
                    "year": 1,
                    "focus": "Python, programmazione procedurale e robotica 2D",
                    "units": curriculum_units,
                }
            ],
        },
    )
    write(
        COURSE / "handouts" / "y1-u20-capstone-rubric.md",
        """# Rubrica capstone primo anno

| Criterio | 0 punti | 1 punto | 2 punti |
| --- | --- | --- | --- |
| Missione | Non esegue | Parziale o instabile | Tutti i check deterministici passano |
| Struttura | Codice non leggibile | Sequenza comprensibile | Funzioni piccole e nomi espliciti |
| Debug | Nessuna evidenza | Descrive un tentativo | Usa traiettoria ed eventi con metodo |
| Safety | Motori attivi alla fine | Stop presente | Stop motivato e comportamento d'errore spiegato |
| Comunicazione | Nessuna spiegazione | Spiegazione incompleta | Collega API, backend e risultato osservato |

Il grader automatico fornisce evidenze, ma la rubrica resta una valutazione docente trasparente.
""",
    )
    write(
        COURSE / "docs" / "first-year-plan.md",
        """# Piano del primo anno

Venti unità portano dalle prime chiamate Python a una missione con checkpoint. Ogni unità usa
previsione, esecuzione deterministica, lettura delle evidenze e breve riflessione. Le prime dieci
unità privilegiano l'API `romeo.easy`; dalla sesta compare gradualmente `Robot.drive` per rendere
visibile il controllo delle ruote. Il robot fisico entra solo dopo una prova sicura nel simulatore.

Con un solo Romeo fisico, le coppie ruotano tra simulazione, code review, osservazione hardware e
documentazione. Il docente conserva il controllo dell'alimentazione e verifica calibrazione e area.
""",
    )
    write(
        COURSE / "optional" / "README.md",
        "# Contenuti opzionali\n\nQuesta directory ospiterà estensioni non necessarie alla progressione principale. M12 non modifica le attività 2D stabili.\n",
    )
    write(
        COURSE / "scripts" / "README.md",
        "# Script del bundle\n\nGli script autoritativi sono nella radice del repository. `build_first_year_bundle.py` genera soltanto M10; `build_second_year_bundle.py` rigenera l'intero corso M10–M11. `validate_course.py` controlla il risultato offline.\n",
    )
    write(
        COURSE / "README.md",
        "# Course Bundle Romeo\n\nBundle TheBitLab per il biennio. I contenuti sono originali e separano materiali studente, guide docente, handout e asset di grading. Rigenera il primo anno con `python scripts/build_first_year_bundle.py` e valida con `python scripts/validate_course.py`.\n",
    )


if __name__ == "__main__":
    build()
