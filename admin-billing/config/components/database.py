from config.components.env_setting import env_settings

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env_settings.psql_name,
        'USER': env_settings.psql_user,
        'PASSWORD': env_settings.psql_password,
        'HOST': env_settings.psql_host,
        'PORT': env_settings.psql_port,
        'OPTIONS': {
            'options': '-c search_path=public,content',
        },
    },
}
