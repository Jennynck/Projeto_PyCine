from datetime import date
from typing import List
from pydantic import BaseModel, computed_field

class User(BaseModel):
   id: int
   name: str
   email: str
   # campo opicional
   avatar: str | None = None

class Movie(BaseModel):
   id: int
   original_title: str
   genre_ids: list | None = None
   overview: str
   popularity: float
   poster_path: str | None = None
   title: str
   release_date: str
   vote_average: float
   vote_count: int

   @computed_field
   @property
   def poster_url(self) -> str:
      return f"http://image.tmdb.org/t/p/w185{self.poster_path}"

class Genre(BaseModel):
   id: int
   name: str
   
   @computed_field
   @property
   def label(self) -> str:
      return self.name.replace(" ","-").lower()

class Person(BaseModel):
   id: int
   name: str
   gender: int | None = None
   popularity: float | None = None
   known_for_department: str | None = None
   profile_path: str | None = None

   @computed_field
   @property
   def profile_url(self) -> str:
      return f"http://image.tmdb.org/t/p/w185{self.profile_path}"
   
class MovieCollection(BaseModel):
    movies: List[Movie]
