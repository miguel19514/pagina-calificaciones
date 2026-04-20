from flask import Blueprint, request, jsonify
from app.models.alumno import Alumno

alumnos_bp = Blueprint('alumnos', __name__)


@alumnos_bp.route('/api/alumnos', methods=['GET'])
def obtener_alumnos():
    """Retorna todos los alumnos"""
    try:
        alumnos = Alumno.obtener_todos()
        return jsonify(alumnos), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@alumnos_bp.route('/api/alumnos/<int:id>', methods=['GET'])
def obtener_alumno(id):
    """Retorna un alumno especifico"""
    try:
        alumno = Alumno.obtener_por_id(id)
        if alumno is None:
            return jsonify({"error": "Alumno no encontrado"}), 404
        return jsonify(alumno), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@alumnos_bp.route('/api/alumnos/salon/<int:salon_id>', methods=['GET'])
def obtener_alumnos_por_salon(salon_id):
    """Retorna todos los alumnos de un salon especifico"""
    try:
        alumnos = Alumno.obtener_por_salon(salon_id)
        return jsonify(alumnos), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@alumnos_bp.route('/api/alumnos', methods=['POST'])
def crear_alumno():
    """Crea un alumno nuevo"""
    try:
        datos = request.get_json()
        nombre = datos.get('nombre')
        apellido = datos.get('apellido')
        matricula = datos.get('matricula')
        salon_id = datos.get('salon_id')

        if not nombre or not apellido or not matricula or not salon_id:
            return jsonify({"error": "nombre, apellido, matricula y salon_id son requeridos"}), 400

        id_nuevo = Alumno.crear(nombre, apellido, matricula, salon_id)
        return jsonify({"mensaje": "Alumno creado", "id": id_nuevo}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@alumnos_bp.route('/api/alumnos/<int:id>', methods=['PUT'])
def actualizar_alumno(id):
    """Modifica un alumno existente"""
    try:
        alumno = Alumno.obtener_por_id(id)
        if alumno is None:
            return jsonify({"error": "Alumno no encontrado"}), 404

        datos = request.get_json()
        nombre = datos.get('nombre')
        apellido = datos.get('apellido')
        matricula = datos.get('matricula')
        salon_id = datos.get('salon_id')

        if not nombre or not apellido or not matricula or not salon_id:
            return jsonify({"error": "nombre, apellido, matricula y salon_id son requeridos"}), 400

        Alumno.actualizar(id, nombre, apellido, matricula, salon_id)
        return jsonify({"mensaje": "Alumno actualizado"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@alumnos_bp.route('/api/alumnos/<int:id>', methods=['DELETE'])
def eliminar_alumno(id):
    """Elimina un alumno"""
    try:
        alumno = Alumno.obtener_por_id(id)
        if alumno is None:
            return jsonify({"error": "Alumno no encontrado"}), 404

        Alumno.eliminar(id)
        return jsonify({"mensaje": "Alumno eliminado"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
