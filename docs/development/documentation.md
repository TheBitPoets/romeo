# Sviluppare la documentazione

La documentazione Romeo è parte del prodotto e viene validata dalla CI.

## Stack

- Sphinx come motore;
- MyST per usare Markdown come sorgente nativa;
- `autodoc`/`autosummary` per la reference Python;
- Furo come tema HTML;
- `-W` per trasformare i warning in failure.

## Ambiente

```console
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
python -m pip install -e ".[web,docs]"
```

Su Windows attiva invece `.venv\Scripts\Activate.ps1`.

## Catalogo del corso

Le pagine delle unità non vanno duplicate manualmente. Generale da `course/curriculum.json` e dagli `activity.json`:

```console
python scripts/generate_course_docs.py
```

Poi costruisci il sito:

```console
python -m sphinx -W --keep-going -b html docs docs/_build/html
```

## Dove scrivere

Scrivi la spiegazione nel percorso del pubblico che la usa:

- `docs/student/` per uso quotidiano dello studente;
- `docs/teacher/` per conduzione della classe;
- `docs/operations/` per installazione/deployment;
- `docs/development/` per chi modifica il software;
- `docs/authoring/` per chi crea Activity e scenari;
- cartelle tecniche esistenti per architettura, safety e release.

## Evitare duplicazioni

Una regola deve avere una fonte autorevole e gli altri documenti devono collegarla. Per esempio il threat model resta nella sezione security; la guida docente lo riassume senza copiarlo integralmente.

## Esempi di codice

Quando un esempio è importante e riutilizzabile, preferisci un file reale sotto `examples/` e includilo nella documentazione. In questo modo può essere almeno compilato/testato dalla CI e non diventa un frammento dimenticato.

## Modifiche API

Se cambi una funzione pubblica, controlla sia autodoc sia le guide narrative. La firma generata può essere corretta mentre un tutorial continua a insegnare il vecchio comportamento.
