# -*- coding:utf-8 -*-
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
