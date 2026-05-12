from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from repositories.reportes_repository import ReportRepository
from db import Database

report_bp = Blueprint('reportes', __name__)
report_repo = ReportRepository(Database())

@report_bp.route('/caja/<int:num_caja>', methods=['GET'])
@jwt_required()
def reporte_caja(num_caja):
    """
    Genera un reporte de ventas por caja en un periodo de fechas.
    ---
    tags:
      - Reportes
    security:
      - Bearer: []
    parameters:
      - name: num_caja
        in: path
        type: integer
        required: true
        description: Número de la caja a consultar.
      - name: inicio
        in: query
        type: string
        required: true
        description: Fecha de inicio (YYYY-MM-DD).
      - name: fin
        in: query
        type: string
        required: true
        description: Fecha de fin (YYYY-MM-DD).
    responses:
      200:
        description: Reporte generado exitosamente.
        schema:
          properties:
            num_caja:
              type: integer
            periodo:
              type: object
              properties:
                desde:
                  type: string
                hasta:
                  type: string
            ventas:
              type: array
              items:
                type: object
      400:
        description: Faltan parámetros de fecha.
      500:
        description: Error al generar el reporte.
    """
    inicio = request.args.get('inicio')
    fin = request.args.get('fin')

    if not inicio or not fin:
        return jsonify({"error": "Debes proporcionar fecha de inicio y fin"}), 400

    try:
        reporte = report_repo.ventas_por_caja(num_caja, inicio, fin)
        return jsonify({
            "num_caja": num_caja,
            "periodo": {"desde": inicio, "hasta": fin},
            "ventas": reporte
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500