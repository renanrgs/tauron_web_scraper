import os
from enum import Enum


class Environment(Enum):
    TAURON_USER = os.environ.get("TAURON_USER")
    TAURON_PASSWORD = os.environ.get("TAURON_PASSWORD")
