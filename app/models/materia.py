from app.database import get_connection


class Materia:
    def __init__(self, id, nombre, min_aprobatorio):
        self.id = id
        self.nombre = nombre
        self.min_aprobatorio = min_aprobatorio

    @staticmethod
    def obtener_todas():
        """Retorna todas las materias"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, min_aprobatorio FROM materias")
        filas = cursor.fetchall()
        conn.close()
        materias = []
        for fila in filas:
            materias.append({
                "id": fila[0],
                "nombre": fila[1],
                "min_aprobatorio": float(fila[2])
            })
        return materias

    @staticmethod
    def obtener_por_salon(salon_id):
        """Retorna todas las materias asignadas a un salon especifico"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT m.id, m.nombre, m.min_aprobatorio
            FROM materias m
            INNER JOIN salon_materias sm ON m.id = sm.materia_id
            WHERE sm.salon_id = %s
        """, (salon_id,))
        filas = cursor.fetchall()
        conn.close()
        materias = []
        for fila in filas:
            materias.append({
                "id": fila[0],
                "nombre": fila[1],
                "min_aprobatorio": float(fila[2])
            })
        return materias

    @staticmethod
    def obtener_por_id(id):
        """Retorna una materia especifica por su id"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, nombre, min_aprobatorio FROM materias WHERE id = %s", (id,))
        fila = cursor.fetchone()
        conn.close()
        if fila is None:
            return None
        return {
            "id": fila[0],
            "nombre": fila[1],
            "min_aprobatorio": float(fila[2])
        }

    @staticmethod
    def crear(nombre, min_aprobatorio=70.0):
        """Crea una materia nueva, el minimo aprobatorio es 70 por defecto"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO materias (nombre, min_aprobatorio) VALUES (%s, %s) RETURNING id",
            (nombre, min_aprobatorio)
        )
        resultado = cursor.fetchone()
        conn.commit()
        conn.close()
        if resultado:
            return resultado[0]
        return None

    @staticmethod
    def asignar_a_salon(salon_id, materia_id):
        """Asigna una materia existente a un salon"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO salon_materias (salon_id, materia_id) VALUES (%s, %s)",
            (salon_id, materia_id)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def actualizar(id, nombre, min_aprobatorio):
        """Modifica una materia existente"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE materias SET nombre = %s, min_aprobatorio = %s WHERE id = %s",
            (nombre, min_aprobatorio, id)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def eliminar(id):
        """Elimina una materia por su id"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM materias WHERE id = %s", (id,))
        conn.commit()
        conn.close()

    @staticmethod
    def quitar_de_salon(salon_id, materia_id):
        """Quita una materia de un salon especifico"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM salon_materias WHERE salon_id = %s AND materia_id = %s",
            (salon_id, materia_id)
        )
        conn.commit()
        conn.close()
