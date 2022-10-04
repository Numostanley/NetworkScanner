"""
Abstracting CORS Settings from core.settings.base
"""

class CORS_CONFIG:
    """django_cors_headers config"""
    def __init__(self, allowed_origins: str):
        self.allowed_origins = allowed_origins.split(',')

    def settings(self):
        CORS_ALLOWED_ORIGINS = self.allowed_origins
        CORS_ALLOW_ALL_ORIGINS = False
        CORS_ALLOW_CREDENTIALS = False

        return CORS_ALLOWED_ORIGINS, CORS_ALLOW_ALL_ORIGINS, CORS_ALLOW_CREDENTIALS
