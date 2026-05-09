from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from db import Database
from repositories.user_repository import UserRepository
from services.user_service import UserService
from werkzeug.security import check_password_hash

auth_bp = Blueprint('auth', __name__)

datab = Database()
user_repo = UserRepository(datab)
auth_service = UserService(user_repo)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email', None)
    contrasena = data.get('contrasena', None)
    
    if not email or not contrasena:
        return jsonify({"error": "Email y contraseña son requeridos"}), 400
    
    # Aquí deberías validar el email y contraseña con la base de datos
    # Por simplicidad, vamos a asumir que cualquier email/contraseña es válido
    # En un caso real, deberías verificar el hash de la contraseña almacenada
    
    conn = datab.connect()
    cur = conn.cursor()
    cur.execute("SELECT contrasena FROM USUARIO WHERE email = %s", (email,))
    row =cur.fetchone()
    cur.close()
    conn.close()
    
    if not row:
        return jsonify({"error": "Usuario no encontrado"}), 401
    
    stored_password = row[0]
    
    if not check_password_hash(stored_password, contrasena):
        return jsonify({"error": "Contraseña incorrecta"}), 401 
    
    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token), 200

@auth_bp.route('/register', methods=['POST'])
def registro():
    data = request.get_json()
    try:
        
        nuevo_usuario = auth_service.create_Usuario(data)
        return jsonify({"mensaje": "Usuario registrado exitosamente",
                        "usuario": nuevo_usuario.email}), 201
        
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    
    except Exception as e:
        # Importamos esta herramienta rápida para imprimir el error real
        import traceback
        traceback.print_exc() 
        
        # Le regresamos a Postman el error con más detalle
        return jsonify({"error": f"Error interno del servidor: {str(e)}"}), 500