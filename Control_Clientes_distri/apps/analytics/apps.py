from django.apps import AppConfig

class AnalyticsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.analytics'  # según tu estructura

    def ready(self):
        import apps.analytics.signals
