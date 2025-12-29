from django.apps import AppConfig


class ResultConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'result'

    def ready(self):
        """
        Импортируем сигналы при загрузке приложения.
        """
        import result.signals
