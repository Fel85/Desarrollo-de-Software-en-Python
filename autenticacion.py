import hashlib
from database import conectar


def hash_password(password: str) -> str:
    """Devuelve el hash SHA-256 de la contraseña recibida."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def crear_usuario_admin_inicial():
    """Crea un usuario ADMIN por defecto si la tabla de usuarios está vacía.
       Usuario: admin | Contraseña: admin123"""
    conn = conectar()
    if conn is None:
        return
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM usuarios;")
    count = cur.fetchone()[0]
    if count == 0:
        print("Creando usuario ADMIN inicial...")
        username = "admin"
        nombre_completo = "Administrador Inicial"
        password = "admin123"
        hash_pass = hash_password(password)
        id_rol_admin = 1  # Asumiendo que el rol ADMIN tiene id_rol = 1
        cur.execute("""
            INSERT INTO usuarios (username, nombre_completo, hash_password, id_rol, activo)
            VALUES (?, ?, ?, ?, 1);
        """, (username, nombre_completo, hash_pass, id_rol_admin))
        conn.commit()
        print("Usuario ADMIN inicial creado: usuario='admin', contraseña='admin123'")
    conn.close()


def autenticar_usuario(username: str, password: str):
    """
    Verifica si las credenciales del usuario son correctas.
    Devuelve un dict con id_usuario, username y rol, o None si falla.
    """
    conn = conectar()
    if conn is None:
        return None
    cur = conn.cursor()
    cur.execute(
        """
        SELECT u.id_usuario, u.username, u.hash_password, r.nombre_rol
        FROM usuarios u
        JOIN roles r ON u.id_rol = r.id_rol
        WHERE u.username = ? AND u.activo = 1;
        """,
        (username,),
    )
    row = cur.fetchone()
    conn.close()

    if row is None:
        return None

    id_usuario, username_db, hash_db, rol = row
    if hash_password(password) == hash_db:
        return {
            "id_usuario": id_usuario,
            "username": username_db,
            "rol": rol,
        }
    else:
        return None
