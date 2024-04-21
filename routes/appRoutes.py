from flask import Blueprint, request, jsonify
from databases.db_mysql import get_connection
from utils.webToken import crearToken, validarToken
from werkzeug.security import generate_password_hash, check_password_hash

routes_auth = Blueprint('routes_auth', __name__)


@routes_auth.route('/login', methods=['POST'])
def loginRoute():
    # traemos todos los datos mandados en el body
    user = request.get_json()
    # especificamos en el correo y contraseña para hacer la comparacion en la bd
    correo = user['correo']
    contrasena = user['contrasena']

    # abrimos la conexion a la bd
    conn = get_connection()
    cur = conn.cursor()
    # generamos la consulta
    cur.execute(
        "SELECT * FROM tb_usuario_register WHERE correo = '{}' and tb_usuario_register.estado = 'Activo'".format(correo))

    result = cur.fetchone()

    if result is None or result == ():
        response = jsonify({'message': 'Correo o Contraseña incorrecta y/o usuario inactivado'})
        response.status_code = 401
        return response

    # cerramos la conexion a la bd
    conn.commit()
    cur.close()
    conn.close()

    validacionContrasena = check_password_hash(result[3], contrasena)

    # si el resultado es none no existe este usuario en la bd

    if not validacionContrasena:
        # retornamos mensanje
        response = jsonify({'message': 'Correo o Contraseña incorrecta'})
        response.status_code = 401
        return response
    else:
        # si el usuario existe creamos el token

        # pasamos de tupla a diccionario
        dataParaToken: dict = {

            'id': result[0],
            'nombre': result[1],
            'correo': result[2],

        }

        return crearToken(dataParaToken)
