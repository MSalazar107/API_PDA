from typing import List, Optional 
from models.usuario import Usuario
from mysql.connector import Error
from db import Database

class UserRepository:
    def __init__(self,db: Database):
        self.db= db
    
    def add(self, usuario: Usuario):
        
        conn = self.db.connect()
        cur = conn.cursor()
        
        try:
            
            params = (
                usuario.email,
                usuario.nombre,
                usuario.apellidos,
                usuario.contrasena,
                usuario.fecha_nac,
                usuario.alias,
                usuario.telefono,
                usuario.direccion,
                usuario.imagen_ruta 
            )
            
            cur.callproc('RegistrarUsuario', params)
            conn.commit()
            return True
        except Error as e:
            print(f"Error al registrar usuario: {e}")
            return False
        finally:
            cur.close()
            conn.close()
        
        return resultado is not None
    
    def update_foto(self, email: str, foto_blob):
        """
        Llama al procedimiento ActualizarFotoUsuario
        """
        try:
            conn = self.db.connect()
            cur = conn.cursor()
            
           
            cur.callproc('ActualizarFotoUsuario', (email, foto_blob))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error al actualizar la foto: {e}")
            return False
        finally:
            cur.close()
            conn.close()
    
    def get_by_email(self, email):
        try:
            conn = self.db.connect()
            cur = conn.cursor(dictionary=True)
            cur.execute("SELECT * FROM USUARIO WHERE email = %s", (email,))
            return cur.fetchone()
        finally:
            cur.close()
            conn.close()
    def email_existe(self, email: str) -> bool:
        
        conn = self.db.connect()
        cur = conn.cursor()
        try:
           
            cur.execute("SELECT email FROM USUARIO WHERE email = %s", (email,))
            resultado = cur.fetchone()
            
            
            return resultado is not None
        finally:
            cur.close()
            conn.close()