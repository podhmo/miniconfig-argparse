# -*- coding:utf-8 -*-
import argparse
from cached_property import cached_property as reify
from miniconfig import ConfiguratorCore, Control, PHASE1_CONFIG
from enum import Enum
from .parsertree import ParserTree


PHASE0_CONFIG = PHASE1_CONFIG - 10


class AnnotateType(Enum):
    # todo: rename
    all = 1
    partial = 2
    only = 3


class WrappedArgumentParser(object):
    def __init__(self, parser):
        self.parser = parser
        self.callbacks = []

    def add_callback(self, callback, annotate=AnnotateType.all):
        self.callbacks.append((callback, annotate))

    def __getattr__(self, k):
        return getattr(self.parser, k)

    def activate_callbacks(self, args, skip_at):
        for callback, annotate in self.callbacks:
            if annotate == skip_at:
                continue
            result = callback(args)
            if result is not None:
                args = result
        return args

    def parse_args(self, args):
        args = self.parser.parse_args(args)
        args = self.activate_callbacks(args, skip_at=AnnotateType.partial)
        return args

    def parse_known_args(self, args):
        args, rest = self.parser.parse_known_args(args)
        args = self.activate_callbacks(args, skip_at=AnnotateType.only)
        return args, rest

    def __repr__(self):
        return "<{} parser={!r} at {}>".format(self.__class__.__name__, self.parser, hex(id(self)))


class ParserControl(Control):
    @reify
    def parser(self):
        return WrappedArgumentParser(argparse.ArgumentParser())


class Configurator(ConfiguratorCore):
    DEFAULT_INCLUDES = [
        "miniconfig_argparse.verbosity_adjustment"
    ]

    def __init__(self, settings=None, module=None, control=None, skip_defaults=False):
        control = control or ParserControl()
        super(Configurator, self).__init__(settings, module, control)
        self.skip_defaults = skip_defaults

    def include_defaults(self):
        if not self.skip_defaults:
            for f in self.DEFAULT_INCLUDES:
                self.include(f)

    def make_args(self, argv):
        self.include_defaults()
        self.commit()
        return self.parser.parse_args(argv)

    def make_partial_args(self, argv):
        self.include_defaults()
        self.commit()
        return self.parser.parse_known_args(argv)


class ParserTreeControl(ParserControl):
    @reify
    def parser(self):
        return WrappedArgumentParser(ParserTree())


def get_configurator(*args, **kwargs):
    config = Configurator(*args, **kwargs)
    config.include(includeme)
    return config


def get_support_subcommand_configurator(*args, **kwargs):
    kwargs["control"] = ParserTreeControl()
    config = Configurator(*args, **kwargs)
    config.include(includeme)
    config.include("miniconfig_argparse.parsertree")
    return config


def includeme(config):
    config.include("miniconfig_argparse.transform")
