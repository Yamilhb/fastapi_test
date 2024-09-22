from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel # Field -> para valida datos
from user_jwt import createToken


routerUser = APIRouter()

# CLASES
# Seguridad-autenticación de usuario
class User(BaseModel):
    email: str
    password: str



# ENDPOINTS
@routerUser.post('/login', tags=['authentication'])
def login(user:User):
    if user.email == 'mail@gmail.com' and user.password == '1234': # Estamos validando que el usuario esté autenticado para generar el token
        token: str = createToken(user.dict())
        return JSONResponse(content={'message':'Se ha generado el token correctamente: ','TOKEN':token})

