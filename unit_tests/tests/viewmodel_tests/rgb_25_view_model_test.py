"""Unit test for rgb25 view model"""
# Disable the redefined-outer-name warning as
# it's normal to pass mocked object in tests function
# pylint: disable=redefined-outer-name,unused-argument,too-many-statements,protected-access
from __future__ import annotations

from unittest.mock import call
from unittest.mock import MagicMock
from unittest.mock import Mock
from unittest.mock import patch

import pytest

from src.model.enums.enums_model import AssetType
from src.model.enums.enums_model import TransferStatusEnumModel
from src.model.rgb_model import AssetBalanceResponseModel
from src.model.rgb_model import FailTransferResponseModel
from src.model.rgb_model import ListTransferAssetWithBalanceResponseModel
from src.model.rgb_model import SendAssetResponseModel
from src.utils.custom_exception import CommonException
from src.utils.error_message import ERROR_AUTHENTICATION_CANCELLED
from src.utils.error_message import ERROR_FAIL_TRANSFER
from src.utils.error_message import ERROR_SOMETHING_WENT_WRONG
from src.utils.info_message import INFO_ASSET_SENT
from src.utils.info_message import INFO_FAIL_TRANSFER_SUCCESSFULLY
from src.utils.info_message import INFO_REFRESH_SUCCESSFULLY
from src.utils.page_navigation import PageNavigation
from src.viewmodels.rgb_25_view_model import RGB25ViewModel
from unit_tests.factories.transfer_assets import make_transfer_asset


@pytest.fixture
def setup_navigation():
    """Fixture to set up and tear down PAGE_NAVIGATION."""
    mock_page_navigation = MagicMock(spec=PageNavigation)
    yield mock_page_navigation
    # Clean up after tests


@pytest.fixture
def rgb25_view_model(setup_navigation):
    """Fixture to create an instance of the RGB25ViewModel class."""
    return RGB25ViewModel(setup_navigation)


@pytest.fixture
def mock_asset_details_response():
    """Fixture to mock asset details response."""
    return ListTransferAssetWithBalanceResponseModel(
        transfers=[
            make_transfer_asset(
                idx=11,
                created_at=1718280342,
                updated_at=1718280342,
                created_at_date='2024-06-13',
                created_at_time='17:35:42',
                update_at_date='2024-06-13',
                updated_at_time='17:35:42',
                status='Settled',
                amount=69,
                amount_status='+69',
                kind='Issuance',
                transfer_Status=TransferStatusEnumModel.INTERNAL,
            ),
        ],
        asset_balance=AssetBalanceResponseModel(
            settled=69,
            future=69,
            spendable=69,
            offchain_outbound=0,
            offchain_inbound=0,
        ),
    )


@patch('src.data.service.asset_detail_page_services.AssetDetailPageService.get_asset_transactions')
def test_get_rgb25_asset_detail_success(mock_get_asset_transactions, rgb25_view_model, mock_asset_details_response):
    """Test for successfully retrieving RGB25 asset detail."""
    mock_txn_list_loaded_signal = Mock()
    mock_is_loading_signal = Mock()
    rgb25_view_model.txn_list_loaded.connect(mock_txn_list_loaded_signal)
    rgb25_view_model.is_loading.connect(mock_is_loading_signal)

    mock_get_asset_transactions.return_value = mock_asset_details_response

    asset_id = 'test_asset_id'
    asset_name = 'test_asset_name'
    image_path = 'test_image_path'
    asset_type = 'test_asset_type'

    rgb25_view_model.get_rgb25_asset_detail(
        asset_id, asset_name, image_path, asset_type,
    )
    rgb25_view_model.worker.result.emit(mock_asset_details_response)

    mock_txn_list_loaded_signal.assert_called_once_with(
        asset_id, asset_name, image_path, asset_type,
    )
    mock_is_loading_signal.assert_called_with(False)
    assert rgb25_view_model.asset_id == asset_id
    assert rgb25_view_model.asset_name == asset_name
    assert rgb25_view_model.image_path == image_path
    assert rgb25_view_model.asset_type == asset_type


@patch('src.utils.worker.ThreadManager.run_in_thread', autospec=True)
def test_on_send_click(mock_run_in_thread, rgb25_view_model):
    """Test the on_send_click method of RGB25ViewModel without executing the actual method."""
    # Setup test parameters
    amount = 100
    blinded_utxo = 'test_blinded_utxo'
    transport_endpoints = ['test_endpoint']
    fee_rate = 1.0
    min_confirmation = 1

    # Ensure asset_id is set before calling the method
    rgb25_view_model.asset_id = 'test_asset_id'

    # Mock the worker object
    mock_worker = MagicMock()
    rgb25_view_model.worker = mock_worker

    # Call the method
    rgb25_view_model.on_send_click(
        amount, blinded_utxo, transport_endpoints, fee_rate, min_confirmation,
    )

    # Verify the state changes
    assert rgb25_view_model.amount == amount
    assert rgb25_view_model.blinded_utxo == blinded_utxo
    assert rgb25_view_model.transport_endpoints == transport_endpoints
    assert rgb25_view_model.fee_rate == fee_rate
    assert rgb25_view_model.min_confirmation == min_confirmation


@patch('src.data.repository.rgb_repository.RgbRepository.fail_transfer')
@patch('src.views.components.toast.ToastManager.success')
@patch('src.views.components.toast.ToastManager.error')
def test_on_fail_transfer(mock_toast_error, mock_toast_success, mock_fail_transfer, rgb25_view_model):
    """Test for handling fail transfer operation."""
    # Mock necessary attributes and methods
    rgb25_view_model.is_loading = MagicMock()
    rgb25_view_model.get_rgb25_asset_detail = MagicMock()

    # Mock the repository method return value
    mock_fail_transfer.return_value = FailTransferResponseModel(
        transfers_changed=True,
    )

    # Mock run_in_thread to directly invoke the success callback
    def mock_run_in_thread(func, args):
        # Simulate the success callback being called
        args['callback'](mock_fail_transfer.return_value)

    rgb25_view_model.run_in_thread = MagicMock(side_effect=mock_run_in_thread)

    # Set up the asset ID
    rgb25_view_model.asset_id = 'test_asset_id'

    # Call the method
    batch_transfer_idx = 1
    rgb25_view_model.on_fail_transfer(batch_transfer_idx)

    # Verify the behavior
    rgb25_view_model.is_loading.emit.assert_called_with(
        True,
    )  # Loading state is set
    mock_toast_success.assert_called_once_with(
        description=INFO_FAIL_TRANSFER_SUCCESSFULLY,
    )  # Success toast is shown
    rgb25_view_model.get_rgb25_asset_detail.assert_called_once_with(
        rgb25_view_model.asset_id, rgb25_view_model.asset_name, None, rgb25_view_model.asset_type,
    )

    # Test when transfers_changed=False
    mock_fail_transfer.return_value.transfers_changed = False

    def mock_run_in_thread_fail(func, args):
        # Simulate the error callback being called
        args['callback'](mock_fail_transfer.return_value)

    rgb25_view_model.run_in_thread = MagicMock(
        side_effect=mock_run_in_thread_fail,
    )

    rgb25_view_model.on_fail_transfer(batch_transfer_idx)

    rgb25_view_model.is_loading.emit.assert_called_with(
        False,
    )  # Loading state is unset
    mock_toast_error.assert_called_once_with(
        description=ERROR_FAIL_TRANSFER,
    )  # Error toast is shown

    # Test for handling error while failing a transfer
    mock_exception = CommonException('Error sending asset')
    mock_fail_transfer.side_effect = mock_exception
    rgb25_view_model.run_in_thread = MagicMock(
        side_effect=lambda func, args: args['error_callback'](mock_exception),
    )

    rgb25_view_model.on_fail_transfer(batch_transfer_idx)

    rgb25_view_model.is_loading.emit.assert_called_with(
        False,
    )  # Loading state is unset
    mock_toast_error.assert_called_with(
        description='Something went wrong: Error sending asset',
    )

    # Test for handling generic exception while failing a transfer
    mock_fail_transfer.side_effect = Exception('Generic error')
    rgb25_view_model.run_in_thread = MagicMock(
        side_effect=lambda func, args: func(),
    )

    rgb25_view_model.on_fail_transfer(batch_transfer_idx)

    rgb25_view_model.is_loading.emit.assert_called_with(
        False,
    )  # Loading state is unset
    mock_toast_error.assert_called_with(
        description='Something went wrong: Generic error',
    )

# Test on_refresh_click functionality


@patch('src.viewmodels.rgb_25_view_model.Cache')
@patch('src.viewmodels.rgb_25_view_model.ToastManager')
@patch('src.viewmodels.rgb_25_view_model.RgbRepository')
def test_on_refresh_click(mock_rgb_repository, mock_toast_manager, mock_cache, rgb25_view_model):
    """Test the on_refresh_click method behavior."""
    # Set up mocks
    mock_cache_session = MagicMock()
    mock_cache.get_cache_session.return_value = mock_cache_session
    mock_toast_success = mock_toast_manager.success
    mock_toast_error = mock_toast_manager.error

    # Set up the view model
    rgb25_view_model.refresh = MagicMock()
    rgb25_view_model.is_loading = MagicMock()
    rgb25_view_model.send_rgb25_button_clicked = MagicMock()
    rgb25_view_model.get_rgb25_asset_detail = MagicMock()
    rgb25_view_model.asset_id = 'test_asset_id'
    rgb25_view_model.asset_name = 'test_asset'
    rgb25_view_model.asset_type = 'RGB25'

    # Test successful refresh
    def mock_run_in_thread(func, args):
        args['callback']()

    rgb25_view_model.run_in_thread = MagicMock(side_effect=mock_run_in_thread)

    # Call the method
    rgb25_view_model.on_refresh_click()

    # Verify behavior for successful case
    mock_cache_session.invalidate_cache.assert_called_once()
    rgb25_view_model.send_rgb25_button_clicked.emit.assert_called_once_with(
        True,
    )
    rgb25_view_model.is_loading.emit.assert_has_calls(
        [call(True), call(False)],
    )
    rgb25_view_model.refresh.emit.assert_called_once_with(True)
    mock_toast_success.assert_called_once_with(
        description=INFO_REFRESH_SUCCESSFULLY,
    )
    rgb25_view_model.get_rgb25_asset_detail.assert_called_once_with(
        rgb25_view_model.asset_id,
        rgb25_view_model.asset_name,
        None,
        rgb25_view_model.asset_type,
    )

    # Test error case with CommonException
    mock_exception = CommonException('Refresh error')
    rgb25_view_model.run_in_thread = MagicMock(
        side_effect=lambda func, args: args['error_callback'](mock_exception),
    )

    # Reset mocks
    rgb25_view_model.refresh.reset_mock()
    rgb25_view_model.is_loading.reset_mock()
    mock_toast_error.reset_mock()
    mock_cache_session.invalidate_cache.reset_mock()

    # Call the method
    rgb25_view_model.on_refresh_click()

    # Verify behavior for error case
    rgb25_view_model.refresh.emit.assert_called_once_with(False)
    rgb25_view_model.is_loading.emit.assert_has_calls(
        [call(True), call(False)],
    )
    mock_toast_error.assert_called_once_with(
        description=f'{ERROR_SOMETHING_WENT_WRONG}: {mock_exception}',
    )

    # Test generic exception case
    generic_exception = Exception('Generic error')
    rgb25_view_model.run_in_thread = MagicMock(side_effect=generic_exception)

    # Reset mocks
    rgb25_view_model.refresh.reset_mock()
    rgb25_view_model.is_loading.reset_mock()
    mock_toast_error.reset_mock()
    mock_cache_session.invalidate_cache.reset_mock()

    # Call the method
    rgb25_view_model.on_refresh_click()

    # Verify behavior for generic exception case
    rgb25_view_model.refresh.emit.assert_called_once_with(False)
    rgb25_view_model.is_loading.emit.assert_has_calls(
        [call(True), call(False)],
    )
    mock_toast_error.assert_called_once_with(
        description=f'{ERROR_SOMETHING_WENT_WRONG}: Generic error',
    )

    # Test when cache is None
    mock_cache.get_cache_session.return_value = None
    rgb25_view_model.run_in_thread = MagicMock(side_effect=mock_run_in_thread)

    # Reset mocks
    rgb25_view_model.refresh.reset_mock()
    rgb25_view_model.is_loading.reset_mock()
    mock_toast_success.reset_mock()
    mock_cache_session.invalidate_cache.reset_mock()

    # Call the method
    rgb25_view_model.on_refresh_click()

    # Verify behavior when cache is None
    # Should not be called when cache is None
    mock_cache_session.invalidate_cache.assert_not_called()
    rgb25_view_model.send_rgb25_button_clicked.emit.assert_called_with(True)
    rgb25_view_model.is_loading.emit.assert_has_calls(
        [call(True), call(False)],
    )
    rgb25_view_model.refresh.emit.assert_called_once_with(True)
    mock_toast_success.assert_called_once_with(
        description=INFO_REFRESH_SUCCESSFULLY,
    )


def test_on_success_send_rgb_asset(rgb25_view_model, mocker):
    """Test on_success_send_rgb_asset behavior"""
    rgb25_view_model.send_rgb25_button_clicked = MagicMock()
    rgb25_view_model.is_loading = MagicMock()
    rgb25_view_model.on_error = MagicMock()  # Mock on_error as MagicMock
    # Mock toast_error
    mock_toast_error = mocker.patch(
        'src.viewmodels.rgb_25_view_model.ToastManager.error',
    )

    # Test successful case
    rgb25_view_model.asset_id = 'test_asset_id'
    rgb25_view_model.amount = 100
    rgb25_view_model.blinded_utxo = 'test_blinded_utxo'
    rgb25_view_model.transport_endpoints = ['endpoint1', 'endpoint2']
    rgb25_view_model.fee_rate = 1.0
    rgb25_view_model.min_confirmation = 1
    rgb25_view_model.run_in_thread = MagicMock()

    # Call method with success=True
    rgb25_view_model.on_success_send_rgb_asset(True)

    # Verify behavior for success case
    rgb25_view_model.send_rgb25_button_clicked.emit.assert_called_once_with(
        True,
    )
    rgb25_view_model.is_loading.emit.assert_called_once_with(True)
    rgb25_view_model.run_in_thread.assert_called_once()

    # Verify run_in_thread arguments
    call_args = rgb25_view_model.run_in_thread.call_args[0][1]
    assert call_args['args'][0].asset_id == rgb25_view_model.asset_id
    assert call_args['args'][0].amount == rgb25_view_model.amount
    assert call_args['args'][0].recipient_id == rgb25_view_model.blinded_utxo
    assert call_args['args'][0].transport_endpoints == rgb25_view_model.transport_endpoints
    assert call_args['args'][0].fee_rate == rgb25_view_model.fee_rate
    assert call_args['args'][0].min_confirmations == rgb25_view_model.min_confirmation
    assert call_args['callback'] == rgb25_view_model.on_success_rgb25
    assert call_args['error_callback'] == rgb25_view_model.on_error

    # Test exception case
    mock_exception = Exception('Test error')
    rgb25_view_model.run_in_thread = MagicMock(side_effect=mock_exception)

    # Reset mocks
    rgb25_view_model.send_rgb25_button_clicked.reset_mock()
    rgb25_view_model.is_loading.reset_mock()
    rgb25_view_model.on_error.reset_mock()
    mock_toast_error.reset_mock()

    # Call method with success=True (will raise exception)
    rgb25_view_model.on_success_send_rgb_asset(True)

    # Verify behavior for exception case
    rgb25_view_model.send_rgb25_button_clicked.emit.assert_has_calls([
        call(True),
    ])
    rgb25_view_model.is_loading.emit.assert_has_calls([call(True)])
    rgb25_view_model.on_error.assert_called_once()
    assert isinstance(
        rgb25_view_model.on_error.call_args[0][0], CommonException,
    )
    assert str(mock_exception) in str(
        rgb25_view_model.on_error.call_args[0][0],
    )

    # Test authentication cancelled case
    # Reset mocks
    rgb25_view_model.send_rgb25_button_clicked.reset_mock()
    rgb25_view_model.is_loading.reset_mock()
    mock_toast_error.reset_mock()

    # Call method with success=False
    rgb25_view_model.on_success_send_rgb_asset(False)

    # Verify behavior for cancelled case
    rgb25_view_model.send_rgb25_button_clicked.emit.assert_not_called()
    rgb25_view_model.is_loading.emit.assert_not_called()
    mock_toast_error.assert_called_once_with(
        description=ERROR_AUTHENTICATION_CANCELLED,
    )


def test_on_error(rgb25_view_model, mocker):
    """Test the on_error method of RGB25ViewModel."""
    rgb25_view_model.is_loading = MagicMock()
    rgb25_view_model.send_rgb25_button_clicked = MagicMock()
    # Create test error
    mock_error = CommonException('Test error message')

    mock_toast_error = mocker.patch(
        'src.viewmodels.rgb_25_view_model.ToastManager.error',
    )

    # Reset mocks
    rgb25_view_model.is_loading.reset_mock()
    rgb25_view_model.send_rgb25_button_clicked.reset_mock()
    mock_toast_error.reset_mock()

    # Call on_error method
    rgb25_view_model.on_error(mock_error)

    # Verify behavior
    rgb25_view_model.is_loading.emit.assert_called_once_with(False)
    rgb25_view_model.send_rgb25_button_clicked.emit.assert_called_once_with(
        False,
    )
    mock_toast_error.assert_called_once_with(description=mock_error.message)


def test_on_success_rgb25(rgb25_view_model, mocker):
    """Test the on_success_rgb25 method of RGB25ViewModel."""
    # Setup mocks
    rgb25_view_model.is_loading = MagicMock()
    rgb25_view_model.send_rgb25_button_clicked = MagicMock()
    rgb25_view_model._page_navigation = MagicMock()
    mock_toast_success = mocker.patch(
        'src.viewmodels.rgb_25_view_model.ToastManager.success',
    )

    # Create test tx_id
    mock_tx_id = SendAssetResponseModel(txid='test_txid_123')

    # Test RGB25 asset type
    rgb25_view_model.asset_type = AssetType.RGB25.value
    rgb25_view_model.on_success_rgb25(mock_tx_id)

    # Verify behavior for RGB25
    rgb25_view_model.is_loading.emit.assert_called_once_with(False)
    rgb25_view_model.send_rgb25_button_clicked.emit.assert_called_once_with(
        False,
    )
    mock_toast_success.assert_called_once_with(
        description=INFO_ASSET_SENT.format(mock_tx_id.txid),
    )
    rgb25_view_model._page_navigation.collectibles_asset_page.assert_called_once()

    # Reset mocks
    rgb25_view_model.is_loading.reset_mock()
    rgb25_view_model.send_rgb25_button_clicked.reset_mock()
    rgb25_view_model._page_navigation.reset_mock()
    mock_toast_success.reset_mock()

    # Test RGB20 asset type
    rgb25_view_model.asset_type = AssetType.RGB20.value
    rgb25_view_model.on_success_rgb25(mock_tx_id)

    # Verify behavior for RGB20
    rgb25_view_model.is_loading.emit.assert_called_once_with(False)
    rgb25_view_model.send_rgb25_button_clicked.emit.assert_called_once_with(
        False,
    )
    mock_toast_success.assert_called_once_with(
        description=INFO_ASSET_SENT.format(mock_tx_id.txid),
    )
    rgb25_view_model._page_navigation.fungibles_asset_page.assert_called_once()
