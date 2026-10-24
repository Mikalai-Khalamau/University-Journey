from __future__ import annotations

from src.application.services.task_tracker import TaskStatusTracker
from src.application.services.auth_service import AuthService
from src.application.services.validator import FractalValidator
from src.application.use_cases.delete_fractal import DeleteFractalUseCase
from src.application.use_cases.export_params import ExportParamsUseCase
from src.application.use_cases.generate_fractal import GenerateFractalUseCase
from src.application.use_cases.get_collection import GetFractalCollectionUseCase
from src.application.use_cases.import_params import ImportParamsUseCase
from src.application.use_cases.update_fractal import UpdateFractalUseCase
from src.core.exceptions import UnauthorizedError
from src.core.config import ConfigLoader
from src.infrastructure.factories.generator_factory import FractalGeneratorFactory
from src.infrastructure.auth.jwt_service import JwtService
from src.infrastructure.repositories.sqlalchemy_repo import SQLAlchemyFractalRepository, SQLAlchemyUserRepository
from src.infrastructure.storage.file_storage import FileImageStorage
from src.infrastructure.workers.async_worker import AsyncFractalWorker
from src.infrastructure.notifiers.ui_notifier import UINotifier
from src.infrastructure.notifiers.email_notifier import EmailNotifier
from src.application.facades.stats_facade import StatsFacade
from fastapi import Header

config = ConfigLoader().load()
repository = SQLAlchemyFractalRepository(config.database_url)
user_repository = SQLAlchemyUserRepository(config.database_url)
storage = FileImageStorage(config.media_dir)
factory = FractalGeneratorFactory()
validator = FractalValidator(config)
jwt_service = JwtService(config)
auth_service = AuthService(user_repository, jwt_service)
task_tracker = TaskStatusTracker()
stats_facade = StatsFacade(repository)

generate_use_case = GenerateFractalUseCase(repository, storage, factory, validator)
collection_use_case = GetFractalCollectionUseCase(repository)
delete_use_case = DeleteFractalUseCase(repository, storage)
export_use_case = ExportParamsUseCase(repository)
import_use_case = ImportParamsUseCase(generate_use_case)
update_use_case = UpdateFractalUseCase(repository)

worker = AsyncFractalWorker(generate_use_case.execute)
worker.attach(task_tracker)

ui_notifier = UINotifier()
email_notifier = EmailNotifier(
    smtp_host=config.smtp_host,
    smtp_port=config.smtp_port,
    from_email=config.email_from,
    use_tls=config.smtp_use_tls,
)

worker.attach(task_tracker)
worker.attach(ui_notifier)
worker.attach(email_notifier)

__all__ = [
    "ui_notifier",
    "email_notifier",
    "stats_facade",
]

def get_current_user(authorization: str | None = Header(default=None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise UnauthorizedError("Authorization token is required")
    token = authorization.replace("Bearer ", "", 1).strip()
    return auth_service.get_user_from_token(token)
