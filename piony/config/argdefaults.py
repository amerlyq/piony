from piony import __version__
# from piony.config import gvars


def G_ARGUMENTS_DEFAULT_F(ps):
    ## Configuration
    farg = ps.add_argument
    farg('buds', metavar='bud', nargs='*', type=str,
         default=None,
         help="Setup profile layout in json directly on cmdline. "
              "Can be specified several times -- one for each slice. "
              "Or use pathes to files with slices inside.")
    farg('-v', '--version', action='version', default=None,
         version="%(prog)s {0}".format(__version__),
         help="Version of program.")

    gr_window = ps.add_argument_group('Window')
    warg = gr_window.add_argument
    warg('-c', '--config', default=None,
         help="Config file with default settings.")
    warg('-p', '--print', default=None,
         help="Toggle action print/execute to use as frontend only.")

    ## Appearance
    warg('-s', '--size', type=int, default=None,
         help="Sets window size WxH=NxN to derive all rings sizes from it.")
    warg('-F', '--fullscreen', action='store_true', default=None,
         help="Overlay fullscreen/local")
    warg('-T', '--no-tooltip', action='store_true', default=None,
         help="Disable pop-up items, for those who is irritated.")

    ## Process
    gr_general = ps.add_argument_group('General')
    garg = gr_general.add_argument
    garg('-k', '--kill', action='store_true', default=None,
         help="Kill running daemonized program.")
    garg('-V', '--verbose', nargs='?', type=str,
         const='a', choices=['a', 'v', 'k'], default=None,
         help="Verbose (debug): [a]ll (default), [v]isuals, [k]eys.")
