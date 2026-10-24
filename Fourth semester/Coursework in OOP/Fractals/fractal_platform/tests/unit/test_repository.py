from src.core.config import ConfigLoader
from src.infrastructure.repositories.sqlalchemy_repo import SQLAlchemyFractalRepository


def test_repository_list_returns_array():
    config = ConfigLoader().load()
    repo = SQLAlchemyFractalRepository(config.database_url)
    assert isinstance(repo.list(), list)
