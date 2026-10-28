"""Persistence: the hidden .actiontrack/ data folder and the item store."""

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path

DATA_DIR_NAME = ".actiontrack"
ITEMS_FILE = "items.json"
PEOPLE_FILE = "people.json"
ROSTER_FILE = "roster.csv"


class StoreError(Exception):
    """A data file in .actiontrack/ is damaged."""


def _read_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (ValueError, OSError) as err:
        raise StoreError(f"{path.name} in {path.parent} is unreadable ({err}); "
                         "fix or delete it (ingest the notes again to rebuild)") from err


def data_dir(base: Path | str | None = None) -> Path:
    """Return the .actiontrack/ folder under base (default: cwd), creating it."""
    path = Path(base if base is not None else Path.cwd()) / DATA_DIR_NAME
    path.mkdir(exist_ok=True)
    return path


@dataclass
class Item:
    id: int
    first_seen_order: int
    task: str
    owners: list[dict] = field(default_factory=list)
    original_line: str | None = None
    due: str | None = None
    due_raw: str | None = None
    status: str = "open"
    status_manual: bool = False
    flagged: bool = False
    flag_reason: str | None = None
    sources: list[dict] = field(default_factory=list)


class Store:
    """Items kept as JSON in <base>/.actiontrack/items.json."""

    def __init__(self, base: Path | str | None = None):
        self.path = data_dir(base) / ITEMS_FILE
        self._people_path = self.path.with_name(PEOPLE_FILE)
        self._next_id = 1
        self._items: dict[int, Item] = {}
        if self.path.exists():
            raw = _read_json(self.path)
            try:
                self._next_id = raw["next_id"]
                self._items = {i["id"]: Item(**i) for i in raw["items"]}
            except (KeyError, TypeError) as err:
                raise StoreError(f"{self.path.name} in {self.path.parent} has an unexpected "
                                 f"structure ({err!r}); fix or delete it") from err

    def _save(self) -> None:
        raw = {"next_id": self._next_id, "items": [asdict(i) for i in self.all()]}
        self.path.write_text(json.dumps(raw, indent=2, sort_keys=True), encoding="utf-8")

    def people_names(self) -> list[str]:
        """Names learned from attendees, in first-seen order."""
        if not self._people_path.exists():
            return []
        names = _read_json(self._people_path)
        if not isinstance(names, list):
            raise StoreError(f"{self._people_path.name} in {self._people_path.parent} should be a list; "
                             "fix or delete it")
        return names

    def learn_people(self, names: list[str]) -> None:
        known = self.people_names()
        added = [n for n in dict.fromkeys(names) if n not in known]
        if added:  # written only on change, so a repeat ingest leaves the file alone
            self._people_path.write_text(json.dumps(known + added, indent=2), encoding="utf-8")

    def add(self, **values) -> Item:
        item = Item(id=self._next_id, first_seen_order=self._next_id, **values)
        self._items[item.id] = item
        self._next_id += 1
        self._save()
        return item

    def get(self, item_id: int) -> Item | None:
        return self._items.get(item_id)

    def all(self) -> list[Item]:
        return sorted(self._items.values(), key=lambda i: i.first_seen_order)

    def add_source(self, item_id: int, source: dict) -> None:
        item = self._items[item_id]
        if source not in item.sources:
            item.sources.append(source)
            self._save()

    def update(self, item_id: int, **changes) -> Item:
        """Change fields on an item; id, first_seen_order and sources are never touched."""
        immutable = {"id", "first_seen_order", "sources"} & changes.keys()
        if immutable:
            raise ValueError(f"cannot update {sorted(immutable)}")
        item = self._items[item_id]
        for key, value in changes.items():
            if not hasattr(item, key):
                raise ValueError(f"unknown item field: {key}")
            if key == "status" and item.status_manual:
                continue  # a manual done always sticks
            setattr(item, key, value)
        self._save()
        return item

    def mark_done(self, item_id: int) -> Item:
        item = self._items[item_id]
        item.status, item.status_manual = "done", True
        self._save()
        return item
