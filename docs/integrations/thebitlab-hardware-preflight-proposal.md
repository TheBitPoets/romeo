# Proposta futura: preflight hardware generico TheBitLab

## Problema

Per bloccare **Run on real Romeo** quando il robot non è pronto, il core
TheBitLab deve poter interrogare un health check senza conoscere Romeo. Il
contratto runtime corrente non espone questa operazione. Aggiungerla ora sarebbe
una modifica ABI e non è necessaria per usare `romeo-doctor` localmente.

## Alternative

1. **Comando esterno solo Romeo**. TheBitLab mostra istruzioni e il docente
   esegue `romeo-doctor` separatamente. Nessun impatto ABI, ma la UI non può
   bloccare automaticamente il run.
2. **Capability opzionale `device-preflight.v1`** (raccomandata). Un runtime che
   controlla hardware dichiara la capability e implementa un'operazione passiva
   che restituisce un report normalizzato. Runtime puramente software come
   Efesto non la dichiarano e non cambiano comportamento. Richiede ADR, nuova
   versione additiva del contratto, test di compatibilità e UX fail-closed.
3. **Servizio health HTTP separato**. Evita di estendere il plugin ABI, ma
   introduce discovery, autenticazione, lifecycle e deployment di un nuovo
   servizio; è sproporzionato per il primo rollout.

## Raccomandazione e impatto

Adottare in una PR TheBitLab separata l'alternativa 2 dopo decisione
architetturale. L'operazione deve essere passiva, avere timeout breve, non
contenere segreti e restituire almeno `ready`, check bloccanti e messaggio
studente. Qualunque errore o timeout deve bloccare l'esecuzione reale, senza
impedire simulazione e grading.

Efesto e gli altri runtime non richiedono implementazione: l'assenza della
capability significa “nessun device fisico gestito dal runtime”, non errore.
Romeo può adattare internamente `romeo.hardware_diagnostic.v1` al report comune.

## Decisione richiesta prima del codice core

Serve approvare nome, semantica fail-closed e versione del contratto. Nessuna
modifica ABI TheBitLab viene effettuata in questo branch Romeo.
