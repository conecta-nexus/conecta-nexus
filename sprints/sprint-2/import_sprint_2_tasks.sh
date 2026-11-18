#!/usr/bin/env bash
# ==============================================================================
# Conecta Nexus - Script de Importación de Tareas Técnicas del Sprint 2
# ==============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=============================================================================="
echo "🚀 INICIANDO IMPORTACIÓN DE TAREAS DEL SPRINT 2 (challenge, frontend, infra, gateway)"
echo "=============================================================================="

# 1. Verificar dependencias
if ! command -v gh &> /dev/null; then
    echo "❌ Error: GitHub CLI ('gh') no está instalado."
    exit 1
fi

if ! command -v python3 &> /dev/null; then
    echo "❌ Error: python3 no está instalado."
    exit 1
fi

# 2. Verificar estado de autenticación en GitHub
echo "🔑 Verificando autenticación en GitHub..."
if ! gh auth status &> /dev/null; then
    echo "❌ Error: No has iniciado sesión en GitHub CLI."
    echo "   Por favor ejecuta: gh auth login"
    exit 1
fi
echo "✔ Autenticación exitosa."

# 3. Generar o actualizar CSV de tareas del Sprint 2
echo "📄 Generando/verificando conecta_nexus_sprint_2_tasks.csv..."
python3 create_sprint2_tasks_csv.py

# 4. Ejecutar importación a GitHub Issues y Proyecto #2
echo "🚀 Ejecutando import_sprint_2_tasks.py..."
python3 import_sprint_2_tasks.py

echo "=============================================================================="
echo "🎉 IMPORTACIÓN DEL SPRINT 2 FINALIZADA"
echo "=============================================================================="
