"""Item listing: status, filters and output for `actiontrack list`."""

from actiontrack.store import Item


def item_status(item: Item, today: str) -> str:
    """"done", "overdue" (open, resolved due date strictly before today, not flagged) or "open"."""
    if item.status == "done":
        return "done"
    if item.due and not item.flagged and item.due < today:
        return "overdue"
    return "open"
