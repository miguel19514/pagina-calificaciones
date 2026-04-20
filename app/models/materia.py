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
