"""This module contains the test fixtures for the bitcoin page helper."""
from __future__ import annotations

import pytest


@pytest.fixture
def mock_calculate_transaction_amount(mocker):
    """Mocked calculate_transaction_amount function"""
    def _mock_calculate_transaction_amount(value):
        return mocker.patch(
            'src.data.service.helpers.bitcoin_page_helper.calculate_transaction_amount',
            return_value=value,
        )

    return _mock_calculate_transaction_amount


@pytest.fixture
def mock_get_transaction_status(mocker):
    """Mocked get_transaction_status function"""
    def _mock_get_transaction_status(value):
        return mocker.patch(
            'src.data.service.helpers.bitcoin_page_helper.get_transaction_status',
            return_value=value,
        )

    return _mock_get_transaction_status
