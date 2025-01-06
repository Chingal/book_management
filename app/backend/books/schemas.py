from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class BookSchema(BaseModel):
    """
    Schema for representing book data with validation rules.
    """
    title: str = Field(
        ..., title="Title", max_length=200, description="The title of the book"
    )
    author: str = Field(
        ..., title="Author", max_length=100, description="The author of the book"
    )
    published_date: Optional[date] = Field(
        None, title="Published Date", description="The publication date of the book"
    )
    genre: Optional[str] = Field(
        None, title="Genre", max_length=50, description="The genre of the book"
    )
    price: float = Field(
        ..., gt=0, title="Price", description="The price of the book (must be positive)"
    )
    id: Optional[str] = None
