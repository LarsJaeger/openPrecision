import types
from multiprocessing.managers import SyncManager, NamespaceProxy

from open_precision.core.model.model_base import Model
from open_precision.manager import Manager
from open_precision.managers import data_manager
from open_precision.managers.config_manager import ConfigManager
from open_precision.managers.data_manager import DataManager
from open_precision.managers.plugin_manager import PluginManager
from open_precision.managers.vehicle_manager import VehicleManager


def proxy(target):
    dic = {'types': types}
    exec('''def __getattr__(self, key):
                print(f'PRINT {key}')
                result = self._callmethod('__getattribute__', (key,))
                if isinstance(result, types.MethodType):
                    def wrapper(*args, **kwargs):
                        return self._callmethod(key, args, kwargs)
                    return wrapper
                return result''', dic)
    proxy_name = target.__name__ + "Proxy"
    proxy_type = type(proxy_name, (NamespaceProxy,), dic)
    proxy_type._exposed_ = tuple(dir(target))
    return proxy_type


class CustomSyncManager(SyncManager):
    def __init__(self, *args, **kwargs):
        # register model
        for cls in data_manager.subclasses_recursive(Model):
            self.register(cls.__name__, cls, proxy(cls))

        # register managers
        self.register('Manager', Manager, proxy(Manager))

        self.register('Config', ConfigManager, proxy(ConfigManager))
        self.register('Data', DataManager, proxy(DataManager))
        self.register('Vehicles', VehicleManager, proxy(VehicleManager))
        self.register('Plugins', PluginManager, proxy(PluginManager))

        super().__init__(*args, **kwargs)
