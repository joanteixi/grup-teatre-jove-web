#!/usr/bin/env bash
#
# publica.sh — publica els canvis de la web del Grup de Teatre Jove.
#
# Fa les tres coses, en ordre:
#   1. Compila la web
#   2. La desplega a Azure Static Web Apps
#   3. Guarda els canvis al GitHub del grup (si n'hi ha)
#
# Us:   ./publica.sh "missatge del canvi"
#
# Si alguna cosa falla, s'atura i ho diu. No desplega res a mitges.

set -euo pipefail
cd "$(dirname "$0")"

MISSATGE="${1:-Actualitzacio de la web}"
CREDS="$HOME/.hermes/credentials/staticwebapp-teatre.env"
URL="https://thankful-sky-0b824f603.3.azurestaticapps.net"

if [ ! -f "$CREDS" ]; then
  echo "ERROR: no trobo les credencials a $CREDS" >&2
  exit 1
fi
TOKEN=$(grep SWA_DEPLOYMENT_TOKEN "$CREDS" | cut -d= -f2)
if [ -z "$TOKEN" ]; then
  echo "ERROR: el fitxer de credencials no te el token" >&2
  exit 1
fi

echo "1/3  Compilant..."
npm run build

echo "2/3  Desplegant a Azure..."
swa deploy ./dist --deployment-token "$TOKEN" --env production

echo "3/3  Guardant al GitHub..."
git add -A
if git diff --cached --quiet; then
  echo "     (no hi ha canvis per guardar)"
else
  git -c user.name="Apuntador" -c user.email="apuntador@grupteatrejove.cat" \
      commit -q -m "$MISSATGE"
  git push -q origin main && echo "     pujat a GitHub"
fi

echo
echo "Fet. La web ja esta publicada a:"
echo "  $URL"
