#!/usr/bin/env python3
# vim: fileencoding=utf-8

import pytest
from piony.config.argparser import ArgsParser

def args_check(cmdline, opts={}):
   argdic = vars(ArgsParser().parse(cmdline))
   return all(item in argdic for item in opts)

class TestArgDefault():
    def test_default(self):
        assert args_check("", {'no_tooltip':False, 'size':360,
            'verbose':'', 'fullscreen':''})

#==========================================
    def test_size(self):
        assert args_check("-s 300", {'size':300})
        # assert args_check("-s 300 400", {'size':300})
        # assert args_check("-s", {'size':None})

    def test_fullscreen(self):
        assert args_check("-F", {'fullscreen':True})

    def test_no_tooltip(self):
        assert args_check("-T", {'no_tooltip':True})

    def test_verbose(self):
        assert args_check("-V", {'verbose':'l'})
        assert args_check("-V v", {'verbose':'v'})
        assert args_check("-V a", {'verbose':'a'})
        # assert args_check("-r", {})
        # assert args_check("-V s", {})
#==========================================
    def test_combination(self):
        assert args_check("-s 300 -V", {'size':300, 'verbose':'l'})
        assert args_check("-s 300 -F", {'size':300, 'fullscreen':True})
        assert args_check("-TF", {'no_tooltip':True, 'fullscreen':True})
        assert args_check("-TFV", {'no_tooltip':True
            , 'fullscreen':True, 'verbose':'l'})
        assert args_check("-TFV v", {'no_tooltip':True
            , 'fullscreen':True, 'verbose':'v'})
        assert args_check("-TFV a", {'no_tooltip':True
            , 'fullscreen':True, 'verbose':'a'})
        assert args_check("-TFs 400", {'no_tooltip':True
            , 'fullscreen':True, 'size':400})

#==========================================
    def test_mytest(self):
        with pytest.raises(SystemExit):
            args_check("-O")

