from db import Database

class ReportRepository:
    def __init__(self, db: Database):
        self.db = db

    def ventas_por_caja(self, num_caja, fecha_inicio, fecha_fin):
        conn = self.db.connect()
        cur = conn.cursor(dictionary=True)
        
        query = """
            SELECT * FROM Vista_Reporte_Ventas WHERE
             numero_de_caja = %s AND fecha BETWEEN %s AND %s
             ORDER BY fecha DESC
        """
        cur.execute(query, (num_caja, fecha_inicio, fecha_fin))
        resultados = cur.fetchall()
        cur.close()
        conn.close()
        return resultados

    def total_ventas_periodo(self, fecha_inicio, fecha_fin):
        
        conn = self.db.connect()
        cur = conn.cursor(dictionary=True)
        query = "SELECT SUM(total) as gran_total FROM TICKET WHERE fecha BETWEEN %s AND %s"
        cur.execute(query, (fecha_inicio, fecha_fin))
        resultado = cur.fetchone()
        cur.close()
        conn.close()
        return resultado['gran_total'] if resultado else 0