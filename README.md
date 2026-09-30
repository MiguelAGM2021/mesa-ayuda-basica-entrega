# Mesa de Ayuda — versión básica (Python)

Sistema de gestión de tickets de fallas para la universidad. Es la
versión **100% básica** del proyecto original (`mesa-ayuda-v2`, hecho en
JavaScript con Firebase, base de datos en tiempo real y hosting web) —
acá no hay nada de eso: es un programa de consola en Python puro, pensado
para un nivel más temprano de la materia (todavía sin ver bases de datos
ni hosting).

## Qué se conserva del proyecto original

- La misma idea: reportar, asignar y resolver tickets de fallas (red,
  hardware, software, cuenta) en una universidad.
- La misma estructura de clases y el mismo foco en **Programación
  Orientada a Objetos**:
  - `Usuario` (clase base) → `Estudiante`, `Docente`, `TecnicoSoporte`
    (herencia + polimorfismo con `obtener_rol()`).
  - `Ticket` (clase base) → `TicketRed`, `TicketHardware`,
    `TicketSoftware`, `TicketCuenta` (herencia + polimorfismo con
    `obtener_detalle()`).
  - `SistemaGestionTickets`: clase administradora que registra, busca,
    filtra y cuenta tickets.

## Qué NO tiene (a propósito)

- Sin Firebase, sin base de datos, sin hosting. La versión de consola
  (`main.py`) no usa páginas web; hay una versión web opcional (más abajo)
  que sigue sin Firebase/base de datos/hosting, solo agrega HTML/CSS.
- Sin login de verdad — se elige el usuario de una lista, sin contraseña.
- Los datos se guardan en un archivo de texto simple (`datos.json`,
  usando el módulo estándar `json` de Python) para que los tickets no se
  pierdan al cerrar el programa — no es una base de datos, es solo un
  archivo en el disco.

## Cómo correrlo

Necesitás Python 3 instalado (no hace falta instalar nada más, todo el
programa usa solo la librería estándar).

```bash
python main.py
```

La primera vez que lo corrés, no existe `datos.json` todavía, así que el
programa siembra unos usuarios y tickets de ejemplo (los mismos que traía
la versión original) para que el menú tenga con qué probar. A partir de
ahí, cada vez que elegís "Guardar y salir" (opción 0), el estado completo
se guarda en `datos.json` y se recupera la próxima vez que abrís el
programa.

## Estructura de archivos

```
usuario.py   → clases Usuario, Estudiante, Docente, TecnicoSoporte
ticket.py    → clases Ticket, TicketRed, TicketHardware, TicketSoftware, TicketCuenta
sistema.py   → clase SistemaGestionTickets
datos.py     → datos de ejemplo + guardar/cargar en datos.json
main.py      → menú por consola, el programa que se corre
web/         → interfaz web opcional (Flask + Bootstrap 5), ver más abajo
```

## Versión web (opcional, Flask + Bootstrap 5)

Además de la consola, el proyecto tiene una interfaz web que usa las
mismas clases (`Usuario`, `Ticket`, `SistemaGestionTickets`) sin
modificarlas — Flask solo las importa, igual que hace `main.py`. La
pantalla de entrada reemplaza el login por elegir un usuario de una
lista (sin contraseña).

Requiere instalar Flask (no viene en la librería estándar):

```bash
pip install -r requirements.txt
python web/app.py
```

Después abrí `http://127.0.0.1:5000` en el navegador. Los datos se
guardan en el mismo `datos.json` que usa la versión de consola, así que
podés alternar entre `python main.py` y `python web/app.py` y ver los
mismos tickets y usuarios en ambas.
