"""
piony -- Radial menu for Wacom / mouse
"""

__appname__ = "piony"
__version__ = "0.7.2"
__licence__ = "GPL 3.0"
__email__ = "amerlyq@gmail.com"
__url__ = 'https://github.com/amerlyq/piony'


if __debug__:
    G_DEBUG_ACTIONS = True
    G_DEBUG_VISUALS = False

G_ACTIVE_WINDOW = '%1'
G_SOCKET_NAME = 'piony-socket'

import logging
logger = logging.getLogger(__name__)
