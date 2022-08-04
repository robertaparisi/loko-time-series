import os
from ds4biz_commons.utils.config_utils import EnvInit


env=EnvInit()

REPO_PATH = os.path.abspath(env.REPO or '../../repo')
