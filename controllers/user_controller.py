from flask import Blueprint, request, jsonify,send_file
import io
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import Database
from repositories.user_repository import UserRepository
from services.user_service import UserService

user_bp = Blueprint('users', __name__)

db = Database()
user_repo = UserRepository(db)
user_service = UserService(user_repo)

@user_bp.route('/foto', methods=['PUT'])
@jwt_required()
def subir_foto():
    email = get_jwt_identity()
    subir_foto = request.files.get('foto')
    
    try:
        user_service.actualizar_foto_perfil(email, subir_foto)
        return jsonify({"mensaje": "Foto de perfil actualizada exitosamente"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error interno del servidor"}), 500

@user_bp.route('/<email>/foto', methods=['GET'])
def ver_foto_usuario(email):
    try:
        usuario =user_repo.get_by_email(email)
        if not usuario or not usuario.get('imagen_ruta'):
            return jsonify({"error": "Usuario o foto de perfil no encontrado"}), 404
        foto_bytes = usuario['imagen_ruta']
        return send_file(io.BytesIO(foto_bytes), mimetype='image/jpeg', as_attachment=False, download_name=f"{email}_foto.jpg")
    except Exception as e:
        return jsonify({"error": str(e)}), 500  