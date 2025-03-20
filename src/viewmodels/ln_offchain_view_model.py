"""This module contains the LnOffChainViewModel class, which represents the view model
for the terms and conditions page activities.
"""
from __future__ import annotations

from PySide6.QtCore import QObject
from PySide6.QtCore import Signal

from src.data.repository.invoices_repository import InvoiceRepository
from src.data.repository.payments_repository import PaymentRepository
from src.data.service.offchain_page_service import OffchainService
from src.model.enums.enums_model import PaymentStatus
from src.model.invoices_model import DecodeInvoiceResponseModel
from src.model.invoices_model import DecodeLnInvoiceRequestModel
from src.model.invoices_model import LnInvoiceRequestModel
from src.model.invoices_model import LnInvoiceResponseModel
from src.model.payments_model import CombinedDecodedModel
from src.model.payments_model import ListPaymentResponseModel
from src.utils.custom_exception import CommonException
from src.utils.error_message import ERROR_LN_OFF_CHAIN_UNABLE_TO_SEND_ASSET
from src.utils.error_message import ERROR_SOMETHING_WENT_WRONG
from src.utils.info_message import INFO_ASSET_SENT_SUCCESSFULLY
from src.utils.worker import ThreadManager
from src.views.components.toast import ToastManager


class LnOffChainViewModel(QObject, ThreadManager):
    """Represents the activities of the off-chain page."""

    invoice_get_event = Signal(str)
    payment_list_event = Signal(ListPaymentResponseModel)
    is_loading = Signal(bool)
    invoice_detail = Signal(DecodeInvoiceResponseModel)
    is_sent = Signal(bool)
    is_invoice_valid = Signal(bool)

    def __init__(self, page_navigation) -> None:
        """Initialize the LnOffChainViewModel."""
        super().__init__()
        self._page_navigation = page_navigation

    def _handle_error(self, error: Exception, emit_loading: bool = True, emit_invoice_valid: bool = False):
        """
        Centralized error handler to avoid repetitive code.

        Args:
            error (Exception): The raised exception.
            emit_loading (bool): Whether to emit loading status as False.
            emit_invoice_valid (bool): Whether to emit invoice validity as False.
        """
        if emit_loading:
            self.is_loading.emit(False)
        if emit_invoice_valid:
            self.is_invoice_valid.emit(False)

        description = error.message if isinstance(
            error, CommonException,
        ) else ERROR_SOMETHING_WENT_WRONG
        ToastManager.error(description=description)

    def get_invoice(self, expiry: int, asset_id=None, amount=None, amount_msat=None) -> None:
        """
        Retrieve an invoice for the specified asset and amount.

        Args:
            expiry (int): The expiry time for the invoice in seconds.
            asset_id (str): The ID of the asset (optional).
            amount (int): The asset amount (optional).
            amount_msat (int): The amount in milli-satoshis (optional).
        """
        self.is_loading.emit(True)
        self.run_in_thread(
            InvoiceRepository.ln_invoice,
            {
                'args': [LnInvoiceRequestModel(asset_id=asset_id, asset_amount=amount, expiry_sec=expiry, amt_msat=amount_msat)],
                'callback': self.on_success_get_invoice,
                'error_callback': self._handle_error,
            },
        )

    def on_success_get_invoice(self, encoded_invoice: LnInvoiceResponseModel) -> None:
        """Handle the successful retrieval of an invoice."""
        self.is_loading.emit(False)
        self.invoice_get_event.emit(encoded_invoice.invoice)

    def send_asset_offchain(self, ln_invoice: str) -> None:
        """
        Send an asset off-chain using the provided Lightning Network invoice.

        Args:
            ln_invoice (str): The Lightning Network invoice.
        """
        self.is_loading.emit(True)
        self.run_in_thread(
            OffchainService.send,
            {
                'args': [ln_invoice],
                'callback': self.on_success_send_asset,
                'error_callback': self._handle_error,
            },
        )

    def on_success_send_asset(self, response: CombinedDecodedModel) -> None:
        """
        Handle the successful sending of an asset off-chain.

        Args:
            response (CombinedDecodedModel): The response model containing the combined decoded data.
        """
        self.is_loading.emit(False)
        if response.send.status == PaymentStatus.FAILED.value:
            ToastManager.error(
                description=ERROR_LN_OFF_CHAIN_UNABLE_TO_SEND_ASSET,
            )
        else:
            ToastManager.success(description=INFO_ASSET_SENT_SUCCESSFULLY)
            self.is_sent.emit(True)

    def list_ln_payment(self) -> None:
        """List all Lightning Network payments."""
        self.is_loading.emit(True)
        self.run_in_thread(
            PaymentRepository.list_payment,
            {
                'args': [],
                'callback': self.on_success_of_list,
                'error_callback': self._handle_error,
            },
        )

    def on_success_of_list(self, payments: ListPaymentResponseModel) -> None:
        """Handle the successful retrieval of a list of payments."""
        self.is_loading.emit(False)
        self.payment_list_event.emit(payments)

    def decode_invoice(self, invoice: str) -> None:
        """Decode the Lightning Network invoice."""
        self.run_in_thread(
            InvoiceRepository.decode_ln_invoice,
            {
                'args': [DecodeLnInvoiceRequestModel(invoice=invoice)],
                'callback': self.on_success_decode_invoice,
                'error_callback': lambda exc: self._handle_error(exc, emit_invoice_valid=True),
            },
        )

    def on_success_decode_invoice(self, decoded_invoice: DecodeInvoiceResponseModel) -> None:
        """Handle the successful decode process of an invoice."""
        self.is_invoice_valid.emit(True)
        self.invoice_detail.emit(decoded_invoice)
