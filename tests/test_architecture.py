import importlib

from app.services.payment_service import FakePaymentGateway, process_payment


def test_domain_services_infrastructure_are_importable():
    importlib.import_module("app.domain")
    importlib.import_module("app.services")
    importlib.import_module("app.infrastructure")


def test_process_payment_uses_structural_gateway():
    gateway = FakePaymentGateway()

    assert process_payment(gateway, 10.0) is True
    assert process_payment(gateway, 0.0) is False
