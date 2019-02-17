import os

# Statement for enabling the development environment
ENV = os.environ.get('ENVIRONMENT', 'development')
DEBUG = os.environ.get('DEBUG', True)

# Define the application directory

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_BASE = os.path.abspath(os.path.join(BASE_DIR, 'uploads'))

# Define the database - we are working with (defaults to $PROJECT_ROOT/safe.db (sqlite3))
DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///' + os.path.join(BASE_DIR, 'safe.db'))
SQLALCHEMY_DATABASE_URI = DATABASE_URI
SQLALCHEMY_TRACK_MODIFICATIONS = True
DATABASE_CONNECT_OPTIONS = {}

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 8

# # Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED     = True

# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = "secret"

# Secret key for signing cookies
SECRET_KEY = "secret"
