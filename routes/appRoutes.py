from flask import Blueprint, request, jsonify
from databases.db_mysql import get_connection
from utils.webToken import crearToken, validarToken
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from pymysql import err

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
        "SELECT * FROM tb_usuario_register WHERE correo = '{}' and tb_usuario_register.estado = 'Activo'".format(
            correo))

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

            'id': result[0], 'nombre': result[1], 'correo': result[2],

        }

        return crearToken(dataParaToken)


@routes_auth.route('/verificarToken', methods=['GET'])
def verificarToken():
    token = request.headers['Authorization'].split(" ")[1]

    validacion = validarToken(token, False)

    if validacion:
        return jsonify({"message": "Token success", "Authorization": True})

    else:
        return validacion


@routes_auth.route('/register', methods=['POST'])
def register():
    dat = request.get_json()
    nombre = dat['nombre']
    correo = dat['correo']
    contrasena = dat['contrasena']

    token = request.headers['Authorization'].split(" ")[1]
    validacion = validarToken(token, False)

    ## si el token es valido
    if validacion:

        datosToken = validarToken(token, True)

        try:
            fecha_creacion = datetime.now()
            nombre = dat['nombre']
            correo = dat['correo']
            contra_encriptado = generate_password_hash(dat['contraseña'], 'pbkdf2:sha256', 30)
            estado = 'Activo'

            conn = get_connection()
            cur = conn.cursor()

            print(fecha_creacion)

            cur.execute("""INSERT INTO tb_usuario_register (nombre, correo, contrasena, fecha_creacion, estado) VALUES ('{}', '{}', '{}', '{}', '{}' )""".format(nombre, correo, contra_encriptado, fecha_creacion, estado))

            # cerramos la conexion a la bd
            conn.commit()
            cur.close()
            conn.close()

            return jsonify({"message": "El usuario se ha creado con exito"})

        except err.IntegrityError as er:

            # organizamos y limpiamos el error
            error = format(er).replace('(', '').replace(')', '').replace('/', '').replace('"', '').split(',')

            if error[0] == '1062':
                response = jsonify({'message': 'Este usuario ya existe', 'numErro': error[0]})
                response.status_code = 400
                return response

            ## Quitamos caracteres innecesarios
            response = jsonify({'message': error[1], 'numErro': error[0]})
            response.status_code = 400
            return response

    else:
        return validacion
