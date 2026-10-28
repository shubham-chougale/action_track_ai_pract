"""Mark done: close one item by hand."""

from actiontrack.display import owner_label
from actiontrack.store import Item, Store


class DoneError(Exception):
    """The ID given to `done` is not a number or matches no item."""


def mark_done(store: Store, raw_id: str) -> tuple[Item, bool]:
    """Mark the item done by hand; returns (item, was_already_done)."""
    if not raw_id.isascii() or not raw_id.isdigit():
        raise DoneError(f"'{raw_id}' is not an item ID (a whole number)")
    item = store.get(int(raw_id))
    if item is None:
        raise DoneError(f"no item with ID {raw_id}")
    already = item.status == "done"
    store.mark_done(item.id)  # also pins a note-ticked item so a later [ ] cannot reopen it
    return item, already


def describe(item: Item) -> str:
    return f"#{item.id} {owner_label(item)}: {item.task}"
