# M1 exit coverage baseline

The baseline data object is `coverage-baseline.json`.

- Generated from: `uv run --locked --project cli pytest cli/tests --cov governance --cov-branch --cov-report json:reports/coverage.json`
- Source commit: `c363ab63e0a90bd4f1b1fc455bd26ee173fdd9cc`
- SHA-256: `2ba89d2721ef03f101c32f4a8610cb2343ed769a52bb32b6c57118b46612d8a7`
- Line coverage: 54.50%.
- Branch coverage: 37.30%.

This is intentionally not an M1 pass threshold. It is the digest-addressed M2
input required by v4.1; M1's applicable coverage gates are patch coverage and
branch exact for the two DECISION modules.
