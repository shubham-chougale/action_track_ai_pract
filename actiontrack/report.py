"""Ingest report: what `actiontrack ingest` did and what needs attention."""

from actiontrack.ingest import IngestResult


def format_report(result: IngestResult) -> str:
    lines = [
        f"Files scanned:   {result.scanned}",
        f"Files ingested:  {result.ingested}",
        f"Files skipped:   {len(result.skipped)}",
        f"Items new:       {result.counts['new']}",
        f"Items merged:    {result.counts['merged']}",
        f"Items unchanged: {result.counts['unchanged']}",
    ]
    if result.skipped:
        lines += ["", "Skipped files:"]
        lines += [f"  {s.name}: {s.reason}" for s in result.skipped]
    for heading, entries in _flag_groups(result):
        lines += ["", heading]
        lines += [f"  {e}" for e in entries]
    return "\n".join(lines)


def _flag_groups(result: IngestResult) -> list[tuple[str, list[str]]]:
    """Flagged mentions grouped by cause; one with several causes is listed under each."""
    owners, dues, decoys = [], [], []
    for m in result.flagged:
        where, line = m.source["file"], m.original_line.strip()
        for reason in (m.flag_reason or "").split("; "):
            if reason.endswith(" owner"):
                kind = reason.removesuffix(" owner")
                owners.append(f"{where}: owner '{m.owners[0]['raw']}' ({kind}) - {line}")
            elif reason == "unresolved date":
                dues.append(f"{where}: due '{m.due_raw}' - {line}")
            elif reason in ("code block", "comment"):
                decoys.append(f"{where}: {reason} - {line}")
    groups = [
        ("Flagged - ambiguous or unknown owner:", owners),
        ("Flagged - unresolved due phrase:", dues),
        ("Flagged - found in a code block or comment:", decoys),
    ]
    return [(heading, entries) for heading, entries in groups if entries]
