from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager



app = Flask (__name__)

app.config["JWT_SECRET_KEY"] = "jwt-secret-key"
jwt = JWTManager(app)

@app.route('/', methods =['GET'])
def index():
    return {"mensaje": "API del Punto de Venta corriendo al 100%"}

if __name__ == "__main__":
    app.run(debug=True, port= 5000) 