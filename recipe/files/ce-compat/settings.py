# ReadyStack CE: values for the settings PostHog's MIT-licensed code reads by name but which PostHog defines only in
# its Enterprise settings module (not in this build). Every value is ReadyStack's own: an API key, URL or secret is
# read from the environment (empty when unset, so the feature reports itself unconfigured); an Enterprise-only switch
# is off. PostHog's MIT code guards its Enterprise paths with settings.EE_AVAILABLE, which stays False in this build.
import os


def _env(name, default=""):
    return os.environ.get(name, default)


def _env_int(name, default):
    try:
        return int(os.environ.get(name, default))
    except ValueError:
        return default


def _env_bool(name, default=False):
    v = os.environ.get(name)
    return default if v is None else v.strip().lower() in ("1", "true", "yes", "on")


# API keys and endpoints of third-party services some MIT features call (set them to enable those features)
for _n in ("ANTHROPIC_API_KEY", "OPENAI_API_KEY", "OPENAI_MODEL", "GEMINI_API_KEY", "MISTRAL_API_KEY", "PPLX_API_KEY",
           "INKEEP_API_KEY", "BRAINTRUST_API_KEY", "HARMONIC_API_KEY", "HARMONIC_BASE_URL", "AZURE_INFERENCE_CREDENTIAL",
           "AZURE_INFERENCE_ENDPOINT", "LLM_GATEWAY_API_KEY", "LLM_GATEWAY_URL", "REPLAY_VISION_GEMINI_API_KEY",
           "LLMA_EVAL_ANTHROPIC_API_KEY", "LLMA_EVAL_GEMINI_API_KEY", "LLMA_EVAL_OPENAI_API_KEY",
           "LLMA_EVAL_OPENAI_BASE_URL", "CUSTOMER_IO_API_KEY", "CUSTOMER_IO_API_URL", "DEV_API_KEY"):
    globals()[_n] = _env(_n)
OPENAI_BASE_URL = _env("OPENAI_BASE_URL", "https://api.openai.com/v1")

# PostHog Cloud billing, Salesforce, Vercel and admin-portal integrations: not part of this build
BILLING_SERVICE_URL = ""
BILLING_PROVIDER_WEBHOOK_SECRET = ""
BILLING_ACCESS_TOKEN_TTL_SECONDS = 900
SALESFORCE_INTERNAL_CONSUMER_KEY = SALESFORCE_INTERNAL_CONSUMER_SECRET = SALESFORCE_INTERNAL_DOMAIN = ""
SALESFORCE_USERNAME = SALESFORCE_PASSWORD = SALESFORCE_SECURITY_TOKEN = ""
VERCEL_CLIENT_INTEGRATION_ID = VERCEL_CLIENT_INTEGRATION_SECRET = VERCEL_INTEGRATION_SLUG = ""
ADMIN_PORTAL_ENABLED = _env_bool("ADMIN_PORTAL_ENABLED", False)
ENFORCE_ADMIN_OAUTH2 = False
ADMIN_AUTH_GOOGLE_OAUTH2_KEY = ADMIN_AUTH_GOOGLE_OAUTH2_SECRET = None
ADMIN_AUTH_GOOGLE_ALLOWED_DOMAINS = []
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = _env("SOCIAL_AUTH_GOOGLE_OAUTH2_KEY") or None
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = _env("SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET") or None
SQS_QUEUES = {}

# Enterprise-only ClickHouse column materialisation: off
MATERIALIZE_COLUMNS_SCHEDULE_CRON = ""
MATERIALIZE_COLUMNS_MINIMUM_QUERY_TIME = 0
MATERIALIZE_COLUMNS_ANALYSIS_PERIOD_HOURS = 0
MATERIALIZE_COLUMNS_BACKFILL_PERIOD_DAYS = 0
MATERIALIZE_COLUMNS_MAX_AT_ONCE = 0

# Report/subscription asset generation timeout (minutes) used by MIT subscription delivery
PARALLEL_ASSET_GENERATION_MAX_TIMEOUT_MINUTES = _env_int("PARALLEL_ASSET_GENERATION_MAX_TIMEOUT_MINUTES", 10)
TEMPORAL_TASK_TIMEOUT_MINUTES = PARALLEL_ASSET_GENERATION_MAX_TIMEOUT_MINUTES * 1.5

# No Enterprise single-sign-on backends: the authentication backends are PostHog's own (MIT code reads this list
# from here to tell SSO logins apart).
from posthog.settings.web import AUTHENTICATION_BACKENDS  # noqa: E402,F401


def __getattr__(name):
    # Any other setting MIT code reads from this module directly is PostHog's own Django setting.
    from django.conf import settings
    return getattr(settings, name)
