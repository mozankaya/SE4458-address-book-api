"""Address Book REST API (SE4458 Assignment 2, Group 1)."""

from typing import Literal, Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import RedirectResponse

from app import store
from app.models import Contact, ContactCreate, ContactList, ContactPatch

app = FastAPI(
    title="Address Book API",
    version="1.0.0",
    description="Create, edit, update, delete, search, sort and favorite contacts. "
                "Data is stored in memory and resets when the server restarts.",
)


def find_contact(contact_id: int) -> dict:
    contact = store.contacts.get(contact_id)
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact


@app.get("/", include_in_schema=False)
def root():
    # Open Swagger UI when someone visits the base URL
    return RedirectResponse(url="/docs")


@app.get("/contacts", response_model=ContactList, summary="List, search, filter and sort contacts")
def list_contacts(
    search: Optional[str] = Query(None, description="Search in name, email and tags"),
    tag: Optional[str] = Query(None, description="Only contacts with this tag"),
    favorite: Optional[bool] = Query(None, description="true = only favorites"),
    sort_by: Literal["first_name", "last_name", "email"] = "first_name",
    order: Literal["asc", "desc"] = "asc",
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
):
    result = store.search_and_sort(search, tag, favorite, sort_by, order)
    start = (page - 1) * page_size
    return {
        "items": result[start:start + page_size],
        "total": len(result),
        "page": page,
        "page_size": page_size,
    }


@app.get("/contacts/{contact_id}", response_model=Contact, summary="Get a contact")
def get_contact(contact_id: int):
    return find_contact(contact_id)


@app.post("/contacts", response_model=Contact, status_code=201, summary="Create a contact")
def create_contact(body: ContactCreate):
    return store.add(body.model_dump())


@app.put("/contacts/{contact_id}", response_model=Contact, summary="Update a contact (all fields)")
def update_contact(contact_id: int, body: ContactCreate):
    contact = find_contact(contact_id)
    contact.update(body.model_dump())
    return contact


@app.patch("/contacts/{contact_id}", response_model=Contact, summary="Edit a contact (only sent fields)")
def edit_contact(contact_id: int, body: ContactPatch):
    contact = find_contact(contact_id)
    # exclude_none: fields that were not sent (or sent as null) stay the same
    contact.update(body.model_dump(exclude_none=True))
    return contact


@app.delete("/contacts/{contact_id}", status_code=204, summary="Delete a contact")
def delete_contact(contact_id: int):
    find_contact(contact_id)
    del store.contacts[contact_id]


@app.patch("/contacts/{contact_id}/favorite", response_model=Contact, summary="Toggle favorite")
def toggle_favorite(contact_id: int):
    contact = find_contact(contact_id)
    contact["is_favorite"] = not contact["is_favorite"]
    return contact
