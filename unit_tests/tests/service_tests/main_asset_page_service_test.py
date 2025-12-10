"""Unit tests for main asset page service"""
# pylint: disable=redefined-outer-name,unused-argument,too-many-arguments,unused-import
from __future__ import annotations

from src.data.service.main_asset_page_service import MainAssetPageDataService
from src.model.common_operation_model import MainPageDataResponseModel
from src.model.enums.enums_model import FilterAssetEnumModel
from src.model.enums.enums_model import WalletType
from src.model.rgb_model import FilterAssetRequestModel
from src.model.rgb_model import RefreshTransferResponseModel
from src.model.setting_model import IsHideExhaustedAssetEnabled
from unit_tests.repository_fixture.btc_repository_mock import mock_get_btc_balance
from unit_tests.repository_fixture.rgb_repository_mock import mock_get_asset
from unit_tests.repository_fixture.rgb_repository_mock import mock_refresh_transfer
from unit_tests.repository_fixture.setting_repository_mocked import mock_get_wallet_type
from unit_tests.repository_fixture.setting_repository_mocked import mock_is_exhausted_asset_enabled
from unit_tests.service_test_resources.mocked_fun_return_values.main_asset_service import (
    mock_balance_response_data,
)
from unit_tests.service_test_resources.mocked_fun_return_values.main_asset_service import mock_cfa_asset_when_wallet_type_connect
from unit_tests.service_test_resources.mocked_fun_return_values.main_asset_service import mock_get_asset_response_model
from unit_tests.service_test_resources.mocked_fun_return_values.main_asset_service import mock_get_asset_response_model_when_exhausted_asset
from unit_tests.service_test_resources.service_fixture.main_asset_page_helper_mock import mock_convert_digest_to_hex
from unit_tests.service_test_resources.service_fixture.main_asset_page_helper_mock import mock_get_asset_name
from unit_tests.service_test_resources.service_fixture.main_asset_page_helper_mock import (
    mock_get_offline_asset_ticker,
)


def test_get_assets(
    mock_get_btc_balance,
    mock_get_asset,
    mock_get_offline_asset_ticker,
    mock_get_asset_name,
    mock_refresh_transfer,
    mock_get_wallet_type,
    mock_is_exhausted_asset_enabled,
):
    """Test case  for main asset page service when wallet type embedded"""

    # Taking mocked object to check if the method is called once
    # Passing data for the return value of the mocked function
    get_btc_balance = mock_get_btc_balance(mock_balance_response_data)
    refresh_asset = mock_refresh_transfer(
        RefreshTransferResponseModel(status=True),
    )
    get_asset = mock_get_asset(mock_get_asset_response_model)
    asset_name = mock_get_asset_name('rBitcoin')
    asset_ticker = mock_get_offline_asset_ticker('rBTC')
    is_exhausted_asset_enabled = mock_is_exhausted_asset_enabled(
        IsHideExhaustedAssetEnabled(is_enabled=False),
    )
    wallet_type = mock_get_wallet_type(WalletType.EMBEDDED_TYPE_WALLET)
    # Execute the function under test
    result = MainAssetPageDataService.get_assets()

    # Assert results
    assert result.nia == mock_get_asset_response_model.nia
    assert result.cfa == mock_get_asset_response_model.cfa
    assert result.uda == mock_get_asset_response_model.uda
    assert result.vanilla.ticker == 'rBTC'
    assert result.vanilla.name == 'rBitcoin'
    assert result.vanilla.balance.settled == mock_balance_response_data.vanilla.settled
    assert (
        result.vanilla.balance.spendable == mock_balance_response_data.vanilla.spendable
    )
    assert result.vanilla.balance.future == mock_balance_response_data.vanilla.future
    assert isinstance(result.vanilla.balance.settled, int)
    assert isinstance(result.vanilla.balance.spendable, int)
    assert isinstance(result.vanilla.balance.future, int)
    assert isinstance(result, MainPageDataResponseModel)

    # checking the method is called once
    get_asset.assert_called_once_with(
        FilterAssetRequestModel(
            filter_asset_schemas=[
                FilterAssetEnumModel.NIA,
                FilterAssetEnumModel.CFA,
                FilterAssetEnumModel.UDA,
            ],
        ),
    )
    refresh_asset.assert_called_once()
    asset_name.assert_called_once()
    asset_ticker.assert_called_once()
    get_btc_balance.assert_called_once()
    wallet_type.assert_called_once()
    is_exhausted_asset_enabled.assert_called_once()


def test_get_asset_when_wallet_type_connect(
    mock_get_btc_balance,
    mock_get_asset,
    mock_get_offline_asset_ticker,
    mock_get_asset_name,
    mock_refresh_transfer,
    mock_get_wallet_type,
    mock_convert_digest_to_hex,
    mock_is_exhausted_asset_enabled,
):
    """Test case  for main asset page service when wallet type connect"""
    wallet_type = mock_get_wallet_type(WalletType.REMOTE_TYPE_WALLET)
    get_btc_balance = mock_get_btc_balance(mock_balance_response_data)
    refresh_asset = mock_refresh_transfer(
        RefreshTransferResponseModel(status=True),
    )
    asset_name = mock_get_asset_name('rBitcoin')
    asset_ticker = mock_get_offline_asset_ticker('rBTC')
    get_asset = mock_get_asset(mock_get_asset_response_model)
    convert_digest_to_hex = mock_convert_digest_to_hex(
        mock_cfa_asset_when_wallet_type_connect,
    )
    is_exhausted_asset_enabled = mock_is_exhausted_asset_enabled(
        IsHideExhaustedAssetEnabled(is_enabled=False),
    )
    result = MainAssetPageDataService.get_assets()
    assert result.cfa[0].media.hex == mock_cfa_asset_when_wallet_type_connect.media.hex
    get_asset.assert_called_once_with(
        FilterAssetRequestModel(
            filter_asset_schemas=[
                FilterAssetEnumModel.NIA,
                FilterAssetEnumModel.CFA,
                FilterAssetEnumModel.UDA,
            ],
        ),
    )
    refresh_asset.assert_called_once()
    asset_name.assert_called_once()
    asset_ticker.assert_called_once()
    get_btc_balance.assert_called_once()
    wallet_type.assert_called_once()
    convert_digest_to_hex.assert_called_once()
    is_exhausted_asset_enabled.assert_called_once()


def test_when_asset_exhausted(
    mock_get_btc_balance,
    mock_get_asset,
    mock_get_offline_asset_ticker,
    mock_get_asset_name,
    mock_refresh_transfer,
    mock_get_wallet_type,
    mock_is_exhausted_asset_enabled,
):
    """Test case  for main asset page service when asset_exhausted"""
    wallet_type = mock_get_wallet_type(WalletType.EMBEDDED_TYPE_WALLET)
    get_btc_balance = mock_get_btc_balance(mock_balance_response_data)
    refresh_asset = mock_refresh_transfer(
        RefreshTransferResponseModel(status=True),
    )
    asset_name = mock_get_asset_name('rBitcoin')
    asset_ticker = mock_get_offline_asset_ticker('rBTC')
    get_asset = mock_get_asset(
        mock_get_asset_response_model_when_exhausted_asset,
    )
    is_exhausted_asset_enabled = mock_is_exhausted_asset_enabled(
        IsHideExhaustedAssetEnabled(is_enabled=True),
    )
    result = MainAssetPageDataService.get_assets()
    assert len(result.cfa) == 1
    assert len(result.uda) == 1
    assert len(result.nia) == 1
    get_asset.assert_called_once_with(
        FilterAssetRequestModel(
            filter_asset_schemas=[
                FilterAssetEnumModel.NIA,
                FilterAssetEnumModel.CFA,
                FilterAssetEnumModel.UDA,
            ],
        ),
    )
    refresh_asset.assert_called_once()
    asset_name.assert_called_once()
    asset_ticker.assert_called_once()
    get_btc_balance.assert_called_once()
    wallet_type.assert_called_once()
    is_exhausted_asset_enabled.assert_called_once()
