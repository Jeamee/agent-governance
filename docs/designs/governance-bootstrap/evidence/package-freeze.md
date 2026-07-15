# Frozen package import evidence

## Immutable import

The frozen governance package was introduced by commit
`6e38a3f65bae65a65863cf9670410ff6f6c8091d` (`Merge pull request #1 from
Jeamee/bootstrap/m0`). The bootstrap authorization record subsequently pins
that commit as both `design_ref.commit` and `gate_ref.commit`.

The nine bootstrap files were compared byte-for-byte with
`~/.agents/governance-build/bootstrap/`; all comparisons returned no output
from `diff -q`. The design package itself also matches its frozen source.

| Frozen file | SHA-256 |
| --- | --- |
| `design-package-v1.1.md` | `2c5e18b403cc61fd38ea8e175e1bedfe35780e33ff8430af96c2e844087e57e1` |
| `business-design.md` | `93a5077395e34211bad4505847540be004e8f04040867ef5b443e257d80f4d12` |
| `architecture-design.md` | `0814635d90b297ee13477bc1dbc500eb322d927741fdab83020c4f0ee1e033b8` |
| `modules.yaml` | `e18dcca53ace697570fa252c859990033b52a2afdbcc28c5b673b5d50a75edd9` |
| `requirements.yaml` | `0b09ab7d06bf3fe2b3cbdabcdbc0df92c79b25ae5ae3a633ae4a8bc5988efe28` |
| `verification-plan.yaml` | `0937288b07c349f50fa6cc0847b9faec893c0c071b68e2176addf80f7bd95b01` |
| `evidence-scenes.yaml` | `c3789d897b8af63af3cdd57afb91bb60cb512318d8e175188f6b00ee2bb14201` |
| `implementation-plan.yaml` | `acfc005c914d59a795cc6efe82b1b5a90cbf657f9d50f2feb4f7d25cb74f88d9` |
| `implementation-plan.md` | `af95a1432000726748215a933d92880e8db0e7b2d86a328bb22d5723c9c61755` |
| `rollout.md` | `9f914bf428c043411b3f3a4db5c8974c7a85342a14e972366b1b03eb320b48f7` |

## Authorization binding

`.governance/authorizations/GOV-BOOTSTRAP-M0.yaml` records
`design_ref.digest=f6ceea941823792cfde27ab6a0cd73316645a3b9791d2c0cf7a75915e2a3fb4b`
and implementation-plan digest
`90db55b41efd8eb14d2e1f37bb0081dcb9625dc20549467e705b49c81ce950c7`.
The authorization was merged by commit
`5e4a363fe52dfa6f9bc6517f14ee65c443ceea77`.

No frozen-file deviation is declared.
