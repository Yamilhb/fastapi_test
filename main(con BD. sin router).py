from fastapi import FastAPI, Body, Path, Query, Request,HTTPException, Depends # Path -> para validar parámetros de ruta. Query -> valid parámetros de query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security import HTTPBearer
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field # Field -> para valida datos
from typing import Optional
from user_jwt import createToken, validateToken
from bd.database import Session, engine, Base
from models.movies import Movie as ModelMovie

# APLICACIÓN
app = FastAPI(
    title = 'Aprendiendo FastAPI',
    description = 'Primeros pasos',
    version = '0.0.1'
)

# BASE
Base.metadata.create_all(bind = engine)

# CLASES

# Esta clase la usamos para proteger ruta
class BearerJWT(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validateToken(auth.credentials)
        if data['email'] != 'mail@gmail.com':
            raise HTTPException(status_code=403, detail = 'Credenciales incorrectas')

# Seguridad-autenticación de usuario
class User(BaseModel):
    email: str
    password: str

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


# VAR AUXILIAR
movies = [
    {
        'id': 1,
        'Title': 'El Padrinazo',
        'Year': 1972
    },
    {
        'id': 2,
        'Title': 'Mamabicho',
        'Year': 1959
    },
]


# ENDPOINTS
@app.post('/login', tags=['authentication'])
def login(user:User):
    if user.email == 'mail@gmail.com' and user.password == '1234': # Estamos validando que el usuario esté autenticado para generar el token
        token: str = createToken(user.dict())
        return JSONResponse(content={'message':'Se ha generado el token correctamente: ','TOKEN':token})


@app.get('/', tags = ['Inicio'])
def read_root():
    # return {'Hello': 'World'}
    return HTMLResponse('<h2> Hola Mundo! </h2>')


@app.get('/movies', tags = ['Movies'], dependencies=[Depends(BearerJWT())]) # Esta ruta sólo la verán los usuarios autenticados que generen token válido
def get_movies():
    db = Session()
    data = db.query(ModelMovie).all()
    return JSONResponse(content=jsonable_encoder(data))

# PARÁMETROS DE RUTA
@app.get('/movies/{id}', tags = ['Movies'])
def get_movie(id: int = Path(ge=0, le=100)):
    db = Session()
    data = db.query(ModelMovie).filter(ModelMovie.id == id).first()
    if not data:
        return JSONResponse(status_code=404, content = {'message': 'Recurso no encontrado'})
    return JSONResponse(status_code=200, content = jsonable_encoder(data))

# PARÁMETROS DE QUERY (Buscar por título)
@app.get('/movies/', tags = ['Movies'])
def get_movies_by_title(title: str = Query(min_length = 3)):
    db = Session()
    data = db.query(ModelMovie).filter(ModelMovie.Title == title).all()
    if not data:
        return JSONResponse(status_code = 404, content={'message': 'No se encontró el recurso'})
    return JSONResponse(status_code = 200, content = jsonable_encoder(data))

# POSTEAMOS RECURSO
@app.post('/movies', tags = ['Movies'])
def create_movie(movie: Movie):
    db = Session()
    newMovie = ModelMovie(**movie.to_dict())
    db.add(newMovie)
    db.commit()
    return JSONResponse(content={'message': 'Se ha cargado una nueva película.',
                                 'películas': movie.to_dict()})

# PUT Y DELETE
@app.put('/movies/{id}', tags = ['Movies'])
def update_movies(id: int, movie: Movie):
    db = Session()
    data = db.query(ModelMovie).filter(ModelMovie.id == id).first()
    if not data:
        return JSONResponse(status_code = 404, content={'message': 'No se encontró el recurso'})
    data.Title = movie.Title
    data.Year = movie.Year
#    db.add(data)
    db.commit()
    return JSONResponse(status_code=200, content={'message':' Película modificada correctamente','Películas':jsonable_encoder(data)})

@app.delete('/movies/{id}', tags = ['Movies'])
def delete_movies(id: int):
    db = Session()
    data = db.query(ModelMovie).filter(ModelMovie.id == id).first()
    if not data:
        return JSONResponse(status_code = 404, content={'message': 'No se encontró el recurso'})
    db.delete(data)
    db.commit()
    return JSONResponse(content={'message': 'Se ha borrado la película.',
                                 'Película borrada': jsonable_encoder(data)})
           
            


# POSTEAMOS RECURSO
# Sin la clase de pydantic quedaría así:
# @app.post('/movies', tags = ['Movies'])
# def create_movie(
#     id: int = Body(),
#     Title: str = Body(),
#     Year: int = Body()
#     ):
#     movies.append({
#         'id': id,
#         'Title': Title,
#         'Year': Year
#     })
#     return Title