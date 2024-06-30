from .settings import *

# Override the MEDIA_ROOT for tests
MEDIA_ROOT = os.path.join(BASE_DIR, "files", "tests")
