"""
Django settings for insurance_site (lab: insurance company).
SQLite for local dev; PostgreSQL when POSTGRES_HOST or DATABASE_URL is set (Docker / prod).

Это центральный конфигурационный файл проекта Django:
здесь задаются база данных, установленные приложения, шаблоны,
статик-файлы, авторизация и логирование.
"""

import importlib.util  # используется, чтобы проверить наличие whitenoise без его импорта
import os              # доступ к переменным окружения (DJANGO_*, POSTGRES_*, DATABASE_URL)
from pathlib import Path
from urllib.parse import urlparse  # разбор строки подключения DATABASE_URL на составные части

# Корневая папка проекта (родитель папки с этим файлом: в ней лежат db.sqlite3, templates, static)
BASE_DIR = Path(__file__).resolve().parent.parent

# Секретный ключ Django: используется для подписей (CSRF, сессии и т.д.).
# В продакшене обязательно задавать через переменную окружения, значение по умолчанию — только для разработки.
SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "dev-only-change-in-production-not-for-real-use",
)

# Режим отладки: включает подробные страницы ошибок и авто-перезагрузку.
# Включается из окружения (1/true/yes), по умолчанию — true (удобно для разработки).
DEBUG = os.environ.get("DJANGO_DEBUG", "true").lower() in ("1", "true", "yes")

# Список доменов, которые могут обслуживать сайт (защита от Host-header атак).
ALLOWED_HOSTS = [
    h.strip()
    for h in os.environ.get("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
    if h.strip()
]

# Установленные приложения: стандартные модули Django + наше приложение insurance.
INSTALLED_APPS = [
    "django.contrib.admin",         # админ-панель
    "django.contrib.auth",          # система пользователей и ролей
    "django.contrib.contenttypes",  # фреймворк для связей между моделями
    "django.contrib.sessions",      # сессии (хранение состояния между запросами)
    "django.contrib.messages",      # флеш-сообщения для пользователя
    "django.contrib.staticfiles",   # раздача статических файлов (css/js/картинки)
    "insurance",                    # наше приложение «страховая компания»
]

# Проверяем, установлен ли пакет whitenoise (сервировка статики в продакшене).
_WHITENOISE_AVAILABLE = importlib.util.find_spec("whitenoise") is not None

# Middleware — цепочка обработчиков, через которые проходит каждый запрос
# (защита, сессии, авторизация, CSRF и т.д.). Порядок важен!
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",  # базовая веб-защита
]
if _WHITENOISE_AVAILABLE:
    # WhiteNoise должен идти сразу после SecurityMiddleware,
    # чтобы отдавать статику раньше, чем запрос попадёт к приложению.
    MIDDLEWARE.append("whitenoise.middleware.WhiteNoiseMiddleware")
MIDDLEWARE += [
    "django.contrib.sessions.middleware.SessionMiddleware",   # поддержка сессий
    "django.middleware.common.CommonMiddleware",              # URL-нормализация (www, слеши)
    "django.middleware.csrf.CsrfViewMiddleware",              # защита от CSRF-атак
    "django.contrib.auth.middleware.AuthenticationMiddleware", # привязка пользователя к запросу
    "django.contrib.messages.middleware.MessageMiddleware",   # флеш-сообщения
    "django.middleware.clickjacking.XFrameOptionsMiddleware", # защита от clickjacking
]

# Точка входа для разрешения URL-адресов (файл urls.py на уровне проекта).
ROOT_URLCONF = "insurance_site.urls"

# Настройка шаблонов: где искать HTML и какие переменные добавлять во все шаблоны.
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],  # общая папка шаблонов проекта
        "APP_DIRS": True,                  # искать шаблоны также внутри приложений
        "OPTIONS": {
            "context_processors": [        # автоматически подмешиваются в контекст каждого шаблона
                "django.template.context_processors.debug",
                "django.template.context_processors.request",  # даёт шаблонам доступ к request
                "django.contrib.auth.context_processors.auth", # текущий пользователь
                "django.contrib.messages.context_processors.messages",
                "insurance.context_processors.access_flags",   # наши флаги доступа для шаблонов
            ],
        },
    },
]

# Точка входа для WSGI-сервера (gunicorn/uwsgi при деплое).
WSGI_APPLICATION = "insurance_site.wsgi.application"


def _database_config():
    """Выбор базы данных по приоритету: DATABASE_URL -> POSTGRES_* -> SQLite (локальная разработка)."""
    url = os.environ.get("DATABASE_URL", "").strip()
    if url:
        # Полная строка подключения (например, postgres://user:pass@host:5432/dbname).
        u = urlparse(url)
        if u.scheme not in ("postgres", "postgresql"):
            raise ValueError("DATABASE_URL must use postgres:// or postgresql://")
        path = (u.path or "").lstrip("/")  # имя базы данных из пути URL
        return {
            "default": {
                "ENGINE": "django.db.backends.postgresql",
                "NAME": path or "insurance",
                "USER": u.username or "insurance",
                "PASSWORD": u.password or "",
                "HOST": u.hostname or "localhost",
                "PORT": str(u.port or 5432),
                "CONN_MAX_AGE": int(os.environ.get("DB_CONN_MAX_AGE", "60")),  # переиспользование соединений
            }
        }
    host = os.environ.get("POSTGRES_HOST", "").strip()
    if host:
        # Настройка Postgres отдельными переменными окружения (удобно для Docker Compose).
        return {
            "default": {
                "ENGINE": "django.db.backends.postgresql",
                "NAME": os.environ.get("POSTGRES_DB", "insurance"),
                "USER": os.environ.get("POSTGRES_USER", "insurance"),
                "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "insurance"),
                "HOST": host,
                "PORT": os.environ.get("POSTGRES_PORT", "5432"),
                "CONN_MAX_AGE": int(os.environ.get("DB_CONN_MAX_AGE", "60")),
            }
        }
    # Резервный вариант: серверная база в файле db.sqlite3 — используется локально в разработке.
    return {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }


DATABASES = _database_config()

# Валидаторы паролей: запрещают слишком простые / похожие на имя пользователя пароли.
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Локализация: сайт на русском языке, часовой пояс Минска.
LANGUAGE_CODE = "ru-ru"
TIME_ZONE = 'Europe/Minsk'
USE_I18N = True          # включаем систему переводов
USE_TZ = True            # хранить даты в UTC, показывать локально

# Статические файлы (CSS/JS/картинки).
# Leading slash required: otherwise /news/ resolves img src to /news/static/... (404).
STATIC_URL = "/static/"  # URL-префикс, по которому отдаются стат. файлы
_STATIC_DIR = BASE_DIR / "static"
STATICFILES_DIRS = [_STATIC_DIR] if _STATIC_DIR.is_dir() else []  # исходная папка статики
STATIC_ROOT = BASE_DIR / "staticfiles"  # сюда собирается статика командой collectstatic для продакшена

# Выбор бэкенда для статики: WhiteNoise (сжатие) при наличии, иначе стандартный.
_static_backend = (
    "whitenoise.storage.CompressedStaticFilesStorage"
    if _WHITENOISE_AVAILABLE
    else "django.contrib.staticfiles.storage.StaticFilesStorage"
)
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",  # загрузка файлов на диск
    },
    "staticfiles": {
        "BACKEND": _static_backend,
    },
}

# WhiteNoise serves /static/ in runserver, Docker, and hosting (DEBUG true or false).
# WhiteNoise отдаёт статику в любом режиме — не нужен отдельный nginx для файлов.
if _WHITENOISE_AVAILABLE:
    WHITENOISE_USE_FINDERS = True
    # Если стоит за обратным прокси (nginx/Cloudflare), доверяем заголовку https.
    if os.environ.get("DJANGO_BEHIND_PROXY", "").lower() in ("1", "true", "yes"):
        SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    # Отправлять куки только по HTTPS (включать в продакшене).
    if os.environ.get("DJANGO_SECURE_COOKIES", "").lower() in ("1", "true", "yes"):
        SESSION_COOKIE_SECURE = True
        CSRF_COOKIE_SECURE = True
    # Доверенные источники для CSRF (домены, с которых принимаются POST-запросы).
    _csrf = os.environ.get("DJANGO_CSRF_TRUSTED_ORIGINS", "")
    if _csrf.strip():
        CSRF_TRUSTED_ORIGINS = [x.strip() for x in _csrf.split(",") if x.strip()]

# Тип автоинкремента для первичных ключей моделей.
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Куда перенаправлять после входа/выхода и где страница логина.
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"
LOGIN_URL = "/accounts/login/"

# Уровень логирования и флаг записи в файл — настраиваются через окружение.
# Log level from config (stage 8 will expand handlers)
LOG_LEVEL = os.environ.get("DJANGO_LOG_LEVEL", "INFO")
LOG_TO_FILE = os.environ.get("DJANGO_LOG_TO_FILE", "false").lower() in ("1", "true", "yes")

# Настройка логирования: в консоль всегда, в файл logs/insurance.log — по флагу.
LOG_DIR = BASE_DIR / "logs"
_handlers = {
    "console": {
        "class": "logging.StreamHandler",   # пишем логи в консоль/stdout
        "formatter": "verbose",
    },
}
if LOG_TO_FILE:
    LOG_DIR.mkdir(parents=True, exist_ok=True)  # создаём папку logs, если её ещё нет
    _handlers["file"] = {
        "class": "logging.FileHandler",
        "filename": str(LOG_DIR / "insurance.log"),
        "formatter": "verbose",
    }

LOGGING = {
    "version": 1,                       # формат конфигурации
    "disable_existing_loggers": False,  # не отключать логгеры сторонних библиотек
    "formatters": {
        "verbose": {
            # формат строки лога: время, уровень, имя логгера, сообщение
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        },
    },
    "handlers": _handlers,   # все настроенные обработчики (console + возможно file)
    "root": {
        "handlers": list(_handlers.keys()),
        "level": LOG_LEVEL,
    },
    "loggers": {                        # свои уровни для конкретных "семейств" логгеров
        "django": {
            "handlers": list(_handlers.keys()),
            "level": LOG_LEVEL,
            "propagate": False,         # не передавать записи выше по иерархии (избегаем дублей)
        },
        "django.request": {
            "handlers": list(_handlers.keys()),
            "level": "WARNING",         # ошибки запросов логируем только от WARNING и выше
            "propagate": False,
        },
        "insurance": {
            "handlers": list(_handlers.keys()),
            "level": LOG_LEVEL,
            "propagate": False,
        },
        "insurance.external": {
            "handlers": list(_handlers.keys()),
            "level": LOG_LEVEL,
            "propagate": False,
        },
        "insurance.api": {
            "handlers": list(_handlers.keys()),
            "level": LOG_LEVEL,
            "propagate": False,
        },
    },
}