"""Console entry point for the grai-gate package.

The engine accepts -h. This wrapper also accepts --help so the installed
command behaves like a standard CLI without changing the shared engine.
"""

import sys

from . import gate


def main():
    argv = ["-h" if arg == "--help" else arg for arg in sys.argv[1:]]
    previous = sys.argv
    sys.argv = [previous[0]] + argv
    try:
        return gate.main()
    finally:
        sys.argv = previous


if __name__ == "__main__":
    sys.exit(main())
