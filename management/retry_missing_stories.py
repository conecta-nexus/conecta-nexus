#!/usr/bin/env python3
"""
Conecta Nexus - Reintento Quirúrgico de Historias Pendientes
Procesa únicamente HU-01, HU-11 y HU-13 con reintentos automáticos de red.
"""

import sys
import csv
import time
import shutil
import subprocess

ORG = "conecta-nexus"
PROJECT_NUM = "2"
PROJECT_TITLE = "Conecta Nexus Management"
CSV_FILENAME = "conecta_nexus_user_stories.csv"
PENDING_IDS = {"HU-01", "HU-11", "HU-13"}

def check_prerequisites():
    if not shutil.which("gh"):
        print("❌ GitHub CLI ('gh') no está instalado.")
        sys.exit(1)
    res = subprocess.run(["gh", "auth", "status"], capture_output=True, text=True)
    if res.returncode != 0:
        print("❌ Sesión no iniciada en gh. Ejecuta: gh auth login")
        sys.exit(1)

def run_command_with_retry(cmd, max_retries=3, delay=3):
    """Ejecuta un comando con reintentos ante caídas transitorias de red."""
    for attempt in range(1, max_retries + 1):
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode == 0:
            return True, res.stdout.strip()
        err_msg = res.stderr.strip()
        if "connecting to api.github.com" in err_msg or "timeout" in err_msg.lower():
            print(f"    ⚠️ Intento {attempt}/{max_retries} falló por red. Reintentando en {delay}s...")
            time.sleep(delay)
        else:
            return False, err_msg
    return False, err_msg

def ensure_label_exists(target_repo, label_name="user-story"):
    cmd_label = [
        "gh", "label", "create", label_name,
        "--repo", target_repo,
        "--color", "0E8A16",
        "--description", "User Story backlog item",
        "--force"
    ]
    subprocess.run(cmd_label, capture_output=True, text=True)

def main():
    check_prerequisites()

    print("\n" + "=" * 80)
    print("🔁 REINTENTO DE HISTORIAS DE USUARIO PENDIENTES")
    print(f"   Objetivo: {', '.join(sorted(PENDING_IDS))}")
    print(f"   Proyecto: #{PROJECT_NUM} ({PROJECT_TITLE})")
    print("=" * 80 + "\n")

    try:
        with open(CSV_FILENAME, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            pending_stories = [row for row in reader if row.get("id") in PENDING_IDS]
    except FileNotFoundError:
        print(f"❌ No se encontró el archivo '{CSV_FILENAME}'.")
        sys.exit(1)

    total = len(pending_stories)
    success = 0

    for idx, row in enumerate(pending_stories, start=1):
        hu_id = row["id"]
        repo = row["repo"]
        title = row["title"]
        body = row["body"]
        target_repo = f"{ORG}/{repo}"

        print(f"[{idx}/{total}] Reintentando {hu_id} ➔ {target_repo}...")
        print(f"    Título: {title}")

        # 1. Asegurar label
        ensure_label_exists(target_repo, "user-story")

        # 2. Crear issue con reintento ante microcortes
        cmd_create = [
            "gh", "issue", "create",
            "--repo", target_repo,
            "--title", title,
            "--body", body,
            "--label", "user-story"
        ]
        ok_issue, out_issue = run_command_with_retry(cmd_create)

        # Fallback sin label si fallara por permisos de etiquetas
        if not ok_issue and "label" in out_issue.lower():
            cmd_fallback = [
                "gh", "issue", "create",
                "--repo", target_repo,
                "--title", title,
                "--body", body
            ]
            ok_issue, out_issue = run_command_with_retry(cmd_fallback)

        if not ok_issue:
            print(f"    ❌ Error definitivo al crear issue: {out_issue}")
            print("-" * 70)
            continue

        issue_url = out_issue
        print(f"    ✔ Issue creado: {issue_url}")

        # 3. Enlazar al Proyecto #2
        cmd_link = [
            "gh", "project", "item-add", PROJECT_NUM,
            "--owner", ORG,
            "--url", issue_url
        ]
        ok_link, out_link = run_command_with_retry(cmd_link)
        if ok_link:
            print(f"    ✔ Enlazado exitosamente al Proyecto #{PROJECT_NUM}")
            success += 1
        else:
            print(f"    ⚠️ Aviso al enlazar con el proyecto: {out_link}")
            success += 1

        print("-" * 70)
        time.sleep(1)

    print("\n" + "=" * 80)
    print(f"🎉 Finalizado: {success}/{total} historias recuperadas exitosamente.")
    print("=" * 80 + "\n")

if __name__ == "__main__":
    main()
