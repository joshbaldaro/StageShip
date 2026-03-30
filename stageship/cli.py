import argparse as _argparse
import logging as _logging
import sys as _sys

from stageship.helpers.dependency_data import DependencyData


DESCRIPTION = """
===============================================================================
StageShip CLI
StageShip is a tool for analysing USD stages for external dependencies, flattening composed scenes, and packaging them for delivery.
===============================================================================
"""

def _parser():
    parser = _argparse.ArgumentParser(
        formatter_class=_argparse.RawTextHelpFormatter,
        description=DESCRIPTION,
    )

    subparsers = parser.add_subparsers(
        title="Commands",
        dest="cmd",
    )

    subparsers.add_parser(
        "checkhealth",
        help="Check the health of the StageShip environment and dependencies",
    )

    analyse_parser = subparsers.add_parser(
        "analyse",
        help="Analyse a USD file for dependencies and other information",
    )
    analyse_parser.add_argument(
        "file",
        help="The USD file to analyse",
    )
    analyse_parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose logging",
    )

    flatten_parser = subparsers.add_parser(
        "flatten",
        help="Flatten a USD file and all its dependencies into a single file",
    )
    flatten_parser.add_argument(
        "file",
        help="The USD file to flatten",
    )
    flatten_parser.add_argument(
        "-o", "--output",
        help="The output file for the flattened USD (default: <input>_flattened.usd)",
    )
    flatten_parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose logging",
    )

    ship_parser = subparsers.add_parser(
        "ship",
        help="Ship a USD file and all its dependencies to a target location",
    )
    ship_parser.add_argument(
        "file",
        help="The USD file to ship",
    )
    ship_parser.add_argument(
        "--flatten",
        action="store_true",
    )
    ship_parser.add_argument(
        "--torrent",
        action="store_true",
    )
    ship_parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose logging",
    )

    return parser.parse_args()

def setup_logging(level: str = "INFO") -> None:
    numeric_level = getattr(_logging, level.upper(), _logging.INFO)

    _logging.basicConfig(
        level=numeric_level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[
            _logging.StreamHandler(_sys.stdout)
        ],
    )


def main():
    args = _parser()

    if not args.cmd:
        _parser().print_help()

    log_level = "DEBUG" if args.verbose else "INFO"
    setup_logging(level=log_level)

    if args.cmd == "analyse":
        from stageship.core import analyse
        analyse.analyse(args.file)
    elif args.cmd == "flatten":
        from stageship.core import flatten
        flatten.flatten(args.file)
    elif args.cmd == "ship":
        # from .commands import ship
        # ship(args.file, flatten=args.flatten, torrent=args.torrent)
        print(f"Shipping {args.file}...")
    elif args.cmd == "checkhealth":
        try:
            from pxr import Usd
            print("USD python bindings: OK")
        except Exception as e:
            print(f"USD python bindings: {e}")

if __name__ == "__main__":
    main()
