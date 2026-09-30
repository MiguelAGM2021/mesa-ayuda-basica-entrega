import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, render_template, request, redirect, url_for, session, flash, abort

from usuario import TecnicoSoporte, crear_usuario
from ticket import crear_ticket
from datos import cargar_datos, guardar_datos

app = Flask(__name__)
app.secret_key = "dev-secret-key-mesa-ayuda"

sistema, usuarios = cargar_datos()


def obtener_usuario_actual():
    usuario_id = session.get("usuario_id")
    if usuario_id is None:
        return None
    return next((u for u in usuarios if u.id == usuario_id), None)


@app.context_processor
def inject_usuario():
    return {"usuario": obtener_usuario_actual()}


@app.route("/")
def index():
    if obtener_usuario_actual() is None:
        return redirect(url_for("elegir_usuario"))
    return redirect(url_for("ver_tickets"))


@app.route("/elegir-usuario", methods=["GET", "POST"])
def elegir_usuario():
    if request.method == "POST":
        usuario_id = request.form.get("usuario_id", "")
        if usuario_id.isdigit() and any(u.id == int(usuario_id) for u in usuarios):
            session["usuario_id"] = int(usuario_id)
            return redirect(url_for("index"))
        flash("Elegí un usuario de la lista.")
    return render_template("elegir_usuario.html", usuarios=usuarios)


@app.route("/cambiar-usuario", methods=["POST"])
def cambiar_usuario():
    session.pop("usuario_id", None)
    return redirect(url_for("elegir_usuario"))


@app.route("/tickets")
def ver_tickets():
    if obtener_usuario_actual() is None:
        return redirect(url_for("elegir_usuario"))
    tipo = request.args.get("tipo", "todos")
    estado = request.args.get("estado", "")
    tickets = sistema.filtrar_por_tipo(tipo)
    if estado:
        tickets = [t for t in tickets if t.estado == estado]
    return render_template("tickets.html", tickets=tickets, tipo_actual=tipo, estado_actual=estado)


@app.route("/tickets/<int:ticket_id>")
def ver_ticket_detalle(ticket_id):
    if obtener_usuario_actual() is None:
        return redirect(url_for("elegir_usuario"))
    ticket = sistema.buscar_por_id(ticket_id)
    if ticket is None:
        abort(404)
    return render_template("ticket_detalle.html", ticket=ticket)


TIPOS_TICKET = ("red", "hardware", "software", "cuenta")


@app.route("/tickets/nuevo", methods=["GET", "POST"])
def nuevo_ticket():
    if obtener_usuario_actual() is None:
        return redirect(url_for("elegir_usuario"))

    if request.method == "POST":
        tipo = request.form.get("tipo", "")
        titulo = request.form.get("titulo", "").strip()
        descripcion = request.form.get("descripcion", "").strip()
        detalle_extra = request.form.get("detalle_extra", "").strip()
        prioridad = request.form.get("prioridad", "Media")
        usuario_reporta_id = request.form.get("usuario_reporta_id", "")
        reportante = next((u for u in usuarios if str(u.id) == usuario_reporta_id), None)

        if tipo not in TIPOS_TICKET or not titulo or not descripcion or not detalle_extra or reportante is None:
            flash("Completá todos los campos antes de crear el ticket.")
            return render_template("nuevo_ticket.html", usuarios=usuarios, form=request.form)

        ticket = crear_ticket(tipo, sistema.generar_id(), titulo, descripcion,
                               reportante, detalle_extra, prioridad)
        sistema.registrar_ticket(ticket)
        guardar_datos(sistema, usuarios)
        return redirect(url_for("ver_ticket_detalle", ticket_id=ticket.id))

    return render_template("nuevo_ticket.html", usuarios=usuarios, form={})


@app.route("/tickets/<int:ticket_id>/asignar", methods=["POST"])
def asignar_tecnico_ticket(ticket_id):
    usuario = obtener_usuario_actual()
    if usuario is None:
        return redirect(url_for("elegir_usuario"))
    ticket = sistema.buscar_por_id(ticket_id)
    if ticket is None:
        abort(404)
    if not isinstance(usuario, TecnicoSoporte):
        flash("Solo un técnico de soporte puede asignarse tickets.")
        return redirect(url_for("ver_ticket_detalle", ticket_id=ticket_id))
    ticket.asignar_tecnico(usuario)
    guardar_datos(sistema, usuarios)
    return redirect(url_for("ver_ticket_detalle", ticket_id=ticket_id))


@app.route("/tickets/<int:ticket_id>/resolver", methods=["POST"])
def resolver_ticket_ruta(ticket_id):
    usuario = obtener_usuario_actual()
    if usuario is None:
        return redirect(url_for("elegir_usuario"))
    ticket = sistema.buscar_por_id(ticket_id)
    if ticket is None:
        abort(404)
    if ticket.tecnico_asignado is None:
        flash("Este ticket todavía no tiene técnico asignado — asignalo primero.")
        return redirect(url_for("ver_ticket_detalle", ticket_id=ticket_id))
    ticket.tecnico_asignado.resolver_ticket(ticket)
    guardar_datos(sistema, usuarios)
    return redirect(url_for("ver_ticket_detalle", ticket_id=ticket_id))


ROLES = {
    "estudiante": "Carrera",
    "docente": "Facultad",
    "tecnico": "Especialidad",
}


@app.route("/usuarios")
def ver_usuarios():
    if obtener_usuario_actual() is None:
        return redirect(url_for("elegir_usuario"))
    return render_template("usuarios.html", usuarios=usuarios)


@app.route("/usuarios/nuevo", methods=["GET", "POST"])
def nuevo_usuario():
    if obtener_usuario_actual() is None:
        return redirect(url_for("elegir_usuario"))

    if request.method == "POST":
        rol = request.form.get("rol", "")
        nombre = request.form.get("nombre", "").strip()
        correo = request.form.get("correo", "").strip()
        dato_extra = request.form.get("dato_extra", "").strip()

        if rol not in ROLES or not nombre or not correo or not dato_extra:
            flash("Completá todos los campos antes de registrar el usuario.")
            return render_template("nuevo_usuario.html", roles=ROLES, form=request.form)

        siguiente_id = max((u.id for u in usuarios), default=0) + 1
        nuevo = crear_usuario(rol, siguiente_id, nombre, correo, dato_extra)
        usuarios.append(nuevo)
        guardar_datos(sistema, usuarios)
        return redirect(url_for("ver_usuarios"))

    return render_template("nuevo_usuario.html", roles=ROLES, form={})


if __name__ == "__main__":
    app.run(debug=True)
