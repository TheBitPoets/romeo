# Operazioni e deployment

Questa sezione è destinata a chi prepara un'installazione TheBitLab capace di eseguire le Activity Romeo in modo riproducibile e verificabile.

```{toctree}
:maxdepth: 2

deployment-inventory
install-thebitlab-plugin
verify-installation
upgrade-rollback
coding-agent-handoff
```

## Regola architetturale

Il runtime Romeo resta un package esterno scoperto tramite entry point `thebitlab.runtimes`: TheBitLab non deve hardcodare Romeo nel core.

## Regola di sicurezza

Package Python trusted e immagine sandbox OCI sono artefatti distinti. Il grading autorevole usa un digest immutabile e deve fallire chiuso quando il boundary richiesto non è disponibile.
