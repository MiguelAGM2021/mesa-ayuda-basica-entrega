<p align="center">
  <img src="web/static/logo.svg" alt="Mesa de Ayuda" width="520">
</p>

# Mesa de Ayuda — Versión Básica

Sistema de gestión de tickets de fallas técnicas para la universidad,
desarrollado en Python con **Programación Orientada a Objetos**.

Estudiantes y docentes reportan fallas de red, hardware, software o
cuentas; el sistema las registra como tickets, se asignan a un técnico de
soporte y se hace seguimiento hasta cerrarlas.

## Problema que resuelve

En la universidad las fallas técnicas (un laboratorio sin internet, un
proyector que no enciende, un correo institucional bloqueado) se reportan
de forma informal y se pierden. La Mesa de Ayuda centraliza el reporte,
la asignación y la resolución de cada falla en un solo lugar.

## Funcionalidades

- Crear tickets de cuatro tipos: **Red**, **Hardware**, **Software** y **Cuenta**.
- Ver todos los tickets o filtrarlos por tipo y por estado.
- Ver el detalle de cada ticket.
- Asignar un técnico de soporte a un ticket.
- Resolver (cerrar) tickets.
- Registrar y listar usuarios: estudiantes, docentes y técnicos.
- Guardar y recuperar toda la información en `datos.json`.

Cada ticket pasa por tres estados: **Abierto → En proceso → Cerrado**.

## Diseño orientado a objetos

| Concepto | Dónde se aplica |
|---|---|
| Herencia | `Usuario` → `Estudiante`, `Docente`, `TecnicoSoporte` · `Ticket` → `TicketRed`, `TicketHardware`, `TicketSoftware`, `TicketCuenta` |
| Polimorfismo | `obtener_rol()` en cada tipo de usuario y `obtener_detalle()` en cada tipo de ticket |
| Encapsulamiento | Cada ticket administra su propio estado y técnico asignado (`cambiar_estado()`, `asignar_tecnico()`) |
| Clase administradora | `SistemaGestionTickets` registra, busca, filtra y cuenta tickets |
| Fábricas | `crear_usuario()` y `crear_ticket()` crean el objeto correcto según el rol o el tipo |

## Estructura del proyecto

```
mesa-ayuda-basica/
│
├── MODELO (clases del dominio)
│   ├── usuario.py
│   │   ├── Usuario            clase base (id, nombre, correo)
│   │   ├── Estudiante         hereda de Usuario (+ carrera)
│   │   ├── Docente            hereda de Usuario (+ facultad)
│   │   ├── TecnicoSoporte     hereda de Usuario (+ especialidad, resolver_ticket)
│   │   └── crear_usuario()    fábrica: crea el usuario según el rol
│   │
│   └── ticket.py
│       ├── Ticket             clase base (estado, prioridad, técnico asignado)
│       ├── TicketRed          hereda de Ticket (+ zona afectada)
│       ├── TicketHardware     hereda de Ticket (+ equipo afectado)
│       ├── TicketSoftware     hereda de Ticket (+ programa afectado)
│       ├── TicketCuenta       hereda de Ticket (+ tipo de cuenta)
│       └── crear_ticket()     fábrica: crea el ticket según el tipo
│
├── SERVICIOS (lógica del sistema)
│   ├── sistema.py
│   │   └── SistemaGestionTickets   registrar, generar id, buscar,
│   │                               filtrar por estado/tipo, contar
│   └── datos.py                    persistencia
│       ├── sembrar_datos_ejemplo()
│       ├── guardar_datos()   → escribe datos.json
│       └── cargar_datos()    ← lee datos.json
│
└── INTERFAZ (puntos de entrada)
    ├── splash.py             pantalla de inicio en consola (logo + barra de carga)
    ├── main.py               muestra el splash y luego el menú por consola
    │
    └── web/                  interfaz web con la identidad visual CUN (Flask)
        ├── app.py
        │   ├── Configuración visual   CATEGORIAS, PRIORIDAD_COLOR, ETIQUETA_DETALLE
        │   ├── Funciones de apoyo     iniciales, estado_visual, formatear_fecha,
        │   │                          obtener_usuario_actual, personas_por_rol
        │   ├── Inicio de sesión       /elegir-usuario (perfiles de prueba), /cambiar-usuario
        │   ├── Panel alumno/profesor  /panel, /panel/nuevo-ticket
        │   ├── Panel técnico          /panel-tecnico, …/<id>/estado, …/<id>/asignar
        │   └── Usuarios               /usuarios, /usuarios/nuevo
        ├── templates/
        │   ├── base_app.html          encabezado común (logo CUN + ícono del proyecto)
        │   ├── elegir_usuario.html    splash web + selección de perfil y usuario
        │   ├── panel.html             "Nuevo ticket" y "Mis tickets"
        │   ├── panel_tecnico.html     categorías, buscador, lista y detalle
        │   ├── usuarios.html          directorio de usuarios
        │   └── nuevo_usuario.html     registro de usuario
        └── static/
            ├── styles.css             diseño institucional CUN + estilos del splash
            ├── logo.svg               logo del proyecto
            ├── logo-claro.svg         versión clara para el fondo verde del splash
            └── icono.svg              ícono (pestaña del navegador y encabezado)
```

MODELO, SERVICIOS e INTERFAZ son una agrupación lógica: los archivos `.py`
están en la raíz del proyecto.

### Relación entre módulos

```
splash.py <── main.py ──────┐
                            ├──> datos.py ──> sistema.py
              web/app.py ───┘       │
                 │                  └──> usuario.py, ticket.py
                 └──> usuario.py, ticket.py
```

- `usuario.py` y `ticket.py` no importan ningún otro módulo del proyecto; son la base.
- `sistema.py` tampoco importa nada: trabaja con los objetos `Ticket` que recibe.
- `splash.py` solo lo usa `main.py`; no toca el modelo ni los datos.
- `main.py` y `web/app.py` son independientes entre sí y comparten las mismas
  clases y el mismo `datos.json`.

### Cómo se reparte la lógica

| Dónde | Qué lógica tiene |
|---|---|
| Clases del modelo | Reglas de cada objeto: cambiar estado, asignar técnico, mostrar su detalle (polimorfismo) |
| `SistemaGestionTickets` | Manejo del conjunto de tickets: registrar, buscar, filtrar y contar |
| `datos.py` | Guardar y cargar todo en `datos.json` |
| `splash.py` | Solo presentación: logo y barra de carga al iniciar la consola |
| `main.py` | Pedir datos por teclado y mostrar resultados en consola |
| `web/app.py` | Recibir las acciones del navegador, llamar a las clases y elegir qué plantilla mostrar |
| `templates/` y `static/` | Solo presentación visual (HTML y CSS), sin reglas del negocio |

## Tecnologías

- **Python 3** (librería estándar: `json`, `datetime`)
- **Flask** para la interfaz web
- **HTML y CSS propios** con la identidad visual de la CUN (verde institucional y lima)

## Cómo ejecutarlo

### Versión de consola

Solo necesita Python 3:

```bash
python main.py
```

Al iniciar aparece la pantalla de bienvenida con el logo y una barra de
carga. La primera vez se cargan usuarios y tickets de ejemplo. Al elegir
"Guardar y salir" (opción 0) todo queda guardado en `datos.json` y se
recupera la próxima vez.

### Versión web

```bash
pip install -r requirements.txt
python web/app.py
```

Luego abrir `http://127.0.0.1:5000` en el navegador. Primero aparece la
pantalla de inicio con el logo sobre el fondo verde institucional de la CUN;
después se elige un perfil de prueba (Alumno, Profesor o Técnico) y un
usuario de la lista, sin contraseña ni registro:

- **Alumno y Profesor:** reportan fallas desde "Nuevo ticket" y revisan el
  estado de sus tickets en "Mis tickets".
- **Técnico:** ve todos los tickets por categoría, busca por título, cambia
  el estado y asigna técnicos desde el panel de detalle.

La versión web usa las mismas clases y el mismo `datos.json` que la
consola, así que ambas muestran la misma información.
