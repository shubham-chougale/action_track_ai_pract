"""Plain-text labels for stored items, shared by `done` and `list`."""

from actiontrack.store import Item


def owner_labels(item: Item) -> list[str]:
    """Owner names, "unassigned", or the raw owner wording marked ambiguous/unknown."""
    labels = []
    for owner in item.owners:
        if owner["kind"] == "person":
            labels.append(owner["name"])
        elif owner["kind"] == "unassigned":
            labels.append("unassigned")
        else:
            labels.append(f"{owner.get('raw')} ({owner['kind']})")
    return labels or ["unassigned"]


def owner_label(item: Item) -> str:
    return ", ".join(owner_labels(item))
