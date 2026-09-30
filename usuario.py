class Usuario:
    def __init__(self, id_usuario, nombre, correo):
        self.id = id_usuario
        self.nombre = nombre
        self.correo = correo

    def obtener_rol(self):
        return "Usuario genérico"

    def __str__(self):
        return f"{self.nombre} ({self.obtener_rol()}) — {self.correo}"


class Estudiante(Usuario):
    def __init__(self, id_usuario, nombre, correo, carrera):
        super().__init__(id_usuario, nombre, correo)
        self.carrera = carrera

    def obtener_rol(self):
        return "Estudiante"


class Docente(Usuario):
    def __init__(self, id_usuario, nombre, correo, facultad):
        super().__init__(id_usuario, nombre, correo)
        self.facultad = facultad

    def obtener_rol(self):
        return "Docente"


class TecnicoSoporte(Usuario):
    def __init__(self, id_usuario, nombre, correo, especialidad):
        super().__init__(id_usuario, nombre, correo)
        self.especialidad = especialidad

    def obtener_rol(self):
        return "Técnico de Soporte"

    def resolver_ticket(self, ticket):
        ticket.cambiar_estado("Cerrado")


def crear_usuario(rol, id_usuario, nombre, correo, dato_extra):
    if rol == "estudiante":
        return Estudiante(id_usuario, nombre, correo, dato_extra)
    if rol == "docente":
        return Docente(id_usuario, nombre, correo, dato_extra)
    if rol == "tecnico":
        return TecnicoSoporte(id_usuario, nombre, correo, dato_extra)
    raise ValueError(f"Rol de usuario desconocido: {rol}")
