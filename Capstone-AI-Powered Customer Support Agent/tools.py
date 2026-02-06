from langchain_core.tools import tool

@tool
def search_docs(query: str) -> str:
    """Search internal documentation or knowledge base."""
    return f"Mocked KB result for query: {query}"

@tool
def create_escalation_ticket(summary: str) -> str:
    """Create a ticket for human escalation."""
    return f"ESCALATION_TICKET_ID-123 | {summary}"

@tool
def schedule_followup(reason: str, timeframe_hours: int) -> str:
    """Schedule a follow-up task."""
    return f"FOLLOWUP_SCHEDULED in {timeframe_hours} hours | {reason}"

tools = [search_docs, create_escalation_ticket, schedule_followup]