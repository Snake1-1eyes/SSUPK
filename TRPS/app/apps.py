from django.apps import AppConfig


class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'

class VmhConfig(AppConfig):
    name = 'vmh'
    label = 'vmh'