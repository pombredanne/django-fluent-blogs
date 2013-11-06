from django.conf import settings
from distutils.version import StrictVersion
from django.core.exceptions import ImproperlyConfigured
from parler import appsettings as parler_appsettings
import fluent_contents


# Configurable permalink style, yeah!
FLUENT_BLOGS_ENTRY_LINK_STYLE = getattr(settings, "FLUENT_BLOGS_ENTRY_LINK_STYLE", '/{year}/{month}/{slug}/')
FLUENT_BLOGS_BASE_TEMPLATE = getattr(settings, "FLUENT_BLOGS_BASE_TEMPLATE", 'fluent_blogs/base.html')
FLUENT_BLOGS_CATEGORY_MODEL = getattr(settings, "FLUENT_BLOGS_CATEGORY_MODEL", 'categories.Category')
FLUENT_BLOGS_ENTRY_MODEL = getattr(settings, "FLUENT_BLOGS_ENTRY_MODEL", 'fluent_blogs.Entry')

FLUENT_BLOGS_FEED_PROTOCOL = getattr(settings, "FLUENT_BLOGS_FEED_PROTOCOL", 'http')
FLUENT_BLOGS_MAX_FEED_ITEMS = getattr(settings, "FLUENT_BLOGS_MAX_FEED_ITEMS", 30)

FLUENT_BLOGS_INCLUDE_STATIC_FILES = getattr(settings, "FLUENT_BLOGS_INCLUDE_STATIC_FILES", True)

# Note: the default language setting is used during the migrations
FLUENT_DEFAULT_LANGUAGE_CODE = getattr(settings, 'FLUENT_DEFAULT_LANGUAGE_CODE', parler_appsettings.PARLER_DEFAULT_LANGUAGE_CODE)

# Allow this module to have other settings, but default to the shared settings
FLUENT_BLOGS_DEFAULT_LANGUAGE_CODE = getattr(settings, 'FLUENT_BLOGS_DEFAULT_LANGUAGE_CODE', FLUENT_DEFAULT_LANGUAGE_CODE)
FLUENT_BLOGS_LANGUAGES = getattr(settings, 'FLUENT_BLOGS_LANGUAGES', parler_appsettings.PARLER_LANGUAGES)

FLUENT_BLOGS_LANGUAGES = parler_appsettings.add_default_language_settings(
    FLUENT_BLOGS_LANGUAGES, 'FLUENT_BLOGS_LANGUAGES',
    code=FLUENT_BLOGS_DEFAULT_LANGUAGE_CODE,
    fallback=FLUENT_BLOGS_DEFAULT_LANGUAGE_CODE,
    hide_untranslated=False,
)


def get_language_settings(language_code, site_id=None):
    """
    Return the language settings for the current site
    """
    if site_id is None:
        site_id = settings.SITE_ID

    for lang_dict in FLUENT_BLOGS_LANGUAGES.get(site_id, ()):
        if lang_dict['code'] == language_code:
            return lang_dict

    return FLUENT_BLOGS_LANGUAGES['default']


# Perform version checks
if len(FLUENT_BLOGS_LANGUAGES.get(settings.SITE_ID, ())) > 1:
    if StrictVersion(fluent_contents.__version__) < StrictVersion('1.0a1'):
        raise ImproperlyConfigured("Using the multilingual support requires django-fluent-contents 1.0dev")
