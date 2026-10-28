"""Command-line entry point."""

import argparse
import sys

from actiontrack.ingest import ingest_folder
from actiontrack.report import format_report
from actiontrack.scanner import FolderError


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="actiontrack",
        description="Track action items from meeting notes and draft follow-up emails.",
    )
    sub = parser.add_subparsers(dest="command")
    ingest = sub.add_parser("ingest", help="parse every .md meeting note in a folder")
    ingest.add_argument("folder")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "ingest":
        try:
            result = ingest_folder(args.folder)
        except FolderError as err:
            print(f"error: {err}", file=sys.stderr)
            return 1
        print(format_report(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
