# -*- coding:utf-8 -*-
from .transform import includeme_from_handofcats
from handofcats.middlewares.verbosity_adjustment import middleware_verbosity_adjustment
from . import PHASE0_CONFIG


def includeme(config):
    def closure():
        config.include(includeme_from_handofcats(middleware_verbosity_adjustment))
    config.action(closure, order=PHASE0_CONFIG)
