from periodicpy.plugmgr.plugin import Module, ModuleArgument
from periodicpy.plugmgr.plugin.method import ModuleMethod, ModuleMethodArgument
from periodicpy.plugmgr.plugin.dtype import ModuleDataTypes
import os

LIRC_CONFIG_PATH = '/usr/share/periodicpi/user_files/lircd/'

class LircPusher(Module):
    _module_desc = ModuleArgument('lircpush', 'lirc configuration pusher')
    _methods = {'push_remote_file' : ModuleMethod(method_desc='Push remote control description',
                                                  method_args={'remote_name' : ModuleMethodArgument('Remote name',
                                                                                                    required=True,
                                                                                                    data_type=ModuleDataTypes.STRING),
                                                               'file_contents' : ModuleMethodArgument('LIRC remote control description',
                                                                                                      required=True,
                                                                                                      data_type=ModuleDataTypes.STRING),
                                                               'overwrite_file' : ModuleMethodArgument('Overwrite if already existent',
                                                                                                       required=False,
                                                                                                       data_type=ModuleDataTypes.BOOLEAN)},
                                                  method_return=ModuleDataTypes.BOOLEAN)}

    def __init__(self, **kwargs):
        super(LircPusher, self).__init__(**kwargs)

        self._automap_methods()

    def _push_remote_file(self, remote_name, file_contents, overwrite_file=False):

        remote_file = LIRC_CONFIG_PATH+remote_name+'.conf'

        if os.path.isfile(remote_file):
            if overwrite_file == False:
                return False

        file_written = False
        with open(remote_file, 'w') as f:
            f.write(file_contents)
            file_written = True

        if file_written == False:
            return False

        return True

def discover_module(*args):
    return LircPusher
