from typing import List, Optional 
from models.usuario import Usuario
from db import Database

class UserRepository:
    def __init__(self,db: Database):
        self.db= db
    
    def add(self,usuario: Usuario):
        conn= self.db.connect()
        cur = conn.cursor()
        
        
        query = """
            INSERT INTO USUARIO (email, nombre, apellidos, contrasena, fecha_nac, alias, telefono, direccion, imagen_ruta) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
    
        cur.execute(query,(
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
        )
        conn.commit()
        cur.close()
        conn.close()
        
    def email_existe(self, email: str) -> bool:
        conn = self.db.connect()
        cur = conn.cursor()
        
        cur.execute("SELECT email FROM USUARIO WHERE email = %s", (email,))
        resultado = cur.fetchone()
        
        cur.close()
        conn.close()
        
        return resultado is not None
    def update_foto (self, email: str, foto_blob):
        
        try:
            conn = self.db.connect()
            cur = conn.cursor()
            query = "UPDATE USUARIO SET imagen_ruta = %s WHERE email = %s"
            cur.execute(query, (foto_blob, email))
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