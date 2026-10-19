# Conecta Nexus

Repositorio central y punto de entrada para sincronizar, configurar y gestionar todos los microservicios, frontend, gateway, infraestructura y tareas de gestión de proyecto de **Conecta Nexus**.

---

## Estructura del Repositorio

```text
conecta-nexus/
├── setup/                      # Scripts de aprovisionamiento y sincronización de repositorios
│   ├── setup.sh                # Clona / sincroniza los 9 repositorios y sincroniza plantillas de issue
│   └── commit-and-push-all.sh  # Script de ayuda para commits y pushes simultáneos a develop
├── management/                 # Backlog de Historias de Usuario y automatización de GitHub Projects
│   ├── conecta_nexus_user_stories.csv   # Matriz completa de HU (HU-01 a HU-23)
│   ├── configure_sprints_and_deadlines.py # Configuración de iteraciones y campos en GitHub Project #2
│   ├── import_user_stories.py  # Importador de Historias de Usuario a GitHub
│   ├── import_user_stories.sh  # Wrapper bash para la importación del backlog
│   └── retry_missing_stories.py # Utilidad de reintento para sincronización de HU
├── sprints/                    # Planificación y seguimiento técnico por sprint
│   └── sprint-1/               # Sprint 1 (auth & profile)
│       ├── conecta_nexus_sprint_1_tasks.csv # 28 tareas técnicas detalladas
│       ├── create_sprint1_tasks_csv.py      # Generador del CSV de tareas técnicas
│       ├── import_sprint_1_tasks.py         # Creación y vinculación de tareas en GitHub Project #2
│       └── finish_import.py                 # Finalización de importación y enlace al tablero
├── CONTRIBUTING.md             # Guía de contribución, flujo Git y estándares de ramas
└── README.md                   # Este documento
```

---

## Inicialización y Configuración

Para clonar todos los microservicios o sincronizarlos con sus ramas remotas (`main` y `develop`), ejecuta el script de configuración desde la raíz del proyecto:

```bash
./setup/setup.sh
```

El script verificará cada uno de los 9 repositorios del ecosistema:
1. Si no existe localmente, lo clonará vía `git clone`.
2. Si ya existe, ejecutará `fetch` y `pull` para mantener sincronizadas las ramas base.
3. Sincronizará las plantillas de issues (`.github/ISSUE_TEMPLATE/`) de forma uniforme en cada repositorio.

---

## Entorno Local con Podman Compose

El archivo [`compose.yaml`](file:///home/anorak/Code/microservices-college/conecta-nexus/compose.yaml) (o [`podman-compose.yml`](file:///home/anorak/Code/microservices-college/conecta-nexus/podman-compose.yml)) orquesta todos los microservicios, frontend, gateway e inicialización de bases de datos PostgreSQL para desarrollo local.

### Levantar Todo el Ecosistema

```bash
# Construir imágenes e iniciar todos los servicios
podman compose up --build

# O en segundo plano (daemon):
podman compose up --build -d
```

### Detener los Contenedores

```bash
podman compose down
```

### Mapeo de Puertos y Servicios

| Componente | Servicio | Puerto Host | Descripción |
| :--- | :--- | :--- | :--- |
| **API Gateway** | `gateway` | `http://localhost:8080` | Punto de entrada unificado y proxy inverso Nginx |
| **Frontend** | `frontend` | `http://localhost:3000` | Nuxt 4 (Vite HMR activo) |
| **Auth** | `auth` | `http://localhost:8001` | FastAPI (Autenticación y tokens JWT) |
| **Profile** | `profile` | `http://localhost:8002` | Django DRF (Perfiles y consentimiento Ley 1581) |
| **Application** | `application` | `http://localhost:8003` | Django DRF (Postulaciones) |
| **Challenge** | `challenge` | `http://localhost:8004` | FastAPI (Retos y problemáticas) |
| **Moderation** | `moderation` | `http://localhost:8005` | Django DRF (Moderación de contenidos) |
| **Notification** | `notification` | `http://localhost:8006` | FastAPI (Eventos y notificaciones) |
| **Base de Datos** | `postgres` | `localhost:5432` | PostgreSQL 16 con multi-DB (`db_auth`, `db_profiles`, etc.) |

