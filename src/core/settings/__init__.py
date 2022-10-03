"""
Initialize settings environment.
for celery module: This will make sure the app is always imported when
    Django starts so that shared_task will use this app.
"""

from .base import base_env_config
from .celery import app as celery_app


__all__ = ('celery_app',)

def get_settings_environment():
    # detect environment to load settings configuration
    if base_env_config['ENVIRONMENT'] == 'prod':
        ENV_SETTINGS = 'core.settings.prod'
    else:
        ENV_SETTINGS = 'core.settings.dev'
    return ENV_SETTINGS
