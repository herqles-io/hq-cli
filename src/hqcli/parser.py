import argparse


description = """Some description here"""

epilog = """Some epilog here"""

parser = argparse.ArgumentParser(
    description=description,
    epilog=epilog)

subparsers = parser.add_subparsers(help="plugin to use", dest="plugin")
