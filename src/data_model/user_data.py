import os
from dataclasses import asdict, dataclass

from config.env_enum import Environment
from util.singleton import singleton


@singleton
@dataclass(frozen=True)
class UserData:
    username: Environment.TAURON_USER
    password: Environment.TAURON_PASSWORD


credentials = UserData(Environment.TAURON_USER, Environment.TAURON_PASSWORD)
