from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from repositories.reportes_repository import ReportRepository
from db import Database

report_bp = Blueprint('reportes', __name__)
report_repo = ReportRepository(Database())

@report_bp.route('/caja/<int:num_caja>', methods=['GET'])
@jwt_required()
def reporte_caja(num_caja):
    
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