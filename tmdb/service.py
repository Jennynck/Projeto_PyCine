import os
from typing import List
from dotenv import load_dotenv, find_dotenv
from fastapi import Query
import requests
from rich import print

load_dotenv(find_dotenv(".env"))
TOKEN = os.environ["TMDB_TOKEN"]
from models import Genre, Movie, Person

def get_json(url: str, params: dict = None) -> dict:
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {TOKEN}"
    }
    data = requests.get(url, headers=headers, params=params)
    return data.json()

class MovieService:
    def get_top_rated(page:int = 1) -> list[Movie]:
        """
        Obtem a lista de filmes melhores rankeados
            endpoint: /movie/top_rated
        """
        url = "https://api.themoviedb.org/3/movie/top_rated"
        params = {
            "language": "en-US",
            "page": page
        }
        data = get_json(url, params)
        results = data['results']
        movies = [Movie.model_validate(m) for m in results ]
        return movies
    
    @staticmethod
    def find_by_id(id: int) -> Movie:
        """ dados do filme pelo id """

        url = f"https://api.themoviedb.org/3/movie/{id}"
        params = {
            "language": "en-US"
        }
        movie = get_json(url, params)
        movie = Movie.model_validate(movie)
        return movie

    @staticmethod
    def discovery_movies(
        title: str | None = None,
        genre_id: int | None = None, 
        year: int | None = None,
        sort_by: str | None = None,
        page: int = 1
    ) -> List[Movie]:

        # Define a URL correta
        url = "https://api.themoviedb.org/3/search/movie" if title else "https://api.themoviedb.org/3/discover/movie"

        params = {
            "language": "en-US",
            "page": page
        }

        # Filtro por título
        if title:
            params["query"] = title

        # Filtro por gênero
        if genre_id:
            params["with_genres"] = str(genre_id)

        # Filtro por ano
        if year:
            params["primary_release_year"] = year
            
        # Validação para verificar se o ano é válido
        if year is not None and (year < 1900 and year > 2090):
            return {"error": "Nenhum filme encontrado"}

        # Filtro por popularidade asc desc

        data = get_json(url, params)
        results = data.get("results", [])

        if not results:
            return {"error": "Nenhum filme encontrado"}

        movies = [Movie.model_validate(m) for m in results]

        # Ordenação feita após os filmes serem carregados
        if sort_by:
            reverse = sort_by.lower() == "desc"
            movies = sorted(movies, key=lambda m: m.popularity, reverse=reverse)

        return movies
    
    @staticmethod
    def get_genres() -> List[Genre]:
        url = "https://api.themoviedb.org/3/genre/movie/list"
        params = {
            "language": "pt-BR"
        }
        
        data = get_json(url, params=params)
        genres = [Genre.model_validate(g) for g in data.get("genres", [])]

        return genres
    
class PersonService:
    @staticmethod
    def person_by_id(id: int) -> Person:
        url = f"https://api.themoviedb.org/3/person/{id}"
        params = {
            "language": "en-US"
        }
        person = get_json(url, params)
        person = Person.model_validate(person)
        return person
    
    @staticmethod
    def find_by_name(name: str) -> list [Person]:
        url = f"https://api.themoviedb.org/3/search/person"
        params = {
            "query": name,
            "language": "en-US",
        }

        data = get_json(url, params)
        results = data.get('results', [])
        persons = [Person.model_validate(p) for p in results ]
        return persons

    def get_popular(page: int = 1) -> list [Person]:
        url = "https://api.themoviedb.org/3/person/popular"
        params = {
            "language": "en-US",
            "page": page
        }

        data = get_json(url, params)
        results = data['results']
        persons = [Person.model_validate(p) for p in results ]
        return persons

    def get_films_person(person_id: int) -> list [Movie]:
        url = f"https://api.themoviedb.org/3/person/{person_id}/movie_credits"
        params = {
            "language": "en-US"
        }

        data = get_json(url, params)
        cast = data.get('cast', [])
        movies_person = [Movie.model_validate(m) for m in cast ]
        return movies_person
    
    def get_person_trending(time_window: str, page: int = 1) -> list [Person]:
        url = f"https://api.themoviedb.org/3/trending/person/{time_window}"
        params = {
            "language": "en-US",
            "page": page
        }

        data = get_json(url, params)
        results = data.get('results', [])
        persons_trending = [Person.model_validate(m) for m in results]
        return persons_trending



    # url = "https://api.themoviedb.org/3/person/480/movie_credits?language=en-US" 
    # para fazer a rota que exibe os filmes que um artista fez
    
# print(get_top_movies())