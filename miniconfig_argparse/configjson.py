# -*- coding:utf-8 -*-
from handofcats.middlewares.configjson import middleware_config_json
from .transform import includeme_from_handofcats
from . import PHASE0_CONFIG


def includeme(config):
    def closure():
        config.include(includeme_from_handofcats(middleware_config_json))
    config.action(closure, order=PHASE0_CONFIG)
