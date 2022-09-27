"""
Abstracting REST Framework Settings from core.settings.base
"""

class REST_FRAMEWORK_CONFIG:

    @staticmethod
    def settings():
        REST_CONFIG = {
            'DEFAULT_RENDERER_CLASSES': [
                'rest_framework.renderers.JSONRenderer',  # Disable Browsable REST API Form
            ],
            'DEFAULT_AUTHENTICATION_CLASSES': [
                'rest_framework_simplejwt.authentication.JWTAuthentication',
            ],
            'DEFAULT_THROTTLE_CLASSES': [
                'rest_framework.throttling.AnonRateThrottle',
                'rest_framework.throttling.UserRateThrottle'
            ],
            'DEFAULT_THROTTLE_RATES': {
                'anon': '5/minute',
                'user': '10/minute'
            }
        }
        return REST_CONFIG
