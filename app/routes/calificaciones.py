from flask import Blueprint, request, jsonify
from app.models.calificacion import Calificacion
from app.models.materia import Materia

calificaciones_bp = Blueprint('calificaciones', __name__)


@calificaciones_bp.route('/api/calificaciones/alumno/<int:alumno_id>', methods=['GET'])
def obtener_calificaciones_alumno(alumno_id):
    """Retorna todas las calificaciones de un alumno"""
    try:
        calificaciones = Calificacion.obtener_por_alumno(alumno_id)
        return jsonify(calificaciones), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@calificaciones_bp.route('/api/calificaciones/salon/<int:salon_id>', methods=['GET'])
def obtener_calificaciones_salon(salon_id):
    """Retorna todas las calificaciones de un salon"""
    try:
        periodo = request.args.get('periodo')
        calificaciones = Calificacion.obtener_por_salon(salon_id, periodo)
        return jsonify(calificaciones), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@calificaciones_bp.route('/api/calificaciones', methods=['POST'])
def crear_calificacion():
    """Crea una calificacion nueva"""
    try:
        datos = request.get_json()
        alumno_id = datos.get('alumno_id')
        materia_id = datos.get('materia_id')
        calificacion = datos.get('calificacion')
        periodo = datos.get('periodo')

        if not alumno_id or not materia_id or calificacion is None or not periodo:
            return jsonify({"error": "alumno_id, materia_id, calificacion y periodo son requeridos"}), 400

        if calificacion < 0 or calificacion > 100:
            return jsonify({"error": "La calificacion debe estar entre 0 y 100"}), 400

        id_nuevo = Calificacion.crear(
            alumno_id, materia_id, calificacion, periodo)
        return jsonify({"mensaje": "Calificacion creada", "id": id_nuevo}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@calificaciones_bp.route('/api/calificaciones/<int:id>', methods=['PUT'])
def actualizar_calificacion(id):
    """Modifica una calificacion existente"""
    try:
        datos = request.get_json()
        calificacion = datos.get('calificacion')

        if calificacion is None:
            return jsonify({"error": "calificacion es requerida"}), 400

        if calificacion < 0 or calificacion > 100:
            return jsonify({"error": "La calificacion debe estar entre 0 y 100"}), 400

        Calificacion.actualizar(id, calificacion)
        return jsonify({"mensaje": "Calificacion actualizada"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@calificaciones_bp.route('/api/calificaciones/<int:id>', methods=['DELETE'])
def eliminar_calificacion(id):
    """Elimina una calificacion"""
    try:
        Calificacion.eliminar(id)
        return jsonify({"mensaje": "Calificacion eliminada"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@calificaciones_bp.route('/api/materias', methods=['GET'])
def obtener_materias():
    """Retorna todas las materias"""
    try:
        materias = Materia.obtener_todas()
        return jsonify(materias), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@calificaciones_bp.route('/api/materias', methods=['POST'])
def crear_materia():
    """Crea una materia nueva"""
    try:
        datos = request.get_json()
        nombre = datos.get('nombre')
        min_aprobatorio = datos.get('min_aprobatorio', 70.0)

        if not nombre:
            return jsonify({"error": "nombre es requerido"}), 400

        id_nuevo = Materia.crear(nombre, min_aprobatorio)
        return jsonify({"mensaje": "Materia creada", "id": id_nuevo}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@calificaciones_bp.route('/api/materias/salon/<int:salon_id>', methods=['GET'])
def obtener_materias_salon(salon_id):
    """Retorna todas las materias de un salon"""
    try:
        materias = Materia.obtener_por_salon(salon_id)
        return jsonify(materias), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@calificaciones_bp.route('/api/materias/salon', methods=['POST'])
def asignar_materia_salon():
    """Asigna una materia a un salon"""
    try:
        datos = request.get_json()
        salon_id = datos.get('salon_id')
        materia_id = datos.get('materia_id')

        if not salon_id or not materia_id:
            return jsonify({"error": "salon_id y materia_id son requeridos"}), 400

        Materia.asignar_a_salon(salon_id, materia_id)
        return jsonify({"mensaje": "Materia asignada al salon"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500
