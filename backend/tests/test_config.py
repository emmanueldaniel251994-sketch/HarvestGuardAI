from app.config import Settings


def test_render_style_postgres_url_uses_psycopg_v3() -> None:
    settings = Settings(database_url="postgres://user:pass@host.example/db")
    assert settings.database_url == "postgresql+psycopg://user:pass@host.example/db"


def test_standard_postgresql_url_uses_psycopg_v3() -> None:
    settings = Settings(database_url="postgresql://user:pass@host.example/db")
    assert settings.database_url == "postgresql+psycopg://user:pass@host.example/db"


def test_sqlite_url_is_unchanged() -> None:
    settings = Settings(database_url="sqlite:///./test.db")
    assert settings.database_url == "sqlite:///./test.db"


def test_cors_origins_are_trimmed() -> None:
    settings = Settings(cors_origins="https://app.example, http://localhost:3000 ")
    assert settings.allowed_origins == [
        "https://app.example",
        "http://localhost:3000",
    ]
