# pylint:disable=too-few-public-methods
# This class is intentionally designed as a data container (DTO / model).
# It stores structured data only and does not require additional public methods.
"""
This module provides the service for offchain page.
"""
from __future__ import annotations

from src.data.repository.invoices_repository import InvoiceRepository
from src.data.repository.payments_repository import PaymentRepository
from src.model.invoices_model import DecodeInvoiceResponseModel
from src.model.invoices_model import DecodeLnInvoiceRequestModel
from src.model.payments_model import CombinedDecodedModel
from src.model.payments_model import SendPaymentRequestModel
from src.model.payments_model import SendPaymentResponseModel
from src.utils.handle_exception import handle_exceptions


class OffchainService:
    """
    Service class offchain page
    """

    @staticmethod
    def send(encoded_invoice: str) -> CombinedDecodedModel:
        """
         Call decode and payment api and merge data of this two api
        """
        try:
            send_response: SendPaymentResponseModel = PaymentRepository.send_payment(
                SendPaymentRequestModel(invoice=encoded_invoice),
            )
            decode_data: DecodeInvoiceResponseModel = InvoiceRepository.decode_ln_invoice(
                DecodeLnInvoiceRequestModel(invoice=encoded_invoice),
            )
            return CombinedDecodedModel(send=send_response, decode=decode_data)
        except Exception as exc:
            return handle_exceptions(exc)
