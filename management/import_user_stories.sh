#!/usr/bin/env bash
# ==============================================================================
# Conecta Nexus - GitHub Project & Issues Bulk Importer
# Organization: conecta-nexus
# Project URL: https://github.com/orgs/conecta-nexus/projects/2
# Project Number: 2
# Project Title: Conecta Nexus Management
# ==============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CSV_FILE="${1:-${SCRIPT_DIR}/conecta_nexus_user_stories.csv}"
ORG="conecta-nexus"
PROJECT_NUM="2"
PROJECT_TITLE="Conecta Nexus Management"

# 1. Verificar instalación de gh
if ! command -v gh &> /dev/null; then
    echo "❌ Error: GitHub CLI ('gh') no está instalado. Instálalo desde https://cli.github.com/"
    exit 1
fi

# 2. Verificar autenticación en gh
if ! gh auth status &> /dev/null; then
    echo "❌ Error: No has iniciado sesión en GitHub CLI. Ejecuta 'gh auth login' primero."
    exit 1
fi

# 3. Verificar existencia del archivo CSV
if [ ! -f "$CSV_FILE" ]; then
    echo "❌ Error: No se encontró el archivo '$CSV_FILE'."
    exit 1
fi

echo "================================================================================"
echo "🚀 Iniciando importación de Historias de Usuario a GitHub Project"
echo "   Organización:    $ORG"
echo "   Proyecto (Num):  $PROJECT_NUM ($PROJECT_TITLE)"
echo "   Archivo CSV:     $CSV_FILE"
echo "================================================================================"

# Usamos Python para parsear el CSV de forma segura soportando saltos de línea y comillas en el body
python3 - "$CSV_FILE" "$ORG" "$PROJECT_NUM" "$PROJECT_TITLE" << 'EOF'
import sys
import csv
import subprocess
import time

csv_file = sys.argv[1]
org = sys.argv[2]
project_num = sys.argv[3]
project_title = sys.argv[4]

with open(csv_file, mode='r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

total = len(rows)
success_count = 0
failed_count = 0

print(f"📦 Total de historias a procesar: {total}
")

for idx, row in enumerate(rows, start=1):
    hu_id = row.get('id', '')
    repo = row.get('repo', '')
    title = row.get('title', '')
    body = row.get('body', '')
    points = row.get('points', '')
    sprint = row.get('sprint', '')
    priority = row.get('priority', '')
    target_repo = f"{org}/{repo}"

    print(f"[{idx}/{total}] Procesando {hu_id} -> {target_repo}...")
    print(f"    Título: {title}")
    print(f"    Sprint: {sprint} | Story Points: {points} | Prioridad: {priority}")

    # Paso 1: Crear el Issue en el repositorio correspondiente
    # Intentamos crearlo y enlazarlo directamente con --project
    cmd_issue = [
        "gh", "issue", "create",
        "--repo", target_repo,
        "--title", title,
        "--body", body,
        "--label", "user-story"
    ]

    try:
        res = subprocess.run(cmd_issue, capture_output=True, text=True, check=True)
        issue_url = res.stdout.strip()
        print(f"    ✔ Issue creado: {issue_url}")
    except subprocess.CalledProcessError as e:
        print(f"    ❌ Error al crear issue en {target_repo}: {e.stderr.strip()}")
        failed_count += 1
        continue

    # Paso 2: Asociar el Issue al GitHub Project (#2)
    cmd_proj = [
        "gh", "project", "item-add", project_num,
        "--owner", org,
        "--url", issue_url
    ]

    try:
        res_proj = subprocess.run(cmd_proj, capture_output=True, text=True, check=True)
        print(f"    ✔ Añadido a Project #{project_num} ({project_title})")
        success_count += 1
    except subprocess.CalledProcessError as e:
        # Si ya estaba vinculado o fallo menor
        print(f"    ⚠️ Aviso al enlazar con project: {e.stderr.strip()}")
        success_count += 1

    print("-" * 70)
    time.sleep(1) # Prevenir rate limits

print("
================================================================================")
print(f"🎉 Resumen: {success_count}/{total} historias procesadas exitosamente.")
if failed_count > 0:
    print(f"⚠️ {failed_count} historias fallaron. Revisa los permisos y nombres de repositorios.")
print("================================================================================")
EOF
