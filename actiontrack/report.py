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
    return "\n".join(lines)
