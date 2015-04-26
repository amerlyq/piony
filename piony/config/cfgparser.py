#!/usr/bin/env python3
# vim: fileencoding=utf-8

import collections
from configparser import ConfigParser as Cfg_Pars

from piony import gvars
from piony.config import cfgdefaults


class ConfigParser:
    def __init__(self):
        self.config = self.default()

    def default(self, cfg=cfgdefaults.G_CONFIG_DEFAULT):
        return Cfg_Pars(defaults=cfg, dict_type=collections.OrderedDict,
                        allow_no_value=False, delimiters=('=', ':'),
                        comment_prefixes=('#', ';'),
                        inline_comment_prefixes=('#', ';'),
                        strict=True, empty_lines_in_values=False,
                        default_section="DEFAULT", interpolation=None)

    def store_file(self, path=gvars.G_CONFIG_PATH):
        with open(path, 'w') as cfg_file:
            self.config.write(cfg_file)

    def read_file(self, path=gvars.G_CONFIG_PATH):
        self.config.read(path)  # Can specify bunch of possible files
        return self.config

