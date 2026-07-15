# GOV-CLI-M1 implementation plan

`implementation-plan.yaml` is the machine source of truth. The plan starts by
building aggregation and its isolated subchecks, then report parsers, coverage
and policy logic, oracle-backed fixtures, and finally the control-plane CI job.
Verification is deliberately separate: suite, matrix, dual mode, independent
coverage proof, mutation evidence, and CI canary each have their own step.
