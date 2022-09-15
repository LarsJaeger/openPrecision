from __future__ import annotations
from __future__ import print_function

import sys

from open_precision.manager import Manager


def main():
    man = Manager()


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nEnding Example 1")
        sys.exit(0)
