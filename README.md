# 🚁 Drone Package Tracker

Sistema de rastreo y gestión de paquetes para una empresa de reparto mediante drones.

El proyecto tiene como objetivo desarrollar una aplicación web capaz de administrar paquetes, clientes, drones y entregas, además de proporcionar información sobre el estado y el historial de cada envío.

## 📌 Estado del proyecto

> 🚧 En desarrollo

Actualmente el proyecto se encuentra en la etapa de **diseño de arquitectura y base de datos**.

---

## 🎯 Objetivo

Desarrollar un sistema de seguimiento de paquetes que permita:

* Registrar clientes.
* Registrar paquetes.
* Generar números de rastreo.
* Consultar el estado de un paquete.
* Mantener un historial de estados.
* Registrar y administrar drones.
* Asignar drones a paquetes.
* Registrar operadores/pilotos.
* Gestionar posteriormente vuelos y posiciones GPS.
* Proporcionar una interfaz web para clientes y administradores.

A futuro, el sistema podrá integrarse con hardware de los drones para recibir información como posición GPS, batería y estado de vuelo.

---

## 🏗️ Arquitectura

El proyecto estará dividido principalmente en tres componentes:

```text
┌──────────────────────────┐
│        FRONTEND          │
│      HTML / CSS / JS     │
└────────────┬─────────────┘
             │
             │ HTTP / REST API
             ▼
┌──────────────────────────┐
│         BACKEND          │
│      Python + FastAPI    │
└────────────┬─────────────┘
             │
             │ SQL
             ▼
┌──────────────────────────┐
│          MySQL           │
│        Database          │
└──────────────────────────┘
```

Para el acceso remoto se utilizará posteriormente **ngrok**, exponiendo únicamente el backend/API y manteniendo la base de datos fuera del acceso directo desde Internet.

---

## 🗄️ Base de datos

La base de datos será diseñada utilizando un modelo relacional.

Las entidades principales serán:

* **Clientes**
* **Paquetes**
* **Estados de paquetes**
* **Historial de paquetes**
* **Drones**
* **Pilotos/operadores**

Posteriormente podrán incorporarse:

* Vuelos
* Rutas
* Posiciones GPS
* Telemetría
* Incidencias
* Usuarios y roles

### Modelo conceptual inicial

```text
CLIENTES
   │
   │ 1:N
   ▼
PAQUETES ────────────► ESTADOS
   │
   │ 1:N
   ▼
HISTORIAL_PAQUETE

PAQUETES
   │
   │ N:1
   ▼
DRONES
   │
   │ N:1
   ▼
PILOTOS
```

El diseño definitivo de las relaciones se establecerá antes de implementar el esquema SQL.

---

## 📁 Estructura del proyecto

```text
drone-package-tracker/
│
├── README.md
├── .gitignore
│
├── backend/
│   ├── main.py
│   ├── database/
│   ├── routes/
│   ├── schemas/
│   └── services/
│
├── frontend/
│   ├── index.html
│   ├── tracking.html
│   ├── dashboard.html
│   ├── css/
│   └── js/
│
└── database/
    └── schema.sql
```

La estructura anterior representa la arquitectura prevista y podrá modificarse conforme avance el desarrollo.

---

## 🛠️ Tecnologías

### Backend

* Python
* FastAPI
* Uvicorn

### Base de datos

* MySQL
* SQL

### Frontend

* HTML5
* CSS3
* JavaScript

### Acceso remoto

* ngrok

### Control de versiones

* Git
* GitHub

---

## 🔌 API

La comunicación entre frontend y backend se realizará mediante una API REST.

Ejemplo conceptual:

```http
GET /paquetes/{tracking_number}
```

Respuesta esperada:

```json
{
    "tracking_number": "TRK-MX-8F29A31",
    "estado": "EN_TRANSITO",
    "origen": "Ecatepec",
    "destino": "Ciudad de México"
}
```

Los endpoints definitivos serán documentados conforme se implemente el backend.

---

## 🚁 Integración con drones

Una etapa posterior del proyecto contempla integrar los drones físicos con el sistema.

Un dispositivo embarcado podría enviar información al backend:

```text
GPS
 │
 ▼
ESP32 / STM32
 │
 │ Internet
 ▼
FastAPI
 │
 ├──► MySQL
 │
 └──► WebSocket
          │
          ▼
       Frontend
```

Esto permitiría visualizar información como:

* Latitud
* Longitud
* Altitud
* Batería
* Estado del dron
* Velocidad
* Última conexión

---

## 🌐 Acceso remoto

Durante el desarrollo local:

```text
Frontend
    │
    ▼
localhost
    │
    ▼
FastAPI :8000
    │
    ▼
MySQL
```

Posteriormente:

```text
Internet
    │
    ▼
  ngrok
    │
    ▼
FastAPI :8000
    │
    ▼
  MySQL
```

La base de datos no será expuesta directamente a Internet.

---

## 📋 Roadmap

### Fase 1 — Diseño

* [x] Crear repositorio
* [x] Definir arquitectura inicial
* [ ] Diseñar modelo entidad-relación
* [ ] Normalizar base de datos
* [ ] Crear `schema.sql`

### Fase 2 — Backend

* [ ] Configurar entorno Python
* [ ] Configurar FastAPI
* [ ] Conectar Python con MySQL
* [ ] Crear modelos
* [ ] Implementar CRUD
* [ ] Implementar API de tracking

### Fase 3 — Frontend

* [ ] Página principal
* [ ] Buscador de paquetes
* [ ] Página de tracking
* [ ] Dashboard administrativo

### Fase 4 — Integración

* [ ] Conectar frontend con API
* [ ] Pruebas de integración
* [ ] Manejo de errores
* [ ] Validación de datos

### Fase 5 — Drones

* [ ] Registro de drones
* [ ] Asignación de drones
* [ ] Gestión de vuelos
* [ ] GPS
* [ ] Telemetría
* [ ] Mapa en tiempo real

### Fase 6 — Acceso remoto

* [ ] Configurar ngrok
* [ ] Exponer API
* [ ] Probar acceso externo
* [ ] Seguridad y autenticación

---

## 👨‍💻 Desarrollo

El proyecto está siendo desarrollado como un proyecto experimental para estudiar e integrar:

* Diseño de bases de datos
* Desarrollo backend
* APIs REST
* Desarrollo frontend
* Sistemas IoT
* Telemetría
* Integración hardware/software

---

## 📄 Licencia

Este proyecto se encuentra actualmente en desarrollo. La licencia será definida posteriormente.
