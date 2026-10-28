"""Gmail draft creation through the Gmail MCP connector."""


class DraftError(Exception):
    """The draft could not be created."""


def create_draft(recipient: str | None, subject: str, body: str) -> str:
    raise DraftError("Gmail connector is not wired up yet")
