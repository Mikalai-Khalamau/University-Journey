import os

def get_env(key: str, fallback: str) -> str:
    return os.getenv(key, fallback)
