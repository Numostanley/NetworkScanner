"""
This module contains environment variable that can be separated
from the `core.settings.base`
"""

from core.settings.base import env_config


# REDIS URL
REDIS_URL = env_config['REDIS_URL']