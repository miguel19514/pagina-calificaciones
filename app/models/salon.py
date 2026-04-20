from app.database import get_connection


class Salon:
    def __init__(self, id, nombre, grado, turno):
        self.id = id
        self.nombre = nombre
        self.grado = grado
        self.turno = turno

    @staticmethod
    def obtener_todos():
        """Retorna todos los salones de la base de datos"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, grado, turno FROM salones")
        filas = cursor.fetchall()
        conn.close()
        salones = []
        for fila in filas:
            salones.append({
                "id": fila[0],
                "nombre": fila[1],
                "grado": fila[2],
                "turno": fila[3]
            })
        return salones

    @staticmethod
    def crear(nombre, grado, turno):
        """Crea un salon nuevo en la base de datos"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO salones (nombre, grado, turno) VALUES (%s, %s, %s) RETURNING id",
            (nombre, grado, turno)
        )
        id_nuevo = cursor.fetchone()[0]
        conn.commit()
        conn.close()
        return id_nuevo

    @staticmethod
    def obtener_por_id(id):
        """Retorna un salon especifico por su id"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, nombre, grado, turno FROM salones WHERE id = %s", (id,))
        fila = cursor.fetchone()
        conn.close()
        if fila is None:
            return None
        return {
            "id": fila[0],
            "nombre": fila[1],
            "grado": fila[2],
            "turno": fila[3]
        }

    @staticmethod
    def actualizar(id, nombre, grado, turno):
        """Modifica un salon existente"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE salones SET nombre = %s, grado = %s, turno = %s WHERE id = %s",
            (nombre, grado, turno, id)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def eliminar(id):
        """Elimina un salon por su id"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM salones WHERE id = %s", (id,))
        conn.commit()
        conn.close()
