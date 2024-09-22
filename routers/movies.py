from fastapi import Path, Query, Request,HTTPException, Depends, APIRouter # Path -> para validar parámetros de ruta. Query -> valid parámetros de query
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer
from fastapi.encoders import jsonable_encoder

from pydantic import BaseModel, Field # Field -> para valida datos

from typing import Optional
from user_jwt import validateToken
from bd.database import Session
from models.movies import Movie as ModelMovie

routerMovie = APIRouter()


# CLASES

# Esta clase la usamos para proteger ruta
class BearerJWT(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validateToken(auth.credentials)
        if data['email'] != 'mail@gmail.com':
            raise HTTPException(status_code=403, detail = 'Credenciales incorrectas')
# Clase para validación de datos
class Movie(BaseModel):
    id: Optional[int] = Field(default=None)
    Title: str = Field(default='Poneeeele título boludo', min_length = 3)
    Year: int = Field(ge=1956)

    def to_dict(self):
        return {
            'id': self.id,
            'Title': self.Title,
            'Year': self.Year
        }


# ENDPOINTS
@routerMovie.get('/movies', tags = ['Movies'], dependencies=[Depends(BearerJWT())]) # Esta ruta sólo la verán los usuarios autenticados que generen token válido
def get_movies():
    db = Session()
    data = db.query(ModelMovie).all()
    return JSONResponse(content=jsonable_encoder(data))

@routerMovie.get('/movies/{id}', tags = ['Movies'])
def get_movie(id: int = Path(ge=0, le=100)):
    db = Session()
    data = db.query(ModelMovie).filter(ModelMovie.id == id).first()
    if not data:
        return JSONResponse(status_code=404, content = {'message': 'Recurso no encontrado'})
    return JSONResponse(status_code=200, content = jsonable_encoder(data))

@routerMovie.get('/movies/', tags = ['Movies'])
def get_movies_by_title(title: str = Query(min_length = 3)):
    db = Session()
    data = db.query(ModelMovie).filter(ModelMovie.Title == title).all()
    if not data:
        return JSONResponse(status_code = 404, content={'message': 'No se encontró el recurso'})
    return JSONResponse(status_code = 200, content = jsonable_encoder(data))

@routerMovie.post('/movies', tags = ['Movies'])
def create_movie(movie: Movie):
    db = Session()
    newMovie = ModelMovie(**movie.to_dict())
    db.add(newMovie)
    db.commit()
    return JSONResponse(content={'message': 'Se ha cargado una nueva película.',
                                 'películas': movie.to_dict()})

@routerMovie.put('/movies/{id}', tags = ['Movies'])
def update_movies(id: int, movie: Movie):
    db = Session()
    data = db.query(ModelMovie).filter(ModelMovie.id == id).first()
    if not data:
        return JSONResponse(status_code = 404, content={'message': 'No se encontró el recurso'})
    data.Title = movie.Title
    data.Year = movie.Year
    db.commit()
    return JSONResponse(status_code=200, content={'message':' Película modificada correctamente','Películas':jsonable_encoder(data)})

@routerMovie.delete('/movies/{id}', tags = ['Movies'])
def delete_movies(id: int):
    db = Session()
    data = db.query(ModelMovie).filter(ModelMovie.id == id).first()
    if not data:
        return JSONResponse(status_code = 404, content={'message': 'No se encontró el recurso'})
    db.delete(data)
    db.commit()
    return JSONResponse(content={'message': 'Se ha borrado la película.',
                                 'Película borrada': jsonable_encoder(data)})
           
            
