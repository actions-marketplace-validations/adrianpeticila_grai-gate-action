#!/usr/bin/env python3
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SLOP = (
    "Here is why we ship fast. It is not marketing, it is positioning. "
    "One two three four. Five six seven eight.\n"
)
CLEAN = (
    "Buy it now.\n\n"
    "Post blur hits the moment five tools write with one template voice, so I cut the draft "
    "to one sentence and watched the room lean in.\n\n"
    "Ship smaller.\n"
)


def run(args, stdin_text=None, env=None):
    child = os.environ.copy()
    for key in ("GRAI_UTM_SOURCE", "GITHUB_ACTIONS", "PRE_COMMIT"):
        child.pop(key, None)
    if env:
        child.update(env)
    child["PYTHONPATH"] = str(ROOT / "src")
    return subprocess.run(
        [sys.executable, "-m", "grai_gate.cli"] + list(args),
        input=stdin_text,
        capture_output=True,
        text=True,
        cwd=str(ROOT),
        env=child,
    )


def main():
    proc = run(["--help"])
    assert proc.returncode == 0, proc.stderr
    assert "Usage:" in proc.stdout
    assert "grai-gate FILE" in proc.stdout

    with tempfile.TemporaryDirectory() as directory:
        slop = Path(directory) / "slop.md"
        slop.write_text(SLOP, encoding="utf-8")

        proc = run([str(slop)])
        assert proc.returncode == 1, proc.stdout + proc.stderr
        assert "Slop Score" in proc.stdout
        assert "utm_source=pypi" in proc.stdout

        proc = run([str(slop)], env={"PRE_COMMIT": "1"})
        assert proc.returncode == 1, proc.stdout + proc.stderr
        assert "utm_source=precommit" in proc.stdout

        proc = run([str(slop)], env={"GITHUB_ACTIONS": "true"})
        assert proc.returncode == 1, proc.stdout + proc.stderr
        assert "utm_source=github-action" in proc.stdout

        proc = run([str(slop)], env={"GRAI_UTM_SOURCE": "cli", "GITHUB_ACTIONS": "true"})
        assert proc.returncode == 1, proc.stdout + proc.stderr
        assert "utm_source=cli" in proc.stdout

        clean = Path(directory) / "clean.md"
        clean.write_text(CLEAN, encoding="utf-8")
        proc = run([str(clean)])
        assert proc.returncode == 0, proc.stdout + proc.stderr
        assert proc.stdout == ""

    print("smoke checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
