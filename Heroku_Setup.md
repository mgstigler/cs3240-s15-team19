# Heroku Setup Steps:

1. pip freeze > requirements.txt

    requirements.txt

        Django==1.8
        SQLAlchemy==1.0.0
        dj-database-url==0.3.0
        dj-static==0.0.6
        django-postgrespool==0.3.0
        django-toolbelt==0.0.1
        gunicorn==19.3.0
        psycopg2==2.6
        static3==0.5.1
        virtualenv==12.0.6
        whitenoise==1.0.6
        
2. pip install -r requirements.txt

3. Modify the following:

    wsgi.py
    ```python
    import os
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "group.settings")
    
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()

    from django.core.wsgi import get_wsgi_application
    from whitenoise.django import DjangoWhiteNoise
    
    application = get_wsgi_application()
    application = DjangoWhiteNoise(application)
    ```

    Procfile
    ```
    web: gunicorn group.wsgi --log-file -
    ```

    settings.py
    ```python
    ...
    # Parse database configuration from $DATABASE_URL
    import dj_database_url
    
    # ------------------------------------------------------------
    # NOTE: Commenting this line makes the app work locally.
    # This needs to be uncommented before uploading to Heroku
    # ------------------------------------------------------------
    DATABASES['default'] =  dj_database_url.config()
    
    # Honor the 'X-Forwarded-Proto' header for request.is_secure()
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    
    # Allow all host headers
    ALLOWED_HOSTS = ['*']
    
    # Static asset configuration
    import os
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    STATIC_ROOT = 'staticfiles'
    STATIC_URL = '/static/'
    
    STATICFILES_DIRS = (
        os.path.join(BASE_DIR, 'static'),
    )
    ```

4. git remote rm heroku

5. git add .

6. git commit -m "Initial heroku commit"

7. heroku create --stack cedar

8. git push heroku master

9. heroku ps:scale web=1

10. heroku run python manage.py migrate

11. heroku run python manage.py loaddata initial_data.json

12. heroku open
