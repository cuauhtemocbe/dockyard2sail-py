from app.domain.ports import PaymentGateway


class FakePaymentGateway:
    def charge(self, amount: float) -> bool:
        return amount > 0


def process_payment(gateway: PaymentGateway, amount: float) -> bool:
    return gateway.charge(amount)
