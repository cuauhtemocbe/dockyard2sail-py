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
