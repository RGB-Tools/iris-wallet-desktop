# pylint:disable=too-few-public-methods
# This class is intentionally designed as a data container (DTO / model).
# It stores structured data only and does not require additional public methods.
"""Module containing models related to invoices."""
from __future__ import annotations

from pydantic import BaseModel


# -------------------- Request models -----------------------


class DecodeLnInvoiceRequestModel(BaseModel):
    """Request model for decoding Lightning Network invoices."""

    invoice: str


class LnInvoiceRequestModel(BaseModel):
    """Request model for creating Lightning Network invoices."""

    amt_msat: int = 3000000
    expiry_sec: int = 420
    asset_id: str | None = None
    asset_amount: int | None = None


class InvoiceStatusRequestModel(DecodeLnInvoiceRequestModel):
    """Request model for checking the status of a Lightning Network invoice."""


# -------------------- Response models -----------------------

class DecodeInvoiceResponseModel(BaseModel):
    """Response model for decoding invoices api"""
    amt_msat: int
    expiry_sec: int
    timestamp: int
    asset_id: str | None
    asset_amount: int | None
    payment_hash: str
    payment_secret: str
    payee_pubkey: str
    network: str


class InvoiceStatusResponseModel(BaseModel):
    """Response model for invoice status api"""
    status: str


class LnInvoiceResponseModel(BaseModel):
    """Response model for ln invoice  api"""
    invoice: str
