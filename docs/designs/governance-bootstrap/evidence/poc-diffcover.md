# diff-cover POC

Repository: `governance-poc-diffcover` (isolated sample repository).

## Python

`pytest --cov=python_src --cov-report=xml:coverage-python.xml` generated a
Cobertura report. `uvx diff-cover coverage-python.xml --compare-branch=HEAD~1`
reported changed-line coverage of 100% for the covered Python change.

## TSX

Vitest produced `web/coverage/cobertura-coverage.xml`. A deliberately
uncovered changed statement in `web/src/greeting.tsx` was reported by:

```text
web/src/greeting.tsx (50.0%): Missing lines 3
```

This verifies that Cobertura line numbers map back to the TSX source change;
diff-cover did not silently treat the TSX line as covered.

## Conclusion

D8 is supported for Python and TSX in the sample: use Cobertura input and
diff-cover for patch line coverage. This measures changed executable lines,
not branch coverage or behavioral adequacy.
