
====================================================
SOUNDWAVE MUSIC STORE - SISTEMA EN PYTHON (CONSOLA)
====================================================

1. NOMBRE DEL PROYECTO
----------------------
SoundWave Music Store  
Sistema de gestión para una tienda de instrumentos musicales, orientado a la administración de inventario, ventas y órdenes de servicio de taller.

2. DESCRIPCIÓN GENERAL
----------------------
Este proyecto es una aplicación desarrollada en Python que se ejecuta por consola y utiliza una base de datos SQLite para almacenar la información.

El sistema permite:
- Gestionar usuarios y roles (ADMIN, VENDEDOR/TÉCNICO).
- Administrar el catálogo de productos (instrumentos y accesorios).
- Registrar ventas y actualizar el stock automáticamente.
- Registrar y administrar órdenes de servicio de taller.
- Generar reportes básicos (productos con stock bajo, ventas por rango, servicios más solicitados).

Está pensado como una solución académica para aplicar programación orientada a objetos, manejo de base de datos y metodología ágil (Scrum simplificado).

3. FUNCIONALIDADES PRINCIPALES
------------------------------
- Autenticación de usuarios con contraseña hasheada.
- Menús diferenciados según el rol:
  
- ADMIN:
    - Gestionar usuarios (crear, listar, activar/desactivar).
    - Gestionar productos (crear, listar, actualizar stock, activar/desactivar).
    - Consultar productos con stock bajo.
    - Acceder al módulo de ventas.
    - Acceder al módulo de órdenes de servicio.
    - Consultar reportes.

  - VENDEDOR/TÉCNICO:
    - Consultar productos y stock.
    - Registrar ventas.
    - Registrar órdenes de servicio.
    - Consultar órdenes y reportes básicos.

4. REQUISITOS
-------------
- Python 3.x instalado.
- Sistema operativo compatible con Python (Windows, Linux o macOS).
- No se requieren librerías externas aparte de la biblioteca estándar (se usa sqlite3, hashlib, etc.).

5. INSTALACIÓN Y EJECUCIÓN
--------------------------
1) Clonar o descargar este proyecto en una carpeta local.

2) Abrir una terminal en la carpeta del proyecto, por ejemplo:
   - En Windows (PowerShell o CMD):
     cd ruta\hasta\soundwave

3) Ejecutar el programa principal:
   python main.py

4) En la primera ejecución:
   - Se creará automáticamente la base de datos SQLite (soundwave.db).
   - Se crearán las tablas necesarias si no existen.
   - Se generará un usuario ADMIN por defecto.

6. USUARIOS Y ROLES
-------------------
Usuario administrador inicial (creado automáticamente):

- Usuario:   admin
- Contraseña: admin123
- Rol:      ADMIN

Se recomienda:
- Iniciar sesión con este usuario.
- Crear nuevos usuarios (ADMIN o VENDEDOR/TÉCNICO) desde el menú de administración.
- Utilizar esos usuarios para probar las distintas funcionalidades del sistema.

7. ESTRUCTURA DE ARCHIVOS
-------------------------
Archivos principales del proyecto:

- main.py
  Punto de entrada del sistema. Gestiona el flujo principal, el inicio de sesión y los menús según rol.

- database.py
  Maneja la conexión a la base de datos SQLite (soundwave.db) y la creación de tablas:
  roles, usuarios, clientes (opcional), productos, ventas, detalle_venta, ordenes_servicio.

- autenticacion.py
  Funciones relacionadas con la seguridad:
  - hash de contraseñas (SHA-256).
  - creación de usuario admin inicial.
  - autenticación de usuarios.

- usuarios.py
  Gestión de usuarios:
  - Crear usuario nuevo.
  - Listar usuarios.
  - Activar/desactivar (baja lógica).

- productos.py
  Gestión de productos e inventario:
  - Crear producto.
  - Listar productos.
  - Actualizar stock.
  - Activar/desactivar producto.
  - Listar productos con stock bajo.

- ventas.py
  Gestión de ventas:
  - Registrar una venta con uno o más productos.
  - Actualizar stock según las cantidades vendidas.
  - Consultar ventas por rango de fechas.

- ordenes_servicio.py
  Gestión de órdenes de servicio de taller:
  - Registrar nueva orden de servicio.
  - Listar órdenes y filtrar por estado.
  - Actualizar estado de una orden (Pendiente, En proceso, Finalizada).
  - Reporte de servicios más solicitados.

- soundwave.db (opcional en el repositorio)
  Archivo de base de datos SQLite generado por el sistema.
  Si no se incluye, el programa creará uno nuevo al ejecutarse.

8. NOTAS TÉCNICAS
-----------------
- La base de datos utiliza claves foráneas y restricciones básicas para mantener la integridad de los datos.
- Las contraseñas NO se almacenan en texto plano; se guardan como hash SHA-256.
- Se usan validaciones básicas en consola (conversiones numéricas, opciones de menú, etc.).
- El sistema está diseñado para uso en consola, sin interfaz gráfica, pero la estructura modular permite extenderlo a GUI o aplicaciones web en el futuro.

9. EQUIPO DEL PROYECTO
----------------------
- Product Owner:      Sebastián Pasmiño
- Scrum Master:       Felipe Sanhueza
- Equipo de Desarrollo: Pedro Reyes

10. TRABAJO FUTURO
------------------
Algunas posibles mejoras para versiones posteriores:
- Desarrollar una interfaz gráfica (GUI) o versión web.
- Completar el módulo de clientes con historial de compras y servicios.
- Exportar reportes a formatos como PDF o Excel.
- Añadir validaciones y mecanismos de seguridad más avanzados.
