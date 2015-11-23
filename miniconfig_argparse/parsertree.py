# -*- coding:utf-8 -*-
import argparse
from cached_property import cached_property as reify


class ParserTree(object):
    def __init__(self, path=None, dest="stage"):
        self.dest = dest
        self.path = path or []
        self.children = {}

    @property
    def name(self):
        return ".".join(self.path)

    def __repr__(self):
        return '<{clsname} path="{path}", {dest}={keys!r} at {id}>'.format(
            clsname=self.__class__.__name__,
            path=self.name,
            id=hex(id(self)),
            dest=self.dest, keys=list(self.children.keys())
        )

    def __getattr__(self, k):
        return getattr(self.parser, k)

    @reify
    def parser(self):
        parser = argparse.ArgumentParser(prog=self.name, add_help=False)
        parser.add_argument(self.dest, choices=[])
        return parser

    @reify
    def current_action(self):
        for action in self.parser._actions:
            if action.dest == self.dest:
                return action

    def __setitem__(self, name, parser):
        self.children[name] = parser
        self._update(name)

    def __getitem__(self, name):
        try:
            return self.children[name]
        except KeyError:
            self._update(name)
            new_child = self.children[name] = self.__class__(dest=self.dest, path=self.path + [name])
            return new_child

    def _update(self, name):
        choices = self.current_action.choices
        if name not in choices:
            choices.append(name)

    def parse_known_args(self, argv=None):
        return self.parser.parse_known_args(argv)

    def parse_args(self, argv=None):
        args, rest = self.parse_known_args(argv)
        name = getattr(args, self.dest)
        subargs = self.children[name].parse_args(rest)

        if not hasattr(subargs, "prepend_chain"):
            subargs = ChainedObject(subargs)
        subargs.prepend_chain(args)
        return subargs


class ChainedObject(object):
    def __init__(self, ob):
        self.chain = [ob]

    def append_chain(self, ob):
        self.chain.append(ob)

    def prepend_chain(self, ob):
        self.chain.insert(0, ob)

    def getlist(self, k):
        return [getattr(ob, k) for ob in self.chain if hasattr(ob, k)]

    def __getattr__(self, k):
        for ob in self.chain:
            v = getattr(ob, k, None)
            if v is not None:
                return v
        raise AttributeError(k)

    def __repr__(self):
        return "<Chain {!r} at {}>".format(self.chain, hex(id(self)))


def add_subcommand(config, namelist, parser):
    if hasattr(namelist, "split"):
        namelist = namelist.split(".")
    target = config.parser
    for name in namelist[:-1]:
        target = target.__getitem__(name)
    target.__setitem__(namelist[-1], parser)


def get_subcommand(config, namelist):
    if hasattr(namelist, "split"):
        namelist = namelist.split(".")
    target = config.parser
    for name in namelist:
        target = target.__getitem__(name)
    return target


def includeme(config):
    config.add_directive("add_subcommand", add_subcommand)
    config.add_directive("get_subcommand", get_subcommand)
