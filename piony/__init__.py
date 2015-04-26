#!/usr/bin/env python3
# vim: fileencoding=utf-8

"""
piony -- Radial menu for Wacom / mouse
"""

__appname__ = "piony"
__version__ = "0.6.9"
__licence__ = "GPL 3.0"
__email__ = "amerlyq@gmail.com"


# Disable warning 'unused import' for next lines {{{ pylint:disable=W0611
from piony.config.argparser import ArgsParser
from piony.config.cfgparser import ConfigParser
from piony.config.prfparser import ProfileParser
from piony.window import Window
# }}}
