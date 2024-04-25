from datetime import datetime, timedelta

import pytz
from decouple import config
from jwt import encode, decode, exceptions
from flask import jsonify


# Funcion que determina la duracion del token
def expiracionToken(min: int):
    # Obtener la zona horaria actual
    zona_horaria = pytz.timezone('America/Bogota')  # Cambia 'America/Bogota' según tu zona horaria

    # Obtener la fecha y hora actual en la zona horaria especificada
    fecha_actual = datetime.now(tz=zona_horaria)

    # Calcular la fecha de expiración sumando la cantidad de minutos
    fecha_expiracion = fecha_actual + timedelta(minutes=min)

    return fecha_expiracion


# Funcion Crea Token
def crearToken(data: dict):
    token = encode(payload={**data, "exp": expiracionToken(120)}, key=config('SECRET_KEY'), algorithm="HS256")

    formatoUnicode = token.encode("UTF-8")
    encoding = "UTF-8"

    return jsonify(
        {'message': 'Credenciales Correctas', 'token': formatoUnicode.decode(encoding), 'nombre': data['nombre']})


# Funcion Valida Token
def validarToken(token, date):

    try:
        # Decodificar el token
        decoded_token = decode(token, key=config('SECRET_KEY'), algorithms=["HS256"])

        # Si date es verdadero, solo verifica la validez del token sin verificar la fecha de expiración
        if date:
            return decoded_token

        # Si date es falso, verifica también la fecha de expiración del token
        else:
            return True

    except exceptions.DecodeError:
        # Token inválido
        response = jsonify({"message": "Invalid Token", "Authorization": False})
        response.status_code = 401
        return response

    except exceptions.ExpiredSignatureError:
        # Token expirado
        response = jsonify({"message": "Token Expired", "Authorization": False})
        response.status_code = 401
        return response
