import sqlite3

DB_NAME = "soundwave.db"


def conectar():
    try:
        conn = sqlite3.connect(DB_NAME)
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn
    except sqlite3.Error as e:
        print("Error al conectar con la base de datos :", e)
        return None


def crear_tablas():
    conn = conectar()
    if conn is None:
        return
    cur = conn.cursor()
    cur.executescript("""
    PRAGMA foreign_keys = ON;

    -- Tabla de Roles 
    CREATE TABLE IF NOT EXISTS roles (
        id_rol       INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_rol   TEXT NOT NULL UNIQUE,
        descripcion  TEXT
    );

    -- Tabla de usuarios
    CREATE TABLE IF NOT EXISTS usuarios(
        id_usuario      INTEGER PRIMARY KEY AUTOINCREMENT,
        username        TEXT NOT NULL UNIQUE,
        nombre_completo TEXT NOT NULL,
        hash_password   TEXT NOT NULL,
        id_rol          INTEGER NOT NULL,
        activo          INTEGER NOT NULL DEFAULT 1,
        FOREIGN KEY (id_rol) REFERENCES roles (id_rol)
    );

    -- Tabla de clientes (opcional)
    CREATE TABLE IF NOT EXISTS clientes (
        id_cliente      INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre          TEXT NOT NULL,
        telefono        TEXT,
        email           TEXT
    );

    -- Tabla de productos
    CREATE TABLE IF NOT EXISTS productos (
        id_producto     INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre          TEXT NOT NULL,
        categoria       TEXT NOT NULL,
        marca           TEXT,
        precio          REAL NOT NULL,
        stock_actual    INTEGER NOT NULL,
        stock_minimo    INTEGER NOT NULL,
        activo          INTEGER NOT NULL DEFAULT 1
    ); 

    -- Tabla de ventas
    CREATE TABLE IF NOT EXISTS ventas(
        id_venta            INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha               TEXT  NOT NULL,
        id_usuario          INTEGER NOT NULL,
        id_cliente          INTEGER,
        total               REAL NOT NULL,
        FOREIGN KEY (id_usuario) REFERENCES usuarios (id_usuario),
        FOREIGN KEY (id_cliente) REFERENCES clientes (id_cliente)
    );

    -- Detalle de venta 
    CREATE TABLE IF NOT EXISTS detalle_venta (
        id_detalle          INTEGER PRIMARY KEY AUTOINCREMENT,
        id_venta            INTEGER NOT NULL,
        id_producto         INTEGER NOT NULL,
        cantidad            INTEGER NOT NULL,
        precio_unitario     REAL NOT NULL,
        subtotal            REAL NOT NULL,
        FOREIGN KEY (id_venta) REFERENCES ventas(id_venta),
        FOREIGN KEY (id_producto) REFERENCES productos(id_producto)
    );

    -- Órdenes de servicio (taller)
    CREATE TABLE IF NOT EXISTS ordenes_servicio (
        id_orden            INTEGER PRIMARY KEY AUTOINCREMENT,
        id_cliente          INTEGER,
        nombre_cliente      TEXT NOT NULL,
        instrumento         TEXT NOT NULL,
        tipo_servicio       TEXT NOT NULL,
        descripcion         TEXT,
        estado              TEXT NOT NULL,
        fecha_ingreso       TEXT NOT NULL,
        fecha_salida        TEXT,
        costo               REAL,
        id_usuario_resp     INTEGER,
        FOREIGN KEY (id_cliente)      REFERENCES clientes (id_cliente),
        FOREIGN KEY (id_usuario_resp) REFERENCES usuarios (id_usuario)  
    );

    -- Datos iniciales de roles 
    INSERT OR IGNORE INTO roles (id_rol, nombre_rol, descripcion)
    VALUES
        (1, 'ADMIN', 'Administrador del sistema'),
        (2, 'VENDEDOR', 'Vendedor o técnico de la tienda');
    """)
    conn.commit()
    conn.close()
