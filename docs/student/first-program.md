# Il primo programma Romeo

Questa pagina accompagna il primo programma senza dare per scontato che tu conosca già Python.

## Obiettivo

Fare una cosa semplice e verificabile: muovere Romeo, aspettare un momento e fermarlo.

```{literalinclude} ../../examples/first_move.py
:language: python
:linenos:
```

Questo non è uno snippet copiato nella documentazione: è un vero file del repository e la suite di test lo esegue sul backend mock. Se l'esempio smette di funzionare, la CI deve segnalarlo.

## Leggiamolo una riga alla volta

`from time import sleep` rende disponibile la funzione `sleep`, che sospende il programma per il numero di secondi indicato.

`from romeo.easy import forward, stop` importa due comandi pensati per chi sta iniziando: `forward` fa avanzare Romeo, `stop` porta i motori a zero.

`forward(0.3)` chiede una velocità moderata. Nel corso i valori di velocità sono normalizzati: `0` significa fermo e valori più vicini a `1` indicano una richiesta più alta. Sul robot reale il docente può applicare un limite più conservativo.

`sleep(1)` lascia attivo il comando per circa un secondo.

`stop()` conclude la sequenza in sicurezza.

## Nel simulatore

Nel lavoro normale non si parte dal robot fisico. Esegui prima la consegna in TheBitLab e osserva:

- il verso del movimento;
- la durata;
- la traiettoria;
- lo stato finale;
- il report dei test.

Se il programma non termina con Romeo fermo, correggilo prima di pensare al robot reale.

## Errori utili

Se compare `NameError`, controlla il nome della funzione. Se compare `SyntaxError`, guarda la riga indicata e verifica parentesi e punteggiatura. Se Romeo non si muove come previsto ma il programma parte, confronta il tuo codice con la consegna e con la traiettoria del simulatore.

## Prova tu

Modifica un solo elemento alla volta: cambia `0.3`, poi la durata, poi prova `backward`. Dopo ogni modifica salva, esegui di nuovo e descrivi che cosa è cambiato.

```{admonition} Regola di laboratorio
:class: important
Sul robot fisico non aumentare la velocità per "vedere meglio" un problema. Prima usa il preflight/commissioning previsto dal docente e verifica la causa.
```
