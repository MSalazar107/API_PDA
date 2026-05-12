from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager
from controllers.authcontroller import auth_bp
from controllers.user_controller import user_bp
from controllers.venta_controller import venta_bp
from controllers.product_controller import product_bp
from controllers.reportes_controller import report_bp
from db import Database
import atexit 
from flasgger import Swagger 




app = Flask (__name__)

app.config["JWT_SECRET_KEY"] = "jwt-secret-key"
jwt = JWTManager(app)

template = {
    "swagger": "2.0",
    "info": {
        "title": "API Punto de Venta",
        "description": "Documentación interactiva de la API",
        "version": "1.0.0"
    }
}
swagger = Swagger(app, template=template)

def cerrar_sesiones():
    print("Cerrando sesiones en caja")
    db = Database()
    
    try:
        conn = db.connect()
        cur = conn.cursor()
        cur.execute("UPDATE CAJA SET usuario = NULL")
        conn.commit()
        print("Sesiones cerradas exitosamente")
    except Exception as e:
        print(f"Error al cerrar sesiones: {e}")
    finally:
        if 'cur' in locals(): cur.close
        if 'conn' in locals(): conn.close()
        
atexit.register(cerrar_sesiones)
app.register_blueprint(user_bp, url_prefix='/api/user')
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(venta_bp, url_prefix='/api/ventas')
app.register_blueprint(product_bp, url_prefix='/api/productos')
app.register_blueprint(report_bp, url_prefix='/api/reportes')
@app.route('/')
def index():
    return {"mensaje": "API del Punto de Venta corriendo al 100%"}


if __name__ == "__main__":
    app.run(debug=True) 