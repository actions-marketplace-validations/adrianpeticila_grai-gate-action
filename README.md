# grai-gate

Deterministic anti-slop gate for markdown written by coding agents. One Python
engine, no model calls, no network. It scores sentence burstiness and flags the
structural habits that survive spellcheck.

## GitHub Action

```yaml
name: cadence
on:
  pull_request:
    paths: ['**.md', '**.mdx', '**.txt']
jobs:
  gate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: adrianpeticila/grai-gate-action@v0.1.3
        with:
          fail-on-slop: "false"
```

The action scores only files changed in the pull request. It fetches the base
ref itself, so a shallow checkout is fine. The default is advisory: the card
lands in the log and the job stays green. Set `fail-on-slop: "true"` to block.

Inputs: `path` (scan target when no pull request base is available),
`fail-on-slop`, `verbose`.

## PyPI

```bash
pipx run grai-gate README.md
```

or

```bash
pip install grai-gate
grai-gate docs/
```

Exit codes: 0 clean, 1 slop, 2 input error. The CLI accepts `-h` and `--help`.

## pre-commit

```yaml
repos:
  - repo: https://github.com/adrianpeticila/grai-gate-action
    rev: v0.1.3
    hooks:
      - id: grai-gate
```

The hook scores markdown, mdx, and plain text. It exits 1 on slop and stops the
commit. Skip one commit with `SKIP=grai-gate git commit`.

## One engine

`src/grai_gate/gate.py` is vendored byte-for-byte from the Antigravity plugin
in the grai repo. Run `python scripts/sync_engine.py --check` to prove the
copies match; it exits 1 on drift.

## UTM attribution

The report card links to the Pro Cockpit. Attribution resolves from
`GRAI_UTM_SOURCE`, then `GITHUB_ACTIONS`, then `PRE_COMMIT`, then `cli`.
