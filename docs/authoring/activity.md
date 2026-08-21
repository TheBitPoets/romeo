# Creare una Activity

Le Activity Romeo seguono il contratto TheBitLab già usato dal Course Bundle. Parti da un'unità simile a quella che vuoi creare e modifica il minimo necessario.

## Metadati essenziali

Esempio ridotto:

```json
{
  "schema_version": "1.0",
  "id": "romeo-y1-uXX-esempio",
  "title": "Titolo",
  "kind": "laboratorio",
  "language": "python",
  "difficulty": "B",
  "topics": ["python", "robotica"],
  "objective": "comportamento osservabile che lo studente deve ottenere",
  "prerequisites": ["..."],
  "instructions": "Consegna breve e verificabile",
  "student_support_mode": "hint-progressivi"
}
```

Il repository mantiene per compatibilità anche alcuni alias italiani. Usa i generatori/validatori esistenti per non creare divergenze fra campi equivalenti.

## Runtime Romeo

Una Activity simulata usa `extensions.thebitlab.runtime` con `runtime_id: romeo-sim` e dichiara gli artifact della submission. Le capability richieste devono essere realmente necessarie alla lezione.

Non aggiungere comandi eseguibili, URL o path arbitrari forniti dallo studente nel contratto runtime: la scelta dell'esecuzione appartiene al plugin installato e al broker.

## Starter

Lo starter deve:

- essere piccolo;
- contenere solo concetti già introdotti;
- indicare chiaramente il punto da completare;
- fallire almeno il test che rappresenta il nuovo obiettivo.

Non trasformarlo in una soluzione quasi completa solo per ridurre i fallimenti iniziali.

## Soluzione docente

La soluzione è una fixture di qualità. Deve passare tutti i controlli previsti e rimanere leggibile: serve anche per capire se il grader misura davvero ciò che dichiara la consegna.

## Asset e visibilità

Distingui almeno:

- `student`: distribuito allo studente;
- `grading`: usato dal grading/runtime;
- `teacher`: soluzione/materiale riservato al flusso docente.

Il catalogo Sphinx pubblico mostra solo metadati e asset studente, non incorpora soluzioni o hidden test.

## Checklist prima della PR

- obiettivo singolo e osservabile;
- prerequisiti coerenti;
- tempo realistico;
- difficoltà coerente con le unità vicine;
- starter fallisce;
- soluzione passa;
- scenario valido;
- Activity valida;
- hint non rivela direttamente la soluzione;
- documentazione del concetto presente;
- `python scripts/validate_course.py` verde.
