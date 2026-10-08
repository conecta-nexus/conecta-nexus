#!/usr/bin/env bash
# ==============================================================================
# Script para clonar todos los repos directamente.
# Organización: https://github.com/conecta-nexus
# ==============================================================================

# Paleta de colores para la terminal
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

ORG_NAME="conecta-nexus"
DEFAULT_BRANCH="develop"
FALLBACK_BRANCH="main"

# Lista de microservicios y componentes del ecosistema
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

# Modo de protocolo por defecto: HTTPS (configurable con flag --ssh)
PROTOCOL="https"

imprimir_banner() {
  echo -e "${CYAN}================================================================${NC}"
  echo -e "${CYAN}             CONECTA NEXUS - WORKSPACE SETUP                   ${NC}"
  echo -e "${CYAN}================================================================${NC}"
  echo -e "Organización: ${BLUE}github.com/${ORG_NAME}${NC}"
  echo -e "Protocolo:    ${YELLOW}${PROTOCOL^^}${NC}"
  echo -e "Rama objetivo:${YELLOW}${DEFAULT_BRANCH}${NC} (fallback: ${FALLBACK_BRANCH})"
  echo -e "----------------------------------------------------------------"
}

ayuda() {
  echo "Uso: $0 [OPCIONES]"
  echo ""
  echo "Opciones:"
  echo "  --https       Clonar mediante HTTPS (por defecto)"
  echo "  --ssh         Clonar mediante SSH (git@github.com:...)"
  echo "  --branch, -b  Definir rama inicial a sincronizar (por defecto: develop)"
  echo "  --help, -h    Mostrar este mensaje de ayuda"
  exit 0
}

# Procesar argumentos de terminal
while [[ "$#" -gt 0 ]]; do
  case $1 in
    --ssh) PROTOCOL="ssh"; shift ;;
    --https) PROTOCOL="https"; shift ;;
    -b|--branch) DEFAULT_BRANCH="$2"; shift 2 ;;
    -h|--help) ayuda ;;
    *) echo -e "${RED}Opción desconocida: $1${NC}"; ayuda ;;
  esac
done

imprimir_banner

# Directorio base de ejecución (raíz del repositorio paraguas)
WORKSPACE_DIR="$(pwd)"
EXITOS=0
ACTUALIZADOS=0
FALLIDOS=0

for REPO in "${REPOS[@]}"; do
  echo -e "\n${BLUE}▶ Procesando repositorio: [${REPO}]${NC}"
  
  if [ "$PROTOCOL" == "ssh" ]; then
    REPO_URL="git@github.com:${ORG_NAME}/${REPO}.git"
  else
    REPO_URL="https://github.com/${ORG_NAME}/${REPO}.git"
  fi

  TARGET_DIR="${WORKSPACE_DIR}/${REPO}"

  # Caso 1: El directorio ya existe localmente
  if [ -d "$TARGET_DIR" ]; then
    echo -e "  ${YELLOW}✔ El directorio ya existe. Actualizando cambios remotos...${NC}"
    cd "$TARGET_DIR"
    
    # Sincronizar referencias remotas
    git fetch --all --prune --quiet || true

    # Comprobar estado de la rama
    CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "desconocida")
    echo -e "  Rama local actual: ${CYAN}${CURRENT_BRANCH}${NC}"
    
    # Intentar actualizar con pull solo si no hay cambios locales pendientes
    if git diff-index --quiet HEAD -- 2>/dev/null; then
      git pull --quiet || echo -e "  ${YELLOW}⚠ Advertencia: No se pudo hacer pull en ${CURRENT_BRANCH}.${NC}"
    else
      echo -e "  ${YELLOW}⚠ Hay cambios locales sin confirmar; se omitió 'git pull'.${NC}"
    fi

    cd "$WORKSPACE_DIR"
    ((ACTUALIZADOS++))
    continue
  fi

  # Caso 2: El repositorio no existe -> Proceder a clonar
  echo -e "  Clonando desde: ${CYAN}${REPO_URL}${NC}..."
  if git clone "$REPO_URL" "$TARGET_DIR"; then
    cd "$TARGET_DIR"

    # Intentar cambiar a la rama develop si existe en remoto
    if git ls-remote --exit-code --heads origin "$DEFAULT_BRANCH" >/dev/null 2>&1; then
      git checkout -B "$DEFAULT_BRANCH" "origin/$DEFAULT_BRANCH" --quiet 2>/dev/null || git checkout "$DEFAULT_BRANCH" --quiet
      echo -e "  ${GREEN}✔ Rama configurada en: ${DEFAULT_BRANCH}${NC}"
    else
      echo -e "  ${YELLOW}ℹ La rama '${DEFAULT_BRANCH}' no existe en remoto. Manteniendo rama por defecto.${NC}"
    fi

    cd "$WORKSPACE_DIR"
    echo -e "  ${GREEN}✔ Repositorio [${REPO}] clonado correctamente.${NC}"
    ((EXITOS++))
  else
    echo -e "  ${RED}✖ Error al clonar [${REPO}]. Verifica permisos de red o que el repo exista en la organización.${NC}"
    ((FALLIDOS++))
  fi
done

# ==============================================================================
# Resumen final de la ejecución
# ==============================================================================
echo -e "\n${CYAN}================================================================${NC}"
echo -e "${CYAN}                       RESUMEN DE ESTADO                        ${NC}"
echo -e "${CYAN}================================================================${NC}"
echo -e "  Repositorios clonados:                 ${GREEN}${EXITOS}${NC}"
echo -e "  Repositorios existentes actualizados:  ${YELLOW}${ACTUALIZADOS}${NC}"
echo -e "  Repositorios con error:                ${RED}${FALLIDOS}${NC}"
echo -e "${CYAN}================================================================${NC}"

if [ "$FALLIDOS" -eq 0 ]; then
  echo -e "\n${GREEN}✔ Todos los repositorios están listos.${NC}"
else
  echo -e "\n${YELLOW}⚠ Algunos repositorios no pudieron ser descargados. Revisa la lista superior.${NC}\n"
fi