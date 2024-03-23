from dataclasses import dataclass
import os
from typing import List
from environs import Env


@dataclass
class Settings:
    token: str
    admin_ids: List[int]
    database_url: str


def get_config(path: str):
    env = Env()
    env.read_env(path)

    return Settings(
        token=env.str("TOKEN"),
        database_url=env.str("DATABASE_URL"),
        admin_ids=list(map(int, env.str("ADMIN_IDS", '').split(' '))) if os.getenv("ADMIN_IDS", '') != '' else [],
    )


config = get_config('.env') #Здесь необходимо указать путь до файла с переменными