"""Item listing: status, filters and output for `actiontrack list`."""

from actiontrack.display import owner_label
from actiontrack.store import Item


def item_status(item: Item, today: str) -> str:
    """"done", "overdue" (open, resolved due date strictly before today, not flagged) or "open"."""
    if item.status == "done":
        return "done"
    if item.due and not item.flagged and item.due < today:
        return "overdue"
    return "open"


def sort_items(items: list[Item]) -> list[Item]:
    """Soonest due date first, items without a resolved date last; first-seen order breaks ties."""
    return sorted(items, key=lambda i: (i.due is None, i.due or "", i.first_seen_order))


def _source_label(item: Item) -> str:
    latest = max(item.sources, key=lambda s: s["date"])
    label = f"{latest['file']} ({latest['date']})"
    others = len(item.sources) - 1
    return f"{label} +{others} more" if others else label


def _due_label(item: Item) -> str:
    if item.due:
        return item.due
    return f"{item.due_raw} ?" if item.due_raw else "-"


def _status_label(item: Item, today: str) -> str:
    status = item_status(item, today)
    return f"{status} [!]" if item.flagged else status


def render_table(items: list[Item], today: str) -> str:
    rows = [("ID", "Owner(s)", "Task", "Due", "Status", "Source")]
    for item in sort_items(items):
        rows.append((str(item.id), owner_label(item), item.task, _due_label(item),
                     _status_label(item, today), _source_label(item)))
    widths = [max(len(r[c]) for r in rows) for c in range(len(rows[0]))]
    lines = ["  ".join(cell.ljust(w) for cell, w in zip(r, widths)).rstrip() for r in rows]
    lines.insert(1, "  ".join("-" * w for w in widths))
    lines.append("")
    lines.append(f"Total: {len(items)} items")
    return "\n".join(lines)
