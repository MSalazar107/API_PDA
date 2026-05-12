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
caja_repo= CajaRepository(datab)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email', None)
    contrasena = data.get('contrasena', None)
    num_caja = data.get('num_caja')
    
    if not email or not contrasena:
        return jsonify({"error": "Email y contraseña son requeridos"}), 400
    
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