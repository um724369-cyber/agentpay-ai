import uuid
from datetime import datetime

class PayPalClient:
    def __init__(self, client_id="sandbox_mock_id", secret="sandbox_mock_secret"):
        self.client_id = client_id
        self.secret = secret

    def create_order(self, amount: float, currency: str = "USD"):
        # Real PayPal REST API response format
        order_id = f"PAYID-{uuid.uuid4().hex[:12].upper()}"
        return {
            "id": order_id,
            "status": "CREATED",
            "amount": {"currency_code": currency, "value": f"{amount:.2f}"},
            "links": [
                {
                    "href": f"https://www.sandbox.paypal.com/checkoutnow?token={order_id}",
                    "rel": "approve",
                    "method": "GET"
                }
            ],
            "create_time": datetime.utcnow().isoformat() + "Z"
        }

    def capture_order(self, order_id: str):
        return {
            "id": order_id,
            "status": "COMPLETED",
            "payer": {"payer_id": f"PAYER-{uuid.uuid4().hex[:8].upper()}"},
            "capture_time": datetime.utcnow().isoformat() + "Z"
        }

# Quick Test
if __name__ == "__main__":
    client = PayPalClient()
    order = client.create_order(amount=45.00)
    print("Order Created:", order)
    capture = client.capture_order(order["id"])
    print("Payment Captured:", capture)