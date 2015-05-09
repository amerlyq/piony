#!/usr/bin/env python3
# vim: fileencoding=utf-8

from collections import OrderedDict
from configparser import ConfigParser

from piony.config import gvars
from piony.config import cfgdefaults


class CfgParser:
    def __init__(self):
        self.default()

    def default(self):
        self.cfg = ConfigParser(
            dict_type=OrderedDict,
            allow_no_value=False, delimiters=('=', ':'),
            comment_prefixes=('#', ';'),
            inline_comment_prefixes=('#', ';'),
            strict=True, empty_lines_in_values=False,
            default_section="DEFAULT", interpolation=None)
        self.cfg.read_dict(cfgdefaults.G_CONFIG_DEFAULT)
        return self.cfg

    def read_file(self, path=gvars.G_CONFIG_PATH):
        self.cfg.read(path)  # Can specify bunch of possible files
        return self.cfg

    # def store_file(self, path=gvars.G_CONFIG_PATH):
    #     with open(path, 'w') as cfg_file:
    #         self.cfg.write(cfg_file)
