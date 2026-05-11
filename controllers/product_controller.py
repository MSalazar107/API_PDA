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


@product_bp.route('/',methods=['GET'])
@jwt_required()
def listar_productos():
        productos = product_service.listar_productos()
        return jsonify(productos), 200
    
@product_bp.route('/<codigo>',methods=['GET'])
@jwt_required()
def obtener_producto(codigo):
    try:
        producto = product_service.obtener_producto_por_id(codigo)
        if producto:
            return jsonify(producto), 200
        
        return jsonify({"error":"Producto No encontrado"}), 404
    except Exception as e:
        return jsonify ({"error" : str(e) }), 500    
    
@product_bp.route('/nuevo', methods=['POST'])
@jwt_required() 
def crear():
    try:
        foto = request.files.get('foto')
        blob_imagen = None
        if foto:
            blob_imagen = foto.read()
        data = {
            "codigo": request.form.get('codigo'),
            "descripcion": request.form.get('descripcion'),
            "precio": float(request.form.get('precio')),
            "existencias": int(request.form.get('existencias')),
            "unidad_fk": request.form.get('unidad_fk'),
            "imagen_producto_ruta": blob_imagen
        }
        
        if product_service.registrar_producto(data):
            return jsonify({"mensaje": "Producto registrado con éxito"}), 201
            
        return jsonify({"error": "No se pudo guardar en la base de datos"}), 400
        
    except ValueError as ve:
        
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        
        return jsonify({"error": str(e)}), 500
    
@product_bp.route('/<codigo>', methods=['PUT'])
@jwt_required()
def actualizar (codigo):
    try:
        producto_existente = product_repo.get_by_id(codigo)
        if not producto_existente:
            return jsonify({"error": "Producto no encontrado"}), 404
        
        foto =request.files.get('foto')
        blob_imagen = foto.read if foto else producto_existente['imagen_producto_ruta']
        
        data = {"descripcion": request.form.get('descripcion', producto_existente['descripcion']),
                "precio": float(request.form.get('precio', producto_existente['precio'])),
                "existencias": int(request.form.get('existencias', producto_existente['existencias'])),
                "unidad_fk": request.form.get('unidad_fk', producto_existente['unidad_fk']),
                "imagen_producto_ruta": blob_imagen}
        
        if product_repo.update(codigo, data):
            return jsonify({"mensaje": "Producto actualizado con éxito"}), 200
        return jsonify({"error": "No se pudo actualizar el producto"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@product_bp.route('/<codigo>', methods=['DELETE'])
@jwt_required()
def eliminar(codigo):
    if product_repo.delete_logic(codigo):
        return jsonify({"mensaje": "Producto eliminado con éxito"}), 200
    return jsonify({"error": "No se pudo eliminar el producto"}), 400