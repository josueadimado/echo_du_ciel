#!/bin/bash
# Script de configuration pour PythonAnywhere
# Exécutez ce script dans un Bash Console sur PythonAnywhere

echo "=== Configuration de Louange Echo sur PythonAnywhere ==="

# Variables (modifiez selon votre configuration)
USERNAME=$(whoami)
PROJECT_DIR="$HOME/echo_du_ciel"

echo "Nom d'utilisateur détecté: $USERNAME"
echo "Répertoire du projet: $PROJECT_DIR"

# Aller dans le répertoire du projet
cd $PROJECT_DIR || exit

# Créer l'environnement virtuel
echo "Création de l'environnement virtuel..."
python3.10 -m venv venv

# Activer l'environnement virtuel
echo "Activation de l'environnement virtuel..."
source venv/bin/activate

# Installer les dépendances
echo "Installation des dépendances..."
pip install -r requirements.txt

# Collecter les fichiers statiques
echo "Collecte des fichiers statiques..."
python manage.py collectstatic --noinput

# Appliquer les migrations
echo "Application des migrations..."
python manage.py migrate

# Créer un superutilisateur (optionnel - vous devrez entrer les informations)
echo "Création du superutilisateur..."
echo "Vous devrez entrer un nom d'utilisateur, email et mot de passe"
python manage.py createsuperuser

# Importer les paroles
echo "Importation des paroles..."
python manage.py import_lyrics

echo ""
echo "=== Configuration terminée ==="
echo ""
echo "Prochaines étapes:"
echo "1. Allez dans le Dashboard PythonAnywhere → Web"
echo "2. Configurez le fichier WSGI avec le contenu de wsgi_pythonanywhere.py"
echo "3. Configurez les fichiers statiques:"
echo "   - URL: /static/"
echo "   - Directory: $PROJECT_DIR/staticfiles/"
echo "4. Mettez à jour ALLOWED_HOSTS dans settings.py avec votre domaine PythonAnywhere"
echo "5. Redémarrez l'application web dans le Dashboard"
echo ""
