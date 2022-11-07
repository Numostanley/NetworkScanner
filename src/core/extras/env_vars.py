"""
This module contains environment variable that can be separated
from the `core.settings.base`
"""

from core.settings.base import env_config


# R
REDIS_URL = env_config['REDIS_URL']

# S
S3_DIR_PATH = env_config['S3_DIR_PATH']