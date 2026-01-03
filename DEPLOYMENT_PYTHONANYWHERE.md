# Guide de Déploiement sur PythonAnywhere

Ce guide vous aidera à déployer votre application Django "Louange Echo" sur PythonAnywhere.

## Prérequis

1. Un compte PythonAnywhere (gratuit ou payant)
2. Votre code poussé sur GitHub : https://github.com/josueadimado/echo_du_ciel.git

## Étape 1 : Créer un compte PythonAnywhere

1. Allez sur https://www.pythonanywhere.com/
2. Créez un compte gratuit (Beginner) ou payant
3. Connectez-vous à votre compte

## Étape 2 : Ouvrir un Bash Console

1. Dans le tableau de bord PythonAnywhere, cliquez sur **"Consoles"** dans le menu
2. Cliquez sur **"Bash"** pour ouvrir un terminal

## Étape 3 : Cloner votre dépôt GitHub

Dans le terminal Bash, exécutez :

```bash
cd ~
git clone https://github.com/josueadimado/echo_du_ciel.git
cd echo_du_ciel
```

## Étape 4 : Créer un environnement virtuel

```bash
python3.10 -m venv venv
source venv/bin/activate
```

**Note** : PythonAnywhere utilise Python 3.10 par défaut. Vérifiez la version avec `python3 --version`

## Étape 5 : Installer les dépendances

```bash
pip install --user -r requirements.txt
```

**Note importante** : Sur PythonAnywhere, utilisez `pip install --user` pour éviter les problèmes de permissions.

## Étape 6 : Configurer les fichiers statiques

### 6.1 Collecter les fichiers statiques

```bash
python manage.py collectstatic --noinput
```

### 6.2 Configurer dans le Dashboard PythonAnywhere

1. Allez dans **"Web"** dans le menu
2. Cliquez sur votre application web (ou créez-en une)
3. Dans la section **"Static files"**, ajoutez :
   - **URL** : `/static/`
   - **Directory** : `/home/votre_username/echo_du_ciel/staticfiles/`

## Étape 7 : Configurer la base de données

```bash
python manage.py migrate
```

## Étape 8 : Créer un superutilisateur (admin)

```bash
python manage.py createsuperuser
```

Suivez les instructions pour créer un compte administrateur.

## Étape 9 : Importer les paroles

```bash
python manage.py import_lyrics
```

## Étape 10 : Configurer le fichier WSGI

1. Dans le Dashboard PythonAnywhere, allez dans **"Web"**
2. Cliquez sur **"WSGI configuration file"**
3. Remplacez le contenu par :

```python
import os
import sys

# Add your project directory to the Python path
path = '/home/votre_username/echo_du_ciel'
if path not in sys.path:
    sys.path.insert(0, path)

# Set the Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'louange_echo.settings'

# Activate your virtual environment
activate_this = '/home/votre_username/echo_du_ciel/venv/bin/activate_this.py'
if os.path.exists(activate_this):
    exec(open(activate_this).read(), {'__file__': activate_this})

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

**Important** : Remplacez `votre_username` par votre nom d'utilisateur PythonAnywhere.

## Étape 11 : Configurer les paramètres Django pour la production

Modifiez `louange_echo/settings.py` :

```python
# Dans settings.py, modifiez :
DEBUG = False
ALLOWED_HOSTS = ['votre_username.pythonanywhere.com']

# Pour la production, générez une nouvelle SECRET_KEY
# Vous pouvez utiliser : python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
SECRET_KEY = 'votre-secret-key-generee'
```

## Étape 12 : Redémarrer l'application web

1. Dans le Dashboard PythonAnywhere, allez dans **"Web"**
2. Cliquez sur le bouton **"Reload"** pour redémarrer votre application

## Étape 13 : Tester votre application

Visitez : `https://votre_username.pythonanywhere.com/`

## Configuration supplémentaire (optionnel)

### Pour un domaine personnalisé

Si vous avez un domaine personnalisé :
1. Allez dans **"Web"** → **"Domains"**
2. Ajoutez votre domaine
3. Mettez à jour `ALLOWED_HOSTS` dans `settings.py`

### Pour les fichiers média (images)

Si vous voulez permettre l'upload d'images :
1. Dans **"Web"** → **"Static files"**, ajoutez :
   - **URL** : `/media/`
   - **Directory** : `/home/votre_username/echo_du_ciel/media/`

## Dépannage

### Problème : Erreur 500
- Vérifiez les logs dans **"Web"** → **"Error log"**
- Vérifiez que tous les chemins sont corrects
- Vérifiez que les migrations sont appliquées

### Problème : Fichiers statiques non chargés
- Vérifiez que `collectstatic` a été exécuté
- Vérifiez la configuration des fichiers statiques dans le Dashboard
- Vérifiez que les chemins sont corrects

### Problème : Module non trouvé
- Vérifiez que vous avez installé toutes les dépendances
- Vérifiez que l'environnement virtuel est activé dans le WSGI

## Commandes utiles

```bash
# Activer l'environnement virtuel
source venv/bin/activate

# Voir les logs
tail -f /var/log/votre_username.pythonanywhere.com.error.log

# Mettre à jour le code depuis GitHub
git pull origin main
python manage.py collectstatic --noinput
# Puis redémarrer l'application dans le Dashboard
```

## Support

Pour plus d'aide, consultez :
- Documentation PythonAnywhere : https://help.pythonanywhere.com/
- Documentation Django : https://docs.djangoproject.com/
