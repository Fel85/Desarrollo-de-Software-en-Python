from database import conectar


def crear_producto():
    """Crea un nuevo producto en la base de datos."""
    conn = conectar()
    if conn is None:
        return
    cur = conn.cursor()

    nombre = input("Ingrese el nombre del producto: ").strip()
    categoria = input("Ingrese la categoría del producto: ").strip()
    marca = input("Ingrese la marca del producto: ").strip()
    try:
        precio = float(input("Ingrese el precio del producto: ").strip())
        stock_actual = int(input("Ingrese el stock actual del producto: ").strip())
        stock_minimo = int(input("Ingrese el stock mínimo del producto: ").strip())
    except ValueError:
        print("Precio y stock deben ser números válidos.")
        conn.close()
        return

    try:
        cur.execute("""
            INSERT INTO productos (nombre, categoria, marca, precio, stock_actual, stock_minimo, activo)
            VALUES (?, ?, ?, ?, ?, ?, 1);
        """, (nombre, categoria, marca, precio, stock_actual, stock_minimo))
        conn.commit()
        print(f"Producto '{nombre}' creado exitosamente.")
    except Exception as e:
        print("Error al crear el producto:", e)
    finally:
        conn.close()


def listar_productos():
    """Muestra en pantalla la lista de productos registrados."""
    conn = conectar()
    if conn is None:
        return
    cur = conn.cursor()
    cur.execute("""
        SELECT id_producto, nombre, categoria, marca, precio, stock_actual, stock_minimo, activo
        FROM productos;
    """)
    productos_db = cur.fetchall()
    conn.close()

    print("Lista de Productos:")
    print("-------------------")
    for producto in productos_db:
        id_producto, nombre, categoria, marca, precio, stock_actual, stock_minimo, activo = producto
        estado = "Activo" if activo == 1 else "Inactivo"
        print(f"ID: {id_producto}, Nombre: {nombre}, Categoría: {categoria}, Marca: {marca}, Precio: ${precio}, Stock Actual: {stock_actual}, Stock Mínimo: {stock_minimo}, Estado: {estado}")


def actualizar_stock():
    """Actualiza el stock de un producto existente."""
    conn = conectar()
    if conn is None:
        return
    cur = conn.cursor()
    listar_productos()
    try:
        id_producto = int(input("Ingrese el ID del producto a actualizar: ").strip())
        nuevo_stock = int(input("Ingrese el nuevo stock del producto: ").strip())
    except ValueError:
        print("ID y stock deben ser números válidos.")
        conn.close()
        return

    cur.execute("SELECT nombre FROM productos WHERE id_producto = ?;", (id_producto,))
    row = cur.fetchone()
    if row is None:
        print("Producto no encontrado.")
    else:
        try:
            cur.execute(
                "UPDATE productos SET stock_actual = ? WHERE id_producto = ?;",
                (nuevo_stock, id_producto),
            )
            conn.commit()
            print(f"Stock del producto ID {id_producto} actualizado a {nuevo_stock}.")
        except Exception as e:
            print("Error al actualizar el stock:", e)
    conn.close()


def eliminar_producto_logico():
    """Activa o desactiva un producto (baja lógica)."""
    conn = conectar()
    if conn is None:
        return
    cur = conn.cursor()
    listar_productos()
    try:
        id_producto = int(input("Ingrese el ID del producto a activar/desactivar: ").strip())
    except ValueError:
        print("ID inválido.")
        conn.close()
        return

    cur.execute("SELECT activo FROM productos WHERE id_producto = ?;", (id_producto,))
    row = cur.fetchone()
    if row is None:
        print("Producto no encontrado.")
    else:
        estado_actual = row[0]
        nuevo_estado = 0 if estado_actual == 1 else 1
        try:
            cur.execute(
                "UPDATE productos SET activo = ? WHERE id_producto = ?;",
                (nuevo_estado, id_producto),
            )
            conn.commit()
            estado_texto = "desactivado" if nuevo_estado == 0 else "activado"
            print(f"Producto ID {id_producto} ha sido {estado_texto}.")
        except Exception as e:
            print("Error al actualizar el estado del producto:", e)
    conn.close()


def listar_productos_stock_bajo():
    """Muestra la lista de productos cuyo stock actual es menor o igual al stock mínimo."""
    conn = conectar()
    if conn is None:
        return
    cur = conn.cursor()
    cur.execute("""
        SELECT id_producto, nombre, categoria, marca, precio, stock_actual, stock_minimo
        FROM productos
        WHERE stock_actual <= stock_minimo AND activo = 1;
    """)
    productos_db = cur.fetchall()
    conn.close()

    print("Productos con Stock Bajo:")
    print("-------------------------")
    if not productos_db:
        print("No hay productos con stock bajo.")
        return

    for producto in productos_db:
        id_producto, nombre, categoria, marca, precio, stock_actual, stock_minimo = producto
        print(f"ID: {id_producto}, Nombre: {nombre}, Categoría: {categoria}, Marca: {marca}, Precio: {precio}, Stock Actual: {stock_actual}, Stock Mínimo: {stock_minimo}")
