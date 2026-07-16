import pytest

def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "regression: pruebas críticas de regresión"
    )