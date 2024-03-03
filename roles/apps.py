from django.apps import AppConfig


class RolesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "roles"
    verbose_name = 'perfiles'

    def ready(self):
        import roles.signals
