# uv distribution POC

## Tested paths

1. `uvx --from git+https://github.com/Jeamee/agent-governance.git@<sha>#subdirectory=cli`
   installs and runs the CLI, but does not consume the repository `uv.lock` as
   the authoritative project lock.
2. Fixed-SHA archive/checkout followed by
   `uv run --locked --project cli governance --version` consumes the project
   lock and fails closed when the lock is invalid or stale.

## China Runner verification

Gitea Actions run 886 executed the selected path against fixed commit
`57fb5532eecb8ad6b443ef6db89c32b59798a88c`:

- preloaded `linux/amd64` Python 3.12 job image;
- `pip` installed uv 0.11.2 from Aliyun;
- uv resolved and downloaded dependencies through the Tsinghua PyPI index;
- `uv lock --check` succeeded;
- `uv run --locked --python python3 --project /tmp/archive/cli governance --version`
  printed `agent-governance 0.0.1`.

The earlier PyPI-recorded lock was intentionally not accepted with the Runner's
China index. PR #3 changes `pyproject.toml` and `uv.lock` together so the lock
contains Tsinghua registry URLs. This is the required fix, not a runtime
override.

## Decision (D14)

Select **fixed SHA checkout/archive + `uv run --locked --project cli`**.
Pin uv to 0.11.2 and retain Python 3.12 in the Runner image. `uvx --from git+`
is not selected because it does not make the repository lockfile the delivery
authority.

Raw run: https://git.prodream.cn/Prodream/agent-governance-probe-gitea/actions/runs/886
