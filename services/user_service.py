import re 
from datetime import datetime 
from werkzeug.security import generate_password_hash
from models.usuario import Usuario
from repositories.user_repository import UserRepository

class UserService:
    
    def __init__(self,repo: UserRepository):
        self.repo = repo
        
    
    def _validar_password(self, password: str) -> bool:
        
        """Valida: min 8 caracteres, una mayuscula, una minuscula y un numero"""
        if len(password) < 8: return False
        if not re.search(r"[A-Z]", password): return False
        if not re.search(r"[a-z]", password): return False
        if not re.search(r"[0-9]", password): return False
        return True
    
    def _es_mayor_de_edad(self, fecha_nac_str: str) -> bool:
        """Valida que la fecha de nacimiento indique 18 a;os o mas"""
        
        try:
            fecha_nac = datetime.strptime(fecha_nac_str, '%Y-%m-%d')
            hoy = datetime.today()
            edad = hoy.year - fecha_nac.year  -((hoy.month, hoy.day)< (fecha_nac.month, fecha_nac.day))
            return edad>= 18
        except ValueError:
            raise ValueError("Formato de fecha invalido. Usa YYYY-MM-DD")
        
    def create_Usuario(self, data: dict) -> Usuario:
        
        if self.repo.email_existe(data["email"]):
            raise ValueError("El corrreo ya esta registrado.")
        
        if not self._validar_password(data["contrasena"]):
            raise ValueError("La contraseña debe tener al menos 8 caracteres, una mayuscula, minuscula y un numero")
        
        if not self._es_mayor_de_edad(data["fecha_nac"]):
            raise ValueError("Debes ser mayor de edad para registrarte")
        
        hashed_password  = generate_password_hash(data["contrasena"])
        
        usuario = Usuario(
            email = data["email"],
            nombre = data["nombre"],
            apellidos = data["apellidos"],
            contrasena = hashed_password,
            fecha_nac = data ["fecha_nac"],
            
            alias = data.get("alias"),
            telefono = data.get("telefono"),
            direccion = data.get("direccion"),
            imagen_ruta = data.get("imagen_ruta")  
        )
        
        self.repo.add(usuario)
        
        return usuario