import pytest
from pydantic import ValidationError

from app.config import Environment, Settings


def test_settings_load_from_environment_variables(monkeypatch):
    monkeypatch.setenv("ENVIRONMENT", "development")
    monkeypatch.setenv("PORT", "8000")

    settings = Settings()

    assert settings.environment == Environment.DEVELOPMENT
    assert settings.port == 8000


def test_settings_default_port(monkeypatch):
    monkeypatch.delenv("PORT", raising=False)

    settings = Settings()

    assert settings.port == 8000


def test_settings_invalid_port_raises_validation_error(monkeypatch):
    monkeypatch.setenv("PORT", "not-a-number")

    with pytest.raises(ValidationError):
        Settings()


@pytest.mark.parametrize(
    "value,should_succeed",
    [
        ("development", True),
        ("staging", True),
        ("production", True),
        ("qa", False),
    ],
)
def test_settings_environment_only_accepts_known_values(
    monkeypatch, value, should_succeed
):
    monkeypatch.setenv("ENVIRONMENT", value)

    if should_succeed:
        settings = Settings()
        assert settings.environment == value
    else:
        with pytest.raises(ValidationError):
            Settings()


def test_settings_cors_origins_default_to_empty(monkeypatch):
    monkeypatch.delenv("CORS_ALLOWED_ORIGINS", raising=False)

    settings = Settings()

    assert settings.cors_allowed_origins == []


def test_settings_cors_origins_parse_single_value(monkeypatch):
    monkeypatch.setenv("CORS_ALLOWED_ORIGINS", "https://app.example.com")

    settings = Settings()

    assert settings.cors_allowed_origins == ["https://app.example.com"]


def test_settings_cors_origins_parse_comma_separated_values(monkeypatch):
    monkeypatch.setenv(
        "CORS_ALLOWED_ORIGINS",
        "https://app.example.com,https://admin.example.com",
    )

    settings = Settings()

    assert settings.cors_allowed_origins == [
        "https://app.example.com",
        "https://admin.example.com",
    ]
