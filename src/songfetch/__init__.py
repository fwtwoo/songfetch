import platform

if platform.system() == 'Darwin':
    from .player_utils_mac import *
elif platform.system() == 'Linux':
    from .player_utils_linux import *
else:
    # Fallback to Linux for other systems
    from .player_utils_linux import *

