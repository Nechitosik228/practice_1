from unittest import main,TestCase
from pydantic import BaseModel,field_validator
from db import Config,Book,migrate
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
            return ValueError
        return y

    @field_validator("isbn")
    @classmethod
    def check_isbn(cls,i:str):
        if not re.match("^(?=(?:[^0-9]*[0-9]){10}(?:(?:[^0-9]*[0-9]){3})?$)[\\d-]+$",i):
            return ValueError
        with Session() as session:
            book=session.scalar(select(Book).where(Book.isbn==i))
            if book:
                return ValueError
        return i
    


class TestModel(TestCase):

    def test_model(self):
        migrate()
        model = CreateBook(name="Nikita",author="Vasya",release_year=2024,genre="roman",isbn="786-987-0769-434")
        data = {"name":"Nikita",
                "author":"Vasya",
                "release_year":2024,
                "genre":"roman",
                "isbn":"786-987-0769-434"}
        model_data = {"name":model.name,
                     "author":model.author,
                     "release_year":model.release_year,
                     "genre":model.genre,
                     "isbn":model.isbn}
        self.assertEqual(model_data,data)


    def test_release_year(self):
        resp=CreateBook(name="Nikita",author="Vasya",release_year=2025,genre="roman",isbn="786-987-0769-439")
        self.assertEqual(resp.release_year,ValueError)

    def test_isbn(self):
        with Session.begin() as session:
            book = Book(name="Nikita",author="Vasya",release_year=2024,genre="roman",isbn="786-987-0769-432")
            session.add(book)
        test_1=CreateBook(name="Nikita",author="Vasya",release_year=2024,genre="roman",isbn="786-987-0769-432")
        test_2=CreateBook(name="Nikita",author="Vasya",release_year=2024,genre="roman",isbn="786-987-0769-43")
        self.assertEqual(test_1.isbn,ValueError)
        self.assertEqual(test_2.isbn,ValueError)
    
    

if __name__ == "__main__":
    main()

            