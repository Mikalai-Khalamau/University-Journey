from __future__ import annotations

import json
from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, Float, ForeignKey, String, create_engine, select, text, delete, func
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker

from src.domain.entities.fractal import Fractal
from src.domain.entities.user import User
from src.domain.interfaces.repository import IFractalRepository
from src.domain.interfaces.user_repository import IUserRepository
from src.domain.value_objects.fractal_params import FractalParams, build_fractal_params
from src.domain.value_objects.image_metadata import ImageMetadata


class Base(DeclarativeBase):
    pass


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    username: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    email: Mapped[str | None] = mapped_column(String(120), nullable=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class FractalModel(Base):
    __tablename__ = "fractals"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), index=True)
    name: Mapped[str] = mapped_column(String(120))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    fractal_type: Mapped[str] = mapped_column(String(50), index=True)
    params_json: Mapped[str]
    file_path: Mapped[str]
    width: Mapped[int]
    height: Mapped[int]
    gamma: Mapped[float]
    generation_time_ms: Mapped[float] = mapped_column(Float)


class FractalTagModel(Base):
    """Composite pattern: тег как часть коллекции фрактала."""
    __tablename__ = "fractal_tags"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    fractal_id: Mapped[str] = mapped_column(String(36), ForeignKey("fractals.id", ondelete="CASCADE"), index=True)
    tag: Mapped[str] = mapped_column(String(32), index=True)


def _migrate(engine) -> None:
    with engine.connect() as conn:
        cols = {row[1] for row in conn.execute(text("PRAGMA table_info(fractals)")).fetchall()}
        if cols and "user_id" not in cols:
            conn.execute(text("ALTER TABLE fractals ADD COLUMN user_id VARCHAR(36)"))
            conn.execute(text("ALTER TABLE fractals ADD COLUMN name VARCHAR(120) DEFAULT 'Fractal'"))
            conn.commit()


class SQLAlchemyUserRepository(IUserRepository):
    def __init__(self, database_url: str) -> None:
        self.engine = create_engine(database_url, future=True)
        self.session_factory = sessionmaker(self.engine, expire_on_commit=False, class_=Session)
        Base.metadata.create_all(self.engine)
        _migrate(self.engine)

    def save(self, user: User) -> User:
        with self.session_factory() as session:
            session.merge(
                UserModel(
                    id=str(user.id),
                    username=user.username,
                    email=user.email,
                    password_hash=user.password_hash,
                    created_at=user.created_at,
                )
            )
            session.commit()
        return user

    def get_by_id(self, user_id: UUID) -> User | None:
        with self.session_factory() as session:
            model = session.get(UserModel, str(user_id))
            return self._to_entity(model) if model else None

    def get_by_username(self, username: str) -> User | None:
        with self.session_factory() as session:
            model = session.scalar(select(UserModel).where(UserModel.username == username))
            return self._to_entity(model) if model else None

    @staticmethod
    def _to_entity(model: UserModel) -> User:
        return User(
            id=UUID(model.id),
            username=model.username,
            email=model.email,
            password_hash=model.password_hash,
            created_at=model.created_at,
        )


class SQLAlchemyFractalRepository(IFractalRepository):
    def __init__(self, database_url: str) -> None:
        self.engine = create_engine(database_url, future=True)
        self.session_factory = sessionmaker(self.engine, expire_on_commit=False, class_=Session)
        Base.metadata.create_all(self.engine)
        _migrate(self.engine)

    def save(self, fractal: Fractal) -> Fractal:
        with self.session_factory() as session:
            session.merge(
                FractalModel(
                    id=str(fractal.id),
                    user_id=str(fractal.user_id),
                    name=fractal.name,
                    created_at=fractal.created_at,
                    fractal_type=fractal.fractal_type,
                    params_json=json.dumps(fractal.params.to_dict()),
                    file_path=fractal.file_path,
                    width=fractal.metadata.width,
                    height=fractal.metadata.height,
                    gamma=fractal.metadata.gamma,
                    generation_time_ms=fractal.generation_time_ms,
                )
            )
            session.execute(
                delete(FractalTagModel).where(FractalTagModel.fractal_id == str(fractal.id))
            )
            for tag in (fractal.tags or ["basic"]):
                session.add(FractalTagModel(fractal_id=str(fractal.id), tag=tag))
            session.commit()
        return fractal

    def get_by_id(self, fractal_id: UUID, user_id: UUID) -> Fractal | None:
        with self.session_factory() as session:
            model = session.scalar(
                select(FractalModel).where(
                    FractalModel.id == str(fractal_id),
                    FractalModel.user_id == str(user_id),
                )
            )
            if not model:
                return None
            tags = self._load_tags(session, str(fractal_id))
            return self._to_entity(model, tags)

    def list_by_user(self, user_id: UUID) -> list[Fractal]:
        with self.session_factory() as session:
            rows = session.scalars(
                select(FractalModel)
                .where(FractalModel.user_id == str(user_id))
                .order_by(FractalModel.created_at.desc())
            ).all()
            result = []
            for r in rows:
                tags = self._load_tags(session, r.id)
                result.append(self._to_entity(r, tags))
            return result

    def update_name(self, fractal_id: UUID, user_id: UUID, name: str) -> Fractal | None:
        with self.session_factory() as session:
            model = session.scalar(
                select(FractalModel).where(
                    FractalModel.id == str(fractal_id),
                    FractalModel.user_id == str(user_id),
                )
            )
            if not model:
                return None
            model.name = name
            session.commit()
            session.refresh(model)
            tags = self._load_tags(session, str(fractal_id))
            return self._to_entity(model, tags)

    def update_tags(self, fractal_id: UUID, user_id: UUID, tags: list[str]) -> Fractal | None:
        """Обновляет теги фрактала (Repository pattern)."""
        with self.session_factory() as session:
            model = session.scalar(
                select(FractalModel).where(
                    FractalModel.id == str(fractal_id),
                    FractalModel.user_id == str(user_id),
                )
            )
            if not model:
                return None
            session.execute(
                delete(FractalTagModel).where(FractalTagModel.fractal_id == str(fractal_id))
            )
            for tag in tags:
                session.add(FractalTagModel(fractal_id=str(fractal_id), tag=tag))
            session.commit()
            return self._to_entity(model, tags)

    def list_user_tags(self, user_id: UUID) -> list[str]:
        """Возвращает все уникальные теги пользователя."""
        with self.session_factory() as session:
            fractal_ids = session.scalars(
                select(FractalModel.id).where(FractalModel.user_id == str(user_id))
            ).all()
            if not fractal_ids:
                return []
            rows = session.scalars(
                select(FractalTagModel.tag)
                .where(FractalTagModel.fractal_id.in_(fractal_ids))
                .distinct()
                .order_by(FractalTagModel.tag)
            ).all()
            return list(rows)

    def delete(self, fractal_id: UUID, user_id: UUID) -> bool:
        with self.session_factory() as session:
            model = session.scalar(
                select(FractalModel).where(
                    FractalModel.id == str(fractal_id),
                    FractalModel.user_id == str(user_id),
                )
            )
            if not model:
                return False
            session.delete(model)
            session.commit()
            return True

    @staticmethod
    def _load_tags(session: Session, fractal_id: str) -> list[str]:
        rows = session.scalars(
            select(FractalTagModel.tag).where(FractalTagModel.fractal_id == fractal_id)
        ).all()
        return list(rows) if rows else ["basic"]

    from sqlalchemy import func
    from src.domain.value_objects.user_stats import UserStats

    def get_user_stats(self, user_id: UUID) -> UserStats:
        user_id_str = str(user_id)

        with self.session_factory() as session:
            sample = session.scalar(
                select(FractalModel.user_id).where(FractalModel.user_id == user_id_str).limit(1)
            )
            print(f"[Repo] Stats debug: looking for user_id='{user_id_str}', found sample='{sample}'")

            # Агрегация: количество и среднее время
            result = session.execute(
                select(
                    func.count(FractalModel.id),
                    func.avg(FractalModel.generation_time_ms)
                ).where(FractalModel.user_id == user_id_str)
            ).first()

            total = result[0] if result and result[0] else 0
            avg_time = float(result[1]) if result and result[1] else 0.0

            if total == 0:
                return UserStats()

            fav_result = session.execute(
                select(
                    FractalModel.fractal_type,
                    func.count(FractalModel.id).label('cnt')
                )
                .where(FractalModel.user_id == user_id_str)
                .group_by(FractalModel.fractal_type)
                .order_by(func.count(FractalModel.id).desc())
            ).first()

            favorite_type = fav_result[0] if fav_result else None

            return UserStats(
                total_generated=total,
                favorite_type=favorite_type,
                avg_generation_time_ms=round(avg_time, 2),
                total_time_ms=round(avg_time * total, 2)
            )

    def _to_entity(self, model: FractalModel, tags: list[str] | None = None) -> Fractal:
        raw = json.loads(model.params_json)
        raw.setdefault("fractal_type", model.fractal_type)
        try:
            params = build_fractal_params(raw)
        except Exception:
            params = FractalParams(**{k: v for k, v in raw.items() if k in {"fractal_type", "width", "height", "max_iter", "gamma"}})
        metadata = ImageMetadata(width=model.width, height=model.height, gamma=model.gamma)
        return Fractal(
            id=UUID(model.id),
            user_id=UUID(model.user_id),
            name=model.name,
            created_at=model.created_at,
            fractal_type=model.fractal_type,
            params=params,
            metadata=metadata,
            file_path=model.file_path,
            generation_time_ms=model.generation_time_ms,
            tags=tags or ["basic"],
        )

    def list_all(self) -> list[Fractal]:
        with self.session_factory() as session:
            rows = session.scalars(select(FractalModel)).all()
            return [self._to_entity(r) for r in rows]

    def get_by_id_raw(self, fractal_id: UUID) -> Fractal | None:
        with self.session_factory() as session:
            model = session.get(FractalModel, str(fractal_id))
            if not model:
                return None
            tags = self._load_tags(session, str(fractal_id))
            return self._to_entity(model, tags)