miniconfig-argparse
========================================

argparse settings with miniconfig

code
----------------------------------------

.. code-block:: python

   import sys
   from miniconfig_argparse import Configurator


   config = Configurator()
   config.include("yourmodule")
   config.include("yourmodule.extra")

   args = config.make_args(sys.argv[1:])
   # using args

in yourmodule, using config like a below.

.. code-block:: python

   def includeme(config):
       parser = config.parser

       parser.add_argument(
           '-v', '--verbose', action='count', default=0,
           help="(default option: increment logging level(default is WARNING))"
       )
       parser.add_argument(
           '-q', '--quiet', action='count', default=0,
           help="(default option: decrement logging level(default is WARNING))"
       )

       def setup_closure(args):
           logging_level = logging.WARN + 10 * args.quiet - 10 * args.verbose
           logging.basicConfig(level=logging_level)
           return args

       parser.add_callback(setup_closure)
