# Metodologia didattica

Romeo usa un ciclo **spiega poco → prova subito → osserva → correggi → verbalizza**. Il robot è un mezzo per rendere visibili concetti di programmazione e sistemi, non un premio alla fine della teoria.

## Progressione del primo anno

Il primo anno riduce il carico cognitivo:

1. istruzioni e primi comandi;
2. LED e feedback immediato;
3. motori e velocità;
4. sequenze temporali;
5. funzioni;
6. condizioni;
7. `for` e `while`;
8. simulazione, coordinate e missioni;
9. capstone.

L'API `romeo.easy` evita di introdurre classi, driver e networking quando lo studente sta ancora imparando chiamate di funzione e sequenze.

## Progressione del secondo anno

Il secondo anno usa Romeo come sistema distribuito concreto:

```text
host -> IP -> porta -> socket -> protocollo -> JSON -> HTTP/REST
     -> FastAPI -> WebSocket -> controller -> camera -> eventi -> gamepad
```

Ogni nuovo livello riusa quello precedente e collega una nozione di rete a un comportamento osservabile del robot.

## Simulatore come laboratorio principale

Ogni studente/gruppo può avere una sessione simulata. Questo rende possibile:

- ripetere gli esperimenti;
- ricevere grading deterministico;
- provare senza attendere il robot fisico;
- distinguere errori logici da errori hardware.

Il robot reale entra dopo come validazione del modello e occasione per discutere calibrazione, attrito, alimentazione e sensori.

## Errori come materiale didattico

Il report non serve soltanto a dire "passato/fallito". Gli errori ricorrenti diventano esempi di lezione: sintassi, sequenza, tempo, stato finale, rete, protocollo, safety.

## Attività graduate

Ogni unità dovrebbe avere almeno:

- modello mentale;
- esempio minimo;
- prova guidata;
- esercizio base;
- esercizio intermedio;
- eventuale mini-sfida;
- errori tipici;
- autoverifica.

Il catalogo Sphinx descrive le unità; il materiale operativo completo resta nel Course Bundle.

## Dal fare allo spiegare

Una soluzione non è completa se lo studente non sa descrivere che cosa si aspettava e perché. Nei capstone la rubrica può quindi combinare comportamento automatico e spiegazione/metodo osservati dal docente.
