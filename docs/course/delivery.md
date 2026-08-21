# Course Delivery Dashboard

Romeo applica il **Course Delivery Standard v1** riusando il portale e i manuali già esistenti, senza duplicare il Course Bundle.

## Punti di ingresso

I materiali del delivery layer che vivono fuori dal source tree Sphinx sono collegati come sorgenti GitHub; i manuali sotto `docs/` restano pagine native del portale.

- [Dashboard completo nel repository](https://github.com/TheBitPoets/romeo/blob/main/course/delivery/README.md)
- [Indice slide docente](https://github.com/TheBitPoets/romeo/blob/main/slides/romeo/README.md)
- [Delivery Change Log](https://github.com/TheBitPoets/romeo/blob/main/course/delivery/DELIVERY_CHANGELOG.md)
- [Manuale studente](../student/index.md)
- [Manuale docente](../teacher/index.md)
- [Operations](../operations/index.md)

## Struttura delle slide

I 43 content item/Activity restano nel Course Bundle. Le slide sono organizzate in **10 macro-deck** per raccontare il percorso senza copiare una presentazione per ogni singola unità:

- corso e workflow;
- quattro blocchi del primo anno;
- quattro blocchi del secondo anno;
- transizione simulatore → robot reale.

## Policy di aggiornamento

Slide, chiarimenti, setup e troubleshooting possono evolvere durante l'anno e vengono registrati nel Delivery Change Log.

Le modifiche a unità, grading contract, runtime, safety behavior o hardware non sono semplici revisioni di delivery e devono seguire la review tecnica/curricolare appropriata.

```{admonition} Romeo Doctor e versione installata
:class: warning
`romeo-doctor` è una capability opzionale di preflight/commissioning. Non assumerne la disponibilità dalla sola documentazione: verificare lo SHA/versione realmente installato. Se il comando è presente e validato in quella versione, può automatizzare i check passivi previsti; altrimenti restano autorevoli le checklist hardware. In ogni caso il doctor non sostituisce il commissioning supervisionato per verso motori, movimento fisico, calibrazione e altre osservazioni che richiedono feedback umano.
```