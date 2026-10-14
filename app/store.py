"""
In-memory database.

Contacts are kept in a Python dict, so all data is lost when the server
restarts. A few sample contacts are added at startup so the API is not empty.
"""

from typing import Dict, List, Optional

contacts: Dict[int, dict] = {}
next_id = 1


def add(data: dict) -> dict:
    global next_id
    contact = {"id": next_id, **data}
    contacts[next_id] = contact
    next_id += 1
    return contact


def search_and_sort(search: Optional[str], tag: Optional[str],
                    favorite: Optional[bool], sort_by: str, order: str) -> List[dict]:
    result = list(contacts.values())

    # Search in name, email and tags (case-insensitive)
    if search:
        text = search.lower()
        result = [
            c for c in result
            if text in f"{c['first_name']} {c['last_name']}".lower()
            or text in (c["email"] or "").lower()
            or any(text in t.lower() for t in c["tags"])
        ]

    # Filter by tag
    if tag:
        result = [c for c in result if tag.lower() in (t.lower() for t in c["tags"])]

    # Filter by favorite
    if favorite is not None:
        result = [c for c in result if c["is_favorite"] == favorite]

    # Sort (empty values such as a missing email are treated as "")
    result.sort(key=lambda c: (c[sort_by] or "").lower(), reverse=(order == "desc"))
    return result


SAMPLE_CONTACTS = [
    {"first_name": "Alan", "last_name": "Turing", "email": "alan.turing@example.com",
     "phone": "+1 555 123 4567", "tags": ["Work"], "is_favorite": True},
    {"first_name": "Marie", "last_name": "Curie", "email": "marie.curie@example.com",
     "phone": "+1 555 234 5678", "tags": ["Family"], "is_favorite": False},
    {"first_name": "Katherine", "last_name": "Johnson", "email": "katherine.johnson@example.com",
     "phone": "+1 555 345 6789", "tags": ["Phone"], "is_favorite": True},
    {"first_name": "Charles", "last_name": "Darwin", "email": "charles.darwin@example.com",
     "phone": None, "tags": ["Tag"], "is_favorite": False},
    {"first_name": "Ada", "last_name": "Lovelace", "email": "ada.lovelace@example.com",
     "phone": "+44 555 567 8901", "tags": ["Work", "Friends"], "is_favorite": False},
    {"first_name": "Cahit", "last_name": "Arf", "email": "cahit.arf@example.com",
     "phone": "+90 555 012 3456", "tags": ["Family"], "is_favorite": True},
    {"first_name": "Grace", "last_name": "Hopper", "email": "grace.hopper@example.com",
     "phone": "+1 555 678 9012", "tags": ["Work"], "is_favorite": False},
    {"first_name": "Nikola", "last_name": "Tesla", "email": None,
     "phone": "+1 555 789 0123", "tags": ["Friends"], "is_favorite": False},
]


def reset() -> None:
    """Clear everything and load the sample contacts again."""
    global next_id
    contacts.clear()
    next_id = 1
    for data in SAMPLE_CONTACTS:
        add(dict(data, tags=list(data["tags"])))


reset()
