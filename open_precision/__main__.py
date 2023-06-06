from __future__ import annotations
from __future__ import print_function

import sys

from open_precision.system_hub import SystemHub


def main():
    man = SystemHub()


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nEnding Example 1")
        sys.exit(0)
