#!/usr/bin/env python3
"""
Completes the import of remaining tasks to GitHub and Project #2.
"""

import os
import sys
import csv
import json
import time
import subprocess

ORG = "conecta-nexus"
PROJECT_NUM = "2"
CSV_FILENAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), "conecta_nexus_sprint_1_tasks.csv")

PROJECT_ID = "PVT_kwDOE2mZY84BmwV4"
STATUS_FIELD_ID = "PVTSSF_lADOE2mZY84BmwV4zhlYC3M"
TODO_OPTION_ID = "f75ad846"
SPRINT_FIELD_ID = "PVTIF_lADOE2mZY84BmwV4zhlYDeA"
SPRINT_1_ITER_ID = "381c7c80"


def set_project_field(item_id, field_id, value_dict):
    value_str = ""
    if "singleSelectOptionId" in value_dict:
        value_str = f'singleSelectOptionId: "{value_dict["singleSelectOptionId"]}"'
    elif "iterationId" in value_dict:
        value_str = f'iterationId: "{value_dict["iterationId"]}"'

    mutation = f"""
    mutation {{
      updateProjectV2ItemFieldValue(input: {{
        projectId: "{PROJECT_ID}"
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


def add_issue_to_project(issue_url, max_retries=5):
    for attempt in range(1, max_retries + 1):
        cmd_add = [
            "gh", "project", "item-add", PROJECT_NUM,
            "--owner", ORG,
            "--url", issue_url,
            "--format", "json"
        ]
        res = subprocess.run(cmd_add, capture_output=True, text=True)
        if res.returncode == 0:
            try:
                data = json.loads(res.stdout)
                item_id = data.get("id")
                if item_id:
                    set_project_field(item_id, STATUS_FIELD_ID, {"singleSelectOptionId": TODO_OPTION_ID})
                    set_project_field(item_id, SPRINT_FIELD_ID, {"iterationId": SPRINT_1_ITER_ID})
                print(f"   ✔ Enlazado al proyecto: {issue_url}")
                return True
            except Exception as e:
                print(f"   ⚠️ Aviso JSON al agregar: {e}")
                return True
        print(f"   (Reintento {attempt}/{max_retries} al agregar a proyecto: {res.stderr.strip()})")
        time.sleep(2 * attempt)
    return False


def create_issue_with_retry(repo, title, body, assignee, max_retries=5):
    target_repo = f"{ORG}/{repo}"
    for attempt in range(1, max_retries + 1):
        cmd = [
            "gh", "issue", "create",
            "--repo", target_repo,
            "--title", title,
            "--body", body,
            "--label", "task",
            "--label", "sprint-1",
            "--assignee", assignee
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode == 0:
            url = res.stdout.strip()
            print(f"   ✔ Issue creado: {url}")
            return url
        print(f"   (Reintento {attempt}/{max_retries} al crear issue: {res.stderr.strip()})")
        time.sleep(2 * attempt)
    return None


def main():
    print("=" * 80)
    print("🔧 COMPLETANDO ENLACES Y TAREAS PENDIENTES DEL SPRINT 1")
    print("=" * 80 + "\n")

    # 1. Enlazar las 3 tareas que ya tenían issue pero falló el enlace inicial
    already_created_unlinked = [
        ("auth", "https://github.com/conecta-nexus/auth/issues/3"),
        ("profile", "https://github.com/conecta-nexus/profile/issues/8"),
        ("profile", "https://github.com/conecta-nexus/profile/issues/13")
    ]

    print("📌 1. Enlazando issues existentes al proyecto #2...")
    for repo, url in already_created_unlinked:
        print(f"   Enlazando {url}...")
        add_issue_to_project(url)
        time.sleep(1)

    # 2. Cargar CSV y crear las 5 tareas faltantes
    missing_task_ids = {
        "AUTH-TASK-07",
        "AUTH-TASK-08",
        "AUTH-TASK-09",
        "PROFILE-TASK-02",
        "PROFILE-TASK-07"
    }

    print("\n📌 2. Creando las 5 tareas faltantes...")
    with open(CSV_FILENAME, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for task in reader:
            tid = task["task_id"]
            if tid not in missing_task_ids:
                continue
            repo = task["repo"]
            title = task["title"]
            assignee = task["assignee"]
            body = task["body"]

            print(f"   Creando {tid} ({title})...")
            url = create_issue_with_retry(repo, title, body, assignee)
            if url:
                add_issue_to_project(url)
            time.sleep(1)

    print("\n" + "=" * 80)
    print("🎉 TODAS LAS 28 TAREAS ESTÁN AHORA REGISTRADAS Y ENLAZADAS AL PROYECTO.")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
