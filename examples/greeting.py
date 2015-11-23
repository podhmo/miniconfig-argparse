# -*- coding:utf-8 -*-
import logging
logger = logging.getLogger(__name__)


def greeting(message, is_surprised=False, name="foo"):
    """ greeting message

    :param message: message of greeting
    :param is_surprised: surprised or not (default=False)
    :param name: name of actor
    """
    logger.info("greeting start (name=%s)", name)
    suffix = "!" if is_surprised else ""
    print("{name}: {message}{suffix}".format(name=name, message=message, suffix=suffix))


def includeme(config):
    parser = config.make_parser(greeting)
    config.replace_parser(parser)


if __name__ == "__main__":
    from miniconfig_argparse import get_configurator
    config = get_configurator()
    config.include(includeme)
    args = config.make_args()
    config.call_function_as_command(greeting, args)
