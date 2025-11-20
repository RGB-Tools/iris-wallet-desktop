# pylint:disable=too-few-public-methods
# This class is intentionally designed as a data container (DTO / model).
# It stores structured data only and does not require additional public methods.
"""
Module containing models related to the success widget.
"""
from __future__ import annotations

from typing import Callable

from pydantic import BaseModel


class SuccessPageModel(BaseModel):
    """This model class used for success widget page"""
    header: str
    title: str
    description: str
    button_text: str
    callback: Callable
