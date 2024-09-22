from fastapi import FastAPI, Body, Path, Query, Request,HTTPException, Depends # Path -> para validar parámetros de ruta. Query -> valid parámetros de query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security import HTTPBearer
from pydantic import BaseModel, Field # Field -> para valida datos
from typing import Optional
from user_jwt import createToken, validateToken


# APLICACIÓN
app = FastAPI(
    title = 'Aprendiendo FastAPI',
    description = 'Primeros pasos',
    version = '0.0.1'
)

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

@app.get('/movies', tags = ['Movies'], dependencies=[Depends(BearerJWT())]) # Esta ruta sólo la verán los usuarios autenticados que generen token válido
def get_movies():
    return movies

# PARÁMETROS DE RUTA
@app.get('/movies/{id}', tags = ['Movies'])
def get_movie(id: int = Path(ge=0, le=100)):
    for items in movies:
        if items['id'] == id:
            return items

# PARÁMETROS DE QUERY
@app.get('/movies/', tags = ['Movies'])
def get_movies_by_title(title: str = Query(min_length = 3)):
    return title

# POSTEAMOS RECURSO
@app.post('/movies', tags = ['Movies'])
def create_movie(movie: Movie):
    movies.append(movie)
    return JSONResponse(content={'message': 'Se ha cargado una nueva película.',
                                 'películas': movie.to_dict()})

# PUT Y DELETE
@app.put('/movies/{id}', tags = ['Movies'])
def update_movies(
    id: int,
    movie: Movie
    ):
    for mv in movies:
        if mv["id"] == id:
            mv['Title'] = movie.Title
            mv['Year'] = movie.Year
    return movies

@app.delete('/movies/{id}', tags = ['Movies'])
def delete_movies(id: int):
    for mv in movies:
        if mv["id"] == id:
            movies.remove(mv)
    return JSONResponse(content={'message': 'Se ha borrado la película. Las películas presentes son:',
                                 'películas': [dict(x) for x in movies]})
           
            


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