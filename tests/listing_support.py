"""Seed a store with hand-made items so list tests do not depend on parsing."""

from actiontrack.store import Store


def person(name):
    return {"kind": "person", "name": name}


def seed(base, **values):
    """Add one item; sources defaults to a single note on 2026-10-01."""
    sources = values.pop("sources", None) or [
        {"file": "a.md", "date": "2026-10-01", "title": "A"}]
    values.setdefault("owners", [person("Priya Nair")])
    store = Store(base)
    item = store.add(**values)
    for source in sources:
        store.add_source(item.id, source)
    return item


def table_rows(out):
    """Data rows of the printed table: lines between the header rule and the total line."""
    lines = out.splitlines()
    start = next(i for i, line in enumerate(lines) if set(line.strip()) <= {"-", " "} and line.strip()) + 1
    return [line for line in lines[start:] if line.strip() and not line.startswith("Total")]
