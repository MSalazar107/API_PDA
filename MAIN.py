from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager
from controllers.authcontroller import auth_bp



app = Flask (__name__)

app.config["JWT_SECRET_KEY"] = "jwt-secret-key"
jwt = JWTManager(app)

app.register_blueprint(auth_bp, url_prefix='/api/auth')
@app.route('/')
def index():
    return {"mensaje": "API del Punto de Venta corriendo al 100%"}

if __name__ == "__main__":
    app.run(debug=True) 