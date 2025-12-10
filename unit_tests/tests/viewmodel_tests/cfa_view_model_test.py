"""Unit test for cfa view model"""
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
from src.model.enums.enums_model import AssignmentEnumModel
from src.model.enums.enums_model import TransferStatusEnumModel
from src.model.rgb_model import AssetBalanceResponseModel
from src.model.rgb_model import AssignmentModel
from src.model.rgb_model import FailTransferResponseModel
from src.model.rgb_model import ListTransferAssetWithBalanceResponseModel
from src.model.rgb_model import SendAssetResponseModel
from src.model.rgb_model import TransferAsset
from src.utils.custom_exception import CommonException
from src.utils.error_message import ERROR_AUTHENTICATION_CANCELLED
from src.utils.error_message import ERROR_FAIL_TRANSFER
from src.utils.error_message import ERROR_SOMETHING_WENT_WRONG
from src.utils.info_message import INFO_ASSET_SENT
from src.utils.info_message import INFO_FAIL_TRANSFER_SUCCESSFULLY
from src.utils.info_message import INFO_REFRESH_SUCCESSFULLY
from src.utils.page_navigation import PageNavigation
from src.viewmodels.cfa_view_model import CFAViewModel


@pytest.fixture
def setup_navigation():
    """Fixture to set up and tear down PAGE_NAVIGATION."""
    mock_page_navigation = MagicMock(spec=PageNavigation)
    yield mock_page_navigation
    # Clean up after tests


@pytest.fixture
def cfa_view_model(setup_navigation):
    """Fixture to create an instance of the CFAViewModel class."""
    return CFAViewModel(setup_navigation)


@pytest.fixture
def mock_asset_details_response():
    """Fixture to mock asset details response."""
    return ListTransferAssetWithBalanceResponseModel(
        transfers=[
            TransferAsset(
                idx=11,
                created_at=1718280342,
                updated_at=1718280342,
                created_at_date='2024-06-13',
                created_at_time='17:35:42',
                update_at_date='2024-06-13',
                updated_at_time='17:35:42',
                status='Settled',
                assignment=AssignmentModel(
                    type=AssignmentEnumModel.FUNGIBLE, value=69,
                ),
                requested_assignment=AssignmentModel(
                    type=AssignmentEnumModel.FUNGIBLE, value=69,
                ),
                amount_status='+69',
                kind='Issuance',
                transfer_Status=TransferStatusEnumModel.INTERNAL,
                txid=None,
                receive_utxo=None,
                change_utxo=None,
                recipient_id=None,
                expiration=None,
                transport_endpoints=[],
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
def test_get_cfa_asset_detail_success(mock_get_asset_transactions, cfa_view_model, mock_asset_details_response):
    """Test for successfully retrieving CFA asset detail."""
    mock_txn_list_loaded_signal = Mock()
    mock_is_loading_signal = Mock()
    cfa_view_model.txn_list_loaded.connect(mock_txn_list_loaded_signal)
    cfa_view_model.is_loading.connect(mock_is_loading_signal)

    mock_get_asset_transactions.return_value = mock_asset_details_response

    asset_id = 'test_asset_id'
    asset_name = 'test_asset_name'
    image_path = 'test_image_path'
    asset_type = 'test_asset_type'

    cfa_view_model.get_cfa_asset_detail(
        asset_id, asset_name, image_path, asset_type,
    )
    cfa_view_model.worker.result.emit(mock_asset_details_response)

    mock_txn_list_loaded_signal.assert_called_once_with(
        asset_id, asset_name, image_path, asset_type,
    )
    mock_is_loading_signal.assert_called_with(False)
    assert cfa_view_model.asset_id == asset_id
    assert cfa_view_model.asset_name == asset_name
    assert cfa_view_model.image_path == image_path
    assert cfa_view_model.asset_type == asset_type


@patch('src.utils.worker.ThreadManager.run_in_thread', autospec=True)
def test_on_send_click(mock_run_in_thread, cfa_view_model):
    """Test the on_send_click method of CFAViewModel without executing the actual method."""
    # Setup test parameters
    amount = 100
    blinded_utxo = 'test_blinded_utxo'
    transport_endpoints = ['test_endpoint']
    fee_rate = 1.0
    min_confirmation = 1

    # Ensure asset_id is set before calling the method
    cfa_view_model.asset_id = 'test_asset_id'

    # Mock the worker object
    mock_worker = MagicMock()
    cfa_view_model.worker = mock_worker

    # Call the method
    cfa_view_model.on_send_click(
        amount, blinded_utxo, transport_endpoints, fee_rate, min_confirmation,
    )

    # Verify the state changes
    assert cfa_view_model.amount == amount
    assert cfa_view_model.blinded_utxo == blinded_utxo
    assert cfa_view_model.transport_endpoints == transport_endpoints
    assert cfa_view_model.fee_rate == fee_rate
    assert cfa_view_model.min_confirmation == min_confirmation


@patch('src.data.repository.rgb_repository.RgbRepository.fail_transfer')
@patch('src.views.components.toast.ToastManager.success')
@patch('src.views.components.toast.ToastManager.error')
def test_on_fail_transfer(mock_toast_error, mock_toast_success, mock_fail_transfer, cfa_view_model):
    """Test for handling fail transfer operation."""
    # Mock necessary attributes and methods
    cfa_view_model.is_loading = MagicMock()
    cfa_view_model.get_cfa_asset_detail = MagicMock()

    # Mock the repository method return value
    mock_fail_transfer.return_value = FailTransferResponseModel(
        transfers_changed=True,
    )

    # Mock run_in_thread to directly invoke the success callback
    def mock_run_in_thread(func, args):
        # Simulate the success callback being called
        args['callback'](mock_fail_transfer.return_value)

    cfa_view_model.run_in_thread = MagicMock(side_effect=mock_run_in_thread)

    # Set up the asset ID
    cfa_view_model.asset_id = 'test_asset_id'

    # Call the method
    batch_transfer_idx = 1
    cfa_view_model.on_fail_transfer(batch_transfer_idx)

    # Verify the behavior
    cfa_view_model.is_loading.emit.assert_called_with(
        True,
    )  # Loading state is set
    mock_toast_success.assert_called_once_with(
        description=INFO_FAIL_TRANSFER_SUCCESSFULLY,
    )  # Success toast is shown
    cfa_view_model.get_cfa_asset_detail.assert_called_once_with(
        cfa_view_model.asset_id, cfa_view_model.asset_name, None, cfa_view_model.asset_type,
    )

    # Test when transfers_changed=False
    mock_fail_transfer.return_value.transfers_changed = False

    def mock_run_in_thread_fail(func, args):
        # Simulate the error callback being called
        args['callback'](mock_fail_transfer.return_value)

    cfa_view_model.run_in_thread = MagicMock(
        side_effect=mock_run_in_thread_fail,
    )

    cfa_view_model.on_fail_transfer(batch_transfer_idx)

    cfa_view_model.is_loading.emit.assert_called_with(
        False,
    )  # Loading state is unset
    mock_toast_error.assert_called_once_with(
        description=ERROR_FAIL_TRANSFER,
    )  # Error toast is shown

    # Test for handling error while failing a transfer
    mock_exception = CommonException('Error sending asset')
    mock_fail_transfer.side_effect = mock_exception
    cfa_view_model.run_in_thread = MagicMock(
        side_effect=lambda func, args: args['error_callback'](mock_exception),
    )

    cfa_view_model.on_fail_transfer(batch_transfer_idx)

    cfa_view_model.is_loading.emit.assert_called_with(
        False,
    )  # Loading state is unset
    mock_toast_error.assert_called_with(
        description='Something went wrong: Error sending asset',
    )

    # Test for handling generic exception while failing a transfer
    mock_fail_transfer.side_effect = Exception('Generic error')
    cfa_view_model.run_in_thread = MagicMock(
        side_effect=lambda func, args: func(),
    )

    cfa_view_model.on_fail_transfer(batch_transfer_idx)

    cfa_view_model.is_loading.emit.assert_called_with(
        False,
    )  # Loading state is unset
    mock_toast_error.assert_called_with(
        description='Something went wrong: Generic error',
    )

# Test on_refresh_click functionality


@patch('src.viewmodels.cfa_view_model.Cache')
@patch('src.viewmodels.cfa_view_model.ToastManager')
@patch('src.viewmodels.cfa_view_model.RgbRepository')
def test_on_refresh_click(mock_rgb_repository, mock_toast_manager, mock_cache, cfa_view_model):
    """Test the on_refresh_click method behavior."""
    # Set up mocks
    mock_cache_session = MagicMock()
    mock_cache.get_cache_session.return_value = mock_cache_session
    mock_toast_success = mock_toast_manager.success
    mock_toast_error = mock_toast_manager.error

    # Set up the view model
    cfa_view_model.refresh = MagicMock()
    cfa_view_model.is_loading = MagicMock()
    cfa_view_model.send_cfa_button_clicked = MagicMock()
    cfa_view_model.get_cfa_asset_detail = MagicMock()
    cfa_view_model.asset_id = 'test_asset_id'
    cfa_view_model.asset_name = 'test_asset'
    cfa_view_model.asset_type = 'CFA'

    # Test successful refresh
    def mock_run_in_thread(func, args):
        args['callback']()

    cfa_view_model.run_in_thread = MagicMock(side_effect=mock_run_in_thread)

    # Call the method
    cfa_view_model.on_refresh_click()

    # Verify behavior for successful case
    mock_cache_session.invalidate_cache.assert_called_once()
    cfa_view_model.send_cfa_button_clicked.emit.assert_called_once_with(
        True,
    )
    cfa_view_model.is_loading.emit.assert_has_calls(
        [call(True), call(False)],
    )
    cfa_view_model.refresh.emit.assert_called_once_with(True)
    mock_toast_success.assert_called_once_with(
        description=INFO_REFRESH_SUCCESSFULLY,
    )
    cfa_view_model.get_cfa_asset_detail.assert_called_once_with(
        cfa_view_model.asset_id,
        cfa_view_model.asset_name,
        None,
        cfa_view_model.asset_type,
    )

    # Test error case with CommonException
    mock_exception = CommonException('Refresh error')
    cfa_view_model.run_in_thread = MagicMock(
        side_effect=lambda func, args: args['error_callback'](mock_exception),
    )

    # Reset mocks
    cfa_view_model.refresh.reset_mock()
    cfa_view_model.is_loading.reset_mock()
    mock_toast_error.reset_mock()
    mock_cache_session.invalidate_cache.reset_mock()

    # Call the method
    cfa_view_model.on_refresh_click()

    # Verify behavior for error case
    cfa_view_model.refresh.emit.assert_called_once_with(False)
    cfa_view_model.is_loading.emit.assert_has_calls(
        [call(True), call(False)],
    )
    mock_toast_error.assert_called_once_with(
        description=f'{ERROR_SOMETHING_WENT_WRONG}: {mock_exception}',
    )

    # Test generic exception case
    generic_exception = Exception('Generic error')
    cfa_view_model.run_in_thread = MagicMock(side_effect=generic_exception)

    # Reset mocks
    cfa_view_model.refresh.reset_mock()
    cfa_view_model.is_loading.reset_mock()
    mock_toast_error.reset_mock()
    mock_cache_session.invalidate_cache.reset_mock()

    # Call the method
    cfa_view_model.on_refresh_click()

    # Verify behavior for generic exception case
    cfa_view_model.refresh.emit.assert_called_once_with(False)
    cfa_view_model.is_loading.emit.assert_has_calls(
        [call(True), call(False)],
    )
    mock_toast_error.assert_called_once_with(
        description=f'{ERROR_SOMETHING_WENT_WRONG}: Generic error',
    )

    # Test when cache is None
    mock_cache.get_cache_session.return_value = None
    cfa_view_model.run_in_thread = MagicMock(side_effect=mock_run_in_thread)

    # Reset mocks
    cfa_view_model.refresh.reset_mock()
    cfa_view_model.is_loading.reset_mock()
    mock_toast_success.reset_mock()
    mock_cache_session.invalidate_cache.reset_mock()

    # Call the method
    cfa_view_model.on_refresh_click()

    # Verify behavior when cache is None
    # Should not be called when cache is None
    mock_cache_session.invalidate_cache.assert_not_called()
    cfa_view_model.send_cfa_button_clicked.emit.assert_called_with(True)
    cfa_view_model.is_loading.emit.assert_has_calls(
        [call(True), call(False)],
    )
    cfa_view_model.refresh.emit.assert_called_once_with(True)
    mock_toast_success.assert_called_once_with(
        description=INFO_REFRESH_SUCCESSFULLY,
    )


def test_on_success_send_rgb_asset(cfa_view_model, mocker):
    """Test on_success_send_rgb_asset behavior"""
    cfa_view_model.send_cfa_button_clicked = MagicMock()
    cfa_view_model.is_loading = MagicMock()
    cfa_view_model.on_error = MagicMock()  # Mock on_error as MagicMock
    # Mock toast_error
    mock_toast_error = mocker.patch(
        'src.viewmodels.cfa_view_model.ToastManager.error',
    )

    # Test successful case
    cfa_view_model.asset_id = 'test_asset_id'
    cfa_view_model.amount = 100
    cfa_view_model.blinded_utxo = 'test_blinded_utxo'
    cfa_view_model.transport_endpoints = ['endpoint1', 'endpoint2']
    cfa_view_model.fee_rate = 1.0
    cfa_view_model.min_confirmation = 1
    cfa_view_model.run_in_thread = MagicMock()

    # Call method with success=True
    cfa_view_model.on_success_send_rgb_asset(True)

    # Verify behavior for success case
    cfa_view_model.send_cfa_button_clicked.emit.assert_called_once_with(
        True,
    )
    cfa_view_model.is_loading.emit.assert_called_once_with(True)
    cfa_view_model.run_in_thread.assert_called_once()

    # Verify run_in_thread arguments
    call_args = cfa_view_model.run_in_thread.call_args[0][1]
    assert call_args['args'][0].asset_id == cfa_view_model.asset_id
    assert call_args['args'][0].assignment.value == cfa_view_model.amount
    assert call_args['args'][0].recipient_id == cfa_view_model.blinded_utxo
    assert call_args['args'][0].transport_endpoints == cfa_view_model.transport_endpoints
    assert call_args['args'][0].fee_rate == cfa_view_model.fee_rate
    assert call_args['args'][0].min_confirmations == cfa_view_model.min_confirmation
    assert call_args['callback'] == cfa_view_model.on_success_cfa
    assert call_args['error_callback'] == cfa_view_model.on_error

    # Test exception case
    mock_exception = Exception('Test error')
    cfa_view_model.run_in_thread = MagicMock(side_effect=mock_exception)

    # Reset mocks
    cfa_view_model.send_cfa_button_clicked.reset_mock()
    cfa_view_model.is_loading.reset_mock()
    cfa_view_model.on_error.reset_mock()
    mock_toast_error.reset_mock()

    # Call method with success=True (will raise exception)
    cfa_view_model.on_success_send_rgb_asset(True)

    # Verify behavior for exception case
    cfa_view_model.send_cfa_button_clicked.emit.assert_has_calls([
        call(True),
    ])
    cfa_view_model.is_loading.emit.assert_has_calls([call(True)])
    cfa_view_model.on_error.assert_called_once()
    assert isinstance(
        cfa_view_model.on_error.call_args[0][0], CommonException,
    )
    assert str(mock_exception) in str(
        cfa_view_model.on_error.call_args[0][0],
    )

    # Test authentication cancelled case
    # Reset mocks
    cfa_view_model.send_cfa_button_clicked.reset_mock()
    cfa_view_model.is_loading.reset_mock()
    mock_toast_error.reset_mock()

    # Call method with success=False
    cfa_view_model.on_success_send_rgb_asset(False)

    # Verify behavior for cancelled case
    cfa_view_model.send_cfa_button_clicked.emit.assert_not_called()
    cfa_view_model.is_loading.emit.assert_not_called()
    mock_toast_error.assert_called_once_with(
        description=ERROR_AUTHENTICATION_CANCELLED,
    )


def test_on_error(cfa_view_model, mocker):
    """Test the on_error method of CFAViewModel."""
    cfa_view_model.is_loading = MagicMock()
    cfa_view_model.send_cfa_button_clicked = MagicMock()
    # Create test error
    mock_error = CommonException('Test error message')

    mock_toast_error = mocker.patch(
        'src.viewmodels.cfa_view_model.ToastManager.error',
    )

    # Reset mocks
    cfa_view_model.is_loading.reset_mock()
    cfa_view_model.send_cfa_button_clicked.reset_mock()
    mock_toast_error.reset_mock()

    # Call on_error method
    cfa_view_model.on_error(mock_error)

    # Verify behavior
    cfa_view_model.is_loading.emit.assert_called_once_with(False)
    cfa_view_model.send_cfa_button_clicked.emit.assert_called_once_with(
        False,
    )
    mock_toast_error.assert_called_once_with(description=mock_error.message)


def test_on_success_cfa(cfa_view_model, mocker):
    """Test the on_success_cfa method of CFAViewModel."""
    # Setup mocks
    cfa_view_model.is_loading = MagicMock()
    cfa_view_model.send_cfa_button_clicked = MagicMock()
    cfa_view_model._page_navigation = MagicMock()
    mock_toast_success = mocker.patch(
        'src.viewmodels.cfa_view_model.ToastManager.success',
    )

    # Create test tx_id
    mock_tx_id = SendAssetResponseModel(txid='test_txid_123')

    # Test CFA asset type
    cfa_view_model.asset_type = AssetType.CFA.value
    cfa_view_model.on_success_cfa(mock_tx_id)

    # Verify behavior for CFA
    cfa_view_model.is_loading.emit.assert_called_once_with(False)
    cfa_view_model.send_cfa_button_clicked.emit.assert_called_once_with(
        False,
    )
    mock_toast_success.assert_called_once_with(
        description=INFO_ASSET_SENT.format(mock_tx_id.txid),
    )
    cfa_view_model._page_navigation.collectibles_asset_page.assert_called_once()

    # Reset mocks
    cfa_view_model.is_loading.reset_mock()
    cfa_view_model.send_cfa_button_clicked.reset_mock()
    cfa_view_model._page_navigation.reset_mock()
    mock_toast_success.reset_mock()

    # Test NIA asset type
    cfa_view_model.asset_type = AssetType.NIA.value
    cfa_view_model.on_success_cfa(mock_tx_id)

    # Verify behavior for NIA
    cfa_view_model.is_loading.emit.assert_called_once_with(False)
    cfa_view_model.send_cfa_button_clicked.emit.assert_called_once_with(
        False,
    )
    mock_toast_success.assert_called_once_with(
        description=INFO_ASSET_SENT.format(mock_tx_id.txid),
    )
    cfa_view_model._page_navigation.fungibles_asset_page.assert_called_once()
