# CredIRM

Sistema web para la gestión y administración de préstamos, clientes, cuotas y pagos.

CredIRM es una aplicación desarrollada con Django que permite llevar un control organizado de los clientes y de sus préstamos, facilitando el seguimiento de cuotas, pagos y estados de cada operación.

---

##  Características

-  Gestión de clientes
  - Registrar clientes
  - Consultar información
  - Editar datos
  - Eliminar clientes

-  Gestión de préstamos
  - Registrar préstamos
  - Definir monto e interés
  - Establecer número de cuotas
  - Configurar frecuencia de pago
  - Controlar fechas de inicio y finalización

-  Gestión de cuotas
  - Generación y seguimiento de cuotas
  - Control de cuotas pendientes
  - Control de cuotas pagadas
  - Identificación de cuotas vencidas

-  Gestión de pagos
  - Registro de pagos
  - Métodos de pago:
    - Efectivo
    - Transferencia
    - Depósito
  - Registro de referencias y observaciones

-  Dashboard
  - Total de clientes
  - Préstamos activos
  - Cuotas atrasadas
  - Pagos recientes
  - Total cobrado durante el mes

-  Autenticación
  - Inicio de sesión
  - Cierre de sesión
  - Control de acceso
  - Permisos para administradores

---

##  Tecnologías utilizadas

- Python
- Django 4.2
- HTML5
- CSS3
- SQLite
- Git
- GitHub

---

## Estructura del proyecto

```text
CredIRM/
│
├── credirm/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── prestamo/
│   ├── migrations/
│   ├── templates/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── static/
│   └── css/
│
├── manage.py
├── requirements.txt
└── README.md
