"""Unit test for Send LN invoice ui."""
# Disable the redefined-outer-name warning as
# it's normal to pass mocked objects in test functions
# pylint: disable=redefined-outer-name,unused-argument,protected-access
from __future__ import annotations

from unittest.mock import MagicMock

import pytest
from PySide6.QtCore import QSize

from src.model.enums.enums_model import AssetType
from src.model.enums.enums_model import ChannelFetchingModel
from src.viewmodels.main_view_model import MainViewModel
from src.views.ui_send_ln_invoice import SendLnInvoiceWidget


@pytest.fixture
def send_ln_invoice_widget(qtbot):
    """Fixture to create and return an instance of SendLnInvoiceWidget."""
    mock_navigation = MagicMock()
    view_model = MagicMock(MainViewModel(mock_navigation))
    asset_type = 'NIA'
    widget = SendLnInvoiceWidget(view_model, asset_type)
    qtbot.addWidget(widget)
    return widget


def test_show_invoice_detail(send_ln_invoice_widget: SendLnInvoiceWidget):
    """Test the show_invoice_detail method with a valid invoice detail."""
    invoice_detail_mock = MagicMock()
    invoice_detail_mock.recipient_id = 'utxob:2PoDFyk-8aegNHZE4-inHHn4nWz-rNtAX3MWv-sTiVPQYrF-ed2bXM'
    invoice_detail_mock.asset_id = 'rgb:2eVw8uw-8G88LQ2tQ-kexM12SoD-nCX8DmQrw-yLMu6JDfK-xx1SCfc'
    invoice_detail_mock.amount = 69
    invoice_detail_mock.network = 'Regtest'
    invoice_detail_mock.expiration_timestamp = 1698325849
    invoice_detail_mock.transport_endpoints = [
        'rpcs://proxy.iriswallet.com/0.2/json-rpc',
    ]

    send_ln_invoice_widget.show_invoice_detail(invoice_detail_mock)
    assert send_ln_invoice_widget.asset_id_value.text(
    ) == 'rgb:2eVw8uw-8G88LQ2tQ-kexM12SoD-nCX8DmQrw-yLMu6JDfK-xx1SCfc'


def test_show_invoice_detail_with_none_asset_id(send_ln_invoice_widget: SendLnInvoiceWidget):
    """Test the show_invoice_detail method when asset_id is None."""
    invoice_detail_mock = MagicMock()

    invoice_detail_mock.asset_id = None

    send_ln_invoice_widget.show_invoice_detail(invoice_detail_mock)

    assert not send_ln_invoice_widget.asset_id_value.isVisible()
    assert not send_ln_invoice_widget.asset_id_label.isVisible()


def test_show_invoice_detail_with_none_asset_amount(send_ln_invoice_widget: SendLnInvoiceWidget):
    """Test the show_invoice_detail method when asset_amount is None."""
    invoice_detail_mock = MagicMock()

    invoice_detail_mock.asset_amount = None

    send_ln_invoice_widget.show_invoice_detail(invoice_detail_mock)

    assert not send_ln_invoice_widget.asset_amount_value.isVisible()
    assert not send_ln_invoice_widget.asset_amount_label.isVisible()


def test_handle_button_enable(send_ln_invoice_widget: SendLnInvoiceWidget):
    """Test the handle_button_enable method to toggle the send button."""
    send_ln_invoice_widget.handle_button_enable()
    assert not send_ln_invoice_widget.send_button.isEnabled()

    send_ln_invoice_widget.ln_invoice_input.setPlainText('200')
    send_ln_invoice_widget.handle_button_enable()
    assert send_ln_invoice_widget.send_button.isEnabled()


def test_store_invoice_details(send_ln_invoice_widget):
    """Test the store_invoice_details method."""

    # Prepare mock invoice details
    invoice_details = {
        'asset_id': 'rgb:xyz123',
        'amount': 100,
        'network': 'Bitcoin',
        'recipient': 'recipient_id',
    }

    # Call the method to store the invoice details
    send_ln_invoice_widget.store_invoice_details(invoice_details)

    # Assert that the invoice detail was correctly stored
    assert send_ln_invoice_widget.invoice_detail == invoice_details


@pytest.mark.parametrize(
    'is_valid, expected_is_valid, expected_min_size, send_button_disabled', [
        (True, True, None, False),  # When valid, the send button should be enabled
        # When invalid, the send button should be disabled and the size changed
        (False, False, QSize(650, 400), True),
    ],
)
def test_set_is_invoice_valid(send_ln_invoice_widget, is_valid, expected_is_valid, expected_min_size, send_button_disabled):
    """Test the set_is_invoice_valid method."""

    # Mock methods to avoid actual calls to the view model
    send_ln_invoice_widget._view_model.channel_view_model.available_channels = MagicMock()

    # Mock the UI elements to track calls to their methods
    send_ln_invoice_widget.invoice_detail_frame = MagicMock()
    send_ln_invoice_widget.invoice_detail_label = MagicMock()
    send_ln_invoice_widget.amount_validation_error_label = MagicMock()
    send_ln_invoice_widget.enter_ln_invoice_widget.setMinimumSize = MagicMock()
    send_ln_invoice_widget.send_button.setDisabled = MagicMock()

    # Call the method with the test parameter
    send_ln_invoice_widget.set_is_invoice_valid(is_valid)

    # Assert the invoice validity flag is updated
    assert send_ln_invoice_widget.is_invoice_valid == expected_is_valid

    if expected_min_size:
        # Assert the minimum size is updated when the invoice is invalid
        send_ln_invoice_widget.enter_ln_invoice_widget.setMinimumSize.assert_called_once_with(
            expected_min_size,
        )
    else:
        # When valid, the size shouldn't change
        send_ln_invoice_widget.enter_ln_invoice_widget.setMinimumSize.assert_not_called()

    # Assert the send button is enabled/disabled as per the test scenario
    if is_valid:
        # Should not be called when valid
        send_ln_invoice_widget.send_button.setDisabled.assert_not_called()
    else:
        send_ln_invoice_widget.send_button.setDisabled.assert_called_once_with(
            send_button_disabled,
        )

    if not is_valid:
        # Ensure hidden elements when invoice is invalid
        send_ln_invoice_widget.invoice_detail_frame.hide.assert_called_once()
        send_ln_invoice_widget.invoice_detail_label.hide.assert_called_once()
        send_ln_invoice_widget.amount_validation_error_label.hide.assert_called_once()


def test_update_max_asset_local_balance(send_ln_invoice_widget):
    """Test the _update_max_asset_local_balance method."""

    # Mock the channels
    channel_1 = MagicMock()
    channel_1.asset_id = 'asset_1'
    channel_1.is_usable = True
    channel_1.ready = True
    channel_1.asset_local_amount = 500

    channel_2 = MagicMock()
    channel_2.asset_id = 'asset_1'
    channel_2.is_usable = False  # Not usable, should not be considered
    channel_2.ready = True
    channel_2.asset_local_amount = 200

    channel_3 = MagicMock()
    channel_3.asset_id = 'asset_1'
    channel_3.is_usable = True
    channel_3.ready = True
    channel_3.asset_local_amount = 300

    send_ln_invoice_widget._view_model.channel_view_model.channels = [
        channel_1, channel_2, channel_3,
    ]

    # Mock the detail object with asset_id 'asset_1'
    detail = MagicMock()
    detail.asset_id = 'asset_1'

    # Call the method
    send_ln_invoice_widget._update_max_asset_local_balance(detail)

    # Assert that the max asset local balance is correctly updated
    # The max should be the highest usable, ready amount (500)
    assert send_ln_invoice_widget.max_asset_local_balance == 500


@pytest.mark.parametrize(
    'asset_id, asset_amount, max_balance, expected_error_shown, expected_button_disabled', [
        # If asset_id is None, fields should hide, button enabled
        (None, None, None, False, False),
        # Valid amount, error should be hidden, button enabled
        ('asset_1', 400, 500, False, False),
        # Invalid amount, error should be shown, button disabled
        ('asset_1', 600, 500, True, True),
    ],
)
def test_validate_asset_amount(send_ln_invoice_widget, asset_id, asset_amount, max_balance, expected_error_shown, expected_button_disabled):
    """Test the _validate_asset_amount method."""

    # Mock the detail object
    detail = MagicMock()
    detail.asset_id = asset_id
    detail.asset_amount = asset_amount

    # Set the max balance for the widget
    send_ln_invoice_widget.max_asset_local_balance = max_balance

    # Mock UI elements
    send_ln_invoice_widget.amount_validation_error_label = MagicMock()
    send_ln_invoice_widget.send_button.setDisabled = MagicMock()

    # Call the method
    send_ln_invoice_widget._validate_asset_amount(detail)

    # Test visibility of the error label
    if expected_error_shown:
        send_ln_invoice_widget.amount_validation_error_label.show.assert_called_once()
    else:
        # If no error is shown, ensure the hide() method was called
        send_ln_invoice_widget.amount_validation_error_label.hide.assert_called_once()

    # Test if the send button is enabled or disabled
    send_ln_invoice_widget.send_button.setDisabled.assert_called_once_with(
        expected_button_disabled,
    )


@pytest.mark.parametrize(
    'is_loading, is_fetching, is_invoice_valid, expected_actions', [
        (
            True, None, None, [
                ('_SendLnInvoiceWidget__loading_translucent_screen.start', 1),
                ('ln_invoice_input.setReadOnly', 1),
                ('send_button.setDisabled', 1),
                ('close_btn_send_ln_invoice_page.setDisabled', 1),
            ],
        ),
        (
            False, ChannelFetchingModel.FETCHED.value, True, [
                ('show_invoice_detail', 1),  # Adjusted to handle single action
                ('_SendLnInvoiceWidget__loading_translucent_screen.stop', 1),
                ('ln_invoice_input.setReadOnly', 1),
                ('send_button.setDisabled', 0),
                ('close_btn_send_ln_invoice_page.setDisabled', 1),
            ],
        ),
        (
            False, ChannelFetchingModel.FAILED.value, True, [
                ('send_button.setDisabled', 1),
                ('_SendLnInvoiceWidget__loading_translucent_screen.stop', 1),
                ('close_btn_send_ln_invoice_page.setDisabled', 1),
            ],
        ),
        (
            False, None, False, [
                ('_SendLnInvoiceWidget__loading_translucent_screen.stop', 1),
                ('send_button.setDisabled', 1),
                ('invoice_detail_frame.hide', 1),
                ('invoice_detail_label.hide', 1),
                ('close_btn_send_ln_invoice_page.setDisabled', 1),
            ],
        ),
    ],
)
def test_is_channel_fetched(send_ln_invoice_widget, is_loading, is_fetching, is_invoice_valid, expected_actions):
    """Test the is_channel_fetched method."""

    # Mocking the widget methods
    send_ln_invoice_widget._SendLnInvoiceWidget__loading_translucent_screen = MagicMock()
    send_ln_invoice_widget.ln_invoice_input = MagicMock()
    send_ln_invoice_widget.send_button = MagicMock()
    send_ln_invoice_widget.close_btn_send_ln_invoice_page = MagicMock()
    send_ln_invoice_widget.show_invoice_detail = MagicMock()
    send_ln_invoice_widget.invoice_detail_frame = MagicMock()
    send_ln_invoice_widget.invoice_detail_label = MagicMock()

    # Mock the start and stop methods
    send_ln_invoice_widget._SendLnInvoiceWidget__loading_translucent_screen.start = MagicMock()
    send_ln_invoice_widget._SendLnInvoiceWidget__loading_translucent_screen.stop = MagicMock()

    # Set the invoice validity
    send_ln_invoice_widget.is_invoice_valid = is_invoice_valid

    # Call the method
    send_ln_invoice_widget.is_channel_fetched(is_loading, is_fetching)

    # Check the expected actions
    for action, times in expected_actions:
        if '.' in action:
            obj, method = action.rsplit('.', 1)
            mocked_method = getattr(
                getattr(send_ln_invoice_widget, obj), method,
            )
        else:
            mocked_method = getattr(send_ln_invoice_widget, action)
        assert mocked_method.call_count == times


def test_get_invoice_detail(send_ln_invoice_widget):
    """Test the get_invoice_detail method."""

    # Mocking the widget's properties and methods
    send_ln_invoice_widget.ln_invoice_input = MagicMock()
    send_ln_invoice_widget._view_model = MagicMock()
    send_ln_invoice_widget._view_model.ln_offchain_view_model.decode_invoice = MagicMock()
    send_ln_invoice_widget.invoice_detail_frame = MagicMock()
    send_ln_invoice_widget.invoice_detail_label = MagicMock()
    send_ln_invoice_widget.enter_ln_invoice_widget = MagicMock()
    send_ln_invoice_widget.send_button = MagicMock()

    # Test case 1: Invoice length > 200
    long_invoice = 'x' * 201
    send_ln_invoice_widget.ln_invoice_input.toPlainText.return_value = long_invoice

    send_ln_invoice_widget.get_invoice_detail()

    # Assert decode_invoice was called
    send_ln_invoice_widget._view_model.ln_offchain_view_model.decode_invoice.assert_called_once_with(
        long_invoice,
    )
    send_ln_invoice_widget.invoice_detail_frame.hide.assert_not_called()
    send_ln_invoice_widget.invoice_detail_label.hide.assert_not_called()
    send_ln_invoice_widget.enter_ln_invoice_widget.setMinimumSize.assert_not_called()
    send_ln_invoice_widget.send_button.setDisabled.assert_not_called()

    # Reset mocks
    send_ln_invoice_widget._view_model.ln_offchain_view_model.decode_invoice.reset_mock()
    send_ln_invoice_widget.invoice_detail_frame.hide.reset_mock()
    send_ln_invoice_widget.invoice_detail_label.hide.reset_mock()
    send_ln_invoice_widget.enter_ln_invoice_widget.setMinimumSize.reset_mock()
    send_ln_invoice_widget.send_button.setDisabled.reset_mock()

    # Test case 2: Invoice length <= 200
    short_invoice = 'x' * 200
    send_ln_invoice_widget.ln_invoice_input.toPlainText.return_value = short_invoice

    send_ln_invoice_widget.get_invoice_detail()

    # Assert decode_invoice was not called
    send_ln_invoice_widget._view_model.ln_offchain_view_model.decode_invoice.assert_not_called()

    # Assert the other actions were performed
    send_ln_invoice_widget.invoice_detail_frame.hide.assert_called_once()
    send_ln_invoice_widget.invoice_detail_label.hide.assert_called_once()
    send_ln_invoice_widget.enter_ln_invoice_widget.setMinimumSize.assert_called_once_with(
        QSize(650, 400),
    )
    send_ln_invoice_widget.send_button.setDisabled.assert_called_once_with(
        True,
    )


def test_send_asset(send_ln_invoice_widget):
    """Test the send_asset method."""

    # Mocking the widget's properties and methods
    send_ln_invoice_widget.ln_invoice_input = MagicMock()
    send_ln_invoice_widget._view_model = MagicMock()
    send_ln_invoice_widget._view_model.ln_offchain_view_model.send_asset_offchain = MagicMock()

    # Define the test invoice
    test_invoice = 'sample_invoice'
    send_ln_invoice_widget.ln_invoice_input.toPlainText.return_value = test_invoice

    # Call the method
    send_ln_invoice_widget.send_asset()

    # Assert send_asset_offchain is called with the correct invoice
    send_ln_invoice_widget._view_model.ln_offchain_view_model.send_asset_offchain.assert_called_once_with(
        test_invoice,
    )


def test_on_success_sent_navigation_collectibles(send_ln_invoice_widget):
    """Test the on_success_sent_navigation method when asset type is CFA (collectibles)."""

    # Mocking the widget's properties and methods
    send_ln_invoice_widget._view_model = MagicMock()
    send_ln_invoice_widget._view_model.page_navigation.collectibles_asset_page = MagicMock()
    send_ln_invoice_widget._view_model.page_navigation.fungibles_asset_page = MagicMock()

    # Set the asset type to CFA (collectibles)
    send_ln_invoice_widget.asset_type = AssetType.CFA.value

    # Call the method
    send_ln_invoice_widget.on_success_sent_navigation()

    # Assert collectibles_asset_page is called
    send_ln_invoice_widget._view_model.page_navigation.collectibles_asset_page.assert_called_once()

    # Assert fungibles_asset_page is not called
    send_ln_invoice_widget._view_model.page_navigation.fungibles_asset_page.assert_not_called()


def test_on_success_sent_navigation_fungibles(send_ln_invoice_widget):
    """Test the on_success_sent_navigation method when asset type is not CFA (fungibles)."""

    # Mocking the widget's properties and methods
    send_ln_invoice_widget._view_model = MagicMock()
    send_ln_invoice_widget._view_model.page_navigation.collectibles_asset_page = MagicMock()
    send_ln_invoice_widget._view_model.page_navigation.fungibles_asset_page = MagicMock()

    # Set the asset type to a non-CFA value (fungibles)
    send_ln_invoice_widget.asset_type = 'some_other_asset_type'

    # Call the method
    send_ln_invoice_widget.on_success_sent_navigation()

    # Assert fungibles_asset_page is called
    send_ln_invoice_widget._view_model.page_navigation.fungibles_asset_page.assert_called_once()

    # Assert collectibles_asset_page is not called
    send_ln_invoice_widget._view_model.page_navigation.collectibles_asset_page.assert_not_called()


def test_update_loading_state_loading(send_ln_invoice_widget):
    """Test the update_loading_state method when is_loading is True."""

    # Mocking the widget's properties and methods
    send_ln_invoice_widget.render_timer = MagicMock()
    send_ln_invoice_widget.send_button = MagicMock()

    # Call the method with is_loading = True
    send_ln_invoice_widget.update_loading_state(is_loading=True)

    # Assert render_timer.start and send_button.start_loading are called
    send_ln_invoice_widget.render_timer.start.assert_called_once()
    send_ln_invoice_widget.send_button.start_loading.assert_called_once()

    # Assert render_timer.stop and send_button.stop_loading are not called
    send_ln_invoice_widget.render_timer.stop.assert_not_called()
    send_ln_invoice_widget.send_button.stop_loading.assert_not_called()


def test_update_loading_state_not_loading(send_ln_invoice_widget):
    """Test the update_loading_state method when is_loading is False."""

    # Mocking the widget's properties and methods
    send_ln_invoice_widget.render_timer = MagicMock()
    send_ln_invoice_widget.send_button = MagicMock()

    # Call the method with is_loading = False
    send_ln_invoice_widget.update_loading_state(is_loading=False)

    # Assert render_timer.stop and send_button.stop_loading are called
    send_ln_invoice_widget.render_timer.stop.assert_called_once()
    send_ln_invoice_widget.send_button.stop_loading.assert_called_once()

    # Assert render_timer.start and send_button.start_loading are not called
    send_ln_invoice_widget.render_timer.start.assert_not_called()
    send_ln_invoice_widget.send_button.start_loading.assert_not_called()


def test_on_click_close_button_collectibles(send_ln_invoice_widget):
    """Test the on_click_close_button method when asset type is CFA (collectibles)."""

    # Mocking the widget's properties and methods
    send_ln_invoice_widget._view_model = MagicMock()
    send_ln_invoice_widget._view_model.page_navigation.collectibles_asset_page = MagicMock()
    send_ln_invoice_widget._view_model.page_navigation.fungibles_asset_page = MagicMock()

    # Set the asset type to CFA (collectibles)
    send_ln_invoice_widget.asset_type = AssetType.CFA.value

    # Call the method
    send_ln_invoice_widget.on_click_close_button()

    # Assert collectibles_asset_page is called
    send_ln_invoice_widget._view_model.page_navigation.collectibles_asset_page.assert_called_once()

    # Assert fungibles_asset_page is not called
    send_ln_invoice_widget._view_model.page_navigation.fungibles_asset_page.assert_not_called()


def test_on_click_close_button_fungibles(send_ln_invoice_widget):
    """Test the on_click_close_button method when asset type is not CFA (fungibles)."""

    # Mocking the widget's properties and methods
    send_ln_invoice_widget._view_model = MagicMock()
    send_ln_invoice_widget._view_model.page_navigation.collectibles_asset_page = MagicMock()
    send_ln_invoice_widget._view_model.page_navigation.fungibles_asset_page = MagicMock()

    # Set the asset type to a non-CFA value (fungibles)
    send_ln_invoice_widget.asset_type = 'some_other_asset_type'

    # Call the method
    send_ln_invoice_widget.on_click_close_button()

    # Assert fungibles_asset_page is called
    send_ln_invoice_widget._view_model.page_navigation.fungibles_asset_page.assert_called_once()

    # Assert collectibles_asset_page is not called
    send_ln_invoice_widget._view_model.page_navigation.collectibles_asset_page.assert_not_called()
