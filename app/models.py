"""Request and response schemas. FastAPI uses them for validation and Swagger docs."""

from typing import List, Optional

from pydantic import BaseModel, Field


class ContactCreate(BaseModel):
    """Body for POST /contacts and PUT /contacts/{id}."""

    first_name: str = Field(..., min_length=1, max_length=50, examples=["Alan"])
    last_name: str = Field(..., min_length=1, max_length=50, examples=["Turing"])
    # Simple email format check: something@something.something
    email: Optional[str] = Field(None, pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$",
                                 examples=["alan.turing@example.com"])
    phone: Optional[str] = Field(None, max_length=25, examples=["+1 555 123 4567"])
    tags: List[str] = Field(default_factory=list, examples=[["Work"]])
    is_favorite: bool = False


class ContactPatch(BaseModel):
    """Body for PATCH /contacts/{id}. Every field is optional."""

    first_name: Optional[str] = Field(None, min_length=1, max_length=50)
    last_name: Optional[str] = Field(None, min_length=1, max_length=50)
    email: Optional[str] = Field(None, pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
    phone: Optional[str] = Field(None, max_length=25)
    tags: Optional[List[str]] = None
    is_favorite: Optional[bool] = None


class Contact(ContactCreate):
    """A contact as returned by the API."""

    id: int


class ContactList(BaseModel):
    """One page of contacts."""

    items: List[Contact]
    total: int
    page: int
    page_size: int
