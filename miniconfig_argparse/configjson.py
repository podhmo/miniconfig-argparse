# -*- coding:utf-8 -*-
from handofcats.middlewares.configjson import middleware_config_json
from .transform import includeme_from_handofcats


def includeme(config):
    config.include(includeme_from_handofcats(middleware_config_json))
