from flask import Blueprint, request, jsonify, send_file
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
    """
    Actualiza la foto de perfil del usuario autenticado.
    ---
    tags:
      - Usuarios
    security:
      - Bearer: []
    consumes:
      - multipart/form-data
    parameters:
      - name: foto
        in: formData
        type: file
        required: true
        description: Archivo de imagen para el perfil.
    responses:
      200:
        description: Foto de perfil actualizada exitosamente.
      400:
        description: Error en el archivo enviado.
      500:
        description: Error interno del servidor.
    """
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
    """
    Obtiene la imagen de perfil de un usuario mediante su email.
    ---
    tags:
      - Usuarios
    parameters:
      - name: email
        in: path
        type: string
        required: true
        description: Correo electrónico del usuario.
    responses:
      200:
        description: Imagen de perfil devuelta correctamente.
        content:
          image/jpeg:
            schema:
              type: string
              format: binary
      404:
        description: Usuario o foto no encontrados.
      500:
        description: Error interno del servidor.
    """
    try:
        usuario = user_repo.get_by_email(email)
        if not usuario or not usuario.get('imagen_ruta'):
            return jsonify({"error": "Usuario o foto de perfil no encontrado"}), 404
        foto_bytes = usuario['imagen_ruta']
        return send_file(io.BytesIO(foto_bytes), mimetype='image/jpeg', as_attachment=False, download_name=f"{email}_foto.jpg")
    except Exception as e:
        return jsonify({"error": str(e)}), 500