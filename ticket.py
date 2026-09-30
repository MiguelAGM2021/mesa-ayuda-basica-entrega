from datetime import datetime


class Ticket:
    def __init__(self, id_ticket, titulo, descripcion, usuario_reporta, prioridad="Media"):
        self.id = id_ticket
        self.titulo = titulo
        self.descripcion = descripcion
        self.usuario_reporta = usuario_reporta
        self.prioridad = prioridad
        self.estado = "Abierto"
        self.fecha_creacion = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.tecnico_asignado = None
        self.tipo = "general"

    def cambiar_estado(self, nuevo_estado):
        self.estado = nuevo_estado

    def asignar_tecnico(self, tecnico):
        self.tecnico_asignado = tecnico
        if self.estado == "Abierto":
            self.cambiar_estado("En proceso")

    def obtener_detalle(self):
        return "Sin detalle adicional"

    def __str__(self):
        tecnico = self.tecnico_asignado.nombre if self.tecnico_asignado else "sin asignar"
        return (f"#{self.id} [{self.tipo}] {self.titulo} — {self.estado} "
                f"(prioridad {self.prioridad}, técnico: {tecnico})")


class TicketRed(Ticket):
    def __init__(self, id_ticket, titulo, descripcion, usuario_reporta, zona_afectada, prioridad="Media"):
        super().__init__(id_ticket, titulo, descripcion, usuario_reporta, prioridad)
        self.tipo = "red"
        self.zona_afectada = zona_afectada

    def obtener_detalle(self):
        return f"Zona afectada: {self.zona_afectada}"


class TicketHardware(Ticket):
    def __init__(self, id_ticket, titulo, descripcion, usuario_reporta, equipo_afectado, prioridad="Media"):
        super().__init__(id_ticket, titulo, descripcion, usuario_reporta, prioridad)
        self.tipo = "hardware"
        self.equipo_afectado = equipo_afectado

    def obtener_detalle(self):
        return f"Equipo afectado: {self.equipo_afectado}"


class TicketSoftware(Ticket):
    def __init__(self, id_ticket, titulo, descripcion, usuario_reporta, programa_afectado, prioridad="Media"):
        super().__init__(id_ticket, titulo, descripcion, usuario_reporta, prioridad)
        self.tipo = "software"
        self.programa_afectado = programa_afectado

    def obtener_detalle(self):
        return f"Programa afectado: {self.programa_afectado}"


class TicketCuenta(Ticket):
    def __init__(self, id_ticket, titulo, descripcion, usuario_reporta, tipo_cuenta, prioridad="Media"):
        super().__init__(id_ticket, titulo, descripcion, usuario_reporta, prioridad)
        self.tipo = "cuenta"
        self.tipo_cuenta = tipo_cuenta

    def obtener_detalle(self):
        return f"Tipo de cuenta: {self.tipo_cuenta}"


def crear_ticket(tipo, id_ticket, titulo, descripcion, usuario_reporta, detalle_extra, prioridad="Media"):
    if tipo == "red":
        return TicketRed(id_ticket, titulo, descripcion, usuario_reporta, detalle_extra, prioridad)
    if tipo == "hardware":
        return TicketHardware(id_ticket, titulo, descripcion, usuario_reporta, detalle_extra, prioridad)
    if tipo == "software":
        return TicketSoftware(id_ticket, titulo, descripcion, usuario_reporta, detalle_extra, prioridad)
    if tipo == "cuenta":
        return TicketCuenta(id_ticket, titulo, descripcion, usuario_reporta, detalle_extra, prioridad)
    raise ValueError(f"Tipo de ticket desconocido: {tipo}")
