"""Unit tests for keyring toggle validate method in common operation service"""
# Disable the redefined-outer-name warning as
# it's normal to pass mocked object in tests  function
# pylint: disable=redefined-outer-name,unused-import
# Some imports are used indirectly through fixtures, mocks, or decorators.
# They are required for PyTest discovery and execution but not referenced directly in the code.
from __future__ import annotations

import pytest

from src.data.repository.setting_repository import SettingRepository
from src.data.service.common_operation_service import CommonOperationService
from src.utils.custom_exception import CommonException
from src.utils.error_message import ERROR_KEYRING_STORE_NOT_ACCESSIBLE
from unit_tests.repository_fixture.setting_repository_mocked import mock_get_wallet_network
from unit_tests.service_test_resources.mocked_fun_return_values.common_operation_service import mocked_data_init_api_response
from unit_tests.service_test_resources.mocked_fun_return_values.common_operation_service import mocked_password
from unit_tests.service_test_resources.mocked_fun_return_values.faucet_service import mocked_network
from unit_tests.service_test_resources.service_fixture.common_operation_service_mock import mock_set_value_keyring_helper


def test_when_keyring_accessible(mock_get_wallet_network, mock_set_value_keyring_helper):
    """Case 1 : When value store in keyring successfully"""
    get_network_obj = mock_get_wallet_network(mocked_network)
    mock_set_value_keyring_helper(True)
    CommonOperationService.keyring_toggle_enable_validation(
        mnemonic=mocked_data_init_api_response.mnemonic, password=mocked_password,
    )
    keyring_status: bool = SettingRepository.get_keyring_status()
    assert keyring_status is False
    get_network_obj.assert_called_once()


def test_when_keyring_not_accessible(mock_get_wallet_network, mock_set_value_keyring_helper):
    """Case 1 : When value not store in keyring successfully"""
    get_network_obj = mock_get_wallet_network(mocked_network)
    mock_set_value_keyring_helper(False)
    with pytest.raises(CommonException, match=ERROR_KEYRING_STORE_NOT_ACCESSIBLE):
        CommonOperationService.keyring_toggle_enable_validation(
            mnemonic=mocked_data_init_api_response.mnemonic, password=mocked_password,
        )
    get_network_obj.assert_called_once()
