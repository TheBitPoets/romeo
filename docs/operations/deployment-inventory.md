# Inventario del deployment reale

Prima di installare Romeo, ricostruisci **come gira davvero TheBitLab**. Questa pagina è un modello di raccolta dati, non una prescrizione di topologia.

## Informazioni da registrare

Compila almeno:

| Voce | Valore osservato |
|---|---|
| sistema operativo | |
| architettura CPU | |
| hostname/nodo | |
| Python | |
| interprete usato da TheBitLab | |
| virtualenv/venv | |
| utente del servizio | |
| path applicazione | |
| avvio | systemd / container / shell / altro |
| Docker engine | |
| accesso al daemon | |
| posizione config persistente | |
| nodo student runtime | |
| nodo grading/broker | |
| meccanismo update | |
| meccanismo rollback | |

Non inserire password, token, cookie o chiavi.

## Perché conta l'interprete Python

TheBitLab scopre i runtime tramite entry point Python. Installare `thebitlab-romeo` in un interprete diverso da quello usato dal servizio produce una situazione ingannevole: `pip` può dire "installato", mentre il processo reale non vede `romeo-sim`.

Verifica sempre il Python effettivo del servizio e usa quello per `list` e `probe`.

## Environment persistente

`ROMEO_SANDBOX_IMAGE` deve essere visibile al processo reale. Un `export` nella shell di amministrazione non configura automaticamente systemd, Docker Compose, Kubernetes o altri supervisor.

Documenta **dove** viene conservato il valore e come il processo viene ricaricato.

## Artefatti distinti

Conserva separatamente:

- versione/SHA del package Python Romeo;
- SHA TheBitLab;
- digest OCI immutabile del runtime worker.

Questi tre identificatori permettono di riprodurre e diagnosticare una sessione senza affidarsi a tag mobili o allo stato corrente di un checkout.
