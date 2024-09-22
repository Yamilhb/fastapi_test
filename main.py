from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from bd.database import engine, Base
from routers.movies import routerMovie
from routers.users import routerUser

# APLICACIÓN
app = FastAPI(
    title = 'Aprendiendo FastAPI',
    description = 'Primeros pasos',
    version = '0.0.1'
)

# RUTAS
app.include_router(routerMovie)
app.include_router(routerUser)

# BASE
Base.metadata.create_all(bind = engine)

# ENDPOINTS
@app.get('/', tags = ['Inicio'])
def read_root():
    # return {'Hello': 'World'}
    return HTMLResponse('<h2> Hola Mundo! </h2>')
