"""Mocked external(helper function) function used in common operation service"""
from __future__ import annotations

import pytest


@pytest.fixture
def mock_set_value_keyring_helper(mocker):
    """Mocked set value helper function of keyring"""
    def _mock_set_value_keyring_helper(value):
        return mocker.patch(
            'src.data.service.common_operation_service.set_value',
            return_value=value,
        )

    return _mock_set_value_keyring_helper


@pytest.fixture
def mock_is_node_locked(mocker):
    """Mocked set value helper function of keyring"""
    def _mock_is_node_locked(value):
        return mocker.patch(
            'src.data.service.common_operation_service.check_node',
            return_value=value,
        )

    return _mock_is_node_locked
