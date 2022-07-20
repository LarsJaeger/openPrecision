from __future__ import annotations
from __future__ import print_function

import sys
from multiprocessing.managers import SyncManager

from open_precision.core.interfaces.user_interface import UserInterface
from open_precision.custom_sync_manager import CustomSyncManager, proxy
from open_precision.manager import Manager


class Main:
    def __init__(self):
        self.run()

    def run(self):
        # init SyncManager
        sync_manager = CustomSyncManager(("127.0.0.1", 50000), authkey=b'open_precision')
        sync_manager.start()
        man = sync_manager.Manager()
        man.plugins[UserInterface].start()

    def close(self):
        pass


if __name__ == "__main__":
    try:
        Main()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nEnding Example 1")
        sys.exit(0)
