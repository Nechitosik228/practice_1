from pydantic import BaseModel,model_validator
from datetime import datetime
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

    @model_validator(mode="after")
    def check_model(self):
        if self.release_year > 2024:
            raise ValueError("Release year cannot be in future")
        if not re.match("^(?=(?:[^0-9]*[0-9]){10}(?:(?:[^0-9]*[0-9]){3})?$)[\\d-]+$",self.isbn):
            raise ValueError("ISBN is not valid")
        with Session() as session:
            book=session.scalar(select(Book).where(Book.isbn==self.isbn))
            if book:
                raise ValueError("Book with this isbn exists")
        return self


