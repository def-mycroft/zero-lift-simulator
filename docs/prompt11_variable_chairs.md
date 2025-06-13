prompt11 - variable chair count

random codname:

```copy
gullible-currency 1b824579
```

***

# Prompt for Codex prompt11 – Extend Lift with Chairs

The current `Lift` class only models loading `capacity` riders at a time and does
not track how many chairs are circulating. We want to upgrade this so a lift can
simulate an arbitrary number of rotating chairs (e.g., 50–100). Each chair has
`capacity` seats and may be simultaneously in transit.

## Requirements

- Add a `num_chairs: int` argument to `Lift.__init__`. Keep `capacity` as seats
  per chair.
- Track how many chairs are currently available at the base versus in use
  (riding up or traversing down). Loading should only occur when at least one
  chair is available.
- When a chair is loaded:
  - Dequeue up to `capacity` riders and mark them as boarded.
  - Mark that chair as occupied and schedule its return after the ride and
    traverse durations.
- When all riders on a chair have completed the cycle, mark that chair
  available again. The lift should allow multiple chairs to be in motion at the
  same time.
- Provide helpers such as `available_chairs()`, `total_chairs()`, and
  `riders_in_transit()` for introspection.
- Update any event classes that depend on `Lift` so the simulation correctly
  handles multiple chairs returning independently.
- Document new parameters and behavior. Add unit tests to verify chairs cycle
  properly and loading stops once all chairs are occupied.

## Guidelines

- Maintain the existing code style and docstring format.
- Follow `docs/best_practices_coding_with_codex.md`.
- Run `python -m pytest` before committing.

# Git Info
Commit: 9dbd3bbaf41f2ffe006e5d16b15ef8383a0d9b55
Date: 2025-06-13T00:35:24+00:00
