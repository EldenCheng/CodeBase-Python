from pathlib import Path
import os

# file path
PROJECT_DIR = Path(os.path.dirname(__file__))

# log
LOGGER = 'WeSoft'
LOG_LEVEL = 'DEBUG'
LOG_PATH = str(PROJECT_DIR / Path('./app.log'))
DEVICE_LOG = str(PROJECT_DIR / Path('./{0}.log'))
ERROR_LOG = str(PROJECT_DIR / Path('./error.log'))
DEVICE_ERROR_LOG = str(PROJECT_DIR / Path('./{0}_error.log'))
