# GOV-CLI-M1 business design

## Known / Unknown

| Category | Conclusion |
|---|---|
| Known | M0 validates only bootstrap schemas. M1 must provide a deterministic `governance verify` CLI with eight fail-closed subchecks. |
| Known | The protected authorization record selects schema v1 or v2; worker-writable data never selects a validator. |
| Known | A valid M1 result is an observable JSON result plus reports produced in the current run. |
| Unknown | M2 platform coverage baseline and the first Gitea production repository are intentionally out of M1 scope. |

## Business facts and user flow

1. A repository owner freezes a design package and authorization on protected main.
2. A delivery worker supplies a delivery request, an explicit diff base and a fresh report directory.
3. `governance verify --mode local|ci` evaluates the same deterministic input through schema, authorization, frozen, acceptance, plan, coverage, effectiveness, and policy checks.
4. The CLI returns a machine-readable conclusion. A missing prerequisite fails; a platform-only prerequisite is `unverifiable` locally and fails in CI.
5. The fixture runner evaluates the frozen 8×4 oracle matrix. It does not accept worker-created fixture semantics.

## Acceptance six-tuples

| ID | Preconditions | Action | Expected | Forbidden |
|---|---|---|---|---|
| ACC-CLI-001 | Same deterministic files and reports | Run local and CI modes | Deterministic checks have identical conclusions; CI turns `unverifiable` into failure | Local unverifiable is silently pass in CI |
| ACC-SCHEMA-001 | Invalid manifest | Run schema subcheck | Invalid structure is rejected | Invalid structure is accepted |
| ACC-AUTH-001 | Delivery and authorization differ | Run authorization subcheck | Failure names mismatch | Delivery controls authorization |
| ACC-AUTH-002 | Authorization exists only in delivery diff | Run authorization subcheck | Failure | Self-authorized delivery passes |
| ACC-AUTH-003 | Protected revocation targets authorization | Run authorization subcheck | New delivery fails | Revoked authorization is accepted |
| ACC-AUTH-004 | Revocation boundary variants | Run authorization subcheck | All five fail-closed boundaries hold | A replacement or same-PR record silently changes authority |
| ACC-ACC-001 | A required report is absent | Run acceptance subcheck | Failure includes missing ID, source and reproduction command | Missing verifier passes |
| ACC-ACC-002 | Report is missing, truncated, or lacks a shard | Run acceptance subcheck | Failure | Empty report passes |
| ACC-ACC-003 | Playwright result retried | Run acceptance subcheck | Attempts are retained | Retry history disappears |
| ACC-ACC-004 | High-risk verifier has insufficient instances | Run acceptance subcheck | Failure | Partial parameterization passes |
| ACC-PLAN-001 | Slot or profile differs from plan | Run plan subcheck | Failure | Undeclared report is accepted |
| ACC-IPL-001 | References or DAG are malformed | Run schema subcheck | Failure | Broken closure passes |
| ACC-IPL-002 | Frozen plan file is changed | Run frozen subcheck | Failure | Plan baseline is rewritten in delivery |
| ACC-IPL-003 | Diff path is unplanned and undeclared | Run plan subcheck | Failure | Unmapped path passes |
| ACC-IPL-004 | DEV record lacks required conditional data | Run schema subcheck | Failure | Free-form deviation passes |
| ACC-IPL-005 | Completion references a missing verifier artifact | Run schema subcheck | Failure | Unknown command, scene, or rubric passes |
| ACC-IPL-006 | Derived path has no causal source | Run schema subcheck | Failure | Derived declaration launders arbitrary files |
| ACC-IPL-007 | Prefix target is not bound to a module | Run schema subcheck | Failure | Generic source root is accepted |
| ACC-IPL-008 | DEV needs review | Run verify | Final status is `needs_review` | Automatic pass |
| ACC-FRZ-001 | Frozen design file changes | Run frozen subcheck | Failure | Frozen diff passes |
| ACC-FRZ-002 | Diff base is unreachable | Run frozen subcheck | Failure | Empty diff is assumed |
| ACC-FRZ-003 | Design digest differs | Run frozen subcheck | Failure | Mismatched frozen source passes |
| ACC-FRZ-004 | Oracle changes, is omitted, unordered, or path-aliased | Run frozen subcheck | Failure | Oracle semantics can be changed by delivery |
| ACC-COV-001 | Coverage report misses threshold or branches | Run coverage subcheck | Failure | Missing or insufficient coverage passes |
| ACC-EFF-001 | Bugfix has no base-fail/head-pass proof | Run effectiveness subcheck | Failure | Bugfix lacks regression proof |
| ACC-POL-001 | Protected path changes without valid exception | Run policy subcheck | Failure | Protected mutation passes |
| ACC-POL-002 | Warning heuristic fixture is classified | Run policy subcheck | Declared warning classification | Heuristic is omitted or misclassified |
| ACC-POL-003 | Exception lifecycle variants | Run policy subcheck | Only valid scoped exception permits its diff | Expired/revoked/wrong exception passes |
| ACC-ATT-001 | Historical report exists | Run acceptance subcheck | Failure unless current run produced report | Historical artifact is trusted |
| ACC-M1-ORACLE-001 | Fixture set is incomplete | Run fixture meta-test | Failure identifies missing matrix cell | Partial matrix runs |
| ACC-M1-SCHEMAVER-001 | M0 v1, v2, wrong validator, downgrade attack | Run schema checks | Authority selects version and downgrade fails | Worker selects relaxed version |

## State transitions

| From | Trigger | To | Failure rule |
|---|---|---|---|
| prepared | reports and authorization supplied | verifying | Missing required input is fail |
| verifying | all subchecks pass | pass | — |
| verifying | any deterministic check fails | fail | Stop with all collected subcheck results |
| verifying | local-only platform prerequisite | unverifiable | CI maps this state to fail |
| verifying | DEV requires review | needs_review | Do not auto-pass |

## Closed D decisions

| D | Decision |
|---|---|
| D20 | Independent branch proof executes a blob read from `authorization.design_ref.commit`, never PR head. |
| D24/D33 | Authorization is the version authority; v1 default applies only when that protected authorization has no version. |
| D26 | The 8×4 oracle is frozen and digest-covered. |
| D27 | Reports are bound to an empty per-run directory. |
| D28 | Revocations are append-only and block new delivery only. |
| D30 | The implementation goal has standing user authorization for PR creation, merging, CI canaries, and technical Proof Gate operations. |
| D31 | `coverage_base_commit` is captured when the M1 authorization PR is created; M1 creates the M2 baseline evidence without rewriting this plan. |
