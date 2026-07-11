from app.core.config import Settings


def test_builds_database_url_from_db_parts():
    settings = Settings(
        _env_file=None,
        app_env="production",
        debug=False,
        db_host="db.railway.internal",
        db_port=3306,
        db_name="bodega_db",
        db_user="bodega_user",
        db_password="super-secret",
        secret_key="0123456789abcdef0123456789abcdef",
    )

    assert settings.database_url == "mysql+pymysql://bodega_user:super-secret@db.railway.internal:3306/bodega_db"


def test_rejects_insecure_secret_outside_development():
    try:
        Settings(
            _env_file=None,
            app_env="production",
            db_host="db.railway.internal",
            db_port=3306,
            db_name="bodega_db",
            db_user="bodega_user",
            db_password="super-secret",
            secret_key="change-this-secret-key",
        )
    except ValueError as exc:
        assert "SECRET_KEY" in str(exc)
    else:
        raise AssertionError("Expected production validation to reject insecure secret key")


def test_parses_cors_origins():
    settings = Settings(
        _env_file=None,
        app_env="production",
        db_host="db.railway.internal",
        db_port=3306,
        db_name="bodega_db",
        db_user="bodega_user",
        db_password="super-secret",
        secret_key="0123456789abcdef0123456789abcdef",
        frontend_url="https://bodega-frontend.vercel.app",
        allowed_cors_origins_raw="http://localhost:3000, https://admin.example.com",
    )

    assert settings.allowed_cors_origins == [
        "https://bodega-frontend.vercel.app",
        "http://localhost:3000",
        "https://admin.example.com",
    ]
