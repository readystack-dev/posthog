from django.apps import AppConfig


class ReadyStackCEConfig(AppConfig):
    """The Django app label "ee" that PostHog's MIT-licensed models declare (products/access_control ...)."""
    name = "ee"
    label = "ee"
    verbose_name = "ReadyStack CE compatibility (no Enterprise code)"
    default_auto_field = "django.db.models.AutoField"
