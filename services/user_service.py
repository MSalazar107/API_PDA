import re

from datetime import datetime 
from werkzeug.security import generate_password_hash
from models.usuario import Usuario
from repositories.user_repository import UserRepository

class UserService:
    """
    Capa de lógica de negocio (Service) para la gestión de usuarios y personal.
    
    Se encarga de aplicar las políticas de seguridad (contraseñas fuertes), 
    reglas de la empresa (mayoría de edad) y encriptación de datos antes 
    de enviar la información al repositorio para ser guardada en la base de datos.
    """
    
    def __init__(self,repo: UserRepository):
        self.repo = repo
        
    
    def _validar_password(self, password: str) -> bool:
        """
        Valida que la contraseña cumpla con las políticas de seguridad del sistema.
        Requiere: mínimo 8 caracteres, al menos una mayúscula, una minúscula y un número.
        """
        if len(password) < 8: return False
        if not re.search(r"[A-Z]", password): return False
        if not re.search(r"[a-z]", password): return False
        if not re.search(r"[0-9]", password): return False
        return True
    
    def _es_mayor_de_edad(self, fecha_nac_str: str) -> bool:
        """
        Calcula la edad exacta basada en la fecha de nacimiento ingresada y valida 
        que el usuario indique 18 años o más para poder registrarse/trabajar.
        """
        try:
            fecha_nac = datetime.strptime(fecha_nac_str, '%Y-%m-%d')
            hoy = datetime.today()
            edad = hoy.year - fecha_nac.year  -((hoy.month, hoy.day)< (fecha_nac.month, fecha_nac.day))
            return edad>= 18
        except ValueError:
            raise ValueError("Formato de fecha invalido. Usa YYYY-MM-DD")
        
    def create_Usuario(self, data: dict, foto_file=None) -> Usuario:
        """
        Orquesta la creación de un nuevo usuario en el sistema.
        
        Flujo de trabajo:
        1. Verifica que el correo no esté duplicado.
        2. Aplica reglas de validación de contraseña fuerte y mayoría de edad.
        3. Convierte el archivo de imagen a formato binario (BLOB) si existe.
        4. Encripta la contraseña usando un hash (nunca se guarda en texto plano).
        5. Construye el objeto Usuario y lo envía al repositorio.
        """
        if self.repo.email_existe(data["email"]):
            raise ValueError("El correo ya esta registrado.")
        
        if not self._validar_password(data["contrasena"]):
            raise ValueError("La contraseña debe tener al menos 8 caracteres, una mayuscula, minuscula y un numero")
        
        if not self._es_mayor_de_edad(data["fecha_nac"]):
            raise ValueError("Debes ser mayor de edad para registrarte")
        
        foto_blob = None
        if foto_file:
            foto_blob = foto_file.read()
        
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
            imagen_ruta = foto_blob 
        )
        
        self.repo.add(usuario)
        
        return usuario
    
    def actualizar_foto_perfil(self, email: str, foto_file):
        """
        Procesa un nuevo archivo de imagen y lo actualiza en el perfil del usuario.
        Valida que el archivo no esté vacío antes de procesar la lectura de bytes.
        """
        if not foto_file:
            raise ValueError("No se proporcionó una foto válida.")
        
        foto_blob = foto_file.read()
        
        exito = self.repo.update_foto(email, foto_blob)
        if not exito:
            raise Exception("Error al actualizar la foto de perfil.")
        
        return True