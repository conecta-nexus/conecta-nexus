#!/usr/bin/env bash
# ==============================================================================
# Conecta Nexus - Copy Templates & Push to All Repositories
# ==============================================================================

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
RED='\033[0;31m'
NC='\033[0m' # No Color

ROOT_DIR="$(pwd)"

REPOS=(
  "application"
  "auth"
  "challenge"
  "frontend"
  "gateway"
  "infra"
  "moderation"
  "notification"
  "profile"
)

COMMIT_MSG="chore(setup): add repository templates, issue forms, and contributing guidelines"

echo -e "${CYAN}================================================================${NC}"
echo -e "${CYAN}    DISTRIBUCIÓN DE PLANTILLAS Y PUSH A REPOSITORIOS (MAIN/DEV)  ${NC}"
echo -e "${CYAN}================================================================${NC}"
echo -e "Commit message: ${YELLOW}\"${COMMIT_MSG}\"${NC}\n"

# 1. Validar que los templates existan en la raíz
if [ ! -d ".github" ] || [ ! -f "CONTRIBUTING.md" ]; then
  echo -e "${RED}Error: No se encontró la carpeta .github/ o el archivo CONTRIBUTING.md en la raíz.${NC}"
  exit 1
fi

# 2. Recorrer y procesar cada subrepositorio
for REPO in "${REPOS[@]}"; do
  TARGET_PATH="${ROOT_DIR}/${REPO}"

  echo -e "${BLUE}▶ Procesando repositorio: [${REPO}]${NC}"

  if [ ! -d "$TARGET_PATH" ] || [ ! -d "$TARGET_PATH/.git" ]; then
    echo -e "  ${YELLOW}⚠ Carpeta '${REPO}' no encontrada o no es un repositorio Git. Omitiendo.${NC}"
    continue
  fi

  # Copiar la estructura de templates de forma limpia y segura
  mkdir -p "$TARGET_PATH/.github/ISSUE_TEMPLATE"
  cp -f "$ROOT_DIR/.github/PULL_REQUEST_TEMPLATE.md" "$TARGET_PATH/.github/" 2>/dev/null || true
  cp -f "$ROOT_DIR/.github/CODEOWNERS" "$TARGET_PATH/.github/" 2>/dev/null || true
  cp -rf "$ROOT_DIR/.github/ISSUE_TEMPLATE/"* "$TARGET_PATH/.github/ISSUE_TEMPLATE/" 2>/dev/null || true
  cp -f "$ROOT_DIR/CONTRIBUTING.md" "$TARGET_PATH/" 2>/dev/null || true

  echo -e "  ${GREEN}✔ Archivos copiados a ${REPO}/.github/ y ${REPO}/CONTRIBUTING.md${NC}"

  cd "$TARGET_PATH" || continue

  # Asegurarse de estar en main
  git checkout main --quiet 2>/dev/null || true

  # Agregar los templates copiados
  git add .github CONTRIBUTING.md

  # Verificar si hay cambios listos para commit
  if git diff --cached --quiet; then
    echo -e "  ${YELLOW}ℹ No hay cambios nuevos que commitear en ${REPO}.${NC}"
  else
    git commit -m "$COMMIT_MSG" --quiet
    echo -e "  ${GREEN}✔ Commit creado en rama 'main'.${NC}"
  fi

  # Subir rama main a GitHub
  echo -e "  Subiendo cambios a origin/main..."
  git push -u origin main --quiet 2>/dev/null && echo -e "  ${GREEN}✔ main sincronizado en GitHub.${NC}" || echo -e "  ${YELLOW}⚠ Advertencia al subir a origin/main.${NC}"

  # Crear o sincronizar rama develop a partir del main actualizado
  git checkout -B develop --quiet
  echo -e "  Subiendo rama develop a origin/develop..."
  git push -u origin develop --quiet 2>/dev/null && echo -e "  ${GREEN}✔ develop sincronizado en GitHub.${NC}" || echo -e "  ${YELLOW}⚠ Advertencia al subir a origin/develop.${NC}"

  # Dejar el repositorio posicionado en develop para el inicio del sprint
  git checkout develop --quiet 2>/dev/null || true
  echo -e "  ${CYAN}➜ Rama activa fijada en: develop${NC}\n"

  cd "$ROOT_DIR" || exit 1
done

# 3. Procesar el repositorio paraguas raíz (conecta-nexus)
echo -e "${BLUE}▶ Procesando repositorio raíz: [conecta-nexus]${NC}"
cd "$ROOT_DIR" || exit 1

git checkout main --quiet 2>/dev/null || true
git add .github CONTRIBUTING.md .gitignore setup.sh 2>/dev/null || true

if ! git diff --cached --quiet; then
  git commit -m "$COMMIT_MSG" --quiet
  echo -e "  ${GREEN}✔ Commit creado en repositorio raíz.${NC}"
fi

echo -e "  Subiendo rama main del raíz..."
git push -u origin main --quiet 2>/dev/null || true

git checkout -B develop --quiet
echo -e "  Subiendo rama develop del raíz..."
git push -u origin develop --quiet 2>/dev/null || true

git checkout develop --quiet 2>/dev/null || true
echo -e "  ${CYAN}➜ Rama activa del raíz fijada en: develop${NC}"

echo -e "\n${CYAN}================================================================${NC}"
echo -e "${GREEN}✔ ¡Todos los templates fueron distribuidos y subidos a main y develop!${NC}"
echo -e "${CYAN}================================================================${NC}\n"
