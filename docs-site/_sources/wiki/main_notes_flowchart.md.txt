# LiftSim Flowchart

#process-notes
This diagram illustrates how `zero_liftsim.main` orchestrates a simple, single-lift simulation. The `Simulation` engine executes queued `Event` objects. Agents arrive via `ArrivalEvent`, board using `BoardingEvent`, and the lift completes cycles through `ReturnEvent`.

```mermaid
flowchart TD
    subgraph Engine
        S0((start run))
        S0 --> S1{queue empty?}
        S1 -- no --> S2[pop earliest event]
        S2 --> S3[execute event]
        S3 --> S1
        S1 -- yes --> S4((stop))
    end

    subgraph Events
        A[ArrivalEvent] --> |enqueue agent| B{lift idle?}
        B -- yes --> C[BoardingEvent]
        C --> |load agents| D{any boarded?}
        D -- yes --> E[ReturnEvent\n+cycle_time]
        E --> |mark idle| F{queue length > 0?}
        F -- yes --> C
        F -- no --> S1
        D -- no --> S1
        B -- no --> S1
    end
```

The flow captures the interaction of core classes:
- `Simulation`: drives the event loop.
- `Lift`: holds a queue and state (`idle` or `moving`).
- `Agent`: represents a skier.
- `ArrivalEvent`, `BoardingEvent`, `ReturnEvent`: concrete `Event` subclasses defining the lift cycle.
# Git Info
Commit: c936e3318795d8493c35cb3f8299b583141a5be0
Date: 2025-06-11T08:52:59-07:00

