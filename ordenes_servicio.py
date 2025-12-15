from datetime import datetime
from database import conectar


def registrar_orden_servicio(usuario):
    """Registra una nueva orden de servicio en la base de datos."""
    conn = conectar()
    if conn is None:
        return
    cur = conn.cursor()

    print("\n--- Registrar Orden de Servicio ---")
    nombre_cliente = input("Ingrese el nombre del cliente: ").strip()
    instrumento = input("Ingrese el instrumento a reparar: ").strip()
    tipo_servicio = input("Ingrese el tipo de servicio (mantenimiento/reparación/calibración, etc.): ").strip()
    descripcion_problema = input("Describa el problema o servicio requerido: ").strip()

    if not nombre_cliente or not instrumento or not tipo_servicio:
        print("Nombre del cliente, instrumento y tipo de servicio son obligatorios.")
        conn.close()
        return

    estado = "Pendiente"
    fecha_ingreso = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    fecha_salida = None
    costo = None
    id_cliente = None  # no usamos clientes ahora
    id_usuario = usuario["id_usuario"]

    try:
        cur.execute(
            """
            INSERT INTO ordenes_servicio (
                id_cliente, nombre_cliente, instrumento, tipo_servicio, descripcion,
                estado, fecha_ingreso, fecha_salida, costo, id_usuario_resp
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            """,
            (
                id_cliente, nombre_cliente, instrumento, tipo_servicio, descripcion_problema,
                estado, fecha_ingreso, fecha_salida, costo, id_usuario
            )
        )
        conn.commit()
        print("Orden de servicio registrada exitosamente.")
    except Exception as e:
        conn.rollback()
        print("Error al registrar la orden de servicio:", e)
    finally:
        conn.close()


def listar_ordenes(filtro_estado=None):
    """Lista las órdenes de servicio, opcionalmente filtradas por estado."""
    conn = conectar()
    if conn is None:
        return
    cur = conn.cursor()

    if filtro_estado:
        cur.execute(
            """
            SELECT id_orden, nombre_cliente, instrumento, tipo_servicio, estado, fecha_ingreso, fecha_salida, costo
            FROM ordenes_servicio
            WHERE estado = ?;
            """,
            (filtro_estado,)
        )
    else:
        cur.execute(
            """
            SELECT id_orden, nombre_cliente, instrumento, tipo_servicio, estado, fecha_ingreso, fecha_salida, costo
            FROM ordenes_servicio;
            """
        )

    ordenes = cur.fetchall()
    conn.close()

    print("Lista de Órdenes de Servicio:")
    print("-----------------------------")
    if not ordenes:
        print("No hay órdenes registradas.")
        return

    for orden in ordenes:
        (id_orden, nombre_cliente, instrumento, tipo_servicio,
         estado, fecha_ingreso, fecha_salida, costo) = orden
        print(f"ID Orden: {id_orden}, Cliente: {nombre_cliente}, Instrumento: {instrumento}, "
              f"Tipo de Servicio: {tipo_servicio}, Estado: {estado}, "
              f"Fecha Ingreso: {fecha_ingreso}, Fecha Salida: {fecha_salida}, Costo: {costo}")


def seleccionar_estado():
    """Permite al usuario seleccionar un estado para actualizar la orden."""
    print("Seleccione el nuevo estado de la orden:")
    print("1. Pendiente")
    print("2. En proceso")
    print("3. Finalizada")

    opcion = input("Ingrese el número correspondiente al estado: ").strip()

    if opcion == "1":
        return "Pendiente"
    elif opcion == "2":
        return "En proceso"
    elif opcion == "3":
        return "Finalizada"
    else:
        print("Opción inválida.")
        return None


def actualizar_estado_orden():
    """Actualiza el estado de una orden de servicio existente."""
    conn = conectar()
    if conn is None:
        return
    cur = conn.cursor()

    listar_ordenes()

    try:
        id_orden = int(input("Ingrese el ID de la orden de servicio a actualizar: ").strip())
    except ValueError:
        print("ID inválido.")
        conn.close()
        return

    nuevo_estado = seleccionar_estado()
    if nuevo_estado is None:
        print("No se seleccionó un estado válido.")
        conn.close()
        return

    try:
        cur.execute(
            "UPDATE ordenes_servicio SET estado = ? WHERE id_orden = ?;",
            (nuevo_estado, id_orden)
        )
        conn.commit()
        print(f"Estado de la orden ID {id_orden} actualizado a '{nuevo_estado}'.")
    except Exception as e:
        conn.rollback()
        print("Error al actualizar el estado de la orden:", e)
    finally:
        conn.close()


def reporte_servicios_mas_solicitados():
    """Muestra un ranking de tipos de servicio según cantidad de órdenes."""
    conn = conectar()
    if conn is None:
        return
    cur = conn.cursor()

    print("\n--- Servicios Más Solicitados ---")
    try:
        cur.execute(
            """
            SELECT tipo_servicio, COUNT(*) as cantidad
            FROM ordenes_servicio
            GROUP BY tipo_servicio
            ORDER BY cantidad DESC;
            """
        )
        filas = cur.fetchall()
    except Exception as e:
        print(f"Error al generar reporte: {e}")
        conn.close()
        return
    conn.close()

    if not filas:
        print("No se encontraron servicios registrados.")
        return

    for tipo_servicio, cantidad in filas:
        print(f"Servicio: {tipo_servicio}, Cantidad de Solicitudes: {cantidad}")
