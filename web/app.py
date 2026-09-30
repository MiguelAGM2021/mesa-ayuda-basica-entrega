import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, render_template, request, redirect, url_for, session, flash, abort

from usuario import Estudiante, Docente, TecnicoSoporte, crear_usuario
from ticket import crear_ticket
from datos import cargar_datos, guardar_datos

app = Flask(__name__)
app.secret_key = "dev-secret-key-mesa-ayuda"

sistema, usuarios = cargar_datos()


CATEGORIAS = {
    "red": {
        "label": "Red", "color": "var(--blue)", "soft": "var(--blue-soft)",
        "icono": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M5 12.5a11 11 0 0 1 14 0"/><path d="M8.5 16a6 6 0 0 1 7 0"/><circle cx="12" cy="19.5" r="1" fill="currentColor" stroke="none"/></svg>',
    },
    "hardware": {
        "label": "Hardware", "color": "var(--red)", "soft": "var(--red-soft)",
        "icono": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><rect x="3" y="4" width="18" height="12" rx="1.5"/><path d="M8 20h8M12 16v4"/></svg>',
    },
    "software": {
        "label": "Software", "color": "var(--teal)", "soft": "var(--teal-soft)",
        "icono": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 18l-5-6 5-6M15 6l5 6-5 6"/></svg>',
    },
    "cuenta": {
        "label": "Cuenta", "color": "var(--amber)", "soft": "var(--amber-soft)",
        "icono": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="8" cy="8" r="4.5"/><path d="M11 11l8.5 8.5M16 16l2.5-2.5M18.5 18.5L21 16"/></svg>',
    },
}

PRIORIDAD_COLOR = {"Alta": "var(--red)", "Media": "var(--amber)", "Baja": "var(--teal)"}

ETIQUETA_DETALLE = {
    "red": "Zona afectada (ej: Bloque C · Lab 3)",
    "hardware": "Equipo afectado (ej: PC-Lab3-05)",
    "software": "Programa afectado (ej: Sistema Académico)",
    "cuenta": "Tipo de cuenta (ej: Correo institucional)",
}

ETIQUETA_ROL = {"estudiante": "Alumno", "docente": "Profesor", "tecnico": "Técnico"}
ROL_CSS = {"estudiante": "estudiante", "docente": "profesor", "tecnico": "tecnico"}

MESES_CORTOS = {1: "ene", 2: "feb", 3: "mar", 4: "abr", 5: "may", 6: "jun",
                7: "jul", 8: "ago", 9: "sep", 10: "oct", 11: "nov", 12: "dic"}


def iniciales(nombre):
    partes = [p for p in nombre.split(" ") if p and p[0].isupper()]
    return "".join(p[0] for p in partes[:2]).upper()


def estado_visual(estado):
    sello_clase = "sello cerrado" if estado == "Cerrado" else "sello"
    sello_texto = "RESUELTO" if estado == "Cerrado" else estado.upper()
    if estado == "Abierto":
        color, fondo = "var(--blue)", "var(--blue-soft)"
    elif estado == "En proceso":
        color, fondo = "var(--amber)", "var(--amber-soft)"
    else:
        color, fondo = "var(--green)", "var(--green-soft)"
    return {"clase": sello_clase, "texto": sello_texto, "color": color, "fondo": fondo}


def formatear_fecha(fecha_texto):
    try:
        f = datetime.strptime(fecha_texto, "%Y-%m-%d %H:%M")
    except ValueError:
        return fecha_texto
    return f"{f.day:02d} {MESES_CORTOS[f.month]}, {f.strftime('%H:%M')}"


app.jinja_env.filters["iniciales"] = iniciales
app.jinja_env.filters["estado_visual"] = estado_visual
app.jinja_env.filters["fecha_es"] = formatear_fecha
app.jinja_env.globals["CATEGORIAS"] = CATEGORIAS
app.jinja_env.globals["PRIORIDAD_COLOR"] = PRIORIDAD_COLOR


def obtener_usuario_actual():
    usuario_id = session.get("usuario_id")
    if usuario_id is None:
        return None
    return next((u for u in usuarios if u.id == usuario_id), None)


def personas_por_rol(rol):
    if rol == "estudiante":
        return [u for u in usuarios if isinstance(u, Estudiante)]
    if rol == "docente":
        return [u for u in usuarios if isinstance(u, Docente)]
    if rol == "tecnico":
        return [u for u in usuarios if isinstance(u, TecnicoSoporte)]
    return []


@app.context_processor
def inject_usuario():
    return {"usuario": obtener_usuario_actual()}


@app.route("/")
def index():
    usuario = obtener_usuario_actual()
    if usuario is None:
        return redirect(url_for("elegir_usuario"))
    if isinstance(usuario, TecnicoSoporte):
        return redirect(url_for("panel_tecnico"))
    return redirect(url_for("panel"))


@app.route("/elegir-usuario", methods=["GET", "POST"])
def elegir_usuario():
    if request.method == "POST":
        usuario_id = request.form.get("usuario_id", "")
        if usuario_id.isdigit() and any(u.id == int(usuario_id) for u in usuarios):
            session["usuario_id"] = int(usuario_id)
            return redirect(url_for("index"))
        flash("Elegí un usuario de la lista.")
        return redirect(url_for("elegir_usuario"))

    rol = request.args.get("rol")
    if rol not in ETIQUETA_ROL:
        mostrar_splash = not session.get("splash_visto", False)
        session["splash_visto"] = True
        return render_template("elegir_usuario.html", paso="rol", mostrar_splash=mostrar_splash)

    return render_template(
        "elegir_usuario.html", paso="usuario", rol=rol,
        rol_css=ROL_CSS[rol], etiqueta_rol=ETIQUETA_ROL[rol],
        personas=personas_por_rol(rol),
    )


@app.route("/cambiar-usuario", methods=["POST"])
def cambiar_usuario():
    session.pop("usuario_id", None)
    return redirect(url_for("elegir_usuario"))


@app.route("/panel")
def panel():
    usuario = obtener_usuario_actual()
    if usuario is None:
        return redirect(url_for("elegir_usuario"))
    if isinstance(usuario, TecnicoSoporte):
        return redirect(url_for("panel_tecnico"))

    tab = request.args.get("tab", "nuevo")
    mis_tickets = [t for t in sistema.tickets if t.usuario_reporta.id == usuario.id]
    return render_template(
        "panel.html", tab=tab, usuarios=usuarios,
        etiquetas_detalle=ETIQUETA_DETALLE, mis_tickets=mis_tickets, form={},
    )


@app.route("/panel/nuevo-ticket", methods=["POST"])
def panel_nuevo_ticket():
    usuario = obtener_usuario_actual()
    if usuario is None or isinstance(usuario, TecnicoSoporte):
        return redirect(url_for("elegir_usuario"))

    tipo = request.form.get("tipo", "")
    titulo = request.form.get("titulo", "").strip()
    descripcion = request.form.get("descripcion", "").strip()
    detalle_extra = request.form.get("detalle_extra", "").strip()
    prioridad = request.form.get("prioridad", "Media")
    usuario_reporta_id = request.form.get("usuario_reporta_id", "")
    reportante = next((u for u in usuarios if str(u.id) == usuario_reporta_id), None)

    if tipo not in ETIQUETA_DETALLE or not titulo or not descripcion or not detalle_extra or reportante is None:
        flash("Completá todos los campos antes de crear el ticket.")
        mis_tickets = [t for t in sistema.tickets if t.usuario_reporta.id == usuario.id]
        return render_template(
            "panel.html", tab="nuevo", usuarios=usuarios,
            etiquetas_detalle=ETIQUETA_DETALLE, mis_tickets=mis_tickets, form=request.form,
        )

    ticket = crear_ticket(tipo, sistema.generar_id(), titulo, descripcion,
                           reportante, detalle_extra, prioridad)
    sistema.registrar_ticket(ticket)
    guardar_datos(sistema, usuarios)
    return redirect(url_for("panel", tab="mis-tickets"))


@app.route("/panel-tecnico")
def panel_tecnico():
    usuario = obtener_usuario_actual()
    if usuario is None:
        return redirect(url_for("elegir_usuario"))
    if not isinstance(usuario, TecnicoSoporte):
        return redirect(url_for("panel"))

    tipo = request.args.get("tipo", "todos")
    buscar = request.args.get("buscar", "")
    ticket_id = request.args.get("ticket", type=int)

    tickets = sistema.filtrar_por_tipo(tipo)
    if buscar:
        tickets = [t for t in tickets if buscar.lower() in t.titulo.lower()]

    ticket_seleccionado = sistema.buscar_por_id(ticket_id) if ticket_id else None
    tecnicos = [u for u in usuarios if isinstance(u, TecnicoSoporte)]
    conteo = sistema.contar_por_tipo()
    activos = len([t for t in sistema.tickets if t.estado != "Cerrado"])

    return render_template(
        "panel_tecnico.html",
        tickets=tickets, tipo_actual=tipo, buscar=buscar,
        ticket_seleccionado=ticket_seleccionado, tecnicos=tecnicos,
        conteo=conteo, activos=activos, total=len(sistema.tickets),
    )


@app.route("/panel-tecnico/tickets/<int:ticket_id>/estado", methods=["POST"])
def cambiar_estado_ticket(ticket_id):
    usuario = obtener_usuario_actual()
    if usuario is None or not isinstance(usuario, TecnicoSoporte):
        return redirect(url_for("elegir_usuario"))
    ticket = sistema.buscar_por_id(ticket_id)
    if ticket is None:
        abort(404)
    nuevo_estado = request.form.get("estado", "")
    if nuevo_estado in ("Abierto", "En proceso", "Cerrado"):
        ticket.cambiar_estado(nuevo_estado)
        guardar_datos(sistema, usuarios)
    return redirect(url_for(
        "panel_tecnico", ticket=ticket_id,
        tipo=request.form.get("tipo", "todos"), buscar=request.form.get("buscar", ""),
    ))


@app.route("/panel-tecnico/tickets/<int:ticket_id>/asignar", methods=["POST"])
def asignar_tecnico_ticket(ticket_id):
    usuario = obtener_usuario_actual()
    if usuario is None or not isinstance(usuario, TecnicoSoporte):
        return redirect(url_for("elegir_usuario"))
    ticket = sistema.buscar_por_id(ticket_id)
    if ticket is None:
        abort(404)
    tecnico_id = request.form.get("tecnico_id", "")
    tecnico = next((u for u in usuarios if isinstance(u, TecnicoSoporte) and str(u.id) == tecnico_id), None)
    if tecnico is not None:
        ticket.asignar_tecnico(tecnico)
        guardar_datos(sistema, usuarios)
    return redirect(url_for(
        "panel_tecnico", ticket=ticket_id,
        tipo=request.form.get("tipo", "todos"), buscar=request.form.get("buscar", ""),
    ))


ROLES = {"estudiante": "Carrera", "docente": "Facultad", "tecnico": "Especialidad"}


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
