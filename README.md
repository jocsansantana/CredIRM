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

## Tecnologías utilizadas

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
```
## Instalación
- Clonar el repositorio
git clone https://github.com/jocsansantana/CredIRM.git
- Entrar al proyecto
cd CredIRM
- Crear un entorno virtual

## Windows:

python -m venv .venv / py -m venv .venv

Activar el entorno:

.venv\Scripts\activate

## Linux / macOS:

python3 -m venv .venv
source .venv/bin/activate

- Instalar las dependencias
pip install -r requirements.txt

- Aplicar las migraciones
python manage.py migrate

- Crear un usuario administrador
python manage.py createsuperuser

- Ejecutar el servidor
python manage.py runserver

## Luego abre:

http://127.0.0.1:8000/

## Roles y permisos

El sistema utiliza el sistema de autenticación de Django.

Los usuarios autenticados pueden acceder a las funcionalidades del sistema, mientras que determinadas acciones administrativas requieren permisos de administrador.

## Modelo de datos

El sistema está organizado principalmente alrededor de cuatro entidades:
```text
Cliente
   │
   └─── Préstamo
          │
          └─── Cuota
                 │
                 └─── Pago
```
## Cliente
Contiene información básica del cliente:

- Nombres
- Apellidos
- Cédula
- Teléfono
- Fecha de registro
- Estado
- Préstamo

## Permite registrar:

- Cliente
- Monto
- Tasa de interés
- Número de cuotas
- Frecuencia de pago
- Fecha de inicio
- Fecha de finalización
- Interés total
- Total a pagar
- Estado
- Observaciones
- Cuota

## Cada préstamo puede tener varias cuotas con:

- Número de cuota
- Fecha de vencimiento
- Capital
- Interés
- Monto
- Estado
- Pago

## Cada cuota puede registrar pagos indicando:

- Fecha
- Monto
- Método de pago
- Referencia
- Observaciones
- Estados de los préstamos

## Los préstamos pueden encontrarse en los siguientes estados:

- PENDIENTE
- ACTIVO
- PAGADO
- VENCIDO
- CANCELADO

## Las cuotas pueden estar:

- PENDIENTE
- PAGADA
- VENCIDA

## Desarrollo
---
Para ejecutar el proyecto en modo desarrollo:

python manage.py runserver

Para comprobar que Django no tenga errores de configuración:

python manage.py check

## Dependencias

Las principales dependencias del proyecto son:

- Django==4.2
- asgiref==3.12.1
- sqlparse==0.5.5
- tzdata==2026.3
- Próximas mejoras

## Algunas funcionalidades que podrían incorporarse en futuras versiones:

 - Generación de reportes
 - Exportación a PDF
 - Exportación a Excel
 - Gráficos estadísticos
 - Búsqueda avanzada de clientes
 - Historial de pagos
 - Notificaciones de cuotas próximas a vencer
 - Mejoras en el diseño responsive
 - Pruebas automatizadas
 - Despliegue en producción
 
## Licencia

Este proyecto se encuentra actualmente en desarrollo.

Autor: Jocsan Santana

## GitHub:
https://github.com/jocsansantana

## Repositorio:
https://github.com/jocsansantana/CredIRM
