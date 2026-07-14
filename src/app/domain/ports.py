from typing import Protocol


class PaymentGateway(Protocol):
    def charge(self, amount: float) -> bool: ...
