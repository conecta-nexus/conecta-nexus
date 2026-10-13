#!/usr/bin/env bash
# ==============================================================================
# Conecta Nexus - Initial Commit & Push Automation Script
# Standards: Conventional Commits in English (chore), develop & main sync.
# ==============================================================================

# Paleta de colores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
RED='\033[0;31m'
NC='\033[0m'

ROOT_DIR="$(pwd)"

# Lista de repositorios hijos
REPOS=(
  "frontend"
  "gateway"
  "auth"
  "profile"
  "challenge"
  "application"
  "moderation"
  "notification"
  "infra"
)

# Mensaje de commit estandarizado bajo Conventional Commits (en inglés)
COMMIT_MSG="chore(setup): initialize project templates, documentation and workspace structure"

echo -e "${CYAN}================================================================${NC}"
echo -e "${CYAN}         CONECTA NEXUS - COMMIT & PUSH TO MAIN / DEVELOP        ${NC}"
echo -e "${CYAN}================================================================${NC}"
echo -e "Commit message: ${YELLOW}\"${COMMIT_MSG}\"${NC}\n"

# Función para procesar un repositorio específico
commit_and_push_repo() {
  local target_path="$1"
  local repo_name="$2"

  echo -e "${BLUE}▶ Procesando repositorio: [${repo_name}]${NC}"
  cd "$target_path" || return

  if [ ! -d ".git" ]; then
    echo -e "  ${RED}✖ No es un repositorio git. Omitiendo.${NC}"
    cd "$ROOT_DIR" || return
    return
  fi

  # Asegurar staging de archivos
  git add -A

  # Comprobar si hay cambios pendientes por commitear
  if git diff-index --quiet HEAD -- 2>/dev/null; then
    echo -e "  ${YELLOW}ℹ No hay cambios nuevos en el working tree.${NC}"
  else
    git commit -m "$COMMIT_MSG"
    echo -e "  ${GREEN}✔ Commit creado exitosamente.${NC}"
  fi

  # Detectar la rama actual (generalmente main)
  CURRENT_BRANCH=$(git symbolic-ref --short HEAD 2>/dev/null || echo "main")
  
  # Subir rama actual (main)
  echo -e "  Subiendo cambios a ${CYAN}origin/${CURRENT_BRANCH}${NC}..."
  git push -u origin "$CURRENT_BRANCH" 2>/dev/null || echo -e "  ${YELLOW}⚠ Advertencia al pushear a ${CURRENT_BRANCH}.${NC}"

  # Crear y subir la rama develop para habilitar el flujo de PRs
  echo -e "  Sincronizando rama ${CYAN}develop${NC}..."
  git checkout -B develop 2>/dev/null
  git push -u origin develop 2>/dev/null || echo -e "  ${YELLOW}⚠ Advertencia al pushear a develop.${NC}"

  # Regresar a develop como rama de trabajo activa
  git checkout develop --quiet 2>/dev/null || true
  echo -e "  ${GREEN}✔ [${repo_name}] sincronizado en main y develop.${NC}\n"

  cd "$ROOT_DIR" || return
}

# 1. Procesar repositorios hijos
for repo in "${REPOS[@]}"; do
  if [ -d "$ROOT_DIR/$repo" ]; then
    commit_and_push_repo "$ROOT_DIR/$repo" "$repo"
  else
    echo -e "${RED}✖ Directorio $repo no encontrado. Omitiendo.${NC}"
  fi
done

# 2. Procesar el repositorio paraguas raíz (conecta-nexus)
echo -e "${BLUE}▶ Procesando repositorio raíz: [conecta-nexus (paraguas)]${NC}"
commit_and_push_repo "$ROOT_DIR" "conecta-nexus"

echo -e "${CYAN}================================================================${NC}"
echo -e "${GREEN}✔ ¡Todos los repositorios fueron actualizados y subidos!${NC}"
echo -e "${CYAN}================================================================${NC}"
