from sqlalchemy.orm import Mapped,mapped_column
from . import Config

Base=Config.BASE

class Book(Base):
    __tablename__="books"


    id:Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str]
    author:Mapped[str]
    release_year:Mapped[int]
    genre:Mapped[str]
    isbn:Mapped[str]