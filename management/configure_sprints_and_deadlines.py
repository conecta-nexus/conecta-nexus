#!/usr/bin/env python3
"""
Conecta Nexus - Configuración Oficial de Sprints, Deadlines, Story Points y Status
Proyecto: #2 (Conecta Nexus Management)
Organización: conecta-nexus
URL: https://github.com/orgs/conecta-nexus/projects/2
"""

import sys
import json
import re
import time
import shutil
import subprocess

ORG = "conecta-nexus"
PROJECT_NUM = 2
PROJECT_TITLE = "Conecta Nexus Management"

# Cronograma y Metadatos Oficiales de las 14 Historias de Usuario (100 PH)
STORIES_METADATA = {
    # Sprint 1 (10 días: 12 oct - 22 oct 2026) -> Deadline: 2026-10-22 (33 PH)
    "HU-01": {"sprint": "Sprint 1", "points": 5,  "due": "2026-10-22", "priority": "Must Have"},
    "HU-02": {"sprint": "Sprint 1", "points": 5,  "due": "2026-10-22", "priority": "Must Have"},
    "HU-03": {"sprint": "Sprint 1", "points": 5,  "due": "2026-10-22", "priority": "Must Have"},
    "HU-04": {"sprint": "Sprint 1", "points": 8,  "due": "2026-10-22", "priority": "Should Have"},
    "HU-05": {"sprint": "Sprint 1", "points": 10, "due": "2026-10-22", "priority": "Should Have"},

    # Sprint 2 (20 días: 23 oct - 11 nov 2026) -> Deadline: 2026-11-11 (Hito 1: Avance 66%) (33 PH)
    "HU-06": {"sprint": "Sprint 2", "points": 8,  "due": "2026-11-11", "priority": "Must Have"},
    "HU-07": {"sprint": "Sprint 2", "points": 5,  "due": "2026-11-11", "priority": "Should Have"},
    "HU-08": {"sprint": "Sprint 2", "points": 5,  "due": "2026-11-11", "priority": "Should Have"},
    "HU-09": {"sprint": "Sprint 2", "points": 8,  "due": "2026-11-11", "priority": "Must Have"},
    "HU-10": {"sprint": "Sprint 2", "points": 7,  "due": "2026-11-11", "priority": "Should Have"},

    # Sprint 3 (21 días: 12 nov - 02 dic 2026) -> Deadline: 2026-12-02 (Hito 2: MVP 100%) (34 PH)
    "HU-11": {"sprint": "Sprint 3", "points": 8,  "due": "2026-12-02", "priority": "Must Have"},
    "HU-12": {"sprint": "Sprint 3", "points": 10, "due": "2026-12-02", "priority": "Must Have"},
    "HU-13": {"sprint": "Sprint 3", "points": 8,  "due": "2026-12-02", "priority": "Should Have"},
    "HU-14": {"sprint": "Sprint 3", "points": 8,  "due": "2026-12-02", "priority": "Should Have"},
}


def run_graphql_with_retry(query, max_retries=5, delay=2):
    """Ejecuta una consulta GraphQL con reintentos automáticos ante cortes de red."""
    cmd = ["gh", "api", "graphql", "-f", f"query={query}"]
    for attempt in range(1, max_retries + 1):
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode == 0:
            try:
                data = json.loads(res.stdout)
                if "errors" in data and data["errors"]:
                    return False, json.dumps(data["errors"])
                return True, data
            except json.JSONDecodeError as e:
                return False, f"JSONDecodeError: {e}"
        err = res.stderr.strip()
        if "connecting to api.github.com" in err or "timeout" in err.lower():
            time.sleep(delay * attempt)
        else:
            return False, err
    return False, err


def check_prerequisites():
    if not shutil.which("gh"):
        print("❌ Error: GitHub CLI ('gh') no está instalado.")
        sys.exit(1)
    res = subprocess.run(["gh", "auth", "status"], capture_output=True, text=True)
    if res.returncode != 0:
        print("❌ Error: No has iniciado sesión en gh. Ejecuta: gh auth login")
        sys.exit(1)


def get_project_metadata():
    query = f"""
    query {{
      organization(login: "{ORG}") {{
        projectV2(number: {PROJECT_NUM}) {{
          id
          title
          fields(first: 30) {{
            nodes {{
              ... on ProjectV2IterationField {{
                id
                name
                configuration {{
                  iterations {{
                    id
                    title
                    startDate
                    duration
                  }}
                }}
              }}
              ... on ProjectV2SingleSelectField {{
                id
                name
                options {{
                  id
                  name
                }}
              }}
              ... on ProjectV2Field {{
                id
                name
                dataType
              }}
            }}
          }}
        }}
      }}
    }}
    """
    ok, data = run_graphql_with_retry(query)
    if not ok:
        print(f"❌ Error al consultar metadatos del proyecto: {data}")
        sys.exit(1)
    return data["data"]["organization"]["projectV2"]


def ensure_iteration_configuration(project_id, sprint_field):
    """Asegura que el campo Iteration 'Sprint' contenga Sprint 1, Sprint 2 y Sprint 3 con sus fechas."""
    field_id = sprint_field["id"]
    iterations = sprint_field.get("configuration", {}).get("iterations", [])
    iter_by_title = {it["title"]: it for it in iterations}

    s1_id = iter_by_title.get("Sprint 1", {}).get("id", "381c7c80")
    s2_id = iter_by_title.get("Sprint 2", {}).get("id", "54cf5c95")
    s3_id = iter_by_title.get("Sprint 3", {}).get("id", "d2c335bc")

    mutation = f"""
    mutation {{
      updateProjectV2Field(input: {{
        fieldId: "{field_id}"
        name: "Iteration"
        iterationConfiguration: {{
          startDate: "2026-10-12"
          duration: 11
          iterations: [
            {{
              id: "{s1_id}"
              title: "Sprint 1"
              startDate: "2026-10-12"
              duration: 11
            }},
            {{
              id: "{s2_id}"
              title: "Sprint 2"
              startDate: "2026-10-23"
              duration: 20
            }},
            {{
              id: "{s3_id}"
              title: "Sprint 3"
              startDate: "2026-11-12"
              duration: 21
            }}
          ]
        }}
      }}) {{
        projectV2Field {{
          ... on ProjectV2IterationField {{
            id
            name
            configuration {{
              iterations {{
                id
                title
                startDate
                duration
              }}
            }}
          }}
        }}
      }}
    }}
    """
    ok, data = run_graphql_with_retry(mutation)
    if not ok:
        print(f"⚠️ Aviso al actualizar configuración de iteración: {data}")
    else:
        print("✔ Campo Iteration 'Sprint' configurado exitosamente (Sprint 1, Sprint 2, Sprint 3).")


def get_project_items(project_id):
    query = f"""
    query {{
      node(id: "{project_id}") {{
        ... on ProjectV2 {{
          items(first: 100) {{
            nodes {{
              id
              content {{
                ... on Issue {{
                  title
                  number
                  repository {{
                    name
                  }}
                }}
              }}
            }}
          }}
        }}
      }}
    }}
    """
    ok, data = run_graphql_with_retry(query)
    if not ok:
        print(f"❌ Error al consultar items del proyecto: {data}")
        sys.exit(1)
    return data["data"]["node"]["items"]["nodes"]


def extract_hu_id(title):
    match = re.search(r"HU-\d+", title)
    return match.group(0) if match else None


def main():
    check_prerequisites()

    print("=" * 80)
    print("🚀 CONFIGURACIÓN DEFINITIVA DE SPRINTS, DEADLINES, PUNTOS Y ESTADO")
    print(f"   Organización: {ORG}")
    print(f"   Proyecto:     #{PROJECT_NUM} ({PROJECT_TITLE})")
    print("=" * 80 + "\n")

    proj = get_project_metadata()
    project_id = proj["id"]
    fields = proj["fields"]["nodes"]

    sprint_field = None
    points_field = None
    due_field = None
    status_field = None

    for f in fields:
        fname = f.get("name", "")
        if fname in ["Iteration", "Sprint"] and "configuration" in f:
            sprint_field = f
        elif fname == "Story Points":
            points_field = f
        elif fname == "Due Date":
            due_field = f
        elif fname == "Status":
            status_field = f

    if not sprint_field or not points_field or not due_field or not status_field:
        print(f"❌ Faltan campos requeridos en el proyecto: Sprint/Iteration={bool(sprint_field)}, Points={bool(points_field)}, Due={bool(due_field)}, Status={bool(status_field)}")
        sys.exit(1)

    print(f"✔ ID Proyecto:       {project_id}")
    print(f"✔ Campo Iteration:   {sprint_field['id']} ({sprint_field.get('name')})")
    print(f"✔ Campo Story Points:{points_field['id']} (Number)")
    print(f"✔ Campo Due Date:    {due_field['id']} (Date)")
    print(f"✔ Campo Status:      {status_field['id']} (Single Select)\n")

    # Asegurar configuración del campo Iteration
    ensure_iteration_configuration(project_id, sprint_field)

    # Re-consultar para obtener IDs exactos de iteraciones
    proj = get_project_metadata()
    sprint_field = next(f for f in proj["fields"]["nodes"] if f.get("name") in ["Iteration", "Sprint"] and "configuration" in f)
    iteration_ids = {it["title"]: it["id"] for it in sprint_field["configuration"]["iterations"]}

    # Obtener ID de la opción "To Do" en Status
    todo_option_id = None
    for opt in status_field.get("options", []):
        if opt["name"].strip().lower() in ["to do", "todo"]:
            todo_option_id = opt["id"]
            break

    if not todo_option_id:
        print("❌ No se encontró la opción 'To Do' en el campo Status.")
        sys.exit(1)

    print(f"✔ Opción Status 'To Do': {todo_option_id}\n")
    print(f"✔ Iteraciones mapeadas: {iteration_ids}\n")

    # Obtener items del proyecto
    items = get_project_items(project_id)
    print(f"📦 Encontrados {len(items)} ítems en el tablero. Actualizando campos...\n")

    updated = 0
    total_sp_assigned = 0

    for it in items:
        item_id = it["id"]
        content = it.get("content") or {}
        title = content.get("title", "")
        hu_id = extract_hu_id(title)

        if not hu_id or hu_id not in STORIES_METADATA:
            print(f"⏭ Saltando ítem sin HU reconocida: {title}")
            continue

        meta = STORIES_METADATA[hu_id]
        sprint_name = meta["sprint"]
        iter_id = iteration_ids[sprint_name]
        points = meta["points"]
        due_date = meta["due"]

        print(f"▶ [{hu_id}] {title[:55]}...")
        print(f"    Sprint: {sprint_name} ({iter_id}) | SP: {points} | Due: {due_date} | Status: To Do")

        mutation = f"""
        mutation {{
          setSprint: updateProjectV2ItemFieldValue(input: {{
            projectId: "{project_id}"
            itemId: "{item_id}"
            fieldId: "{sprint_field['id']}"
            value: {{ iterationId: "{iter_id}" }}
          }}) {{ projectV2Item {{ id }} }}

          setPoints: updateProjectV2ItemFieldValue(input: {{
            projectId: "{project_id}"
            itemId: "{item_id}"
            fieldId: "{points_field['id']}"
            value: {{ number: {points} }}
          }}) {{ projectV2Item {{ id }} }}

          setDate: updateProjectV2ItemFieldValue(input: {{
            projectId: "{project_id}"
            itemId: "{item_id}"
            fieldId: "{due_field['id']}"
            value: {{ date: "{due_date}" }}
          }}) {{ projectV2Item {{ id }} }}

          setStatus: updateProjectV2ItemFieldValue(input: {{
            projectId: "{project_id}"
            itemId: "{item_id}"
            fieldId: "{status_field['id']}"
            value: {{ singleSelectOptionId: "{todo_option_id}" }}
          }}) {{ projectV2Item {{ id }} }}
        }}
        """

        ok, res = run_graphql_with_retry(mutation)
        if not ok:
            print(f"    ❌ Error al actualizar {hu_id}: {res}")
        else:
            print("    ✔ Actualizado con éxito.")
            updated += 1
            total_sp_assigned += points

        time.sleep(0.3)

    print("\n" + "=" * 80)
    print(f"🎉 ¡PROCESO FINALIZADO CON ÉXITO!")
    print(f"   Historias actualizadas: {updated}/14")
    print(f"   Story Points totales:   {total_sp_assigned}/100 PH")
    print(f"   Sprint 1 (2026-10-12 a 2026-10-22): HU-01 a HU-05 (33 PH)")
    print(f"   Sprint 2 (2026-10-23 a 2026-11-11): HU-06 a HU-10 (33 PH)")
    print(f"   Sprint 3 (2026-11-12 a 2026-12-02): HU-11 a HU-14 (34 PH)")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
