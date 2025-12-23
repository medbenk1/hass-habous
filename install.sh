#!/bin/bash
# Script d'installation pour Salat Time Home Assistant Component
# Usage: ./install.sh

REPO_URL="https://github.com/medbenk1/hass-habous.git"
TEMP_DIR="/tmp/hass-habous-install"
CONFIG_DIR="${HOME_ASSISTANT_CONFIG:-/config}"

echo "=========================================="
echo "Installation de Salat Time pour Home Assistant"
echo "=========================================="
echo ""

# Vérifier si le répertoire config existe
if [ ! -d "$CONFIG_DIR" ]; then
    echo "❌ Erreur: Répertoire config non trouvé: $CONFIG_DIR"
    echo "   Définissez HOME_ASSISTANT_CONFIG avec le chemin vers votre config HA"
    echo "   Exemple: export HOME_ASSISTANT_CONFIG=/config && ./install.sh"
    exit 1
fi

echo "📁 Répertoire config: $CONFIG_DIR"
echo ""

# Créer le répertoire custom_components s'il n'existe pas
if [ ! -d "$CONFIG_DIR/custom_components" ]; then
    echo "📂 Création du répertoire custom_components..."
    mkdir -p "$CONFIG_DIR/custom_components"
fi

# Cloner le repo temporairement
echo "⬇️  Téléchargement depuis GitHub..."
if [ -d "$TEMP_DIR" ]; then
    rm -rf "$TEMP_DIR"
fi

git clone "$REPO_URL" "$TEMP_DIR" --quiet

if [ $? -ne 0 ]; then
    echo "❌ Erreur lors du clonage du dépôt"
    exit 1
fi

# Copier le custom component
echo "📋 Copie des fichiers..."
cp -r "$TEMP_DIR/custom_components/salat_time" "$CONFIG_DIR/custom_components/"

if [ $? -ne 0 ]; then
    echo "❌ Erreur lors de la copie des fichiers"
    rm -rf "$TEMP_DIR"
    exit 1
fi

# Nettoyer
rm -rf "$TEMP_DIR"

echo ""
echo "✅ Installation terminée avec succès!"
echo ""
echo "📝 Prochaines étapes:"
echo "   1. Ajoutez la configuration dans votre configuration.yaml:"
echo ""
echo "      sensor:"
echo "        - platform: salat_time"
echo "          ville: 7"
echo ""
echo "   2. Redémarrez Home Assistant"
echo ""
echo "📚 Documentation: https://github.com/medbenk1/hass-habous"
echo ""

