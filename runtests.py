#!/usr/bin/env python

from __future__ import unicode_literals

import django

from django.conf import settings
from django.core.management import call_command


settings.configure(
    INSTALLED_APPS=(
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sites',
        'django.contrib.admin',
        'django.contrib.sessions',
        'treasuremap',
    ),
    DATABASES={
        'default': {'ENGINE': 'django.db.backends.sqlite3'}
    },
    TEMPLATES=[
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.contrib.auth.context_processors.auth',
                    'django.template.context_processors.request',
                    'django.template.context_processors.debug',
                    'django.template.context_processors.i18n',
                    'django.template.context_processors.media',
                    'django.template.context_processors.static',
                    'django.template.context_processors.tz',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ],
    TREASURE_MAP={
        'BACKEND': 'treasuremap.backends.google.GoogleMapBackend'
    },
    TEST_RUNNER='django.test.runner.DiscoverRunner'
)

django.setup()

if __name__ == '__main__':
    call_command('test', 'treasuremap')
