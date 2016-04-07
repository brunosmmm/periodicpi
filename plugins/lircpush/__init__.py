from viscum.plugin import (Module,
                           ModuleArgument)
import os

LIRC_CONFIG_PATH = '/usr/share/periodicpi/user_files/lircd'


class LircPusher(Module):
    _module_desc = ModuleArgument('lircpush', 'lirc configuration pusher')

    def __init__(self, **kwargs):
        super(LircPusher, self).__init__(**kwargs)

        self._automap_methods()

    def _push_remote_file(self, remote_name,
                          file_contents, overwrite_file=False):

        remote_file = os.path.join(LIRC_CONFIG_PATH,
                                   remote_name+'.conf')

        if os.path.isfile(remote_file):
            if overwrite_file is False:
                return False

        file_written = False
        with open(remote_file, 'w') as f:
            f.write(file_contents)
            file_written = True

        if file_written is False:
            return False

        return True


def discover_module(**kwargs):
    class LircPusherProxy(LircPusher):
        _, _methods, _propertues =\
            Module.build_module_structure_from_file(os.path.join(kwargs['plugin_path'],
                                                                 'lircpush,json'))

    return LircPusherProxy
