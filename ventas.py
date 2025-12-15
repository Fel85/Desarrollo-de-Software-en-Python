from datetime import datetime
from database import conectar
import productos


def registrar_venta(usuario):
    """Registra una venta con uno o más productos, guarda en BD y descuenta stock."""
    conn = conectar()
    if conn is None:
        return
    cur = conn.cursor()

    print("\n--- Registrar Venta ---")
    nombre_cliente = input("Ingrese el nombre del cliente (opcional): ").strip()
    id_cliente = None  # no usamos tabla clientes por ahora

    items_venta = []
    total_venta = 0

    while True:
        print("\nProductos disponibles:")
        productos.listar_productos()

        id_producto = input("Ingrese el ID del producto a vender (ENTER para terminar): ").strip()
        if id_producto == "":
            break

        try:
            id_producto = int(id_producto)
        except ValueError:
            print("ID inválido. Intente nuevamente.")
            continue

        try:
            cantidad = int(input("Ingrese la cantidad a vender: ").strip())
        except ValueError:
            print("Cantidad inválida. Intente nuevamente.")
            continue

        cur.execute(
            "SELECT nombre, precio, stock_actual FROM productos WHERE id_producto = ? AND activo = 1;",
            (id_producto,),
        )
        row = cur.fetchone()
        if row is None:
            print("Producto no encontrado o inactivo.")
            continue

        nombre_producto, precio_unitario, stock_actual = row
        if cantidad > stock_actual:
            print(f"Stock insuficiente. Stock actual: {stock_actual}.")
            continue

        subtotal = precio_unitario * cantidad
        items_venta.append((id_producto, nombre_producto, cantidad, precio_unitario, subtotal))
        total_venta += subtotal

        print(f"Producto '{nombre_producto}' x {cantidad} = ${subtotal}")
        print(f"Total parcial de la venta: ${total_venta}")

    if not items_venta:
        print("No se registraron productos para la venta.")
        conn.close()
        return

    print("\nResumen de la venta:")
    for item in items_venta:
        id_prod, nom_prod, cant, precio_u, sub = item
        print(f"- {nom_prod} x {cant} @ ${precio_u} c/u = ${sub}")
    print(f"Total de la venta: ${total_venta}")

    confirmar = input("¿Confirma la venta? (s/n): ").strip().lower()
    if confirmar != 's':
        print("Venta cancelada.")
        conn.close()
        return

    fecha_venta = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        cur.execute(
            """
            INSERT INTO ventas (fecha, id_usuario, id_cliente, total)
            VALUES (?, ?, ?, ?);
            """,
            (fecha_venta, usuario["id_usuario"], id_cliente, total_venta)
        )
        id_venta = cur.lastrowid

        for item in items_venta:
            id_prod, nom_prod, cant, precio_u, sub = item
            cur.execute(
                """
                INSERT INTO detalle_venta (id_venta, id_producto, cantidad, precio_unitario, subtotal)
                VALUES (?, ?, ?, ?, ?);
                """,
                (id_venta, id_prod, cant, precio_u, sub)
            )
            cur.execute(
                """
                UPDATE productos
                SET stock_actual = stock_actual - ?
                WHERE id_producto = ?;
                """,
                (cant, id_prod)
            )

        conn.commit()
        print("Venta registrada exitosamente.")
    except Exception as e:
        conn.rollback()
        print("Error al registrar la venta:", e)
    finally:
        conn.close()


def listar_ventas_por_rango():
    """Lista las ventas realizadas en un rango de fechas especificado."""
    conn = conectar()
    if conn is None:
        return
    cur = conn.cursor()
    print("\n--- Listar Ventas por Rango de Fecha ---")
    fecha_inicio = input("Ingrese la fecha de inicio (YYYY-MM-DD): ").strip()
    fecha_fin = input("Ingrese la fecha de fin (YYYY-MM-DD): ").strip()

    try:
        cur.execute(
            """
            SELECT v.id_venta, v.fecha, u.username, v.total
            FROM ventas v
            JOIN usuarios u ON v.id_usuario = u.id_usuario
            WHERE DATE(v.fecha) BETWEEN DATE(?) AND DATE(?)
            ORDER BY v.fecha ASC;
            """,
            (fecha_inicio, fecha_fin)
        )
        ventas_db = cur.fetchall()

        if not ventas_db:
            print("No se encontraron ventas en el rango de fechas especificado.")
        else:
            print(f"\nVentas desde {fecha_inicio} hasta {fecha_fin}:")
            for venta in ventas_db:
                id_venta, fecha, username, total = venta
                print(f"- ID Venta: {id_venta}, Fecha: {fecha}, Vendedor: {username}, Total: ${total}")
    except Exception as e:
        print("Error al listar las ventas:", e)
    finally:
        conn.close()
