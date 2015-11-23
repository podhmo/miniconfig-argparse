# -*- coding:utf-8 -*-
import logging
from miniconfig_argparse import Configurator
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    config = Configurator()
    args = config.make_args()

    logger.debug("debug")
    logger.info("info")
    logger.warning("warning")
    logger.error("error")
