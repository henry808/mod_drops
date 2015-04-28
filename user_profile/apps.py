from django.apps import AppConfig


class ImagerAppConfig(AppConfig):

    name = 'user_profile'
    verbose_name = 'Profile App'

    def ready(self):
        import user_profile.handlers