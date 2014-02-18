import os

from settings_base import *
owl_env = os.getenv("OWL_ENV", 'local')

if owl_env == 'production_http':
    from settings_production_http import *
else:
    from settings_local import *
