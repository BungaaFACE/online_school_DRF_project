SECRET_KEY=django-insecure-88888888888888888888888888888888888888888888888888
DEBUG=True

DB_ENGINE=django.db.backends.postgresql_psycopg2
DB_NAME=online_school
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
# DB container
PGDATA=/var/lib/postgresql/data

EMAIL_PORT=465
EMAIL_USE_SSL=True
EMAIL_HOST=smtp.yandex.ru
TEST_EMAIL_LOGIN=mail
TEST_EMAIL_PASSWORD=pass

CACHE_ENABLED=True
CACHE_LOCATION=redis://redis:6379

STRIPE_API_KEY=awdaddwad

CELERY_BROKER_URL=redis://redis:6379
CELERY_RESULT_BACKEND=redis://redis:6379
CELERY_TIMEZONE=Europe/Moscow
CELERY_TASK_TRACK_STARTED=True