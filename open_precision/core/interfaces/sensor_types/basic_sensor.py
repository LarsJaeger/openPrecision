import atexit
from abc import abstractmethod, ABC

from open_precision.core.config_manager import ConfigManager
from open_precision.core.plugin_manager import PluginManager


class BasicSensor(ABC):
    @abstractmethod
    def __init__(self, config_manager: ConfigManager, plugin_manager: PluginManager):
        self._config_manager = config_manager
        atexit.register(self._cleanup())
        pass

    @abstractmethod
    def _cleanup(self):
        pass

    @property
    @abstractmethod
    def is_calibrated(self) -> bool:
        pass

    @abstractmethod
    def calibrate(self) -> bool:
        """calibrate device, (depending on your implementation also set is_calibrated accordingly) and
         return True if calibration succeeded """
        pass
