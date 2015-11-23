# -*- coding:utf-8 -*-
import argparse
import inspect
import handofcats


class DictLike(object):
    """object as dict"""
    def __init__(self, ob):
        self.ob = ob

    def __getitem__(self, k):
        return getattr(self.ob, k)

    def __setitem__(self, k, v):
        setattr(self.ob, k, v)


def includeme_from_handofcats(middleware):
    def includeme(config):
        context = DictLike(config)
        create_parser = lambda ctx: config.parser
        middleware(context, create_parser)
    return includeme


def parser_from_function(fn, prog=None):
    argspec = inspect.getargspec(fn)
    doc = fn.__doc__ or ""
    help_dict = handofcats.get_help_dict(doc)
    description = handofcats.get_description(doc)
    parser_creator = handofcats.ArgumentParserCreator(argspec, help_dict, description)
    parser = parser_creator.create_parser(prog)
    parser.set_defaults(fn=fn)
    return parser


def make_parser(config, prog=None, *args, **kwargs):
    if callable(prog):
        return parser_from_function(prog)
    else:
        return argparse.ArgumentParser(prog, *args, **kwargs)


def replace_parser(config, parser):
    config.parser.parser = parser


def call_function_as_command(config, fn, parsed):
    args = [getattr(parsed, name) for name in config.parser.positionals]
    kwargs = {name: getattr(parsed, name) for name in config.parser.optionals}
    return fn(*args, **kwargs)


def includeme(config):
    config.add_directive("make_parser", make_parser)
    config.add_directive("replace_parser", replace_parser)
    config.add_directive("call_function_as_command", call_function_as_command)
