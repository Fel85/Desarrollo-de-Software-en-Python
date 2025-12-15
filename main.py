from database import *
from autenticacion import * 
import usuarios 
import productos 
import ventas 
import ordenes_servicio

def menu_admin(usuario): 

    """Menú principal para usuarios con rol ADMIN.""" 
    while True: 
        print("")
        print("\n=== Menú Administrador ===") 
        print("---------------------------")
        print(f"Usuario: {usuario['username']}") 
        print("1) Gestionar usuarios") 
        print("2) Gestionar productos") 
        print("3) Ver productos con stock bajo") 
        print("4) Registrar venta") 
        print("5) Ver ventas por rango de fechas") 
        print("6) Menú de órdenes de servicio") 
        print("0) Cerrar sesión")
        print("")
        opcion = input("Seleccione una opción: ").strip()
        print("")

        if opcion == "1":
            menu_gestion_usuarios()
        elif opcion == "2":
            menu_gestion_productos()
        elif opcion == "3":
            productos.listar_productos_stock_bajo()
        elif opcion == "4":
            ventas.registrar_venta(usuario)
        elif opcion == "5":
            ventas.listar_ventas_por_rango()
        elif opcion == "6":
            menu_ordenes_servicio(usuario)
        elif opcion == "0":
            print("Cerrando sesión...")
            break
        else:
            print("Opción inválida.")
 
def menu_vendedor(usuario): 
    """Menú principal para usuarios con rol VENDEDOR/TÉCNICO.""" 
    while True: 
        print("")
        print("\n=== Menú Vendedor/Técnico ===") 
        print("---------------------------")
        print(f"Usuario: {usuario['username']}") 
        print("1) Ver productos") 
        print("2) Ver productos con stock bajo") 
        print("3) Registrar venta") 
        print("4) Ver ventas por rango de fechas") 
        print("5) Menú de órdenes de servicio") 
        print("0) Cerrar sesión")
        print("")
        opcion = input("Seleccione una opción: ").strip()
        print("")

        if opcion == "1":
            productos.listar_productos()
        elif opcion == "2":
            productos.listar_productos_stock_bajo()
        elif opcion == "3":
            ventas.registrar_venta(usuario)
        elif opcion == "4":
            ventas.listar_ventas_por_rango()
        elif opcion == "5":
            menu_ordenes_servicio(usuario)
        elif opcion == "0":
            print("Cerrando sesión...")
            break
        else:
            print("Opción inválida.")
 
def menu_gestion_usuarios(): 
    """Submenú para crear, listar y activar/inactivar usuarios.""" 
    while True: 
        print("")
        print("\n--- Gestión de usuarios ---") 
        print("---------------------------")
        print("1) Crear usuario") 
        print("2) Listar usuarios") 
        print("3) Activar/Inactivar usuario") 
        print("0) Volver")
        print("")
        opcion = input("Opción: ").strip()
        print("")

        if opcion == "1":
            usuarios.crear_usuario()
        elif opcion == "2":
            usuarios.listar_usuarios()
        elif opcion == "3":
            usuarios.desactivar_usuario()
        elif opcion == "0":
            break
        else:
            print("Opción inválida.")
 
def menu_gestion_productos(): 
    """Submenú para crear, listar y actualizar productos.""" 
    while True: 
        print("")
        print("\n--- Gestión de productos ---") 
        print("---------------------------")
        print("1) Crear producto") 
        print("2) Listar productos") 
        print("3) Actualizar stock") 
        print("4) Activar/Inactivar producto") 
        print("0) Volver")
        print("")
        opcion = input("Opción: ").strip()
        print("")

        if opcion == "1":
            productos.crear_producto()
        elif opcion == "2":
            productos.listar_productos()
        elif opcion == "3":
            productos.actualizar_stock()
        elif opcion == "4":
            productos.eliminar_producto_logico()
        elif opcion == "0":
            break
        else:
            print("Opción inválida.")
 
def menu_ordenes_servicio(usuario): 
    """Submenú para trabajar con órdenes de servicio.""" 
    while True: 
        print("")
        print("\n--- Órdenes de servicio ---")
        print("---------------------------")
        print("1) Registrar nueva orden de servicio") 
        print("2) Listar todas las órdenes") 
        print("3) Listar órdenes por estado") 
        print("4) Actualizar estado de una orden") 
        print("5) Reporte: servicios más solicitados") 
        print("0) Volver")
        opcion = input("Opción: ").strip()
        print("")

        if opcion == "1":
                ordenes_servicio.registrar_orden_servicio(usuario)
        elif opcion == "2":
                ordenes_servicio.listar_ordenes()
        elif opcion == "3":
                print("\nEstados posibles: Pendiente / En proceso / Finalizada")
                estado = input("Ingrese el estado a filtrar: ").strip()
                if estado:
                    ordenes_servicio.listar_ordenes(filtro_estado=estado)
                else:
                    print("Estado vacío, operación cancelada.")
        elif opcion == "4":
            ordenes_servicio.actualizar_estado_orden()
        elif opcion == "5":
                ordenes_servicio.reporte_servicios_mas_solicitados()
        elif opcion == "0":
                break
        else:
                print("Opción inválida.")
 
def main(): 

    """Punto de entrada del sistema.""" 
    print("Iniciando sistema SoundWave Music Store...") 
    crear_tablas() 
    crear_usuario_admin_inicial()
    while True:
        print("")
        print("\n=== Inicio de sesión ===")
        print("---------------------------")
        username = input("Ingrese Usuario: ").strip()
        password = input("Ingrese Contraseña: ").strip()
        print("")

        usuario = autenticar_usuario(username, password)
        if usuario:
            print(f"\nBienvenido, {usuario['username']} (Rol: {usuario['rol']})")
            if usuario["rol"] == "ADMIN":
                menu_admin(usuario)
            else:
                menu_vendedor(usuario)
        else:
            print("Credenciales inválidas o usuario inactivo.")

        seguir = input("\n¿Desea intentar iniciar sesión nuevamente? (s/n): ").strip().lower()
        if seguir != "s":
            print("Saliendo del sistema. Hasta luego.")
            break
            
if __name__ == "__main__":
    main()