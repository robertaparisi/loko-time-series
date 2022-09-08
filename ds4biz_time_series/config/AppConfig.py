import os
from ds4biz_commons.utils.config_utils import EnvInit


env=EnvInit()

# RANDOM_STATE = 2502
REPO_PATH = os.path.abspath(env.REPO or '../../repo')
