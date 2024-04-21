from datetime import datetime, timedelta
from decouple import config
from jwt import encode, decode, exceptions
from flask import jsonify


# Funcion que determina la duracion del token
def expiracionToken(minute: int):
    # la duracion del token es 3 horas
    dateNow = datetime.now()

    dateExpiration = dateNow + timedelta(minutes=minute)

    print(dateExpiration)
    return dateExpiration


# Funcion Crea Token
def crearToken(data: dict):
    token = encode(payload={**data, "exp": expiracionToken(180)}, key=config('SECRET_KEY'), algorithm="HS256")

    formatoUnicode = token.encode("UTF-8")
    encoding = "UTF-8"

    return jsonify({'message': 'Credenciales Correctas',
                    'token': formatoUnicode.decode(encoding),
                    'nombre': data['nombre']})


# Funcion Valida Token
def validarToken(token, date):

    if date:
        return decode(token, key=config('SECRET_KEY'), algorithm="HS256")

    else:
        try:
            decode(token, key=config('SECRET_KEY'), algorithms=["HS256"])
            return True

        # En caso de que el token no sea valido
        except exceptions.DecodeError:
            response = jsonify({"message": "Invalid Token", "Authorization": False})
            response.status_code = 401
            return response

        # En caso de que el token expire
        except exceptions.ExpiredSignatureError:
            response = jsonify({"message": "Token Expired", "Authorization": False})
            response.status_code = 401
            return response
