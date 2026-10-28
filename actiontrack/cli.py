"""Command-line entry point."""

import argparse
import re
import sys
from datetime import date

from actiontrack.done import DoneError, describe, mark_done
from actiontrack.ingest import ingest_folder
from actiontrack.listing import filter_items, render_json, render_table
from actiontrack.people import LookupFailure, People
from actiontrack.report import format_report
from actiontrack.scanner import FolderError
from actiontrack.store import Store


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="actiontrack",
        description="Track action items from meeting notes and draft follow-up emails.",
    )
    sub = parser.add_subparsers(dest="command")
    ingest = sub.add_parser("ingest", help="parse every .md meeting note in a folder")
    ingest.add_argument("folder")
    done = sub.add_parser("done", help="mark an action item done")
    done.add_argument("id")
    listing = sub.add_parser("list", help="show tracked action items")
    listing.add_argument("--owner", help="full name, a unique first name, or 'unassigned'")
    listing.add_argument("--status", choices=["open", "done", "overdue"])
    listing.add_argument("--due-before", metavar="YYYY-MM-DD", help="only items due strictly before")
    listing.add_argument("--json", action="store_true", help="machine-readable output")
    listing.add_argument("--today", help="treat this YYYY-MM-DD as today (for stable results)")
    return parser


def _iso_date(value: str | None, option: str) -> str | None:
    """Return value if it is a real YYYY-MM-DD date (None passes through), else raise ValueError."""
    if value is None:
        return None
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        try:
            return date.fromisoformat(value).isoformat()
        except ValueError:
            pass
    raise ValueError(f"{option} needs a date as YYYY-MM-DD, got '{value}'")


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "ingest":
        try:
            result = ingest_folder(args.folder)
        except FolderError as err:
            print(f"error: {err}", file=sys.stderr)
            return 1
        print(format_report(result))
    elif args.command == "done":
        try:
            item, already = mark_done(Store(), args.id)
        except DoneError as err:
            print(f"error: {err}", file=sys.stderr)
            return 1
        print(f"Item already done: {describe(item)}" if already else f"Marked done: {describe(item)}")
    elif args.command == "list":
        today = args.today or date.today().isoformat()
        try:
            due_before = _iso_date(args.due_before, "--due-before")
        except ValueError as err:
            print(f"error: {err}", file=sys.stderr)
            return 1
        store = Store()
        owner = None
        if args.owner is not None:
            people = People()
            people.learn(store.people_names())
            try:
                owner = people.find(args.owner, allow_unassigned=True)
            except LookupFailure as err:
                print(f"error: {err}", file=sys.stderr)
                return 1
        items = filter_items(store.all(), today, owner, args.status, due_before)
        print(render_json(items, today) if args.json else render_table(items, today))
    return 0


if __name__ == "__main__":
    sys.exit(main())
