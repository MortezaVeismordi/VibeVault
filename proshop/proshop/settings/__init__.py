import os
from pathlib import Path

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Django settings for development, production, and testing
DJANGO_ENV = os.environ.get('DJANGO_ENV', 'development')

# Import common settings
from .base import *

# Import environment-specific settings
if DJANGO_ENV == 'production':
    from .production import *
elif DJANGO_ENV == 'testing':
    from .testing import *
else:  # development
    from .development import *
