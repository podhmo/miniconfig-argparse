# -*- coding:utf-8 -*-
import sys
from miniconfig_argparse import Configurator


def includeme(config):
    parser = config.parser
    parser.add_argument("--without-echo", action="store_false", dest="echo")


def main(argv):
    config = Configurator()
    config.include("miniconfig_argparse.configjson")
    config.include(includeme)
    args = config.make_args(argv)

    print(args.echo)
    if args.echo:
        print("echo:")
        print(args)

if __name__ == "__main__":
    # calling with --cli-input-json="file://./config.json"
    argv = sys.argv[1:]
    main(argv)
