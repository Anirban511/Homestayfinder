"""Payment service with a stub/real toggle.

This mirrors the ML service pattern in the scalp-diagnostics project: a single
service object exposes one interface, and a config flag (PAYMENT_MODE) decides
whether it returns a deterministic stub result or calls the real provider.
This keeps the whole app runnable with zero external credentials.
"""
from app.config import settings


class PaymentService:
    def __init__(self) -> None:
        self.mode = settings.PAYMENT_MODE  # "stub" or "real"
        self._stripe = None
        if self.mode == "real" and settings.STRIPE_SECRET_KEY:
            import stripe
            stripe.api_key = settings.STRIPE_SECRET_KEY
            self._stripe = stripe

    def create_intent(self, amount: float, booking_id: int) -> dict:
        """Create a payment intent. Returns a provider reference + client secret."""
        cents = max(1, int(round(amount * 100)))
        if self.mode == "real" and self._stripe:
            intent = self._stripe.PaymentIntent.create(
                amount=cents, currency="usd",
                metadata={"booking_id": str(booking_id)},
            )
            return {"provider_ref": intent.id, "client_secret": intent.client_secret, "mode": "real"}
        # Stub: deterministic fake values, no network call, no charge.
        ref = f"stub_pi_{booking_id}"
        return {"provider_ref": ref, "client_secret": f"stub_secret_{booking_id}", "mode": "stub"}

    def confirm(self, provider_ref: str) -> bool:
        """Confirm a payment. The stub always succeeds; real mode would verify."""
        if self.mode == "real" and self._stripe:
            intent = self._stripe.PaymentIntent.retrieve(provider_ref)
            return intent.status == "succeeded"
        return True


payment_service = PaymentService()
