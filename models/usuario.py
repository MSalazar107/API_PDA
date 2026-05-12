from dataclasses import dataclass
from typing import Optional
import base64

@dataclass
class Usuario:
    email:str
    nombre:str
    apellidos:str
    contrasena:str
    fecha_nac:str

   
    
    alias: Optional[str] = None
    telefono: Optional [str] = None 
    direccion: Optional [str] = None
    imagen_ruta: Optional [str] = None  
    
    def to_dict(self):
        
        foto = None
        if self.imagen_ruta:
            foto = base64.b64encode(self.imagen_ruta).decode('utf-8')
        
        return {
            "email": self.email,
            "nombre": self.nombre,
            "apellidos": self.apellidos,
            "fecha_nac": self.fecha_nac,
            "alias": self.alias,
            "telefono": self.telefono,
            "direccion": self.direccion,
            "imagen_ruta": foto
        }