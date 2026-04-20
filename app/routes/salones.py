from flask import Blueprint, request, jsonify
from app.models.salon import Salon

salones_bp = Blueprint('salones', __name__)


@salones_bp.route('/api/salones', methods=['GET'])
def obtener_salones():
    """Retorna todos los salones"""
    try:
        salones = Salon.obtener_todos()
        return jsonify(salones), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@salones_bp.route('/api/salones/<int:id>', methods=['GET'])
def obtener_salon(id):
    """Retorna un salon especifico"""
    try:
        salon = Salon.obtener_por_id(id)
        if salon is None:
            return jsonify({"error": "Salon no encontrado"}), 404
        return jsonify(salon), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@salones_bp.route('/api/salones', methods=['POST'])
def crear_salon():
    """Crea un salon nuevo"""
    try:
        datos = request.get_json()
        nombre = datos.get('nombre')
        grado = datos.get('grado')
        turno = datos.get('turno')

        if not nombre or not grado or not turno:
            return jsonify({"error": "nombre, grado y turno son requeridos"}), 400

        id_nuevo = Salon.crear(nombre, grado, turno)
        return jsonify({"mensaje": "Salon creado", "id": id_nuevo}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@salones_bp.route('/api/salones/<int:id>', methods=['PUT'])
def actualizar_salon(id):
    """Modifica un salon existente"""
    try:
        salon = Salon.obtener_por_id(id)
        if salon is None:
            return jsonify({"error": "Salon no encontrado"}), 404

        datos = request.get_json()
        nombre = datos.get('nombre')
        grado = datos.get('grado')
        turno = datos.get('turno')

        if not nombre or not grado or not turno:
            return jsonify({"error": "nombre, grado y turno son requeridos"}), 400

        Salon.actualizar(id, nombre, grado, turno)
        return jsonify({"mensaje": "Salon actualizado"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@salones_bp.route('/api/salones/<int:id>', methods=['DELETE'])
def eliminar_salon(id):
    """Elimina un salon"""
    try:
        salon = Salon.obtener_por_id(id)
        if salon is None:
            return jsonify({"error": "Salon no encontrado"}), 404

        Salon.eliminar(id)
        return jsonify({"mensaje": "Salon eliminado"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
