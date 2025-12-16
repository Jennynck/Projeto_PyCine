from fastapi import FastAPI, Query, status, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import models

from models import Genre
from tmdb.service import MovieService, PersonService


app = FastAPI()
# -------------------------------------
import motor
from motor import motor_asyncio
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv(".env"))
TMDB_KEY = os.environ["TMDB_TOKEN"]
# carrega credenciais de acesso ao cloud atlas:
db_url = os.environ["MONGODB_URL"] 
client = motor.motor_asyncio.AsyncIOMotorClient(db_url)
# db => objeto representa a base de dados pycine
db = client.sample_mflix  # <= nome do database
# -------------------------------------

"""
BACKEND (SERVIDOR)
"""
origins = [
   "http://localhost",
   "http://localhost:*",
   "http://localhost:5173",
]

app.add_middleware(
   CORSMiddleware,
   allow_origins=origins,
   allow_credentials=True,
   allow_methods=["*"],
   allow_headers=["*"],
)


@app.get("/")
def hello():
    return {"mensagem": "Web IV"}


@app.get("/mflix/users/find")
async def mflix_list_users():
    """ base de dados: sample_mflix | collection: users """
    collection = db.get_collection("users")
    results = await collection.find().to_list(20)
    results = [user['name'] for user in results]
    return results


@app.get("/mflix/movies/find")
async def mflix_find_movies(max_rows: int=5):
    """ base de dados: sample_mflix | colection: movies """
    collection = db.get_collection("movies")
    # Seleciona apenas os campos: title e year
    # results = await collection.find({}, {"title": 1, "year": 1, "_id": 0}).to_list(max_rows)
    # Todos os campos (exceto _id)
    # SELECT * from movies LIMIT 5
    
    # TODO: "$gt"
    # SELECT * from movies LIMIT 5 WHERE year > 1910
    query = {"year": {"$gt": 1910}}
    projection = {"_id": 0, "title": 1, "year": 1}

    results = await collection.find(query, projection).to_list(max_rows)

    return results


@app.post("/mflix/users/save",
    status_code=status.HTTP_201_CREATED,
)
async def save_user(user: dict = Body(...)):
    """ adiciona um novo usuario na collection users """
    collection = db.get_collection("users")
    # INSERT INTO users values...
    created_user = await collection.insert_one(user)
    print("result %s" % repr(created_user.inserted_id)) # printa o id gerado
    # faz uma consulta para obter o usuario adicionado
    user_added = await collection.find_one({"_id": created_user.inserted_id}, {"_id": 0})
    return user_added  # <= retorna o novo usuario 

@app.get(
   "/find/",
    response_description="List all movies",
    response_model=models.MovieCollection,
    response_model_by_alias=False,
)
async def list_movies():
    movies_collection = db.get_collection("movies")
    return models.MovieCollection(movies=await movies_collection.find().to_list(20))


@app.post("/quotes/save",
    status_code=status.HTTP_201_CREATED,
)
async def save_quote(quote: models.Movie = Body(...)):
    # pega a collection correta no MongoDB
    movies_collection = db.get_collection("quotes")
    
    # insere o documento no banco
    new_quote = await movies_collection.insert_one(quote.model_dump())
    
    # busca o documento inserido para retornar ao front
    created_quote = await movies_collection.find_one(
        {"_id": new_quote.inserted_id}
    )
    
    return created_quote

@app.get("/discover/movie")
def discover_movie(
    title: str = None,
    genre_id: int = None,
    year: int = None,
    popularidade_asc_desc: str = None,
):
    movies = MovieService.discovery_movies(title, genre_id, year, popularidade_asc_desc)
    if not movies:
        return [{"message": "Nenhum filme encontrado"}]
    return movies

@app.get("/genres")
def get_genres():
    return MovieService.get_genres()

#----------------------------- Rotas GET, POST, DELETE - Atividade 6 ------------------------

@app.get("/favorites/person")
async def list_favorites():
    artistas_favoritos = db.get_collection("artistas_favoritos")
    return await artistas_favoritos.find({"known_for_department": "Acting"}, {"_id": 0}).to_list(100)

@app.post("/favorites/person", status_code=status.HTTP_201_CREATED)
async def save_favorite_person(person: dict):
    artistas_favoritos = db.get_collection("artistas_favoritos")

    # Pega o id enviado no body
    person_id = person.get("id")

    # Evita duplicados
    existe = await artistas_favoritos.find_one({"id": person_id})
    if existe:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail="Este artista já está na sua lista de favoritos"
        )

    # Insere o próprio dicionário enviado no body
    result = await artistas_favoritos.insert_one(person)

    # Retorna o artista salvo sem _id
    created = await artistas_favoritos.find_one({"_id": result.inserted_id}, {"_id": 0})

    return created

@app.delete("/favorites/person/{person_id}")
async def delete_favorite_person(person_id: int):
    """
    Deleta um artista favorito do banco de dados usando o seu id
    """

    artistas_favoritos = db.get_collection("artistas_favoritos")
    result = await artistas_favoritos.delete_one({"id": person_id})
    
    if result.deleted_count == 0:
        # Se nada foi deletado é porque o id não foi encontrado
        raise HTTPException(status_code=404, detail="Artista favorito não encontrado")
        
    # Retorna sucesso
    return {"status": "removido com sucesso", "deleted_count": result.deleted_count}

# -----------------------------------------------------------------------------------------

@app.get("/now")
def datetime_now():
    from datetime import datetime
    return {
        "datahora": datetime.now(),
        "pais": "BR"
    }

@app.get("/movies/top")
def get_top_ranked_movies():
    from tmdb.service import MovieService
    movies = MovieService.get_top_rated()
    # movies = MovieService.get_top_rated(page=2)
    return movies

@app.get("/movie/{id}")
def get_movie(id: int):
    from tmdb.service import MovieService
    movie = MovieService.find_by_id(id)
    return movie

@app.get("/person/{id}")
def get_person(id: int):
    from tmdb.service import PersonService
    person = PersonService.person_by_id(id)
    return person

@app.get("/person/name/{name}")
def get_name(name: str, page: int = 1):
    from tmdb.service import PersonService
    person = PersonService.find_by_name(name, page=page)
    return person

@app.get("/persons/popular")
def get_popular_persons(page: int = 1):
    from tmdb.service import PersonService
    persons = PersonService.get_popular(page=page) 
    return persons

@app.get("/person/movies/{person_id}")
def get_person_movies(person_id: int):
    from tmdb.service import PersonService
    movies_p = PersonService.get_films_person(person_id)
    return movies_p

@app.get("/persons/trending/{time_window}")
def get_persons_trending(time_window: str):
    from tmdb.service import PersonService
    persons_trending = PersonService.get_person_trending(time_window)
    return persons_trending

# iniciar o servidor pelo terminal:
# uvicorn main:app --reload