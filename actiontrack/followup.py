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
