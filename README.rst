miniconfig-argparse
========================================

argparse settings with miniconfig

code
----------------------------------------

.. code-block:: python

   import sys
   from miniconfig_argparse import get_configurator


   config = get_configurator()
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

default directives
----------------------------------------

- make_parser
- replace_parser
- call_function_as_command

make_parser(fn) + call_function_as_command
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Using `make_parser()` and `call_function_as_command()` combinations are useful, sometimes.

- `make_parser(fn)` -- creating parser from a function definition.
- `call_function_as_command` -- call function using parsed argument obuject.

Such like a below.

.. code-block:: python

   def greeting(message, is_surprised=False, name="foo"):
       """ greeting message

       :param message: message of greeting
       :param is_surprised: surprised or not (default=False)
       :param name: name of actor
       """
       suffix = "!" if is_surprised else ""
       print("{name}: {message}{suffix}".format(name=name, message=message, suffix=suffix))


   def includeme(config):
       parser = config.make_parser(greeting)
       config.replace_parser(parser)


   if __name__ == "__main__":
       import sys
       from miniconfig_argparse import get_configurator
       config = get_configurator()
       config.include(includeme)

       args = config.make_args(sys.argv[1:])
       config.call_function_as_command(greeting, args)

