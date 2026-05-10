from dataclasses import dataclass
from typing import Optional

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