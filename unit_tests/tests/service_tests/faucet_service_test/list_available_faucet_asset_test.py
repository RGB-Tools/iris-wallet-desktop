"""Unit tests for list available faucet service"""
# Disable the redefined-outer-name warning as
# it's normal to pass mocked object in tests  function
# pylint: disable=redefined-outer-name,unused-import
# Some imports are used indirectly through fixtures, mocks, or decorators.
# They are required for PyTest discovery and execution but not referenced directly in the code.
from __future__ import annotations

import pytest

from src.data.service.faucet_service import FaucetService
from src.model.rgb_faucet_model import ListAvailableAsset
from src.utils.custom_exception import CommonException
from unit_tests.repository_fixture.faucet_repository_mocked import mocked_list_available_faucet_asset
from unit_tests.repository_fixture.setting_repository_mocked import mock_get_wallet_network
from unit_tests.service_test_resources.mocked_fun_return_values.faucet_service import mocked_asset_list
from unit_tests.service_test_resources.mocked_fun_return_values.faucet_service import mocked_asset_list_no_asset
from unit_tests.service_test_resources.mocked_fun_return_values.faucet_service import mocked_network
from unit_tests.service_test_resources.mocked_fun_return_values.faucet_service import mocked_response_of_list_asset_faucet


def test_list_asset(mocked_list_available_faucet_asset, mock_get_wallet_network):
    """Case 1 : when asset available"""
    mock_get_wallet_network(mocked_network)
    list_available_asset_obj = mocked_list_available_faucet_asset(
        mocked_asset_list,
    )
    result: ListAvailableAsset = FaucetService.list_available_asset()
    assert result == mocked_response_of_list_asset_faucet
    assert result.faucet_assets[0].asset_id == mocked_response_of_list_asset_faucet.faucet_assets[0].asset_id
    assert result.faucet_assets[0].asset_name == mocked_response_of_list_asset_faucet.faucet_assets[0].asset_name
    assert len(result.faucet_assets) == 2
    assert isinstance(result, ListAvailableAsset)
    list_available_asset_obj.assert_called_once()


def test_list_asset_when_no_asset(mocked_list_available_faucet_asset, mock_get_wallet_network):
    """Case 2 : when asset not available"""
    mock_get_wallet_network(mocked_network)
    list_available_asset_obj = mocked_list_available_faucet_asset(
        mocked_asset_list_no_asset,
    )
    result: ListAvailableAsset = FaucetService.list_available_asset()
    list_available_asset_obj.assert_called_once()
    assert result is None


def test_exception_while_list_asset(mock_get_wallet_network):
    """Case 3: when faucet service not available"""
    mock_get_wallet_network(mocked_network)
    with pytest.raises(CommonException, match='Connection failed'):
        FaucetService.list_available_asset()
