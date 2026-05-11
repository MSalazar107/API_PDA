from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from db import Database
from repositories.sale_repository import SaleRepository
from repositories.product_repository import ProductRepository
from services.sale_service import SaleService

venta_bp = Blueprint('venta', _name_)

db = Database()
sale_repo = SaleRepository(db)
product_repo = ProductRepository(db)
sale_service = SaleService(sale_repo, product_repo)

@venta_bp.route('/nueva', methods=['POST'])
@jwt_required()
def registrar_venta():
    claims = get_jwt()
    numero_caja = claims.get('num_caja')
    data = request.get_json()

    if not numero_caja:
        return jsonify({"error": "El token no contiene un número de caja válido"}), 400

    try:
        venta_completada = sale_service.procesar_venta(data, numero_caja)
        
        return jsonify({
            "mensaje": "Venta registrada exitosamente",
            "ticket": venta_completada
        }), 201

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({
            "error": "Error interno del servidor",
            "detalle": str(e)
        }), 500