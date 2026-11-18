#!/usr/bin/env python3
"""
Conecta Nexus - Importador Oficial y Robusto de Tareas Técnicas del Sprint 2
Lee conecta_nexus_sprint_2_tasks.csv, asegura etiquetas, crea los issues en
conecta-nexus/challenge, frontend, infra y gateway con reintentos automáticos,
los asocia al proyecto #2 (Conecta Nexus Management) y configura:
  - Status = 'To Do' (f75ad846)
  - Iteration = 'Sprint 2' (54cf5c95)
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
PROJECT_ID = "PVT_kwDOE2mZY84BmwV4"
STATUS_FIELD_ID = "PVTSSF_lADOE2mZY84BmwV4zhlYC3M"
TODO_OPTION_ID = "f75ad846"
SPRINT_FIELD_ID = "PVTIF_lADOE2mZY84BmwV4zhlYDeA"
SPRINT_2_ITER_ID = "54cf5c95"

CSV_FILENAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), "conecta_nexus_sprint_2_tasks.csv")
RESULTS_FILENAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), "import_results.json")


def run_command_with_retry(cmd, max_retries=5, initial_delay=2, is_json=False):
    """Ejecuta un comando con reintentos exponenciales ante fallos transitorios de red."""
    for attempt in range(1, max_retries + 1):
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, check=False)
            if res.returncode == 0:
                if is_json:
                    try:
                        return True, json.loads(res.stdout)
                    except json.JSONDecodeError as e:
                        return False, f"JSONDecodeError: {e} -> stdout: {res.stdout[:100]}"
                return True, res.stdout.strip()

            stderr = res.stderr.strip()
            # Si el error es transitorio de red o corte de API
            transient_signals = [
                "error connecting to api.github.com",
                "timeout",
                "tls handshake timeout",
                "connection reset by peer",
                "network is unreachable",
                "could not resolve host"
            ]
            if any(signal in stderr.lower() for signal in transient_signals):
                wait = initial_delay * attempt
                print(f"      [Reintento {attempt}/{max_retries}] Conexión GitHub inestable. Esperando {wait}s...")
                time.sleep(wait)
                continue

            # Si es otro tipo de error (ej: permiso, validación), retornamos de inmediato
            return False, stderr
        except Exception as exc:
            wait = initial_delay * attempt
            print(f"      [Excepción {attempt}/{max_retries}] {exc}. Esperando {wait}s...")
            time.sleep(wait)

    return False, f"Agotados los {max_retries} reintentos."


def check_prerequisites():
    if not shutil.which("gh"):
        print("❌ Error: GitHub CLI ('gh') no está instalado.")
        sys.exit(1)
    ok, out = run_command_with_retry(["gh", "auth", "status"])
    if not ok:
        print(f"❌ Error: Sesión no válida en GitHub CLI: {out}")
        sys.exit(1)


def ensure_labels(repo: str):
    """Asegura que los labels 'task' y 'sprint-2' existan en el repositorio."""
    labels = [
        ("task", "1D76DB", "Granular engineering task"),
        ("sprint-2", "0E8A16", "Sprint 2 (23 Oct - 11 Nov 2026)"),
    ]
    for name, color, desc in labels:
        cmd = [
            "gh", "label", "create", name,
            "--repo", f"{ORG}/{repo}",
            "--color", color,
            "--description", desc,
            "--force"
        ]
        run_command_with_retry(cmd, max_retries=3, initial_delay=1)


def get_existing_issues(repo: str):
    """Obtiene los issues existentes para garantizar idempotencia."""
    cmd = [
        "gh", "issue", "list",
        "--repo", f"{ORG}/{repo}",
        "--state", "all",
        "--limit", "100",
        "--json", "number,title,url"
    ]
    ok, data = run_command_with_retry(cmd, is_json=True)
    if ok and isinstance(data, list):
        return {item["title"].strip(): item for item in data}
    return {}


def update_project_fields(item_id: str):
    """Actualiza Status='To Do' e Iteration='Sprint 2' en una sola mutación GraphQL."""
    mutation = f"""
    mutation {{
      setStatus: updateProjectV2ItemFieldValue(input: {{
        projectId: "{PROJECT_ID}"
        itemId: "{item_id}"
        fieldId: "{STATUS_FIELD_ID}"
        value: {{ singleSelectOptionId: "{TODO_OPTION_ID}" }}
      }}) {{
        projectV2Item {{ id }}
      }}
      setSprint: updateProjectV2ItemFieldValue(input: {{
        projectId: "{PROJECT_ID}"
        itemId: "{item_id}"
        fieldId: "{SPRINT_FIELD_ID}"
        value: {{ iterationId: "{SPRINT_2_ITER_ID}" }}
      }}) {{
        projectV2Item {{ id }}
      }}
    }}
    """
    cmd = ["gh", "api", "graphql", "-f", f"query={mutation}"]
    ok, res = run_command_with_retry(cmd, is_json=True)
    return ok, res


def add_issue_to_project(issue_url: str):
    """Agrega un issue al Proyecto #2 y configura los campos Status e Iteration."""
    cmd_add = [
        "gh", "project", "item-add", PROJECT_NUM,
        "--owner", ORG,
        "--url", issue_url,
        "--format", "json"
    ]
    ok, data = run_command_with_retry(cmd_add, is_json=True)
    if not ok:
        return False, None, f"Error al agregar a proyecto: {data}"

    item_id = data.get("id")
    if not item_id:
        return True, None, "Aviso: No se retornó item_id en la respuesta"

    ok_field, field_res = update_project_fields(item_id)
    if not ok_field:
        return True, item_id, f"Aviso al configurar campos en ProjectV2: {field_res}"

    return True, item_id, "Configurado con éxito en ProjectV2"


def main():
    check_prerequisites()

    if not os.path.exists(CSV_FILENAME):
        print(f"❌ Error: Archivo '{CSV_FILENAME}' no encontrado.")
        sys.exit(1)

    print("=" * 80)
    print("🚀 IMPORTACIÓN OFICIAL DE LAS 30 TAREAS TÉCNICAS DEL SPRINT 2 A GITHUB")
    print(f"   Organización:      {ORG}")
    print(f"   Proyecto:          #{PROJECT_NUM} (ID: {PROJECT_ID})")
    print(f"   Iteración Destino: Sprint 2 (ID: {SPRINT_2_ITER_ID})")
    print(f"   Estado Destino:    To Do (ID: {TODO_OPTION_ID})")
    print(f"   Archivo CSV:       {CSV_FILENAME}")
    print("=" * 80 + "\n")

    # 1. Asegurar etiquetas en todos los repositorios del Sprint 2
    target_repos = ["challenge", "frontend", "infra", "gateway"]
    for repo in target_repos:
        print(f"🏷 Asegurando etiquetas ('task', 'sprint-2') en {ORG}/{repo}...")
        ensure_labels(repo)
    print()

    # 2. Cargar tareas desde el CSV
    with open(CSV_FILENAME, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        tasks = list(reader)

    total = len(tasks)
    print(f"📋 Se procesarán {total} tareas técnicas distribuidas equitativamente (10 por desarrollador).\n")

    # Cache de issues existentes por repo para idempotencia
    existing_by_repo = {}
    for repo in target_repos:
        print(f"🔍 Consultando estado previo en {ORG}/{repo}...")
        existing_by_repo[repo] = get_existing_issues(repo)
    print()

    results = []
    success_count = 0
    skipped_count = 0
    failed_count = 0

    start_time = time.time()

    for idx, task in enumerate(tasks, start=1):
        task_id = task["task_id"]
        repo = task["repo"]
        target_repo = f"{ORG}/{repo}"
        title = task["title"]
        assignee = task["assignee"]
        body = task["body"]
        parent_story = task.get("parent_story", "")

        print(f"[{idx:02d}/{total:02d}] Procesando {task_id} ({repo}) -> @{assignee} [{parent_story}]")

        existing_map = existing_by_repo.get(repo, {})
        issue_url = None
        item_id = None
        created_now = False

        # Verificar si el issue ya existe
        if title in existing_map:
            issue_url = existing_map[title]["url"]
            print(f"   ℹ️  Issue ya existente: {issue_url}")
            skipped_count += 1
        else:
            # Crear el issue en GitHub
            cmd_create = [
                "gh", "issue", "create",
                "--repo", target_repo,
                "--title", title,
                "--body", body,
                "--label", "task",
                "--label", "sprint-2",
                "--assignee", assignee
            ]
            ok, out = run_command_with_retry(cmd_create)

            # Fallback si falla asignación de usuario
            if not ok and "assignee" in str(out).lower():
                print(f"   ⚠️ Reintentando sin asignación directa para @{assignee}...")
                cmd_fallback = [
                    "gh", "issue", "create",
                    "--repo", target_repo,
                    "--title", title,
                    "--body", body,
                    "--label", "task",
                    "--label", "sprint-2"
                ]
                ok, out = run_command_with_retry(cmd_fallback)

            if not ok:
                print(f"   ❌ Error al crear issue: {out}")
                failed_count += 1
                results.append({
                    "task_id": task_id,
                    "repo": repo,
                    "title": title,
                    "assignee": assignee,
                    "status": "FAILED_CREATION",
                    "error": str(out)
                })
                continue

            issue_url = str(out).strip()
            print(f"   ✔ Issue creado: {issue_url}")
            created_now = True
            success_count += 1

        # Agregar al Proyecto #2 y configurar campos
        ok_proj, item_id, proj_msg = add_issue_to_project(issue_url)
        if ok_proj:
            print(f"   ✔ Vinculado a Proyecto #2: Item ID {item_id} (Status='To Do', Iteration='Sprint 2')")
        else:
            print(f"   ⚠️ Aviso en proyecto: {proj_msg}")

        results.append({
            "task_id": task_id,
            "repo": repo,
            "title": title,
            "assignee": assignee,
            "issue_url": issue_url,
            "item_id": item_id,
            "created": created_now,
            "project_synced": ok_proj,
            "message": proj_msg
        })

        time.sleep(1)  # Pequeña pausa preventiva contra rate-limits de la API de GitHub

    # Guardar reporte de resultados
    with open(RESULTS_FILENAME, mode="w", encoding="utf-8") as rf:
        json.dump(results, rf, indent=2, ensure_ascii=False)

    elapsed = round(time.time() - start_time, 1)

    print("\n" + "=" * 80)
    print("🎉 RESUMEN DE EJECUCIÓN DEL SPRINT 2")
    print(f"   Total Tareas:      {total}")
    print(f"   Creadas nuevas:    {success_count}")
    print(f"   Ya existentes:     {skipped_count}")
    print(f"   Fallidas:          {failed_count}")
    print(f"   Tiempo total:      {elapsed} segundos")
    print(f"   Registro JSON:     {RESULTS_FILENAME}")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
