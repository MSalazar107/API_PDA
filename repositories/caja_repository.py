from mysql.connector import Error

class CajaRepository:
    def __init__(self, db):
        self.db = db

    def get_by_id(self, num_caja):
       
        try:
            conn = self.db.connect()
            cur = conn.cursor(dictionary=True)
            sql = "SELECT * FROM CAJA WHERE num_caja = %s"
            cur.execute(sql, (num_caja,))
            return cur.fetchone()
        finally:
            cur.close()
            conn.close()
            
    def registrar_caja(self, email_usuario, num_caja):
        
        try:
            conn = self.db.connect()
            cur = conn.cursor()
            sql = "INSERT INTO CAJA (usuario, num_caja) VALUES (%s, %s)"
            cur.execute(sql, (email_usuario, num_caja))
            conn.commit()
            return True
        except Error as e:
            print(f"Error al registrar caja: {e}")
            return False
        finally:
            cur.close()
            conn.close()