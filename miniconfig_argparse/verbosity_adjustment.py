# -*- coding:utf-8 -*-
from .transform import includeme_from_handofcats
from handofcats.middlewares.verbosity_adjustment import middleware_verbosity_adjustment


def includeme(config):
    config.include(includeme_from_handofcats(middleware_verbosity_adjustment))
