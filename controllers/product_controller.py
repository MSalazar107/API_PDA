from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import Database
from repositories.product_repository import ProductRepository
from repositories.product_repository import ProductRepository
from services.product_service import ProductService

product_bp = Blueprint('products', __name__)


db = Database()
product_repo = ProductRepository(db)
product_service = ProductService(product_repo)

@product_bp.route('/nuevo', methods=['POST'])
@jwt_required() 
def crear():
    try:
        foto = request.files.get('foto')
        data = {
            "codigo": request.form.get('codigo'),
            "descripcion": request.form.get('descripcion'),
            "precio": request.form.get('precio'),
            "existencias": request.form.get('existencias'),
            "unidad_fk": request.form.get('unidad_fk'),
            "imagen_producto_ruta": foto.read() if foto else None
        }
        
        exito = product_repo.create(data)
        if exito:
            return jsonify({"mensaje": "Producto registrado con éxito"}), 201
        return jsonify({"error": "No se pudo guardar en la base de datos"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500