from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from db import Database
from repositories.user_repository import UserRepository
from repositories.caja_repository import CajaRepository
from services.user_service import UserService
from werkzeug.security import check_password_hash

auth_bp = Blueprint('auth', __name__)

datab = Database()
user_repo = UserRepository(datab)
auth_service = UserService(user_repo)
caja_repo = CajaRepository(datab)

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Inicio de sesión para obtener token de acceso.
    ---
    tags:
      - Autenticación
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - email
            - contrasena
            - num_caja
          properties:
            email:
              type: string
              example: usuario@punto.com
            contrasena:
              type: string
              example: 123456
            num_caja:
              type: integer
              example: 1
    responses:
      200:
        description: Autenticación exitosa.
        schema:
          properties:
            access_token:
              type: string
      400:
        description: Datos faltantes o caja no habilitada.
      401:
        description: Credenciales incorrectas o usuario inexistente.
    """
    data = request.get_json()
    email = data.get('email', None)
    contrasena = data.get('contrasena', None)
    num_caja = data.get('num_caja')
    
    if not email or not contrasena:
        return jsonify({"error": "Email y contraseña son requeridos"}), 400
    
    conn = datab.connect()
    cur = conn.cursor()
    cur.execute("SELECT contrasena FROM USUARIO WHERE email = %s", (email,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    
    if not row:
        return jsonify({"error": "Usuario no encontrado"}), 401
    
    stored_password = row[0]
    
    if not check_password_hash(stored_password, contrasena):
        return jsonify({"error": "Contraseña incorrecta"}), 401 
    
    caja = caja_repo.get_by_id(num_caja)
    
    if not caja:
        return jsonify({"error": f"La caja {num_caja} no está habilitada"}), 400
    
    access_token = create_access_token(
        identity=email, 
        additional_claims={"num_caja": num_caja} 
    )
    
    return jsonify(access_token=access_token), 200

@auth_bp.route('/register', methods=['POST'])
def registro():
    """
    Registro de un nuevo usuario con perfil completo.
    ---
    tags:
      - Autenticación
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - email
            - contrasena
            - nombre
          properties:
            nombre:
              type: string
              example: "Carlos"
            apellidos:
              type: string
              example: "Rodriguez Garza"
            email:
              type: string
              example: "carlos.mty@ejemplo.mx"
            contrasena:
              type: string
              example: "Segura_2026!"
            fecha_nac:
              type: string
              example: "1998-10-24"
            alias:
              type: string
              example: "Charly"
            telefono:
              type: string
              example: "8112345678"
            direccion:
              type: string
              example: "Colonia Centro, Monterrey"
    responses:
      201:
        description: Usuario registrado exitosamente.
      400:
        description: Error en los datos proporcionados.
    """
    data = request.get_json()
    try:
        nuevo_usuario = auth_service.create_Usuario(data)
        return jsonify({"mensaje": "Usuario registrado exitosamente",
                        "usuario": nuevo_usuario.email}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        import traceback
        traceback.print_exc() 
        return jsonify({"error": f"Error interno del servidor: {str(e)}"}), 500