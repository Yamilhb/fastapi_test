# Estructura de JWT: (autenticar y autorizar)
# HEADER: Contiene tipo token y algoritmo que se utiliza.
# PAYLOAD: Información del usuario (id, nombre, mail, roles, etc)
# SIGNATURE: La firma que se crea usando Header + Payload + secret key.

import jwt

def createToken(data: dict):
    token: str = jwt.encode(payload=data, key='importo_clave_secreta', algorithm='HS256')
    return token

# Con esto validamos que el token sea correcto
def validateToken(token: str) -> dict: 
    data: dict = jwt.decode(token, key='importo_clave_secreta', algorithms=['HS256'])
    return data