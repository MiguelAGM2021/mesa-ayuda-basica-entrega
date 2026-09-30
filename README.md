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
├── usuario.py     clases Usuario, Estudiante, Docente, TecnicoSoporte
├── ticket.py      clases Ticket, TicketRed, TicketHardware, TicketSoftware, TicketCuenta
├── sistema.py     clase SistemaGestionTickets
├── datos.py       datos de ejemplo y guardado/carga en datos.json
├── main.py        menú por consola
└── web/           interfaz web con Flask y Bootstrap 5
    ├── app.py
    ├── templates/
    └── static/
```

## Tecnologías

- **Python 3** (librería estándar: `json`, `datetime`)
- **Flask** para la interfaz web
- **Bootstrap 5** para el diseño de las páginas

## Cómo ejecutarlo

### Versión de consola

Solo necesita Python 3:

```bash
python main.py
```

La primera vez se cargan usuarios y tickets de ejemplo. Al elegir
"Guardar y salir" (opción 0) todo queda guardado en `datos.json` y se
recupera la próxima vez.

### Versión web

```bash
pip install -r requirements.txt
python web/app.py
```

Luego abrir `http://127.0.0.1:5000` en el navegador y elegir un usuario
de la lista para entrar. La versión web usa las mismas clases y el mismo
`datos.json` que la consola, así que ambas muestran la misma información.
