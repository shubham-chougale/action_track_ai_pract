"""Command-line entry point."""

import argparse
import sys


def build_parser() -> argparse.ArgumentParser:
    return argparse.ArgumentParser(
        prog="actiontrack",
        description="Track action items from meeting notes and draft follow-up emails.",
    )


def main(argv: list[str] | None = None) -> int:
    build_parser().parse_args(argv)
    return 0


if __name__ == "__main__":
    sys.exit(main())
