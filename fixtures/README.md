# Fixture convention

M1 supplies four fixture classes for every deterministic gate:

- `pass`: valid input that must pass.
- `reject`: invalid input that must fail.
- `boundary`: a boundary condition with an explicit expected result.
- `bypass`: an attempted weakening or evasion that must be classified.

No M1 fixture semantics are pre-created in M0.
