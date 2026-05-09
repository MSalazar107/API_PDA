class ProductService:
    def __init__(self, product_repo):
        self.repo = product_repo

    def registrar_producto(self, data):
        # Validaciones de negocio
        if not data.get('codigo') or not data.get('descripcion'):
            raise ValueError("El código y la descripción son obligatorios.")
            
        if float(data.get('precio', 0)) <= 0:
            raise ValueError("El precio debe ser un número positivo.")

        # Verificar si el código ya existe para no romper la PK
        existente = self.repo.get_by_id(data['codigo'])
        if existente:
            raise ValueError("Este código de producto ya está registrado.")

        # Valores por defecto
        data.setdefault('existencias', 0)
        data.setdefault('imagen_producto_ruta', None)
        
        return self.repo.create(data)

    def listar_productos(self):
        return self.repo.get_all()