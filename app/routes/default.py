from . import app
from db import Config,Book
from ..schemas import CreateBook


Session=Config.SESSION


@app.post("/books",status_code=201)
def create_book(data:CreateBook):
    with Session.begin() as session:
        book=Book(**data.model_dump())
        session.add(book)
        return book