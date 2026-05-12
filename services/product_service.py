import base64
class ProductService:
    def __init__(self, product_repo):
        self.repo = product_repo

    def registrar_producto(self, data):
        
        if not data.get('codigo') or not data.get('descripcion'):
            raise ValueError("El código y la descripción son obligatorios.")
            
        if float(data.get('precio', 0)) <= 0:
            raise ValueError("El precio debe ser un número positivo.")

        
        existente = self.repo.get_by_id(data['codigo'])
        if existente:
            raise ValueError("Este código de producto ya está registrado.")

        
        data.setdefault('existencias', 0)
        data.setdefault('imagen_producto_ruta', None)
        
        return self.repo.create(data)

    def listar_productos(self):
        productos = self.repo.get_all()

        for p in productos:
            if p.get('imagen_producto_ruta'):
                p['imagen_producto_ruta'] = base64.b64encode(p['imagen_producto_ruta']).decode('utf-8')
        return productos
    
    def obtener_producto_por_id(self,codigo):
        
        producto = self.repo.get_by_id(codigo)

        if producto and producto.get('imagen_producto_ruta'):
            producto['imagen_producto_ruta'] = base64.b64encode(producto['imagen_producto_ruta']).decode('utf-8')
            
        return producto 