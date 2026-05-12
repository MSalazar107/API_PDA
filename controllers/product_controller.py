from flask import Blueprint, request, jsonify, send_file 
import io
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import Database
from repositories.product_repository import ProductRepository
from services.product_service import ProductService

product_bp = Blueprint('products', __name__)

db = Database()
product_repo = ProductRepository(db)
product_service = ProductService(product_repo)

@product_bp.route('/', methods=['GET'])
@jwt_required()
def listar_productos():
    """
    Obtiene la lista completa de productos.
    ---
    tags:
      - Productos
    security:
      - Bearer: []
    responses:
      200:
        description: Lista de productos obtenida con éxito.
    """
    productos = product_service.listar_productos()
    return jsonify(productos), 200
    
@product_bp.route('/<codigo>', methods=['GET'])
@jwt_required()
def obtener_producto(codigo):
    """
    Obtiene un producto específico por su código.
    ---
    tags:
      - Productos
    security:
      - Bearer: []
    parameters:
      - name: codigo
        in: path
        type: string
        required: true
        description: Código único del producto.
    responses:
      200:
        description: Producto encontrado.
      404:
        description: Producto no encontrado.
      500:
        description: Error interno del servidor.
    """
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
    """
    Registra un nuevo producto con imagen.
    ---
    tags:
      - Productos
    security:
      - Bearer: []
    consumes:
      - multipart/form-data
    parameters:
      - name: codigo
        in: formData
        type: string
        required: true
      - name: descripcion
        in: formData
        type: string
        required: true
      - name: precio
        in: formData
        type: number
        required: true
      - name: existencias
        in: formData
        type: integer
        required: true
      - name: unidad_fk
        in: formData
        type: string
        required: true
      - name: foto
        in: formData
        type: file
        required: false
        description: Imagen del producto.
    responses:
      201:
        description: Producto registrado con éxito.
      400:
        description: Error en los datos enviados.
      500:
        description: Error interno del servidor.
    """
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
def actualizar(codigo):
    """
    Actualiza los datos de un producto existente.
    ---
    tags:
      - Productos
    security:
      - Bearer: []
    consumes:
      - multipart/form-data
    parameters:
      - name: codigo
        in: path
        type: string
        required: true
      - name: descripcion
        in: formData
        type: string
      - name: precio
        in: formData
        type: number
      - name: existencias
        in: formData
        type: integer
      - name: unidad_fk
        in: formData
        type: string
      - name: foto
        in: formData
        type: file
    responses:
      200:
        description: Producto actualizado correctamente.
      404:
        description: Producto no encontrado.
    """
    try:
        producto_existente = product_repo.get_by_id(codigo)
        if not producto_existente:
            return jsonify({"error": "Producto no encontrado"}), 404
        
        foto = request.files.get('foto')
        blob_imagen = foto.read() if foto else producto_existente['imagen_producto_ruta']
        
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
    """
    Elimina un producto de forma lógica.
    ---
    tags:
      - Productos
    security:
      - Bearer: []
    parameters:
      - name: codigo
        in: path
        type: string
        required: true
    responses:
      200:
        description: Producto eliminado con éxito.
      400:
        description: No se pudo eliminar el producto.
    """
    if product_repo.delete_logic(codigo):
        return jsonify({"mensaje": "Producto eliminado con éxito"}), 200
    return jsonify({"error": "No se pudo eliminar el producto"}), 400

@product_bp.route('/<codigo>/foto', methods=['GET'])
def ver_foto_productoO(codigo):
    """
    Obtiene la imagen binaria de un producto.
    ---
    tags:
      - Productos
    parameters:
      - name: codigo
        in: path
        type: string
        required: true
    responses:
      200:
        description: Imagen del producto.
        content:
          image/jpeg:
            schema:
              type: string
              format: binary
      404:
        description: Imagen no encontrada.
    """
    try:
        producto = product_repo.get_by_id(codigo)
        if not producto or not producto['imagen_producto_ruta']:
            return jsonify({"error": "Producto o imagen no encontrada"}), 404
        foto_bytes = producto['imagen_producto_ruta']
        return send_file(io.BytesIO(foto_bytes), mimetype='image/jpeg', as_attachment=False, download_name=f"{codigo}_foto.jpg")
    except Exception as e:
        return jsonify({"error": str(e)}), 500
      


@product_bp.route('/<codigo>/agregar-stock', methods=['PUT'])
# @jwt_required() # Descoméntalo si usas tokens
def agregar_stock(codigo):
    try:
        # Recibimos cuántos productos nuevos llegaron
        data = request.get_json()
        cantidad_nueva = data.get('cantidad')
        
        if not cantidad_nueva or cantidad_nueva <= 0:
            return jsonify({"error": "Debes enviar una cantidad válida mayor a 0"}), 400
            
        # Llamamos al NUEVO método de tu repositorio
        exito = product_repo.agregar_inventario(codigo, cantidad_nueva)
        
        if exito:
            return jsonify({"mensaje": f"Se agregaron {cantidad_nueva} unidades al producto {codigo}"}), 200
        else:
            return jsonify({"error": "No se pudo actualizar el stock"}), 500
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500