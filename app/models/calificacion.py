from app.database import get_connection


class Calificacion:
    def __init__(self, id, alumno_id, materia_id, calificacion, periodo):
        self.id = id
        self.alumno_id = alumno_id
        self.materia_id = materia_id
        self.calificacion = calificacion
        self.periodo = periodo

    @staticmethod
    def obtener_por_alumno(alumno_id):
        """Retorna todas las calificaciones de un alumno con detalles"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT c.id, c.alumno_id, c.materia_id, c.calificacion, c.periodo,
                   m.nombre, m.min_aprobatorio,
                   a.nombre, a.apellido
            FROM calificaciones c
            INNER JOIN materias m ON c.materia_id = m.id
            INNER JOIN alumnos a ON c.alumno_id = a.id
            WHERE c.alumno_id = %s
        """, (alumno_id,))
        filas = cursor.fetchall()
        conn.close()
        calificaciones = []
        for fila in filas:
            calificaciones.append({
                "id": fila[0],
                "alumno_id": fila[1],
                "materia_id": fila[2],
                "calificacion": float(fila[3]),
                "periodo": fila[4],
                "materia_nombre": fila[5],
                "min_aprobatorio": float(fila[6]),
                "alumno_nombre": fila[7],
                "alumno_apellido": fila[8],
                "aprobado": float(fila[3]) >= float(fila[6])
            })
        return calificaciones

    @staticmethod
    def obtener_por_salon(salon_id, periodo=None):
        """Retorna todas las calificaciones de un salon completo"""
        conn = get_connection()
        cursor = conn.cursor()
        if periodo:
            cursor.execute("""
                SELECT c.id, c.alumno_id, c.materia_id, c.calificacion, c.periodo,
                       m.nombre, m.min_aprobatorio,
                       a.nombre, a.apellido
                FROM calificaciones c
                INNER JOIN materias m ON c.materia_id = m.id
                INNER JOIN alumnos a ON c.alumno_id = a.id
                WHERE a.salon_id = %s AND c.periodo = %s
            """, (salon_id, periodo))
        else:
            cursor.execute("""
                SELECT c.id, c.alumno_id, c.materia_id, c.calificacion, c.periodo,
                       m.nombre, m.min_aprobatorio,
                       a.nombre, a.apellido
                FROM calificaciones c
                INNER JOIN materias m ON c.materia_id = m.id
                INNER JOIN alumnos a ON c.alumno_id = a.id
                WHERE a.salon_id = %s
            """, (salon_id,))
        filas = cursor.fetchall()
        conn.close()
        calificaciones = []
        for fila in filas:
            calificaciones.append({
                "id": fila[0],
                "alumno_id": fila[1],
                "materia_id": fila[2],
                "calificacion": float(fila[3]),
                "periodo": fila[4],
                "materia_nombre": fila[5],
                "min_aprobatorio": float(fila[6]),
                "alumno_nombre": fila[7],
                "alumno_apellido": fila[8],
                "aprobado": float(fila[3]) >= float(fila[6])
            })
        return calificaciones

    @staticmethod
    def crear(alumno_id, materia_id, calificacion, periodo):
        """Crea una calificacion nueva"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO calificaciones 
               (alumno_id, materia_id, calificacion, periodo) 
               VALUES (%s, %s, %s, %s) RETURNING id""",
            (alumno_id, materia_id, calificacion, periodo)
        )
        id_nuevo = cursor.fetchone()[0]
        conn.commit()
        conn.close()
        return id_nuevo

    @staticmethod
    def actualizar(id, calificacion):
        """Modifica una calificacion existente"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE calificaciones SET calificacion = %s WHERE id = %s",
            (calificacion, id)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def eliminar(id):
        """Elimina una calificacion por su id"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM calificaciones WHERE id = %s", (id,))
        conn.commit()
        conn.close()
