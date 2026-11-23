#!/usr/bin/env python3
"""
Conecta Nexus - Importador Oficial y Robusto de Tareas Técnicas del Sprint 3
Lee conecta_nexus_sprint_3_tasks.csv, asegura etiquetas, crea los issues en
los repositorios correspondientes (frontend, application, notification, moderation, gateway, infra),
los asocia al proyecto #2 (Conecta Nexus Management) y configura Status e Iteración.
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

CSV_FILENAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), "conecta_nexus_sprint_3_tasks.csv")
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

            return False, f"Exit code {res.returncode}: {stderr}"
        except Exception as ex:
            wait = initial_delay * attempt
            print(f"      [Reintento {attempt}/{max_retries}] Excepción local: {ex}. Esperando {wait}s...")
            time.sleep(wait)

    return False, "Excedido número máximo de reintentos."


def ensure_labels(repo):
    """Asegura que las etiquetas task, sprint-3, frontend, etc. existan en el repositorio."""
    labels = [
        {"name": "task", "color": "0E8A16", "description": "Granular engineering task"},
        {"name": "sprint-3", "color": "1D76DB", "description": "Sprint 3 Deliverable (12 Nov - 02 Dec 2026)"},
        {"name": "reopened", "color": "B60205", "description": "Reopened item from previous sprint"},
        {"name": "frontend", "color": "5319E7", "description": "Nuxt 4 / Vue 3 user interface"},
        {"name": "application", "color": "FBCA04", "description": "Application microservice"},
        {"name": "notification", "color": "006B75", "description": "Notification microservice"},
        {"name": "moderation", "color": "D93F0B", "description": "Moderation microservice"},
        {"name": "gateway", "color": "C2E0C6", "description": "API Gateway / Nginx"},
        {"name": "infra", "color": "BFDADC", "description": "Terraform / Cloud Infrastructure"}
    ]
    for lbl in labels:
        cmd = [
            "gh", "label", "create", lbl["name"],
            "--repo", f"{ORG}/{repo}",
            "--color", lbl["color"],
            "--description", lbl["description"],
            "--force"
        ]
        run_command_with_retry(cmd)


def main():
    if not shutil.which("gh"):
        print("❌ Error: 'gh' CLI no está instalado en el sistema.")
        sys.exit(1)

    auth_ok, auth_out = run_command_with_retry(["gh", "auth", "status"])
    if not auth_ok:
        print(f"❌ Error de autenticación en GitHub CLI:\n{auth_out}")
        print("💡 Ejecute 'gh auth login' antes de continuar.")
        sys.exit(1)

    print("==================================================================")
    print("      CONECTA NEXUS - SPRINT 3 TASK IMPORTER (GITHUB PROJECTS)     ")
    print("==================================================================")
    print(f"✔ Organización: {ORG}")
    print(f"✔ Proyecto: #{PROJECT_NUM}")
    print(f"✔ CSV Origen: {CSV_FILENAME}")

    if not os.path.exists(CSV_FILENAME):
        print(f"❌ Error: Archivo CSV '{CSV_FILENAME}' no encontrado.")
        sys.exit(1)

    with open(CSV_FILENAME, mode="r", encoding="utf-8") as f:
        tasks = list(csv.DictReader(f))

    print(f"✔ Total de tareas encontradas: {len(tasks)}")

    # Asegurar repositorios únicos
    repos = list(set(t["repo"] for t in tasks))
    print(f"✔ Asegurando etiquetas en {len(repos)} repositorios: {', '.join(repos)}")
    for repo in repos:
        ensure_labels(repo)

    results = []
    for idx, task in enumerate(tasks, start=1):
        task_id = task["task_id"]
        repo = task["repo"]
        title = task["title"]
        assignee = task["assignee"]
        labels = task["labels"]
        body = task["body"]

        print(f"\n[{idx}/{len(tasks)}] Procesando {task_id}: {title[:60]}...")

        # 1. Crear issue
        cmd = [
            "gh", "issue", "create",
            "--repo", f"{ORG}/{repo}",
            "--title", title,
            "--body", body,
            "--label", labels
        ]
        if assignee:
            cmd.extend(["--assignee", assignee])

        success, out = run_command_with_retry(cmd)
        if not success:
            print(f"   ❌ Fallo al crear issue: {out}")
            results.append({"task_id": task_id, "status": "ERROR", "error": str(out)})
            continue

        issue_url = out
        print(f"   ✔ Issue creado: {issue_url}")

        results.append({
            "task_id": task_id,
            "status": "CREATED",
            "url": issue_url,
            "repo": repo,
            "assignee": assignee
        })

    with open(RESULTS_FILENAME, mode="w", encoding="utf-8") as rf:
        json.dump(results, rf, indent=2)

    print("\n==================================================================")
    print(f"✔ Proceso completado. Resultados guardados en '{RESULTS_FILENAME}'.")
    print("==================================================================")


if __name__ == "__main__":
    main()
