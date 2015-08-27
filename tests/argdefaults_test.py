import pytest
from piony.config.argparser import ArgParser


def args_check(cmdline, opts={}):
    argdic = vars(ArgParser().parse(cmdline))
    return all(item in argdic for item in opts)


def args_check_exit(cmdline):
    with pytest.raises(SystemExit):
        args_check(cmdline)


class TestArgDefault():
    def test_default(self):
        assert args_check(" ", {  # Empty cmdline must have space to use
            'config': ':/cfgs/config.yml',
            'print': False,
            # 'size': 360,
            'fullscreen': False,
            'no_tooltip': False,
            'verbose': '',
        })

# ==========================================
    def test_config(self):
        assert args_check("-c ./cfgs/conf.ini", {'config': "./cfgs/conf.ini"})

    def test_size(self):
        assert args_check("-s 300", {'size': 300})

    def test_fullscreen(self):
        assert args_check("-F", {'fullscreen': True})

    def test_no_tooltip(self):
        assert args_check("-T", {'no_tooltip': True})

    def test_verbose(self):
        assert args_check("-V", {'verbose': 'l'})
        assert args_check("-V v", {'verbose': 'v'})
        assert args_check("-V a", {'verbose': 'a'})

# ==========================================
    def test_combination(self):
        assert args_check("-s 300 -V", {'size': 300, 'verbose': 'l'})
        assert args_check("-s 300 -F", {'size': 300, 'fullscreen': True})
        assert args_check("-TF", {'no_tooltip': True, 'fullscreen': True})
        assert args_check("-TFV", {'no_tooltip': True, 'fullscreen': True,
                                   'verbose': 'l'})
        assert args_check("-TFV v", {'no_tooltip': True, 'fullscreen': True,
                                     'verbose': 'v'})
        assert args_check("-TFs 400", {'no_tooltip': True, 'fullscreen': True,
                                       'size': 400})
        assert args_check("-T -s 400 -F ", {'no_tooltip': True, 'fullscreen':
                                            True, 'size': 400})

# ==========================================
## Test situation when program should exit
    def test_wrong_argument(self):
        args_check_exit("-O")

    def test_help(self):
        args_check_exit("-h")

    def test_version(self):
        args_check_exit("-v")
        args_check_exit("-Tv")

    def test_e_fullscreen(self):
        args_check_exit("-F-w")

    def test_e_no_tooltip(self):
        args_check_exit("-T-j")

    def test_e_size(self):
        args_check_exit("-s j")
        args_check_exit("-s 300-j")

    def test_e_verbose(self):
        args_check_exit("-V j")
        args_check_exit("-V v -m")
