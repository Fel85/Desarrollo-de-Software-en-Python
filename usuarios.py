from autenticacion import hash_password
from database import conectar


def crear_usuario():
    """Crea un nuevo usuario con rol ADMIN o Vendedor."""
    conn = conectar()
    if conn is None:
        return
    cur = conn.cursor()

    username = input("Ingrese el nombre de usuario: ").strip()
    nombre_completo = input("Ingrese el nombre completo: ").strip()
    password = input("Ingrese la contraseña: ").strip()

    print("Seleccione el rol del usuario:")
    print("1. ADMIN")
    print("2. Vendedor")
    rol_opcion = input("Ingrese el número correspondiente al rol: ").strip()

    if rol_opcion == "1":
        id_rol = 1  # Rol ADMIN
    elif rol_opcion == "2":
        id_rol = 2  # Rol Vendedor
    else:
        print("Opción de rol inválida.")
        conn.close()
        return

    hash_pass = hash_password(password)

    try:
        cur.execute("""
            INSERT INTO usuarios (username, nombre_completo, hash_password, id_rol, activo)
            VALUES (?, ?, ?, ?, 1);
        """, (username, nombre_completo, hash_pass, id_rol))
        conn.commit()
        print(f"Usuario '{username}' creado exitosamente.")
    except Exception as e:
        print("Error al crear el usuario:", e)
    finally:
        conn.close()


def listar_usuarios():
    """Muestra en pantalla la lista de usuarios registrados."""
    conn = conectar()
    if conn is None:
        return
    cur = conn.cursor()
    cur.execute("""
        SELECT u.id_usuario, u.username, u.nombre_completo, r.nombre_rol, u.activo
        FROM usuarios u
        JOIN roles r ON u.id_rol = r.id_rol;
    """)
    usuarios_db = cur.fetchall()
    conn.close()

    print("Lista de Usuarios:")
    print("------------------")
    for usuario in usuarios_db:
        id_usuario, username, nombre_completo, nombre_rol, activo = usuario
        estado = "Activo" if activo == 1 else "Inactivo"
        print(f"ID: {id_usuario}, Usuario: {username}, Nombre: {nombre_completo}, Rol: {nombre_rol}, Estado: {estado}")


def desactivar_usuario():
    """Activa o desactiva un usuario existente."""
    conn = conectar()
    if conn is None:
        return
    cur = conn.cursor()
    listar_usuarios()
    try:
        id_usuario = int(input("Ingrese el ID del usuario a activar/desactivar: ").strip())
    except ValueError:
        print("ID inválido.")
        conn.close()
        return

    cur.execute("SELECT activo FROM usuarios WHERE id_usuario = ?;", (id_usuario,))
    row = cur.fetchone()
    if row is None:
        print("Usuario no encontrado.")
    else:
        estado_actual = row[0]
        nuevo_estado = 0 if estado_actual == 1 else 1
        try:
            cur.execute(
                "UPDATE usuarios SET activo = ? WHERE id_usuario = ?;",
                (nuevo_estado, id_usuario),
            )
            conn.commit()
            estado_texto = "desactivado" if nuevo_estado == 0 else "activado"
            print(f"Usuario ID {id_usuario} ha sido {estado_texto}.")
        except Exception as e:
            print("Error al actualizar el estado del usuario:", e)
    conn.close()
