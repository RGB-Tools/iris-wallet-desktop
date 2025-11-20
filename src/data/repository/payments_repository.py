"""Module containing PaymentRepository."""
from __future__ import annotations

from src.model.payments_model import KeySendRequestModel
from src.model.payments_model import KeysendResponseModel
from src.model.payments_model import ListPaymentResponseModel
from src.model.payments_model import SendPaymentRequestModel
from src.model.payments_model import SendPaymentResponseModel
from src.utils.custom_context import repository_custom_context
from src.utils.decorators.unlock_required import unlock_required
from src.utils.endpoints import KEY_SEND_ENDPOINT
from src.utils.endpoints import LIST_PAYMENTS_ENDPOINT
from src.utils.endpoints import SEND_PAYMENT_ENDPOINT
from src.utils.helpers import process_response
from src.utils.request import Request


class PaymentRepository:
    """Repository for handling payments."""

    @staticmethod
    @unlock_required
    def key_send(key_send: KeySendRequestModel) -> KeysendResponseModel:
        """Send payment with a key."""
        payload = key_send.dict()
        with repository_custom_context():
            response = Request.post(KEY_SEND_ENDPOINT, payload)
            data = process_response(response, invalidate_cache=True)
            return KeysendResponseModel(**data)

    @staticmethod
    @unlock_required
    def send_payment(send_payment_detail: SendPaymentRequestModel) -> SendPaymentResponseModel:
        """Send a payment."""
        payload = send_payment_detail.dict()
        with repository_custom_context():
            response = Request.post(SEND_PAYMENT_ENDPOINT, payload)
            data = process_response(response, invalidate_cache=True)
            return SendPaymentResponseModel(**data)

    @staticmethod
    @unlock_required
    def list_payment() -> ListPaymentResponseModel:
        """List payments."""
        with repository_custom_context():
            response = Request.get(LIST_PAYMENTS_ENDPOINT)
            data = process_response(response)
            return ListPaymentResponseModel(**data)
