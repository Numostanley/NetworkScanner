"""
Abstracting SIMPLE_JWT Settings from core.settings.base
"""

from datetime import timedelta


class SIMPLE_JWT_CONFIG:
    """rest_framework_simplejwt config"""

    def __init__(self, secret_key: str):
        """initialize settings variables."""
        self.access_token_life_time = timedelta(minutes=10)
        self.auth_headers = ('Bearer', 'Access-Token')
        self.secret_key = secret_key

    def settings(self):
        config_vars = {
            'ACCESS_TOKEN_LIFETIME': self.access_token_life_time,
            'SIGNING_KEY': self.secret_key,
            'AUTH_HEADER_TYPES': self.auth_headers
        }
        return config_vars
