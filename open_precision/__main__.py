"""
This script initializes the SystemHub and therefore starts the whole system. It is the entry point for the system.
"""
from __future__ import annotations
from __future__ import print_function
import argparse
import sys

from open_precision.system_hub import SystemHub

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--debug")
args = parser.parse_args()


def main():
	SystemHub()


if __name__ == "__main__":
	try:
		main()
	except (KeyboardInterrupt, SystemExit):
		print("\nEnding Example 1")
		sys.exit(0)
