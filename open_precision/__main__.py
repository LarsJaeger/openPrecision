from __future__ import annotations
from __future__ import print_function

import sys

from open_precision.manager_hub import ManagerHub


def main():
    man = ManagerHub()


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nEnding Example 1")
        sys.exit(0)
