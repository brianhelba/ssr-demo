from __future__ import annotations

from pathlib import Path

from composed_configuration import (
    ComposedConfiguration,
    ConfigMixin,
    DjangoMixin, AllauthMixin, LoggingMixin, DatabaseMixin,
    WhitenoiseStaticFileMixin, FilterMixin, GirderUtilsMixin, DebugMixin, ConsoleEmailMixin,
    HttpsMixin,
)
from configurations import values


class SsrDemoMixin(ConfigMixin):
    WSGI_APPLICATION = 'ssr_demo.wsgi.application'
    ROOT_URLCONF = 'ssr_demo.urls'

    BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

    @staticmethod
    def mutate_configuration(configuration: ComposedConfiguration) -> None:
        # Install local apps first, to ensure any overridden resources are found first
        configuration.INSTALLED_APPS = [
            'ssr_demo.core.apps.CoreConfig',
        ] + configuration.INSTALLED_APPS

        # Install additional apps
        configuration.INSTALLED_APPS += [
            'widget_tweaks',
        ]


class BaseConfiguration(
    GirderUtilsMixin,
    FilterMixin,
    # CorsMixin must be loaded after WhitenoiseStaticFileMixin
    WhitenoiseStaticFileMixin,
    DatabaseMixin,
    LoggingMixin,
    AllauthMixin,
    # DjangoMixin should be loaded first
    DjangoMixin,
    ComposedConfiguration,
):
    pass


class DevelopmentConfiguration(SsrDemoMixin, DebugMixin, ConsoleEmailMixin, BaseConfiguration):
    DEBUG = True
    SECRET_KEY = 'insecuresecret'
    ALLOWED_HOSTS = values.ListValue(['localhost', '127.0.0.1'])
    INTERNAL_IPS = ['127.0.0.1']


class ProductionConfiguration(SsrDemoMixin, ConsoleEmailMixin, HttpsMixin, BaseConfiguration):
    SECRET_KEY = 'Rig7MgFhHNFf6ffKfNB2GhOPWY6VInmn'
    ALLOWED_HOSTS = values.ListValue(['d118-67-249-129-137.ngrok.io', '127.0.0.1'])
    INTERNAL_IPS = []
