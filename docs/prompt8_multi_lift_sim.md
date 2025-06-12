# Prompt for Codex: Implement Multi-Lift Setup stimulating-divide 3437c905

random codename: stimulating-divide 3437c905

*** 


You're working in the `zero-lift-simulator` codebase to implement a **Multi-Lift Simulation Prototype** that models a fixed two-lift network with agent routing between them. The goal is to evolve LiftSim from a single-lift simulation into a minimal-but-functional **lift network simulator**, enabling the system to demonstrate network-level congestion and throughput dynamics.

This is an **intermediate prototype**, not a full generalization. Focus on concrete functionality and hardcoded configuration to minimize scope. You're building the smallest complete version of a multi-lift world, with two lifts and agents moving between them in a fixed pattern. This unlocks the ability to observe **system-wide bottlenecks** and sets up future extensibility.

### Update Scope

* Modify the simulation engine so that it can model **two lifts**, `L1` and `L2`, with agents routed from `L1` to `L2` after completing a full ride-cycle on each.
* Hardcode the route: all agents begin at `L1`, ride it, descend (fixed delay), queue for `L2`, ride it, descend (fixed delay), and repeat.
* Extend the `Agent` class to track which lift the agent is headed to next (`.next_lift_id` or similar).
* Extend the event system (`Event`, `BoardingEvent`, etc.) so each event is scoped to a specific lift (e.g., include a `lift_id`).
* Add support in the simulation loop to instantiate and manage **two `Lift` objects**, each with their own queue, capacity, and cycle time.
* Lifts should operate independently but **share the agent pool**, meaning agents move from one queue to the next in a cyclical flow.
* Log all events with lift ID and timestamp so we can later analyze where bottlenecks formed.
* Extend the output summary (or optionally, the test suite) to track KPIs **per-lift** (e.g., average wait time on `L1` vs `L2`, throughput, utilization).

### Constraints

* Hardcode the two-lift structure in a single simulation config (no CLI or YAML configs yet).
* Assume each descent from lift takes a fixed simulated duration (e.g., 2 minutes).
* Reuse the existing architecture where possible, but make pragmatic structural changes if needed to support multiple lifts cleanly.
* Avoid dynamic lift creation or graph traversal logic – this version is fixed-structure, not general-purpose.

### Goals

* After this change, LiftSim should simulate N agents rotating between two lifts.
* The system should support analysis of **where the bottleneck is** (e.g., if L1 is slow, queue grows there; if L2 is slow, agents back up downstream).
* This version lays the groundwork for future generalization into a graph of lift nodes and skier preferences.

### Implementation Notes

* Use clear identifiers like `"L1"` and `"L2"` for lifts, and maintain a mapping in the simulation loop.
* Consider whether `Agent` needs a `.history` log or `.lift_sequence` list, or just a `.next_lift` field (keep simple for now).
* Make sure tests still run (some test mocks may assume only one lift).

When you're ready, implement this update and ensure the logs show time-stamped, per-lift event flow. You may use hardcoded arrival times or uniform stochastic arrival for agents.


