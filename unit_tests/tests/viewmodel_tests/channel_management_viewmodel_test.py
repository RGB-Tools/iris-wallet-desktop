"""Tests for the ChannelManagementViewModel class."""
# pylint: disable=redefined-outer-name,unused-argument,protected-access
from __future__ import annotations

from unittest.mock import call
from unittest.mock import MagicMock

import pytest

from src.model.channels_model import Channel
from src.model.channels_model import ChannelsListResponseModel
from src.model.channels_model import CloseChannelResponseModel
from src.model.channels_model import HandleInsufficientAllocationSlotsModel
from src.model.channels_model import OpenChannelResponseModel
from src.model.enums.enums_model import ChannelFetchingModel
from src.model.rgb_model import AssetBalanceResponseModel
from src.model.rgb_model import AssetModel
from src.model.rgb_model import GetAssetResponseModel
from src.utils.custom_exception import CommonException
from src.utils.error_message import ERROR_CREATE_UTXO
from src.utils.error_message import ERROR_INSUFFICIENT_ASSET
from src.utils.error_message import ERROR_INVALID_PUBKEY_TYPE
from src.utils.error_message import ERROR_NO_UNCOLORED_UTXOS_AVAILABLE
from src.utils.error_message import ERROR_SOMETHING_WENT_WRONG
from src.utils.info_message import INFO_CHANNEL_DELETED
from src.viewmodels.channel_management_viewmodel import ChannelManagementViewModel


@pytest.fixture
def channel_view_model():
    """Fixture that creates a ChannelManagementViewModel instance with mocked page navigation."""
    page_navigation = MagicMock()
    return ChannelManagementViewModel(page_navigation)


def test_update_loading_increment(channel_view_model):
    """Test update_loading when incrementing."""
    # Arrange
    channel_view_model.loading_started = MagicMock()
    channel_view_model.loading_finished = MagicMock()
    channel_view_model.loading_tasks = 0

    # Act
    channel_view_model.update_loading(True)

    # Assert
    assert channel_view_model.loading_tasks == 1
    channel_view_model.loading_started.emit.assert_called_once_with(True)
    channel_view_model.loading_finished.emit.assert_not_called()


def test_update_loading_decrement(channel_view_model):
    """Test update_loading when decrementing."""
    # Arrange
    channel_view_model.loading_started = MagicMock()
    channel_view_model.loading_finished = MagicMock()
    channel_view_model.loading_tasks = 1

    # Act
    channel_view_model.update_loading(False)

    # Assert
    assert channel_view_model.loading_tasks == 0
    channel_view_model.loading_started.emit.assert_not_called()
    channel_view_model.loading_finished.emit.assert_called_once_with(True)


def test_available_channels_success(channel_view_model):
    """Test available_channels method with successful response."""
    # Arrange
    channel_view_model.is_channel_fetching = MagicMock()
    channel_view_model.update_loading = MagicMock()
    channel_view_model.check_loading_completion = MagicMock()
    channel_view_model.channel_loaded = MagicMock()
    channel_view_model.run_in_thread = MagicMock()

    mock_channel = Channel(
        channel_id='123',
        capacity=1000,
        local_balance=500,
        remote_balance=500,
        channel_point='point',
        remote_pubkey='pubkey',
        status='active',
        funding_txid='txid',
        peer_pubkey='peer_pubkey',
        peer_alias='peer_alias',
        ready=True,
        capacity_sat=1000,
        local_balance_sat=500000,
        is_usable=True,
        public=True,
    )
    mock_response = ChannelsListResponseModel(channels=[mock_channel])

    # Act
    channel_view_model.available_channels()

    # Get the success callback from run_in_thread call
    run_thread_kwargs = channel_view_model.run_in_thread.call_args[0][1]
    success = run_thread_kwargs['callback']

    # Simulate successful response
    success(mock_response)

    # Assert
    channel_view_model.is_channel_fetching.emit.assert_has_calls([
        call(True, ChannelFetchingModel.FETCHING.value),
        call(False, ChannelFetchingModel.FETCHED.value),
    ])
    channel_view_model.update_loading.assert_has_calls(
        [call(True), call(False)],
    )
    assert channel_view_model.channels == [mock_channel]
    assert channel_view_model.channels_loaded is True
    channel_view_model.check_loading_completion.assert_called_once()
    channel_view_model.channel_loaded.emit.assert_called_once()


def test_close_channel_success(channel_view_model, mocker):
    """Test close_channel method with successful response."""
    # Arrange
    channel_view_model.loading_started = MagicMock()
    channel_view_model.loading_finished = MagicMock()
    channel_view_model.channel_deleted = MagicMock()
    mock_toast_manager = mocker.patch(
        'src.views.components.toast.ToastManager.success',
    )
    channel_view_model.run_in_thread = MagicMock()
    mock_response = CloseChannelResponseModel(status=True)
    test_pub_key = 'test_pub_key'

    # Act
    channel_view_model.close_channel('channel_id', test_pub_key)

    # Get the success callback from run_in_thread call
    run_thread_kwargs = channel_view_model.run_in_thread.call_args[0][1]
    success = run_thread_kwargs['callback']

    # Simulate successful response
    success(mock_response)

    # Assert
    channel_view_model.loading_started.emit.assert_called_once_with(True)
    channel_view_model.loading_finished.emit.assert_called_once_with(True)
    channel_view_model.channel_deleted.emit.assert_called_once_with(True)
    mock_toast_manager.assert_called_once_with(
        description=INFO_CHANNEL_DELETED.format(test_pub_key),
    )
    channel_view_model._page_navigation.channel_management_page.assert_called_once()


def test_create_channel_with_btc_success(channel_view_model):
    """Test create_channel_with_btc method with successful response."""
    # Arrange
    channel_view_model.is_loading = MagicMock()
    channel_view_model.channel_created = MagicMock()
    channel_view_model.run_in_thread = MagicMock()
    mock_response = OpenChannelResponseModel(temporary_channel_id='temp_id')

    # Act
    channel_view_model.create_channel_with_btc('pub_key', '30000', '1000')

    # Get the success callback from run_in_thread call
    run_thread_kwargs = channel_view_model.run_in_thread.call_args[0][1]
    success = run_thread_kwargs['callback']

    # Simulate successful response
    success(mock_response)

    # Assert
    channel_view_model.is_loading.emit.assert_has_calls(
        [call(True), call(False)],
    )
    channel_view_model.channel_created.emit.assert_called_once()


def test_create_channel_with_btc_error(channel_view_model, mocker):
    """Test create_channel_with_btc method with error response."""
    # Arrange
    channel_view_model.is_loading = MagicMock()
    mock_toast_manager = mocker.patch(
        'src.views.components.toast.ToastManager.error',
    )
    channel_view_model.run_in_thread = MagicMock()
    error_message = 'Failed to create channel'
    mock_error = CommonException(error_message)

    # Act
    channel_view_model.create_channel_with_btc('pub_key', '30000', '1000')

    # Get the error callback from run_in_thread call
    run_thread_kwargs = channel_view_model.run_in_thread.call_args[0][1]
    on_error = run_thread_kwargs['error_callback']

    # Simulate error
    on_error(mock_error)

    # Assert
    channel_view_model.is_loading.emit.assert_has_calls(
        [call(True), call(False)],
    )
    mock_toast_manager.assert_called_once_with(description=error_message)


def test_create_channel_with_btc_generic_exception(channel_view_model, mocker):
    """Test create_channel_with_btc method with generic exception."""
    # Arrange
    channel_view_model.is_loading = MagicMock()
    mock_toast_manager = mocker.patch(
        'src.views.components.toast.ToastManager.error',
    )
    channel_view_model.run_in_thread = MagicMock(side_effect=Exception())

    # Act
    channel_view_model.create_channel_with_btc('pub_key', '30000', '1000')

    # Assert
    channel_view_model.is_loading.emit.assert_has_calls(
        [call(True), call(False)],
    )
    mock_toast_manager.assert_called_once_with(
        description=ERROR_SOMETHING_WENT_WRONG,
    )


def test_check_loading_completion_both_loaded(channel_view_model):
    """Test check_loading_completion when both assets and channels are loaded."""
    # Arrange
    channel_view_model.list_loaded = MagicMock()
    channel_view_model.assets_loaded = True
    channel_view_model.channels_loaded = True

    # Act
    channel_view_model.check_loading_completion()

    # Assert
    channel_view_model.list_loaded.emit.assert_called_once_with(True)


def test_check_loading_completion_not_both_loaded(channel_view_model):
    """Test check_loading_completion when either assets or channels are not loaded."""
    # Arrange
    channel_view_model.list_loaded = MagicMock()
    channel_view_model.assets_loaded = True
    channel_view_model.channels_loaded = False

    # Act
    channel_view_model.check_loading_completion()

    # Assert
    channel_view_model.list_loaded.emit.assert_not_called()


def test_get_asset_name(channel_view_model):
    """Test get_asset_name method."""
    # Arrange
    mock_nia_asset = AssetModel(
        asset_id='1',
        name='NIA Asset',
        details=None,
        precision=2,
        issued_supply=4000,
        timestamp=1620700000,
        added_at=1620009000,
        balance=AssetBalanceResponseModel(
            settled=100, future=50, spendable=150, offchain_outbound=0, offchain_inbound=0,
        ),
    )
    mock_cfa_asset = AssetModel(
        asset_id='2',
        name='CFA Asset',
        details=None,
        precision=2,
        issued_supply=1000,
        timestamp=1620008000,
        added_at=1620007000,
        balance=AssetBalanceResponseModel(
            settled=200, future=100, spendable=300, offchain_outbound=0, offchain_inbound=0,
        ),
    )
    channel_view_model.nia_asset = [mock_nia_asset]
    channel_view_model.cfa_asset = [mock_cfa_asset]

    # Act
    result = channel_view_model.get_asset_name()

    # Assert
    expected = {
        '1': 'NIA Asset',
        '2': 'CFA Asset',
    }
    assert result == expected
    assert channel_view_model.total_asset_lookup_list == expected


def test_get_asset_list_success_with_both_assets(channel_view_model, mocker):
    """Test get_asset_list method with both NIA and CFA assets."""
    # Arrange
    channel_view_model.update_loading = MagicMock()
    channel_view_model.asset_loaded_signal = MagicMock()
    channel_view_model.get_asset_name = MagicMock(
        return_value={'1': 'Asset1', '2': 'Asset2'},
    )
    channel_view_model.check_loading_completion = MagicMock()
    channel_view_model.run_in_thread = MagicMock()

    mock_nia_asset = AssetModel(
        asset_id='1',
        name='Asset1',
        details=None,
        precision=2,
        issued_supply=1000,
        timestamp=1620600000,
        added_at=1620001000,
        balance=AssetBalanceResponseModel(
            settled=100, future=50, spendable=150, offchain_outbound=0, offchain_inbound=0,
        ),
    )

    mock_cfa_asset = AssetModel(
        asset_id='2',
        name='Asset2',
        details=None,
        precision=2,
        issued_supply=2000,
        timestamp=1620001000,
        added_at=1620003000,
        balance=AssetBalanceResponseModel(
            settled=200, future=100, spendable=300, offchain_outbound=0, offchain_inbound=0,
        ),
    )

    mock_response = GetAssetResponseModel(
        nia=[mock_nia_asset],
        cfa=[mock_cfa_asset],
    )

    # Act
    channel_view_model.get_asset_list()

    # Get the on_success callback from run_in_thread call
    run_thread_kwargs = channel_view_model.run_in_thread.call_args[0][1]
    on_success = run_thread_kwargs['callback']

    # Simulate successful response
    on_success(mock_response)

    # Assert
    channel_view_model.update_loading.assert_has_calls(
        [call(True), call(False)],
    )
    assert channel_view_model.nia_asset == [mock_nia_asset]
    assert channel_view_model.cfa_asset == [mock_cfa_asset]
    assert channel_view_model.assets_loaded is True
    channel_view_model.asset_loaded_signal.emit.assert_called_once()
    channel_view_model.check_loading_completion.assert_called_once()


def test_get_asset_list_none_response(channel_view_model, mocker):
    """Test get_asset_list method with None response."""
    # Arrange
    channel_view_model.update_loading = MagicMock()
    channel_view_model.asset_loaded_signal = MagicMock()
    channel_view_model.get_asset_name = MagicMock(return_value={})
    channel_view_model.check_loading_completion = MagicMock()
    channel_view_model.run_in_thread = MagicMock()

    # Act
    channel_view_model.get_asset_list()

    # Get the on_success callback from run_in_thread call
    run_thread_kwargs = channel_view_model.run_in_thread.call_args[0][1]
    on_success = run_thread_kwargs['callback']

    # Simulate None response
    on_success(None)

    # Assert
    channel_view_model.update_loading.assert_has_calls(
        [call(True), call(False)],
    )
    channel_view_model.asset_loaded_signal.emit.assert_not_called()
    channel_view_model.check_loading_completion.assert_not_called()


def test_get_asset_list_error_handling(channel_view_model, mocker):
    """Test get_asset_list method error handling."""
    # Arrange
    channel_view_model.update_loading = MagicMock()
    mock_toast_manager = mocker.patch(
        'src.views.components.toast.ToastManager.error',
    )
    channel_view_model.run_in_thread = MagicMock()
    error_message = 'Test error'
    mock_error = CommonException(error_message)

    # Act
    channel_view_model.get_asset_list()

    # Get the on_error callback from run_in_thread call
    run_thread_kwargs = channel_view_model.run_in_thread.call_args[0][1]
    on_error = run_thread_kwargs['error_callback']

    # Simulate error
    on_error(mock_error)

    # Assert
    channel_view_model.update_loading.assert_has_calls(
        [call(True), call(False)],
    )
    mock_toast_manager.assert_called_once_with(description=error_message)


def test_create_rgb_channel_success(channel_view_model, mocker):
    """Test create_rgb_channel method with successful response."""
    # Arrange
    channel_view_model.is_loading = MagicMock()
    channel_view_model.channel_created = MagicMock()
    channel_view_model.run_in_thread = MagicMock()

    mock_response = OpenChannelResponseModel(temporary_channel_id='temp_id')

    # Act
    channel_view_model.create_rgb_channel(
        pub_key='pub_key',
        asset_id='asset_id',
        amount=1000,
        capacity_sat='30000',
        push_msat='0',
    )

    # Get the on_success callback from run_in_thread call
    run_thread_kwargs = channel_view_model.run_in_thread.call_args[0][1]
    on_success = run_thread_kwargs['callback']

    # Simulate successful response
    on_success(mock_response)

    # Assert
    channel_view_model.is_loading.emit.assert_has_calls(
        [call(True), call(False)],
    )
    channel_view_model.channel_created.emit.assert_called_once()


def test_create_rgb_channel_insufficient_allocation_error(channel_view_model, mocker):
    """Test create_rgb_channel method with insufficient allocation error."""
    # Arrange
    channel_view_model.is_loading = MagicMock()
    channel_view_model.handle_insufficient_allocation = MagicMock()
    channel_view_model.run_in_thread = MagicMock()

    error_message = ERROR_NO_UNCOLORED_UTXOS_AVAILABLE
    mock_error = CommonException(error_message)

    # Act
    channel_view_model.create_rgb_channel(
        pub_key='pub_key',
        asset_id='asset_id',
        amount=1000,
        capacity_sat='30000',
        push_msat='0',
    )

    # Get the on_error callback from run_in_thread call
    run_thread_kwargs = channel_view_model.run_in_thread.call_args[0][1]
    on_error = run_thread_kwargs['error_callback']

    # Simulate error
    on_error(mock_error)

    # Assert
    channel_view_model.is_loading.emit.assert_called_once_with(True)
    channel_view_model.handle_insufficient_allocation.assert_called_once()


def test_navigate_to_create_channel_page(channel_view_model, mocker):
    """Test navigation to create channel page."""
    # Arrange
    mock_page_navigation = mocker.patch.object(
        channel_view_model, '_page_navigation',
    )

    # Act
    channel_view_model.navigate_to_create_channel_page()

    # Assert
    mock_page_navigation.create_channel_page.assert_called_once()


def test_create_rgb_channel_hard_stop_invalid_pubkey(channel_view_model, mocker):
    """Ensure invalid pubkey error shows toast and does not retry creating UTXOs."""
    # Arrange
    channel_view_model.is_loading = MagicMock()
    channel_view_model.handle_insufficient_allocation = MagicMock()
    channel_view_model.run_in_thread = MagicMock()
    mock_toast_error = mocker.patch(
        'src.views.components.toast.ToastManager.error',
    )

    mock_error = CommonException(ERROR_INVALID_PUBKEY_TYPE)

    # Act
    channel_view_model.create_rgb_channel(
        pub_key='pub_key', asset_id='asset_id', amount=1000, capacity_sat='30000', push_msat='0',
    )

    run_thread_kwargs = channel_view_model.run_in_thread.call_args[0][1]
    on_error = run_thread_kwargs['error_callback']
    on_error(mock_error)

    # Assert
    channel_view_model.is_loading.emit.assert_called_with(False)
    mock_toast_error.assert_called_once_with(
        description=ERROR_INVALID_PUBKEY_TYPE,
    )
    channel_view_model.handle_insufficient_allocation.assert_not_called()


def test_create_rgb_channel_hard_stop_insufficient_asset(channel_view_model, mocker):
    """Ensure not enough assets error shows toast and does not retry creating UTXOs."""
    # Arrange
    channel_view_model.is_loading = MagicMock()
    channel_view_model.handle_insufficient_allocation = MagicMock()
    channel_view_model.run_in_thread = MagicMock()
    mock_toast_error = mocker.patch(
        'src.views.components.toast.ToastManager.error',
    )

    mock_error = CommonException(ERROR_INSUFFICIENT_ASSET)

    # Act
    channel_view_model.create_rgb_channel(
        pub_key='pub_key', asset_id='asset_id', amount=1000, capacity_sat='30000', push_msat='0',
    )

    run_thread_kwargs = channel_view_model.run_in_thread.call_args[0][1]
    on_error = run_thread_kwargs['error_callback']
    on_error(mock_error)

    # Assert
    channel_view_model.is_loading.emit.assert_called_with(False)
    mock_toast_error.assert_called_once_with(
        description=ERROR_INSUFFICIENT_ASSET,
    )
    channel_view_model.handle_insufficient_allocation.assert_not_called()


def test_handle_insufficient_allocation(channel_view_model, mocker):
    """Test handle_insufficient_allocation method."""
    # Arrange
    channel_view_model.is_loading = MagicMock()
    channel_view_model.create_rgb_channel = MagicMock()
    channel_view_model.run_in_thread = MagicMock()
    mock_toast_manager = mocker.patch(
        'src.views.components.toast.ToastManager.error',
    )

    params = HandleInsufficientAllocationSlotsModel(
        pub_key='test_pub_key',
        asset_id='test_asset_id',
        amount=1000,
        capacity_sat='30000',
        push_msat='0',
    )

    # Act
    channel_view_model.handle_insufficient_allocation(params)

    # Get callbacks from run_in_thread call
    run_thread_kwargs = channel_view_model.run_in_thread.call_args[0][1]
    on_success = run_thread_kwargs['callback']
    on_error = run_thread_kwargs['error_callback']

    # Test success case
    on_success()

    # Assert success case
    channel_view_model.create_rgb_channel.assert_called_once_with(
        params.pub_key,
        params.asset_id,
        params.amount,
        params.capacity_sat,
        params.push_msat,
    )

    # Test error case
    error = CommonException('Test error')
    on_error(error)

    # Assert error case
    channel_view_model.is_loading.emit.assert_called_with(False)
    mock_toast_manager.assert_called_once_with(
        description=ERROR_CREATE_UTXO.format(error.message),
    )
