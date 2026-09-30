import json
import os

from usuario import Estudiante, Docente, TecnicoSoporte, crear_usuario
from ticket import TicketRed, TicketHardware, TicketSoftware, TicketCuenta, crear_ticket
from sistema import SistemaGestionTickets

RUTA_DATOS = os.path.join(os.path.dirname(__file__), "datos.json")


def sembrar_datos_ejemplo():
    sistema = SistemaGestionTickets()

    est1 = Estudiante(1, "Camila Rojas", "camila.rojas@uni.edu", "Ing. de Sistemas")
    doc1 = Docente(2, "Prof. Andrés Ruiz", "andres.ruiz@uni.edu", "Facultad de Ingeniería")
    doc2 = Docente(3, "Prof. Marta León", "marta.leon@uni.edu", "Facultad de Ciencias")
    tec1 = TecnicoSoporte(4, "Julián Pérez", "julian.perez@uni.edu", "Redes")
    tec2 = TecnicoSoporte(5, "Laura Gómez", "laura.gomez@uni.edu", "Hardware")
    tec3 = TecnicoSoporte(6, "Marcela Suárez", "marcela.suarez@uni.edu", "Software")

    usuarios = [est1, doc1, doc2, tec1, tec2, tec3]

    t1 = crear_ticket("red", sistema.generar_id(), "Sin internet en el laboratorio 3",
                       "Los computadores del laboratorio no tienen conexión a internet desde las 8:00 a.m.",
                       est1, "Bloque C · Laboratorio 3", "Alta")

    t2 = crear_ticket("hardware", sistema.generar_id(), "PC no enciende",
                       "El computador no enciende. Se revisó el cable de poder y sigue sin responder.",
                       est1, "Equipo PC-Lab3-05", "Media")
    t2.asignar_tecnico(tec2)

    t3 = crear_ticket("software", sistema.generar_id(), "Error al abrir el sistema académico",
                       "Al intentar ingresar notas, el sistema muestra un error 500 y se cierra.",
                       doc1, "Sistema Académico Institucional", "Alta")

    t4 = crear_ticket("cuenta", sistema.generar_id(), "No puedo entrar a mi correo institucional",
                       "Olvidé mi contraseña y el sistema no me deja recuperarla con la pregunta de seguridad.",
                       est1, "Correo institucional", "Baja")
    t4.tecnico_asignado = tec1
    tec1.resolver_ticket(t4)

    t5 = crear_ticket("red", sistema.generar_id(), "WiFi intermitente en biblioteca",
                       "La señal se cae cada 10-15 minutos en la sala de lectura del segundo piso.",
                       doc2, "Edificio Central · Biblioteca", "Media")

    t6 = crear_ticket("hardware", sistema.generar_id(), "Proyector de aula 204 no proyecta",
                       "El proyector enciende pero no muestra imagen, solo un fondo azul.",
                       doc1, "Aula 204", "Media")
    t6.asignar_tecnico(tec2)
    tec2.resolver_ticket(t6)

    t7 = crear_ticket("software", sistema.generar_id(), "Antivirus desactualizado en sala docentes",
                       "Varios equipos muestran alerta de licencia vencida del antivirus institucional.",
                       doc2, "Licencia institucional", "Baja")
    t7.asignar_tecnico(tec3)

    for t in [t1, t2, t3, t4, t5, t6, t7]:
        sistema.registrar_ticket(t)

    return sistema, usuarios


def _rol_de(usuario):
    if isinstance(usuario, Estudiante):
        return "estudiante"
    if isinstance(usuario, Docente):
        return "docente"
    if isinstance(usuario, TecnicoSoporte):
        return "tecnico"
    raise ValueError(f"No se reconoce el tipo de usuario: {type(usuario)}")


def _dato_extra_usuario(usuario):
    if isinstance(usuario, Estudiante):
        return usuario.carrera
    if isinstance(usuario, Docente):
        return usuario.facultad
    if isinstance(usuario, TecnicoSoporte):
        return usuario.especialidad
    raise ValueError(f"No se reconoce el tipo de usuario: {type(usuario)}")


def _detalle_extra_ticket(ticket):
    if isinstance(ticket, TicketRed):
        return ticket.zona_afectada
    if isinstance(ticket, TicketHardware):
        return ticket.equipo_afectado
    if isinstance(ticket, TicketSoftware):
        return ticket.programa_afectado
    if isinstance(ticket, TicketCuenta):
        return ticket.tipo_cuenta
    raise ValueError(f"No se reconoce el tipo de ticket: {type(ticket)}")


def guardar_datos(sistema, usuarios, ruta=RUTA_DATOS):
    datos = {
        "contador_id": sistema.contador_id,
        "usuarios": [
            {
                "id": u.id,
                "rol": _rol_de(u),
                "nombre": u.nombre,
                "correo": u.correo,
                "dato_extra": _dato_extra_usuario(u),
            }
            for u in usuarios
        ],
        "tickets": [
            {
                "id": t.id,
                "tipo": t.tipo,
                "titulo": t.titulo,
                "descripcion": t.descripcion,
                "usuario_reporta_id": t.usuario_reporta.id,
                "detalle_extra": _detalle_extra_ticket(t),
                "prioridad": t.prioridad,
                "estado": t.estado,
                "fecha_creacion": t.fecha_creacion,
                "tecnico_asignado_id": t.tecnico_asignado.id if t.tecnico_asignado else None,
            }
            for t in sistema.tickets
        ],
    }
    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, ensure_ascii=False, indent=2)


def cargar_datos(ruta=RUTA_DATOS):
    if not os.path.exists(ruta):
        return sembrar_datos_ejemplo()

    with open(ruta, "r", encoding="utf-8") as archivo:
        datos = json.load(archivo)

    usuarios = [
        crear_usuario(u["rol"], u["id"], u["nombre"], u["correo"], u["dato_extra"])
        for u in datos["usuarios"]
    ]
    usuarios_por_id = {u.id: u for u in usuarios}

    sistema = SistemaGestionTickets()
    sistema.contador_id = datos["contador_id"]

    for t in datos["tickets"]:
        ticket = crear_ticket(
            t["tipo"], t["id"], t["titulo"], t["descripcion"],
            usuarios_por_id[t["usuario_reporta_id"]], t["detalle_extra"], t["prioridad"],
        )
        ticket.estado = t["estado"]
        ticket.fecha_creacion = t["fecha_creacion"]
        if t["tecnico_asignado_id"] is not None:
            ticket.tecnico_asignado = usuarios_por_id[t["tecnico_asignado_id"]]
        sistema.registrar_ticket(ticket)

    return sistema, usuarios
