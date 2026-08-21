# Strategia di test

I test di Romeo hanno scopi diversi. Un numero totale elevato non sostituisce la copertura del **percorso reale** che vuoi proteggere.

## Test unitari

Usali per semantica di `Robot`, clamp, safety, parser, scenario, grader e funzioni pure. Devono essere veloci e non richiedere hardware.

## Fake/mock

Servono per provare casi di errore e safety senza CRICKIT o camera. Una nuova diagnostica hardware deve essere progettata in modo che quasi tutta la logica possa essere esercitata con fake.

## Test comportamentali del corso

Per le unità del secondo anno lo starter deve fallire il contratto che lo studente deve completare e la soluzione docente deve passarlo. Non usare marker stdout come prova principale di una competenza che può essere verificata sul comportamento.

## Test cross-contract TheBitLab

Quando tocchi integrazione runtime, attraversa almeno:

```text
prepare_sandbox
 -> broker envelope
 -> worker entrypoint
 -> sandbox result
 -> finalize_sandbox
```

I test isolati di `execute_*` non sostituiscono l'entry point reale.

## Docker smoke

Qualsiasi modifica a worker/Dockerfile/lock deve costruire l'immagine reale e usare l'ENTRYPOINT di produzione con gli stessi vincoli rilevanti del broker.

## Hardware test

I test che richiedono Raspberry Pi, CRICKIT, servo o camera devono essere marcati `hardware`. Non devono trasformare una CI cloud in un falso indicatore di collaudo fisico.

## Documentazione

Sphinx viene costruito con `-W`: link interni, toctree e autodoc devono restare coerenti. Gli esempi e il catalogo generato del corso fanno parte del contratto documentale.

## Gate prima di una PR

```console
python -m ruff check .
python -m mypy src
python scripts/validate_course.py
python -m pytest
python scripts/generate_course_docs.py
python -m sphinx -W --keep-going -b html docs docs/_build/html
```

Se modifichi il runtime runner, aggiungi anche il Docker smoke appropriato.
