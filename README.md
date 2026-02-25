# 📊 Sistema de Gestión de Reportes Asíncronos

Este proyecto implementa una arquitectura distribuida de grado industrial para la generación de reportes pesados. Utiliza un flujo de trabajo asíncrono que permite desacoplar el procesamiento de datos de la interfaz de usuario, garantizando que la aplicación permanezca rápida y disponible mientras el trabajo pesado ocurre en segundo plano.

## 🏗️ Arquitectura del Sistema (Servicios)

El sistema está orquestado mediante **Docker Compose**, lo que permite la comunicación aislada entre cuatro servicios fundamentales a través de una red interna:

1.  **Django (Servicio Web):** Actúa como el orquestador principal y gestor de la interfaz de usuario y la lógica de negocio.
2.  **PostgreSQL (Base de Datos):** Motor relacional encargado de la persistencia de datos. Se utiliza por su robustez, seguridad y capacidad para manejar múltiples conexiones simultáneas (concurrencia) entre la Web y el Worker.
3.  **Redis (Broker):** Almacén de datos en memoria que funciona como mediador o "mensajero". Enlista los pedidos de tareas para que Django no se sobrecargue y pueda delegarlas de forma segura.
4.  **Celery (Worker):** Framework de tareas distribuidas que actúa como el "obrero" del sistema, ejecutando las funciones pesadas en segundo plano sin bloquear el servidor principal.



## 🔄 Flujo de Ejecución

1.  **Solicitud:** El usuario solicita un reporte desde la interfaz web.
2.  **Persistencia:** Django crea un registro en **PostgreSQL** con estado `PENDIENTE` para asegurar la trazabilidad.
3.  **Delegación:** Se envía un mensaje al **Broker (Redis)** conteniendo únicamente el ID del reporte.
4.  **Procesamiento:** El **Worker (Celery)** toma la tarea, procesa los datos y genera el archivo final.
5.  **Notificación:** El registro en la base de datos se actualiza a `COMPLETADO` y el resultado técnico se almacena en `django-celery-results`.

## 🚀 Instalación y Puesta en Marcha

### Requisitos Previos
* Tener instalado [Docker](https://docs.docker.com/get-docker/) y [Docker Compose](https://docs.docker.com/compose/install/).

### Pasos para levantar el entorno de desarrollo

1.  **Construir y encender los contenedores:**
    ```bash
    docker compose up --build -d
    ```

2.  **Ejecutar migraciones (Preparar PostgreSQL):**
    ```bash
    docker compose exec web python manage.py migrate
    ```

3.  **Crear superusuario administrativo:**
    ```bash
    docker compose exec web python manage.py createsuperuser
    ```

## 🌐 Acceso al Sistema
* **Aplicación Web (Módulo de Reportes):** [http://localhost:8000/reportes/](http://localhost:8000/reportes/)
* **Panel de Administración:** [http://localhost:8000/admin/](http://localhost:8000/admin/)

## 🛠️ Comandos Útiles de Mantenimiento
* **Ver logs del Worker en tiempo real:** `docker compose logs -f worker`
* **Detener todos los servicios:** `docker compose down`
* **Entrar a la base de datos desde la terminal:** `docker compose exec db psql -U postgres`

---
🗂️ Modelo de Persistencia (Reporte)
Para gestionar el ciclo de vida de los documentos, se ha definido una entidad Reporte con los siguientes atributos técnicos:

Usuario (ForeignKey): Vinculación relacional con el modelo de autenticación nativo de Django para trazabilidad de autoría.

Estado (CharField): Máquina de estados (PENDIENTE, PROCESANDO, COMPLETADO, ERROR) que sincroniza la vista del usuario con el progreso del Worker.

Archivo (FileField): Puntero de ruta hacia el volumen persistente de Docker donde se aloja el binario generado.

Fecha de Creación (DateTimeField): Marca de tiempo automática para auditoría y control de rendimiento.