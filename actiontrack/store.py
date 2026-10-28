"""Persistence: the hidden .actiontrack/ data folder and the item store."""

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path

DATA_DIR_NAME = ".actiontrack"
ITEMS_FILE = "items.json"


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
        self._next_id = 1
        self._items: dict[int, Item] = {}
        if self.path.exists():
            raw = json.loads(self.path.read_text(encoding="utf-8"))
            self._next_id = raw["next_id"]
            self._items = {i["id"]: Item(**i) for i in raw["items"]}

    def _save(self) -> None:
        raw = {"next_id": self._next_id, "items": [asdict(i) for i in self.all()]}
        self.path.write_text(json.dumps(raw, indent=2, sort_keys=True), encoding="utf-8")

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
