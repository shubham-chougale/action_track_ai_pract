"""Follow-up email: which items go to one owner."""

from actiontrack.listing import filter_items, item_status, sort_items
from actiontrack.store import Item


def select_items(items: list[Item], owner: str, today: str) -> list[Item]:
    """The owner's open and overdue items, soonest due first.

    Done, flagged and not-fully-resolved items are left out: an unassigned or
    ambiguous owner never matches a person's name. Co-owned items match each
    co-owner, and a merged item is a single stored item, so it appears once.
    """
    mine = filter_items(items, today, owner=owner)
    return sort_items([i for i in mine if not i.flagged and item_status(i, today) != "done"])


def count_unassigned(items: list[Item]) -> int:
    return sum(1 for i in items if any(o["kind"] == "unassigned" for o in i.owners))


def _due_text(item: Item) -> str:
    if item.due:
        return f"due {item.due}"
    return f"due {item.due_raw}" if item.due_raw else "no due date"


def _source_text(item: Item) -> str:
    latest = max(item.sources, key=lambda s: s["date"])
    return f"{latest.get('title') or latest['file']} ({latest['date']})"


def _section(heading: str, items: list[Item]) -> list[str]:
    lines = [f"{heading}:"]
    lines += [f"- {i.task} | {_due_text(i)} | {_source_text(i)} | #{i.id}" for i in items]
    return lines + [""]


def compose(owner: str, items: list[Item], today: str) -> tuple[str, str]:
    """(subject, plain-text body) for the owner's selected items.

    The tool adds no sign-off: Gmail appends the user's signature to the draft.
    """
    overdue = [i for i in items if item_status(i, today) == "overdue"]
    open_ = [i for i in items if item_status(i, today) != "overdue"]
    subject = f"Action items follow-up: {owner} ({len(overdue)} overdue, {len(open_)} open)"
    lines = [f"Hi {owner.split()[0]},", "",
             "Here are your action items from our recent meetings that still need attention.", ""]
    if overdue:
        lines += _section("Overdue", overdue)
    if open_:
        lines += _section("Open", open_)
    return subject, "\n".join(lines).rstrip() + "\n"
