#!/usr/bin/env python3
"""Vendor the shared grai-gate engine into the Python package.

The Antigravity plugin in the grai repo is the editable source. This package
keeps a byte-identical copy so PyPI, the Action, and pre-commit all run the
same engine. --check fails when the copies drift.
"""

import argparse
import hashlib
import os
import pathlib
import shutil
import sys

HERE = pathlib.Path(__file__).resolve().parent
TARGET = HERE.parent / "src" / "grai_gate" / "gate.py"
DEFAULT_SOURCE = HERE.parent.parent / "grai" / "plugin" / "grai-gate" / "scripts" / "gate.py"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description="Vendor the grai-gate engine into the package.")
    parser.add_argument(
        "--source",
        default=os.environ.get("GRAI_ENGINE_SOURCE", str(DEFAULT_SOURCE)),
    )
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    source = pathlib.Path(args.source).resolve()
    if not source.is_file():
        print("engine source not found: %s" % source, file=sys.stderr)
        return 2

    if args.check:
        if digest(source) != digest(TARGET):
            print("engine drift: %s and %s differ" % (source, TARGET), file=sys.stderr)
            return 1
        print("engine copies match")
        return 0

    shutil.copyfile(source, TARGET)
    print("vendored %s -> %s" % (source, TARGET))
    return 0


if __name__ == "__main__":
    sys.exit(main())
