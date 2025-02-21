"""Unit test for Send Bitcoin UI."""
# pylint: disable=redefined-outer-name,unused-argument,protected-access
from __future__ import annotations

from unittest.mock import MagicMock
from unittest.mock import patch

import pytest

from src.model.setting_model import DefaultFeeRate
from src.viewmodels.main_view_model import MainViewModel
from src.views.ui_send_bitcoin import SendBitcoinWidget


@pytest.fixture
def send_bitcoin_widget(qtbot):
    """Fixture to initialize the SendBitcoinWidget."""
    mock_navigation = MagicMock()
    view_model = MagicMock(
        MainViewModel(
            mock_navigation,
        ),
    )  # Mock the view model

    # Mock the DefaultFeeRate
    default_fee_rate = DefaultFeeRate(fee_rate=0.0001)

    # Mock the attributes that return the bitcoin balances as strings
    view_model.bitcoin_view_model.spendable_bitcoin_balance_with_suffix = '0.5 BTC'
    view_model.bitcoin_view_model.total_bitcoin_balance_with_suffix = '1.0 BTC'

    # Patch the SettingRepository to return the mocked DefaultFeeRate
    with patch('src.views.ui_send_bitcoin.SettingCardRepository.get_default_fee_rate', return_value=default_fee_rate):
        widget = SendBitcoinWidget(view_model)
        qtbot.addWidget(widget)
    return widget


def test_setup_ui_connection(send_bitcoin_widget: SendBitcoinWidget, qtbot):
    """Test the setup_ui_connection method."""

    # Set initial values for pay_amount and spendable_amount
    send_bitcoin_widget.send_bitcoin_page.pay_amount = 0
    send_bitcoin_widget.send_bitcoin_page.spendable_amount = 0

    # Initially, the button should be disabled
    assert not send_bitcoin_widget.send_bitcoin_page.send_btn.isEnabled()

    # Simulate user input for address and amount using setText
    send_bitcoin_widget.send_bitcoin_page.asset_address_value.setText(
        '1BitcoinAddress',
    )
    send_bitcoin_widget.send_bitcoin_page.asset_amount_value.setText('.001')

    # Ensure the values have been set correctly
    assert send_bitcoin_widget.send_bitcoin_page.asset_address_value.text() == '1BitcoinAddress'
    assert send_bitcoin_widget.send_bitcoin_page.asset_amount_value.text() == '.001'

    # Trigger the button enablement logic
    send_bitcoin_widget.handle_button_enabled()

    # After valid input, the button should be enabled
    assert send_bitcoin_widget.send_bitcoin_page.send_btn.isEnabled()


def test_set_bitcoin_balance(send_bitcoin_widget: SendBitcoinWidget):
    """Test the set_bitcoin_balance method."""
    spendable_balance = '0.5 BTC'
    total_balance = '1.0 BTC'
    send_bitcoin_widget._view_model.bitcoin_view_model.spendable_bitcoin_balance_with_suffix = spendable_balance
    send_bitcoin_widget._view_model.bitcoin_view_model.total_bitcoin_balance_with_suffix = total_balance

    send_bitcoin_widget.set_bitcoin_balance()

    assert send_bitcoin_widget.send_bitcoin_page.asset_balance_label_spendable.text(
    ) == spendable_balance
    assert send_bitcoin_widget.send_bitcoin_page.asset_balance_label_total.text() == total_balance


def test_send_bitcoin_button(send_bitcoin_widget: SendBitcoinWidget, qtbot):
    """Test the send_bitcoin_button method."""
    address = '1BitcoinAddress'
    amount = '.001'
    fee = '.0001'

    # Simulate user input
    send_bitcoin_widget.send_bitcoin_page.asset_address_value.setText(address)
    send_bitcoin_widget.send_bitcoin_page.asset_amount_value.setText(amount)
    send_bitcoin_widget.send_bitcoin_page.fee_rate_value.setText(fee)

    send_bitcoin_widget.send_bitcoin_button()

    send_bitcoin_widget._view_model.send_bitcoin_view_model.on_send_click.assert_called_once_with(
        address, amount, fee,
    )


def test_handle_button_enabled(send_bitcoin_widget: SendBitcoinWidget):
    """Test the handle_button_enabled method."""
    # Test valid address, amount, fee and payment
    send_bitcoin_widget.send_bitcoin_page.asset_address_value.setText(
        '1BitcoinAddress',
    )
    send_bitcoin_widget.send_bitcoin_page.asset_amount_value.setText('0.001')
    send_bitcoin_widget.send_bitcoin_page.fee_rate_value.setText('0.0001')
    send_bitcoin_widget.send_bitcoin_page.pay_amount = 1000
    send_bitcoin_widget.send_bitcoin_page.spendable_amount = 2000

    send_bitcoin_widget.handle_button_enabled()
    assert send_bitcoin_widget.send_bitcoin_page.send_btn.isEnabled()

    # Test invalid address (empty)
    send_bitcoin_widget.send_bitcoin_page.asset_address_value.clear()
    send_bitcoin_widget.handle_button_enabled()
    assert not send_bitcoin_widget.send_bitcoin_page.send_btn.isEnabled()

    # Test invalid amount (zero)
    send_bitcoin_widget.send_bitcoin_page.asset_amount_value.setText('0')
    send_bitcoin_widget.handle_button_enabled()
    assert not send_bitcoin_widget.send_bitcoin_page.send_btn.isEnabled()

    # Test invalid fee (empty)
    send_bitcoin_widget.send_bitcoin_page.asset_amount_value.setText('0.001')
    send_bitcoin_widget.send_bitcoin_page.fee_rate_value.clear()
    send_bitcoin_widget.handle_button_enabled()
    assert not send_bitcoin_widget.send_bitcoin_page.send_btn.isEnabled()

    # Test invalid fee (zero)
    send_bitcoin_widget.send_bitcoin_page.fee_rate_value.setText('0')
    send_bitcoin_widget.handle_button_enabled()
    assert not send_bitcoin_widget.send_bitcoin_page.send_btn.isEnabled()

    # Test invalid payment (pay_amount > spendable_amount)
    send_bitcoin_widget.send_bitcoin_page.fee_rate_value.setText('0.0001')
    send_bitcoin_widget.send_bitcoin_page.pay_amount = 3000
    send_bitcoin_widget.send_bitcoin_page.spendable_amount = 2000
    send_bitcoin_widget.handle_button_enabled()
    assert not send_bitcoin_widget.send_bitcoin_page.send_btn.isEnabled()


def test_refresh_bitcoin_balance(send_bitcoin_widget: SendBitcoinWidget, qtbot):
    """Test the refresh_bitcoin_balance method."""

    # Mock the view model and its method
    send_bitcoin_widget._view_model.bitcoin_view_model.get_transaction_list = MagicMock()

    # Trigger the refresh method
    send_bitcoin_widget.refresh_bitcoin_balance()

    # Verify that the loading_performer is set to 'REFRESH_BUTTON'
    assert send_bitcoin_widget.loading_performer == 'REFRESH_BUTTON'

    # Verify that the get_transaction_list method was called once
    send_bitcoin_widget._view_model.bitcoin_view_model.get_transaction_list.assert_called_once()


def test_update_loading_state(send_bitcoin_widget: SendBitcoinWidget, qtbot):
    """Test the update_loading_state method."""

    # Mock the required methods and attributes
    send_bitcoin_widget.send_bitcoin_page.send_btn.start_loading = MagicMock()
    send_bitcoin_widget.send_bitcoin_page.send_btn.stop_loading = MagicMock()
    send_bitcoin_widget._loading_translucent_screen.start = MagicMock()
    send_bitcoin_widget._loading_translucent_screen.stop = MagicMock()
    send_bitcoin_widget._loading_translucent_screen.make_parent_disabled_during_loading = MagicMock()
    send_bitcoin_widget.render_timer = MagicMock()

    with patch('src.views.ui_send_bitcoin.LoadingTranslucentScreen') as mock_loading_screen:
        # Mock instance of LoadingTranslucentScreen for fee rate loading
        mock_fee_rate_screen = MagicMock()
        mock_loading_screen.return_value = mock_fee_rate_screen

        # Test when is_fee_rate_loading is True and is_loading is True
        send_bitcoin_widget.update_loading_state(
            is_loading=True, is_fee_rate_loading=True,
        )
        mock_loading_screen.assert_called_once_with(
            parent=send_bitcoin_widget, description_text='Getting Fee Rate',
        )
        mock_fee_rate_screen.start.assert_called_once()
        mock_fee_rate_screen.make_parent_disabled_during_loading.assert_called_with(
            True,
        )

        # Test when is_fee_rate_loading is True and is_loading is False
        send_bitcoin_widget.update_loading_state(
            is_loading=False, is_fee_rate_loading=True,
        )
        mock_fee_rate_screen.stop.assert_called_once()
        mock_fee_rate_screen.make_parent_disabled_during_loading.assert_called_with(
            False,
        )

    # Test non-fee rate loading scenarios
    # Test when loading is True and performer is 'REFRESH_BUTTON'
    send_bitcoin_widget.loading_performer = 'REFRESH_BUTTON'
    send_bitcoin_widget.update_loading_state(
        is_loading=True, is_fee_rate_loading=False,
    )
    send_bitcoin_widget._loading_translucent_screen.start.assert_called_once()
    send_bitcoin_widget._loading_translucent_screen.make_parent_disabled_during_loading.assert_called_with(
        True,
    )

    # Test when loading is False and performer is 'REFRESH_BUTTON'
    send_bitcoin_widget.update_loading_state(
        is_loading=False, is_fee_rate_loading=False,
    )
    send_bitcoin_widget._loading_translucent_screen.stop.assert_called_once()
    send_bitcoin_widget._loading_translucent_screen.make_parent_disabled_during_loading.assert_called_with(
        False,
    )
    assert send_bitcoin_widget.loading_performer is None

    # Test when loading is True and performer is not 'REFRESH_BUTTON'
    send_bitcoin_widget.loading_performer = 'OTHER_ACTION'
    send_bitcoin_widget.update_loading_state(
        is_loading=True, is_fee_rate_loading=False,
    )
    send_bitcoin_widget.render_timer.start.assert_called_once()
    send_bitcoin_widget.send_bitcoin_page.send_btn.start_loading.assert_called_once()
    send_bitcoin_widget._loading_translucent_screen.make_parent_disabled_during_loading.assert_called_with(
        True,
    )

    # Test when loading is False and performer is not 'REFRESH_BUTTON'
    send_bitcoin_widget.update_loading_state(
        is_loading=False, is_fee_rate_loading=False,
    )
    send_bitcoin_widget.render_timer.stop.assert_called_once()
    send_bitcoin_widget.send_bitcoin_page.send_btn.stop_loading.assert_called_once()
    send_bitcoin_widget._loading_translucent_screen.make_parent_disabled_during_loading.assert_called_with(
        False,
    )


def test_bitcoin_page_navigation(send_bitcoin_widget: SendBitcoinWidget):
    """Test the bitcoin_page_navigation method."""

    # Mock the view model's page_navigation attribute
    send_bitcoin_widget._view_model.page_navigation.bitcoin_page = MagicMock()

    # Call the method
    send_bitcoin_widget.bitcoin_page_navigation()

    # Assert that the bitcoin_page method was called once
    send_bitcoin_widget._view_model.page_navigation.bitcoin_page.assert_called_once()
