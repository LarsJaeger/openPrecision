from __future__ import annotations
import asyncio
from typing import TYPE_CHECKING

from open_precision.core.plugin_base_classes.navigator import Navigator

if TYPE_CHECKING:
    from open_precision.manager import Manager


class DataManager:
    def __init__(self, manager: Manager):
        self._manager = manager

    async def update_loop(self):
        while True:
            await asyncio.gather(self.update(), asyncio.sleep(10))

    async def update(self):
        self._manager.plugins[Navigator].target_machine_state
