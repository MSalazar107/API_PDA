from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import Database
from repositories.product_repository import ProductRepository
from services.product_service import ProductService

product_bp = Blueprint('products', __name__)

# Instanciamos las capas
db = Database()
product_repo = ProductRepository(db)
product_service = ProductService(product_repo)

@product_bp.route('/nuevo', methods=['POST'])
@jwt_required() # <--- Solo usuarios con Token pueden entrar
def crear():
    data = request.get_json()
    try:
        product_service.registrar_producto(data)
        return jsonify({"mensaje": "Producto guardado correctamente"}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error interno", "detalle": str(e)}), 500

@product_bp.route('/todos', methods=['GET'])
@jwt_required()
def listar():
    productos = product_service.listar_productos()
    return jsonify(productos), 200