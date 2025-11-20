# pylint:disable=too-few-public-methods
# This class is intentionally designed as a data container (DTO / model).
# It stores structured data only and does not require additional public methods.
"""This module contains the public node URL validator."""
from __future__ import annotations

import re

from PySide6.QtGui import QValidator


class NodeValidator(QValidator):
    """This class represents a node URL validator."""

    def validate(self, input_str, pos):
        """This method contains logic to check if the URL is valid or not."""
        pattern = re.compile(r'^[a-f0-9]{66}@[\w\.-]+:\d+$')

        if pattern.match(input_str):
            return QValidator.Acceptable, input_str, pos

        if input_str == '':
            return QValidator.Intermediate, input_str, pos

        return QValidator.Invalid, input_str, pos
