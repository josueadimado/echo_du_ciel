"""
WSGI configuration for PythonAnywhere deployment.
Copy this content to your PythonAnywhere WSGI configuration file.
"""

import os
import sys

# Add your project directory to the Python path
# Replace 'votre_username' with your PythonAnywhere username
path = '/home/votre_username/echo_du_ciel'
if path not in sys.path:
    sys.path.insert(0, path)

# Set the Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'louange_echo.settings'

# Activate your virtual environment
activate_this = '/home/votre_username/echo_du_ciel/venv/bin/activate_this.py'
if os.path.exists(activate_this):
    with open(activate_this) as file_:
        exec(file_.read(), dict(__file__=activate_this))

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
