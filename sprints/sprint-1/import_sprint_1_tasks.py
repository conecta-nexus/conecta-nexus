#!/usr/bin/env python3
"""
Conecta Nexus - Importador de Tareas Técnicas del Sprint 1
Lee conecta_nexus_sprint_1_tasks.csv, crea los issues en los repositorios correspondientes,
los asocia al proyecto #2 (Conecta Nexus Management) y configura Status='To Do' e Iteration='Sprint 1'.
"""

import os
import sys
import csv
import json
import time
import shutil
import subprocess

ORG = "conecta-nexus"
PROJECT_NUM = "2"
CSV_FILENAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), "conecta_nexus_sprint_1_tasks.csv")


def check_prerequisites():
    if not shutil.which("gh"):
        print("❌ Error: GitHub CLI ('gh') no está instalado.")
        sys.exit(1)
    res = subprocess.run(["gh", "auth", "status"], capture_output=True, text=True)
    if res.returncode != 0:
        print("❌ Error: No has iniciado sesión en gh. Ejecuta: gh auth login")
        sys.exit(1)


def ensure_labels(repo: str):
    """Asegura que los labels 'task' y 'sprint-1' existan en el repositorio."""
    labels = [
        ("task", "1D76DB", "Granular engineering task"),
        ("sprint-1", "0E8A16", "Sprint 1 (12 Oct - 22 Oct 2026)")
    ]
    for name, color, desc in labels:
        cmd = [
            "gh", "label", "create", name,
            "--repo", f"{ORG}/{repo}",
            "--color", color,
            "--description", desc,
            "--force"
        ]
        subprocess.run(cmd, capture_output=True, text=True)


def get_project_fields():
    """Consulta los metadatos y campos del proyecto #2 vía GraphQL."""
    query = f"""
    query {{
      organization(login: "{ORG}") {{
        projectV2(number: {PROJECT_NUM}) {{
          id
          fields(first: 30) {{
            nodes {{
              ... on ProjectV2IterationField {{
                id
                name
                configuration {{
                  iterations {{
                    id
                    title
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
            }}
          }}
        }}
      }}
    }}
    """
    cmd = ["gh", "api", "graphql", "-f", f"query={query}"]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"⚠️ Error al consultar campos del proyecto: {res.stderr}")
        return None, None, None, None, None

    data = json.loads(res.stdout)
    proj = data["data"]["organization"]["projectV2"]
    project_id = proj["id"]
    fields = proj["fields"]["nodes"]

    status_field_id = None
    todo_option_id = None
    sprint_field_id = None
    sprint_1_iter_id = None

    for f in fields:
        fname = f.get("name", "")
        if fname == "Status" and "options" in f:
            status_field_id = f["id"]
            for opt in f["options"]:
                if opt["name"].strip().lower() in ["to do", "todo"]:
                    todo_option_id = opt["id"]
                    break
        elif fname in ["Iteration", "Sprint"] and "configuration" in f:
            sprint_field_id = f["id"]
            for it in f["configuration"]["iterations"]:
                if "sprint 1" in it["title"].lower():
                    sprint_1_iter_id = it["id"]
                    break

    return project_id, status_field_id, todo_option_id, sprint_field_id, sprint_1_iter_id


def set_project_field(project_id, item_id, field_id, value_dict):
    """Actualiza un campo del item en ProjectV2 vía GraphQL."""
    value_str = ""
    if "singleSelectOptionId" in value_dict:
        value_str = f'singleSelectOptionId: "{value_dict["singleSelectOptionId"]}"'
    elif "iterationId" in value_dict:
        value_str = f'iterationId: "{value_dict["iterationId"]}"'

    mutation = f"""
    mutation {{
      updateProjectV2ItemFieldValue(input: {{
        projectId: "{project_id}"
        itemId: "{item_id}"
        fieldId: "{field_id}"
        value: {{
          {value_str}
        }}
      }}) {{
        projectV2Item {{
          id
        }}
      }}
    }}
    """
    cmd = ["gh", "api", "graphql", "-f", f"query={mutation}"]
    subprocess.run(cmd, capture_output=True, text=True)


def main():
    check_prerequisites()

    if not os.path.exists(CSV_FILENAME):
        print(f"❌ Error: Archivo '{CSV_FILENAME}' no encontrado. Ejecuta create_sprint1_tasks_csv.py primero.")
        sys.exit(1)

    print("=" * 80)
    print("🚀 IMPORTANDO 28 TAREAS TÉCNICAS A GITHUB Y PROYECTO #2")
    print(f"   Organización: {ORG}")
    print(f"   Proyecto:     #{PROJECT_NUM}")
    print(f"   Archivo:      {CSV_FILENAME}")
    print("=" * 80 + "\n")

    # Asegurar labels en repos de Sprint 1
    for repo in ["auth", "profile"]:
        print(f"🏷 Asegurando labels ('task', 'sprint-1') en {ORG}/{repo}...")
        ensure_labels(repo)

    # Metadatos del proyecto
    project_id, status_field_id, todo_option_id, sprint_field_id, sprint_1_iter_id = get_project_fields()
    print(f"✔ Project ID:         {project_id}")
    print(f"✔ Status Field:       {status_field_id} (To Do option: {todo_option_id})")
    print(f"✔ Sprint Field:       {sprint_field_id} (Sprint 1 iteration: {sprint_1_iter_id})\n")

    with open(CSV_FILENAME, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        tasks = list(reader)

    total = len(tasks)
    success = 0
    failed = 0

    for idx, task in enumerate(tasks, start=1):
        task_id = task["task_id"]
        repo = task["repo"]
        target_repo = f"{ORG}/{repo}"
        title = task["title"]
        assignee = task["assignee"]
        body = task["body"]

        print(f"[{idx}/{total}] Creando {task_id} en {target_repo} -> @{assignee}")

        # 1. Crear el Issue
        cmd_create = [
            "gh", "issue", "create",
            "--repo", target_repo,
            "--title", title,
            "--body", body,
            "--label", "task",
            "--label", "sprint-1",
            "--assignee", assignee
        ]

        res = subprocess.run(cmd_create, capture_output=True, text=True)

        # Fallback si falla asignación de usuario por permisos
        if res.returncode != 0 and "assignee" in res.stderr.lower():
            cmd_create_fallback = [
                "gh", "issue", "create",
                "--repo", target_repo,
                "--title", title,
                "--body", body,
                "--label", "task",
                "--label", "sprint-1"
            ]
            res = subprocess.run(cmd_create_fallback, capture_output=True, text=True)

        if res.returncode != 0:
            print(f"   ❌ Error al crear issue: {res.stderr.strip()}")
            failed += 1
            continue

        issue_url = res.stdout.strip()
        print(f"   ✔ Issue creado: {issue_url}")

        # 2. Agregar al proyecto #2
        cmd_add = [
            "gh", "project", "item-add", PROJECT_NUM,
            "--owner", ORG,
            "--url", issue_url,
            "--format", "json"
        ]
        res_add = subprocess.run(cmd_add, capture_output=True, text=True)
        if res_add.returncode == 0:
            try:
                item_data = json.loads(res_add.stdout)
                item_id = item_data.get("id")
                # Actualizar Status a 'To Do'
                if status_field_id and todo_option_id and item_id:
                    set_project_field(project_id, item_id, status_field_id, {"singleSelectOptionId": todo_option_id})
                # Actualizar Iteration a 'Sprint 1'
                if sprint_field_id and sprint_1_iter_id and item_id:
                    set_project_field(project_id, item_id, sprint_field_id, {"iterationId": sprint_1_iter_id})
                print(f"   ✔ Agregado al proyecto #{PROJECT_NUM} (Status='To Do', Sprint='Sprint 1')")
            except Exception as e:
                print(f"   ✔ Agregado al proyecto #{PROJECT_NUM} (aviso: {e})")
        else:
            print(f"   ⚠️ Aviso al agregar a proyecto: {res_add.stderr.strip()}")

        success += 1
        time.sleep(1)  # Rate limiting protection

    print("\n" + "=" * 80)
    print(f"🎉 COMPLETADO: {success}/{total} tareas creadas y añadidas al proyecto #2.")
    if failed > 0:
        print(f"⚠️ {failed} tareas fallaron.")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
