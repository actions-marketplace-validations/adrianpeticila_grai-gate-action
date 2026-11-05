"""Console entry point for the grai-gate package."""

import os
import sys

from . import gate


def main():
    if (
        not os.environ.get("GRAI_UTM_SOURCE")
        and not os.environ.get("GITHUB_ACTIONS")
        and not os.environ.get("PRE_COMMIT")
    ):
        os.environ["GRAI_UTM_SOURCE"] = "pypi"
    return gate.main()


if __name__ == "__main__":
    sys.exit(main())
