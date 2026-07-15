# agent-governance

Central, public governance tooling for AI-assisted software delivery.

This repository contains only reusable methodology, schemas, a CLI, thin
platform adapters, templates, fixtures, and documentation. Business-task
instances stay in the protected paths of their owning repositories.

`docs/designs/governance-bootstrap/` is the one documented bootstrap
exception: it is this repository's own M0 governance instance.

## Bootstrap status

M0 is being delivered on the `bootstrap/m0` branch. The `main` branch must be
made the default branch and protected by a human repository administrator
before M0 can pass its Proof Gate.
Central governance tooling and immutable design templates for AI delivery
