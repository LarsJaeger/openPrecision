from __future__ import annotations
from __future__ import print_function

import sys


class Main:
    def __init__(self):
        self.run()

    def run(self):
        pass

    def close(self):
        pass


if __name__ == "__main__":
    try:
        Main()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nEnding Example 1")
        sys.exit(0)
