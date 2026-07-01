from django.apps import AppConfig
from django.db.models.signals import post_save

class DevboardConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "devboard"
    verbose_name = "System Zarządzania Projektami v.0.1"

    def ready(self):
        print("Aplikacja DevBOARD została uruchomiona")
        
        # Sygnał, opcja 1:
        # from devboard.models import Task
        # post_save.connect(save_done_info, sender=Task, dispatch_uid="save_done_info_on_task")

        # Sygnał, opcja 2 - @receiver w signals.py:
        from devboard import signals  # noqa: F401        
