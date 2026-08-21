# Grading e feedback per il docente

Romeo separa il feedback formativo dall'esecuzione autorevole di codice non fidato.

## Tre livelli da non confondere

### Simulazione e feedback formativo

Serve allo studente per iterare rapidamente. È il posto in cui traiettoria, eventi e test pubblici aiutano a capire il problema.

### Grading runtime autorevole

Per le Activity che richiedono il runtime Romeo, TheBitLab usa il broker sandbox quando il plugin dichiara `sandbox-plan.v1`. Il codice studente viene eseguito nel boundary previsto e il risultato tecnico viene finalizzato lato trusted.

Un report autorevole deve essere riconoscibile dai metadata dell'esecuzione, per esempio backend effettivo Docker e `authoritative=true`.

### Valutazione didattica del docente

Il punteggio automatico non sostituisce ogni dimensione della rubrica. Qualità della spiegazione, metodo, capacità di descrivere gli errori e lavoro di gruppo possono richiedere osservazione docente.

## Command trace e behavioral tests

Nel primo anno molte missioni possono essere valutate riproducendo in modo trusted una command trace sul simulation engine. Nel secondo anno, per socket/API/eventi, i test comportamentali verificano funzioni importabili e comportamento effettivo invece di affidarsi a marker stdout.

## Hidden non significa segreto crittografico

Un test eseguito nello stesso container del codice studente non deve contenere credenziali o informazioni sensibili. L'autorevolezza deriva dal boundary e dalla finalizzazione trusted, non dal presupposto che Python ostile non possa ispezionare file montati nel proprio container.

## Prima di assegnare una Activity

Verifica sempre due casi:

1. lo starter deve fallire almeno l'obiettivo che lo studente deve implementare;
2. la soluzione docente deve passare.

Se starter e soluzione producono lo stesso esito, il contratto didattico o il grader meritano revisione.

## Leggere i risultati di classe

Distingui:

- errore concettuale diffuso;
- prerequisito mancante;
- grader troppo rigido;
- consegna ambigua;
- problema di runtime/infrastruttura.

Non correggere un problema di infrastruttura abbassando la difficoltà dell'Activity e non correggere una consegna ambigua rendendo il grader meno significativo.
