from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from db import Database
from repositories.sale_repository import SaleRepository
from repositories.product_repository import ProductRepository
from services.sale_service import SaleService

venta_bp = Blueprint('venta', __name__)

db = Database()
sale_repo = SaleRepository(db)
product_repo = ProductRepository(db)
sale_service = SaleService(sale_repo, product_repo)

@venta_bp.route('/nueva', methods=['POST'])
@jwt_required()
def registrar_venta():
    """
    Registra una nueva venta procesando la lista de productos.
    ---
    tags:
      - Ventas
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - productos
          properties:
            productos:
              type: array
              description: Lista de artículos a vender.
              items:
                type: object
                properties:
                  codigo:
                    type: string
                    example: "5001"
                  cantidad:
                    type: integer
                    example: 3
    responses:
      201:
        description: Venta completada. Devuelve el ticket detallado.
        schema:
          properties:
            mensaje:
              type: string
              example: "Venta registrada exitosamente"
            ticket:
              type: object
              properties:
                detalles:
                  type: array
                  items:
                    type: object
                    properties:
                      cantidad:
                        type: integer
                      codigo_producto:
                        type: string
                      importe:
                        type: number
                      nombre_producto:
                        type: string
                      precio_unitario:
                        type: number
      400:
        description: Error en el formato del JSON o falta el número de caja.
      500:
        description: Error interno al procesar la transacción.
    """
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