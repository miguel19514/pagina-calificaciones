from app.database import get_connection


class Alumno:
    def __init__(self, id, nombre, apellido, matricula, salon_id):
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.matricula = matricula
        self.salon_id = salon_id

    @staticmethod
    def obtener_todos():
        """Retorna todos los alumnos con el nombre de su salon"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT a.id, a.nombre, a.apellido, a.matricula, a.salon_id, s.nombre
            FROM alumnos a
            LEFT JOIN salones s ON a.salon_id = s.id
        """)
        filas = cursor.fetchall()
        conn.close()
        alumnos = []
        for fila in filas:
            alumnos.append({
                "id": fila[0],
                "nombre": fila[1],
                "apellido": fila[2],
                "matricula": fila[3],
                "salon_id": fila[4],
                "salon_nombre": fila[5]
            })
        return alumnos

    @staticmethod
    def obtener_por_id(id):
        """Retorna un alumno especifico por su id"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT a.id, a.nombre, a.apellido, a.matricula, a.salon_id, s.nombre
            FROM alumnos a
            LEFT JOIN salones s ON a.salon_id = s.id
            WHERE a.id = %s
        """, (id,))
        fila = cursor.fetchone()
        conn.close()
        if fila is None:
            return None
        return {
            "id": fila[0],
            "nombre": fila[1],
            "apellido": fila[2],
            "matricula": fila[3],
            "salon_id": fila[4],
            "salon_nombre": fila[5]
        }

    @staticmethod
    def obtener_por_salon(salon_id):
        """Retorna todos los alumnos de un salon especifico"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, nombre, apellido, matricula, salon_id
            FROM alumnos
            WHERE salon_id = %s
        """, (salon_id,))
        filas = cursor.fetchall()
        conn.close()
        alumnos = []
        for fila in filas:
            alumnos.append({
                "id": fila[0],
                "nombre": fila[1],
                "apellido": fila[2],
                "matricula": fila[3],
                "salon_id": fila[4]
            })
        return alumnos

    @staticmethod
    def crear(nombre, apellido, matricula, salon_id):
        """Crea un alumno nuevo en la base de datos"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO alumnos (nombre, apellido, matricula, salon_id) VALUES (%s, %s, %s, %s) RETURNING id",
            (nombre, apellido, matricula, salon_id)
        )
        id_nuevo = cursor.fetchone()[0]
        conn.commit()
        conn.close()
        return id_nuevo

    @staticmethod
    def actualizar(id, nombre, apellido, matricula, salon_id):
        """Modifica un alumno existente"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE alumnos SET nombre = %s, apellido = %s, matricula = %s, salon_id = %s WHERE id = %s",
            (nombre, apellido, matricula, salon_id, id)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def eliminar(id):
        """Elimina un alumno por su id"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM alumnos WHERE id = %s", (id,))
        conn.commit()
        conn.close()
