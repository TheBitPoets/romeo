# Gestire una classe con un solo Romeo fisico

Un solo robot non deve diventare il collo di bottiglia del corso. Il modello operativo è **molti simulatori, una stazione fisica condivisa**.

```text
studenti/gruppi
    -> sessioni romeo-sim personali
    -> test e grading
    -> programmi pronti
    -> coda controllata
    -> preflight
    -> Romeo reale
```

## Regole della coda fisica

Una prova sul robot entra in coda solo se:

- il programma è già stato eseguito nel simulatore;
- il comportamento richiesto è stato verificato;
- il report non contiene blocker;
- il gruppo sa spiegare che cosa si aspetta di osservare;
- il robot ha preflight valido;
- il docente autorizza la sessione.

## Mentre un gruppo usa il robot

Gli altri continuano a lavorare. Possono:

- correggere Activity precedenti;
- confrontare traiettorie;
- completare challenge opzionali;
- preparare una previsione quantitativa del comportamento reale;
- analizzare la differenza fra simulazione e prova fisica di un altro gruppo.

## Durata delle sessioni

Preferisci sessioni corte e ripetibili. Una prova fisica non è il momento per fare debug di errori Python banali: quelli devono emergere prima nel simulatore.

## Evidenza utile

Per ogni prova interessante conserva almeno:

- Activity;
- versione del programma;
- risultato simulato;
- esito preflight;
- osservazione fisica;
- eventuale deviazione/calibrazione.

Questi dati possono diventare materiale per discutere modello ideale, rumore, attrito e tolleranze.

## Safety

Il docente mantiene il controllo della disponibilità del robot reale. La presenza di un pulsante o comando tecnico per il run non sostituisce l'autorizzazione della sessione e le regole dell'aula.
