CELERY_BROKER_URL = "pyamqp://guest@localhost"

DEBUG = True

# Run: `python -c "import os; print(repr(os.urandom(24)))"` for a secure key
SECRET_KEY = 'This is insecure.'

# Use postgresql in prod
SQLALCHEMY_DATABASE_URI = "sqlite:///../../../app.sqlite"
