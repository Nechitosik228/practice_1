from pydantic import BaseModel,field_validator
from db import Config,Book
import re
from sqlalchemy import select



Session=Config.SESSION

class CreateBook(BaseModel):
    name:str
    author:str
    release_year:int
    genre:str
    isbn:str

    @field_validator("release_year")
    @classmethod
    def check_model(cls,y:int):
        if y > 2024:
            raise ValueError("Release year cannot be in future")
        return y

    @field_validator("isbn")
    @classmethod
    def check_isbn(cls,i:str):
        if not re.match("^(?=(?:[^0-9]*[0-9]){10}(?:(?:[^0-9]*[0-9]){3})?$)[\\d-]+$",i):
            raise ValueError("Invalid isbn")
        with Session() as session:
            book=session.scalar(select(Book).where(Book.isbn==i))
            if book:
                raise ValueError("Book with this isbn exists")
        return i
    





