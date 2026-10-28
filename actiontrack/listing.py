"""Item listing: status, filters and output for `actiontrack list`."""

import json

from actiontrack.display import owner_label, owner_labels
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


def filter_items(items: list[Item], today: str, status: str | None = None) -> list[Item]:
    return [i for i in items if status is None or item_status(i, today) == status]


def render_json(items: list[Item], today: str) -> str:
    """The same items and order as the table, as a JSON list."""
    out = []
    for item in sort_items(items):
        out.append({
            "id": item.id,
            "owners": owner_labels(item),
            "task": item.task,
            "due": item.due,
            "due_raw": item.due_raw,
            "status": item_status(item, today),
            "flagged": item.flagged,
            "flag_reason": item.flag_reason,
            "sources": item.sources,
        })
    return json.dumps(out, indent=2)


def render_table(items: list[Item], today: str) -> str:
    if not items:
        return "No items match"
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
