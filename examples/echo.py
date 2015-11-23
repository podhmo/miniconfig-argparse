# -*- coding:utf-8 -*-
from miniconfig_argparse import Configurator


def includeme(config):
    parser = config.parser
    parser.add_argument("--without-echo", action="store_false", dest="echo")


def main(argv=None):
    config = Configurator()
    config.include("miniconfig_argparse.configjson")
    config.include(includeme)
    args = config.make_args(argv)

    print(args)
    if args.echo:
        print("echo:")
        print(args)

if __name__ == "__main__":
    # calling with --cli-input-json="file://./config.json"
    main()
