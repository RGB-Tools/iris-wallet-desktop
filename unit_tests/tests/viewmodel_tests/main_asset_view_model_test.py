"""Unit test for main asset view model"""
# Disable the redefined-outer-name warning as
# it's normal to pass mocked object in tests function
# pylint: disable=redefined-outer-name,unused-argument
from __future__ import annotations

from unittest.mock import MagicMock
from unittest.mock import Mock
from unittest.mock import patch

import pytest

from src.model.btc_model import BalanceResponseModel
from src.model.btc_model import BalanceStatus
from src.model.common_operation_model import MainPageDataResponseModel
from src.model.common_operation_model import OfflineAsset
from src.model.rgb_model import AssetBalanceResponseModel
from src.model.rgb_model import AssetModel
from src.utils.custom_exception import CommonException
from src.viewmodels.main_asset_view_model import MainAssetViewModel


@pytest.fixture
def mock_btc_balance_response_with_positive():
    """Fixture for creating a mock for btc balance object with positive scenario."""
    return BalanceResponseModel(
        vanilla=BalanceStatus(settled=1000, future=500, spendable=150000000),
        colored=BalanceStatus(settled=2000, future=1000, spendable=30000000),
    )


@pytest.fixture
def mock_btc_balance_response_with_none():
    """Fixture for creating a mock for btc balance object with none scenario."""
    return BalanceResponseModel(
        vanilla=BalanceStatus(settled=0, future=0, spendable=0),
        colored=BalanceStatus(settled=0, future=0, spendable=0),
    )


@pytest.fixture
def mock_main_page_data_response():
    """Fixture for creating a mock for main page data object."""
    return MainPageDataResponseModel(
        nia=[
            AssetModel(
                asset_id='1',
                details=None,
                name='Asset1',
                issued_supply=1000,
                precision=2,
                timestamp=1620000000,
                added_at=1620001000,
                balance=AssetBalanceResponseModel(
                    settled=100, future=50, spendable=150, offchain_outbound=0, offchain_inbound=0,
                ),
            ),
            AssetModel(
                asset_id='2',
                details=None,
                name='Asset2',
                issued_supply=2000,
                precision=2,
                timestamp=1620002000,
                added_at=1620003000,
                balance=AssetBalanceResponseModel(
                    settled=200, future=100, spendable=300, offchain_outbound=0, offchain_inbound=0,
                ),
            ),
        ],
        uda=[
            AssetModel(
                asset_id='3',
                name='Asset3',
                details=None,
                precision=2,
                issued_supply=3000,
                timestamp=1620004000,
                added_at=1620005000,
                balance=AssetBalanceResponseModel(
                    settled=300, future=150, spendable=450, offchain_outbound=0, offchain_inbound=0,
                ),
            ),
            AssetModel(
                asset_id='4',
                name='Asset4',
                details=None,
                precision=2,
                issued_supply=4000,
                timestamp=1620006000,
                added_at=1620007000,
                balance=AssetBalanceResponseModel(
                    settled=400, future=200, spendable=600, offchain_outbound=0, offchain_inbound=0,
                ),
            ),
        ],
        cfa=[
            AssetModel(
                asset_id='5',
                name='Asset5',
                details=None,
                precision=2,
                issued_supply=5000,
                timestamp=1620008000,
                added_at=1620009000,
                balance=AssetBalanceResponseModel(
                    settled=500, future=250, spendable=750, offchain_outbound=0, offchain_inbound=0,
                ),
            ),
            AssetModel(
                asset_id='6',
                name='Asset6',
                details=None,
                precision=2,
                issued_supply=6000,
                timestamp=1620010000,
                added_at=1620011000,
                balance=AssetBalanceResponseModel(
                    settled=600, future=300, spendable=900, offchain_outbound=0, offchain_inbound=0,
                ),
            ),
        ],
        vanilla=OfflineAsset(
            asset_id='vanilla',
            ticker='VNL',
            balance=BalanceStatus(
                settled=1000, future=500, spendable=1500, offchain_outbound=0, offchain_inbound=0,
            ),
            name='Vanilla Asset',
        ),
    )


@pytest.fixture
def mock_page_navigation():
    """Fixture for creating a mock page navigation object."""
    return MagicMock()


@pytest.fixture
def main_asset_view_model(mock_page_navigation):
    """Fixture for creating an instance of main_asset_view_model with a mock page navigation object."""
    return MainAssetViewModel(mock_page_navigation)


@pytest.fixture
def mock_main_asset_page_data_service(mocker, mock_main_page_data_response):
    """Fixture for creating main asset page data service"""
    return mocker.patch(
        'src.data.service.main_asset_page_service.MainAssetPageDataService.get_assets',
        return_value=mock_main_page_data_response,
    )


@pytest.fixture
def mock_btc_repository(mocker, mock_btc_balance_response_with_positive):
    """Fixture for creating to get btc balance."""
    return mocker.patch(
        'src.data.repository.btc_repository.BtcRepository.get_btc_balance',
        return_value=mock_btc_balance_response_with_positive,
    )


def test_get_assets_success(
    main_asset_view_model,
    mock_main_asset_page_data_service,
    mock_main_page_data_response,
):
    """Test get asset with api success work as expected"""
    list_loaded_mock = Mock()
    main_asset_view_model.asset_loaded.connect(list_loaded_mock)
    mock_main_asset_page_data_service.return_value = mock_main_page_data_response
    main_asset_view_model.get_assets()
    main_asset_view_model.worker.result.emit(
        mock_main_page_data_response, True,
    )
    assert (
        main_asset_view_model.assets == mock_main_asset_page_data_service.return_value
    )

    # Check if the lists have been reversed
    assert main_asset_view_model.assets.nia == mock_main_page_data_response.nia
    assert main_asset_view_model.assets.uda == mock_main_page_data_response.uda
    assert main_asset_view_model.assets.cfa == mock_main_page_data_response.cfa
    list_loaded_mock.assert_called_once_with(True)


def test_get_assets_failure(
    main_asset_view_model,
):
    """Test get asset with api failure"""
    list_loaded_mock = Mock()
    main_asset_view_model.asset_loaded.connect(list_loaded_mock)
    main_asset_view_model.get_assets()

    # Simulate API failure
    main_asset_view_model.worker.error.emit(CommonException('API Error'))

    # Since the worker result is emitting an exception, the assets should be None
    assert main_asset_view_model.assets is None
    list_loaded_mock.assert_called_once_with(False)


def test_navigate_issue_nia_with_enough_balance(
    main_asset_view_model,
    mock_btc_repository,
    mock_btc_balance_response_with_positive,
    mock_page_navigation,
):
    """Test navigation to issue nia page with enough balance."""
    # Mock signals
    message_mock = Mock()
    main_asset_view_model.message.connect(message_mock)

    # Mock navigation
    mock_where = Mock()

    # Mock `run_in_thread` to simulate worker initialization
    main_asset_view_model.run_in_thread = Mock()

    # Simulate `run_in_thread` behavior: call the success callback with the positive balance response
    def mock_run_in_thread(func, kwargs):
        kwargs['callback'](mock_btc_balance_response_with_positive)

    main_asset_view_model.run_in_thread.side_effect = mock_run_in_thread

    # Call the method under test
    main_asset_view_model.navigate_issue_asset(mock_where)

    # Simulate successful balance check
    mock_where.assert_called_once()

    # Check that not_enough_balance signal was not emitted
    message_mock.assert_not_called()


@patch('src.data.repository.btc_repository.BtcRepository.get_address')
@patch('src.utils.cache.Cache.get_cache_session')
def test_get_assets_with_hard_refresh(mock_cache_session, mock_get_address, main_asset_view_model, mock_main_page_data_response):
    """Test for successfully retrieving assets with hard refresh."""

    # Mocking the cache and invalidation
    mock_cache = Mock()
    mock_cache.fetch_cache.return_value = (None, False)
    mock_cache_session.return_value = mock_cache

    # Mocking signals
    mock_asset_loaded_signal = Mock()
    main_asset_view_model.asset_loaded.connect(mock_asset_loaded_signal)

    # Mock worker behavior
    def mock_run_in_thread(func, kwargs):
        kwargs['callback'](mock_main_page_data_response)
    main_asset_view_model.run_in_thread = Mock(side_effect=mock_run_in_thread)

    # Call the method with hard refresh
    main_asset_view_model.get_assets(rgb_asset_hard_refresh=True)

    # Assert cache invalidation
    mock_cache.invalidate_cache.assert_called_once()

    # Assert asset loaded signal emitted correctly
    mock_asset_loaded_signal.assert_called_once_with(True)

    # Assert the assets were updated
    assert main_asset_view_model.assets == mock_main_page_data_response

    # Test error handling
    error_message = 'Error in fetching assets'
    mock_asset_loaded_signal.reset_mock()

    def mock_run_in_thread_error(func, kwargs):
        kwargs['error_callback'](CommonException(error_message))
    main_asset_view_model.run_in_thread = Mock(
        side_effect=mock_run_in_thread_error,
    )

    main_asset_view_model.get_assets(rgb_asset_hard_refresh=True)

    # Assert error handling
    mock_asset_loaded_signal.assert_called_once_with(False)
