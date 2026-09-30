import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from usuario import TecnicoSoporte, crear_usuario
from ticket import crear_ticket
from datos import cargar_datos, guardar_datos

TIPOS_TICKET = {
    "1": ("red", "Red", "Zona afectada"),
    "2": ("hardware", "Hardware", "Equipo afectado"),
    "3": ("software", "Software", "Programa afectado"),
    "4": ("cuenta", "Cuenta", "Tipo de cuenta"),
}

PRIORIDADES = {"1": "Baja", "2": "Media", "3": "Alta"}

ROLES = {
    "1": ("estudiante", "Carrera"),
    "2": ("docente", "Facultad"),
    "3": ("tecnico", "Especialidad"),
}


def pedir_opcion(mensaje, opciones_validas):
    while True:
        opcion = input(mensaje).strip()
        if opcion in opciones_validas:
            return opcion
        print("Opción inválida, probá de nuevo.\n")


def mostrar_menu():
    print("\n=== MESA DE AYUDA — MENÚ PRINCIPAL ===")
    print("1. Ver todos los tickets")
    print("2. Ver tickets por tipo")
    print("3. Ver tickets por estado")
    print("4. Ver detalle de un ticket")
    print("5. Crear ticket nuevo")
    print("6. Asignar técnico a un ticket")
    print("7. Resolver (cerrar) un ticket")
    print("8. Ver usuarios registrados")
    print("9. Registrar usuario nuevo")
    print("0. Guardar y salir")


def listar_tickets(tickets):
    if not tickets:
        print("(no hay tickets para mostrar)")
        return
    for ticket in tickets:
        print(f"  {ticket}")


def elegir_usuario(usuarios, mensaje="Elegí un usuario:"):
    print(mensaje)
    for i, usuario in enumerate(usuarios, start=1):
        print(f"  {i}. {usuario}")
    opcion = pedir_opcion("Número: ", [str(i) for i in range(1, len(usuarios) + 1)])
    return usuarios[int(opcion) - 1]


def elegir_ticket(sistema):
    if not sistema.tickets:
        print("(no hay tickets todavía)")
        return None
    listar_tickets(sistema.tickets)
    id_texto = input("ID del ticket: ").strip()
    if not id_texto.isdigit():
        print("Eso no es un número.")
        return None
    ticket = sistema.buscar_por_id(int(id_texto))
    if ticket is None:
        print("No existe un ticket con ese ID.")
    return ticket


def opcion_ver_todos(sistema):
    print(f"\nTotal de tickets: {len(sistema.tickets)}")
    listar_tickets(sistema.tickets)


def opcion_ver_por_tipo(sistema):
    print("\nTipos: 1) Red  2) Hardware  3) Software  4) Cuenta")
    opcion = pedir_opcion("Elegí un tipo: ", TIPOS_TICKET.keys())
    tipo, nombre, _ = TIPOS_TICKET[opcion]
    print(f"\nTickets de tipo {nombre}:")
    listar_tickets(sistema.filtrar_por_tipo(tipo))


def opcion_ver_por_estado(sistema):
    estado = input("\nEstado a buscar (Abierto / En proceso / Cerrado): ").strip()
    print(f"\nTickets en estado \"{estado}\":")
    listar_tickets(sistema.filtrar_por_estado(estado))


def opcion_ver_detalle(sistema):
    ticket = elegir_ticket(sistema)
    if ticket is None:
        return
    print(f"\n{ticket}")
    print(f"  Descripción: {ticket.descripcion}")
    print(f"  {ticket.obtener_detalle()}")
    print(f"  Reportado por: {ticket.usuario_reporta}")
    print(f"  Creado el: {ticket.fecha_creacion}")


def opcion_crear_ticket(sistema, usuarios):
    print("\nTipos: 1) Red  2) Hardware  3) Software  4) Cuenta")
    opcion_tipo = pedir_opcion("Elegí un tipo: ", TIPOS_TICKET.keys())
    tipo, _, etiqueta_detalle = TIPOS_TICKET[opcion_tipo]

    titulo = input("Título del ticket: ").strip()
    descripcion = input("Descripción: ").strip()
    detalle_extra = input(f"{etiqueta_detalle}: ").strip()

    print("Prioridad: 1) Baja  2) Media  3) Alta")
    opcion_prioridad = pedir_opcion("Elegí una prioridad: ", PRIORIDADES.keys())
    prioridad = PRIORIDADES[opcion_prioridad]

    usuario_reporta = elegir_usuario(usuarios, "\n¿Quién reporta el ticket?")

    ticket = crear_ticket(tipo, sistema.generar_id(), titulo, descripcion,
                           usuario_reporta, detalle_extra, prioridad)
    sistema.registrar_ticket(ticket)
    print(f"\nTicket creado: {ticket}")


def opcion_asignar_tecnico(sistema, usuarios):
    ticket = elegir_ticket(sistema)
    if ticket is None:
        return
    tecnicos = [u for u in usuarios if isinstance(u, TecnicoSoporte)]
    if not tecnicos:
        print("No hay técnicos registrados todavía.")
        return
    tecnico = elegir_usuario(tecnicos, "\n¿A qué técnico se lo asignás?")
    ticket.asignar_tecnico(tecnico)
    print(f"\nListo: {ticket}")


def opcion_resolver_ticket(sistema, usuarios):
    ticket = elegir_ticket(sistema)
    if ticket is None:
        return
    if ticket.tecnico_asignado is None:
        print("Este ticket todavía no tiene técnico asignado — asignalo primero (opción 6).")
        return
    ticket.tecnico_asignado.resolver_ticket(ticket)
    print(f"\nListo: {ticket}")


def opcion_ver_usuarios(usuarios):
    print(f"\nTotal de usuarios: {len(usuarios)}")
    for usuario in usuarios:
        print(f"  {usuario}")


def opcion_registrar_usuario(usuarios):
    print("\nRoles: 1) Estudiante  2) Docente  3) Técnico de soporte")
    opcion_rol = pedir_opcion("Elegí un rol: ", ROLES.keys())
    rol, etiqueta_extra = ROLES[opcion_rol]

    nombre = input("Nombre: ").strip()
    correo = input("Correo: ").strip()
    dato_extra = input(f"{etiqueta_extra}: ").strip()

    siguiente_id = max((u.id for u in usuarios), default=0) + 1
    usuario = crear_usuario(rol, siguiente_id, nombre, correo, dato_extra)
    usuarios.append(usuario)
    print(f"\nUsuario registrado: {usuario}")


def main():
    sistema, usuarios = cargar_datos()
    print("=== Sistema de Gestión de Tickets de Fallas — Universidad ===")
    print("(versión 100% básica en Python, sin base de datos ni hosting)")

    while True:
        mostrar_menu()
        opcion = pedir_opcion("\nElegí una opción: ", [str(i) for i in range(10)])

        if opcion == "1":
            opcion_ver_todos(sistema)
        elif opcion == "2":
            opcion_ver_por_tipo(sistema)
        elif opcion == "3":
            opcion_ver_por_estado(sistema)
        elif opcion == "4":
            opcion_ver_detalle(sistema)
        elif opcion == "5":
            opcion_crear_ticket(sistema, usuarios)
        elif opcion == "6":
            opcion_asignar_tecnico(sistema, usuarios)
        elif opcion == "7":
            opcion_resolver_ticket(sistema, usuarios)
        elif opcion == "8":
            opcion_ver_usuarios(usuarios)
        elif opcion == "9":
            opcion_registrar_usuario(usuarios)
        elif opcion == "0":
            guardar_datos(sistema, usuarios)
            print("\nDatos guardados en datos.json. ¡Hasta luego!")
            break


if __name__ == "__main__":
    main()
