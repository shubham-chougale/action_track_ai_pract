"""Command-line entry point."""

import argparse
import re
import sys
from datetime import date

from actiontrack.followup import compose, count_unassigned, select_items
from actiontrack.gmail import DraftError, create_draft
from actiontrack.done import DoneError, describe, mark_done
from actiontrack.ingest import ingest_folder
from actiontrack.listing import filter_items, render_json, render_table
from actiontrack.people import LookupFailure, People
from actiontrack.report import format_report
from actiontrack.scanner import FolderError
from actiontrack.store import ROSTER_FILE, Store, StoreError, data_dir


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
    followup = sub.add_parser("followup", help="draft a follow-up email for one owner (never sent)")
    followup.add_argument("owner", help="full name or a unique first name")
    followup.add_argument("--today", help="treat this YYYY-MM-DD as today (for stable results)")
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
    try:
        return _dispatch(args)
    except StoreError as err:
        print(f"error: {err}", file=sys.stderr)
        return 1


def _dispatch(args) -> int:
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
        try:
            today = _iso_date(args.today, "--today") or date.today().isoformat()
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
    elif args.command == "followup":
        return _followup(args)
    return 0


def _followup(args) -> int:
    try:
        today = _iso_date(args.today, "--today") or date.today().isoformat()
    except ValueError as err:
        print(f"error: {err}", file=sys.stderr)
        return 1
    store = Store()
    people = People()
    people.learn(store.people_names())
    people.load_roster(data_dir() / ROSTER_FILE)
    try:
        owner = people.find(args.owner)
    except LookupFailure as err:
        print(f"error: {err}", file=sys.stderr)
        return 1
    items = select_items(store.all(), owner, today)
    unassigned = count_unassigned(store.all())
    if not items:
        print(f"No open or overdue items for {owner}; no draft created.")
    else:
        recipient = people.email(owner)
        if recipient is None:
            print(f"warning: no email for {owner} in {data_dir() / ROSTER_FILE}; "
                  "the draft has no recipient", file=sys.stderr)
        subject, body = compose(owner, items, today)
        try:
            draft_id = create_draft(recipient, subject, body)
        except DraftError as err:
            print(f"error: {err}", file=sys.stderr)
            return 1
        print(f"Draft created for {owner} ({len(items)} items): {draft_id}")
    print(f"Unassigned items: {unassigned} (never included in a follow-up)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
