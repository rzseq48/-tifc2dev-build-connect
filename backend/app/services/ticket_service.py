EDITABLE_FIELDS = {"title", "description", "priority", "category", "status", "assigned_to_id"}
VALID_PRIORITIES = {"Low", "Medium", "High"}
VALID_STATUSES = {"New", "Triaged", "In Progress", "Resolved", "Closed"}

def clean_required_text(value):
    return value.strip() if isinstance(value, str) else ""

def validate_ticket_payload(data, partial=False):
    if not isinstance(data, dict):
        return "A JSON request body is required."
    required=("title","description","category")
    if not partial:
        for field in required:
            if not clean_required_text(data.get(field)):
                return f"{field.replace('_',' ').title()} is required."
    for field in required:
        if field in data and not clean_required_text(data[field]):
            return f"{field.replace('_',' ').title()} cannot be empty."
    if "priority" in data and data["priority"] not in VALID_PRIORITIES:
        return "Unsupported ticket priority."
    if "status" in data and data["status"] not in VALID_STATUSES:
        return "Unsupported ticket status."
    return None
