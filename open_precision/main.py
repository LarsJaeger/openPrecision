from __future__ import annotations
from __future__ import print_function

import sys

import uvicorn

from open_precision.manager import Manager


class Main:
    def __init__(self):
        self.run()

    def run(self):
        man = Manager()
        pass

    def close(self):
        pass


if __name__ == "__main__":
    try:
        Main()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nEnding Example 1")
        sys.exit(0)
