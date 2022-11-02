"""
This module contains environment variable that can be separated
from the `core.settings.base`
"""

from core.settings.base import env_config


# R
REDIS_URL = env_config['REDIS_URL']

# S
S3_ACCESS_KEY = env_config['S3_ACCESS_KEY']
S3_BUCKET_NAME = env_config['S3_BUCKET_NAME']
S3_DIR_PATH = env_config['S3_DIR_PATH']
S3_NAMESPACE = env_config['S3_NAMESPACE']
S3_REGION = env_config['S3_REGION']
S3_SECRET_KEY = env_config['S3_SECRET_KEY']