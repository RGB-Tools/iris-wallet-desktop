"""Unit test for Receive RGB asset UI."""
# Disable the redefined-outer-name warning as
# it's normal to pass mocked objects in test functions
# pylint: disable=redefined-outer-name,unused-argument,protected-access
from __future__ import annotations

from unittest.mock import MagicMock
from unittest.mock import patch

import pytest
from PySide6.QtCore import QCoreApplication

from src.model.enums.enums_model import AssetType
from src.model.enums.enums_model import ToastPreset
from src.model.selection_page_model import AssetDataModel
from src.utils.constant import IRIS_WALLET_TRANSLATIONS_CONTEXT
from src.viewmodels.main_view_model import MainViewModel
from src.views.components.toast import ToastManager
from src.views.ui_receive_rgb_asset import ReceiveRGBAssetWidget


@pytest.fixture
def receive_rgb_asset_widget(qtbot):
    """Fixture to create and return an instance of ReceiveRGBAssetWidget."""
    mock_navigation = MagicMock()
    mock_view_model = MagicMock(MainViewModel(mock_navigation))
    asset_data = AssetDataModel(asset_type='CFA', asset_id='test_asset_id')
    widget = ReceiveRGBAssetWidget(mock_view_model, asset_data)
    qtbot.addWidget(widget)
    return widget


def test_generate_invoice(receive_rgb_asset_widget: ReceiveRGBAssetWidget):
    """Test that generate_invoice calls get_rgb_invoice for specific asset types."""
    receive_rgb_asset_widget._view_model.receive_cfa_view_model.get_rgb_invoice = MagicMock()

    receive_rgb_asset_widget.generate_invoice()

    receive_rgb_asset_widget._view_model.receive_cfa_view_model.get_rgb_invoice.assert_called_once_with(
        1, 'test_asset_id',
    )


def test_setup_ui_connection(receive_rgb_asset_widget: ReceiveRGBAssetWidget):
    """Test that UI connections are set up correctly."""
    with patch('src.views.components.toast.ToastManager.success', MagicMock()):
        with patch('src.views.components.toast.ToastManager._create_toast', MagicMock()):
            with patch.object(receive_rgb_asset_widget, 'show_receive_rgb_loading', MagicMock()):
                # Emit the signal to simulate a button click
                # Verify copy button text is set correctly
                assert receive_rgb_asset_widget.receive_rgb_asset_page.copy_button.text() == QCoreApplication.translate(
                    IRIS_WALLET_TRANSLATIONS_CONTEXT, 'copy_rgb_invoice', None,
                )
                receive_rgb_asset_widget.receive_rgb_asset_page.copy_button.clicked.emit()

                # Verify UI connections are set up
                receive_rgb_asset_widget._view_model.receive_cfa_view_model.address.connect.assert_called_once()
                receive_rgb_asset_widget._view_model.ln_offchain_view_model.invoice_get_event.connect.assert_called()
                receive_rgb_asset_widget._view_model.receive_cfa_view_model.message.connect.assert_called()
                receive_rgb_asset_widget._view_model.receive_cfa_view_model.hide_loading.connect.assert_called()

                # Verify address label text is set correctly
                assert receive_rgb_asset_widget.receive_rgb_asset_page.address_label.text() == QCoreApplication.translate(
                    IRIS_WALLET_TRANSLATIONS_CONTEXT, 'rgb_invoice_label', None,
                )


def test_close_button_navigation(receive_rgb_asset_widget):
    """Test navigation on close button click."""
    # Mock all navigation methods in the view model
    receive_rgb_asset_widget._view_model.page_navigation.collectibles_asset_page = MagicMock()
    receive_rgb_asset_widget._view_model.page_navigation.fungibles_asset_page = MagicMock()
    receive_rgb_asset_widget._view_model.page_navigation.channel_management_page = MagicMock()
    receive_rgb_asset_widget._view_model.page_navigation.view_unspent_list_page = MagicMock()
    receive_rgb_asset_widget._view_model.page_navigation.faucets_page = MagicMock()
    receive_rgb_asset_widget._view_model.page_navigation.settings_page = MagicMock()
    receive_rgb_asset_widget._view_model.page_navigation.help_page = MagicMock()
    receive_rgb_asset_widget._view_model.page_navigation.about_page = MagicMock()
    receive_rgb_asset_widget._view_model.page_navigation.backup_page = MagicMock()

    # Mock ToastManager for error messages
    with patch.object(ToastManager, 'error') as mock_error:
        # Test case 1: Navigation for AssetType.CFA
        receive_rgb_asset_widget.close_page_navigation = AssetType.CFA.value
        receive_rgb_asset_widget.close_button_navigation()
        receive_rgb_asset_widget._view_model.page_navigation.collectibles_asset_page.assert_called_once()
        receive_rgb_asset_widget._view_model.page_navigation.collectibles_asset_page.reset_mock()

        # Test case 2: Navigation for AssetType.NIA
        receive_rgb_asset_widget.close_page_navigation = AssetType.NIA.value
        receive_rgb_asset_widget.close_button_navigation()
        receive_rgb_asset_widget._view_model.page_navigation.fungibles_asset_page.assert_called_once()
        receive_rgb_asset_widget._view_model.page_navigation.fungibles_asset_page.reset_mock()

        # Test case 3: Specific originating page (e.g., 'NIA')
        # Simulate no specific asset navigation
        receive_rgb_asset_widget.close_page_navigation = None
        receive_rgb_asset_widget.originating_page = 'NIA'
        receive_rgb_asset_widget.close_button_navigation()
        receive_rgb_asset_widget._view_model.page_navigation.fungibles_asset_page.assert_called_once()
        receive_rgb_asset_widget._view_model.page_navigation.fungibles_asset_page.reset_mock()

        # Test case 4: Specific originating page (e.g., 'channel_management')
        receive_rgb_asset_widget.originating_page = 'channel_management'
        receive_rgb_asset_widget.close_button_navigation()
        receive_rgb_asset_widget._view_model.page_navigation.channel_management_page.assert_called_once()
        receive_rgb_asset_widget._view_model.page_navigation.channel_management_page.reset_mock()

        # Test case 5: Undefined navigation page
        receive_rgb_asset_widget.originating_page = 'undefined_page'
        receive_rgb_asset_widget.close_button_navigation()
        mock_error.assert_called_once_with(
            description='No navigation defined for undefined_page',
        )
        mock_error.reset_mock()

        # Test case 6: Navigation for 'help'
        receive_rgb_asset_widget.originating_page = 'help'
        receive_rgb_asset_widget.close_button_navigation()
        receive_rgb_asset_widget._view_model.page_navigation.help_page.assert_called_once()
        receive_rgb_asset_widget._view_model.page_navigation.help_page.reset_mock()

        # Test case 7: Navigation for 'about'
        receive_rgb_asset_widget.originating_page = 'about'
        receive_rgb_asset_widget.close_button_navigation()
        receive_rgb_asset_widget._view_model.page_navigation.about_page.assert_called_once()
        receive_rgb_asset_widget._view_model.page_navigation.about_page.reset_mock()

        # Test case 8: Navigation for 'backup'
        receive_rgb_asset_widget.originating_page = 'backup'
        receive_rgb_asset_widget.close_button_navigation()
        receive_rgb_asset_widget._view_model.page_navigation.backup_page.assert_called_once()
        receive_rgb_asset_widget._view_model.page_navigation.backup_page.reset_mock()


def test_update_address(receive_rgb_asset_widget: ReceiveRGBAssetWidget):
    """Test that the address is updated correctly."""

    with patch.object(receive_rgb_asset_widget.receive_rgb_asset_page, 'update_qr_and_address', MagicMock()) as mock_update_qr_and_address, \
            patch.object(receive_rgb_asset_widget.receive_rgb_asset_page.wallet_address_description_text, 'setText', MagicMock()) as mock_set_text:

        # Test case 1: Regular address update
        receive_rgb_asset_widget.update_address('new_address')

        mock_update_qr_and_address.assert_called_once_with('new_address')
        mock_set_text.assert_not_called()
        mock_update_qr_and_address.reset_mock()

        # Test case 2: Lightning invoice update
        receive_rgb_asset_widget.expiry_time = 24
        receive_rgb_asset_widget.expiry_unit = 'hours'
        receive_rgb_asset_widget.update_address(
            'ln_invoice_address', ln_invoice=True,
        )
        mock_update_qr_and_address.assert_called_once_with(
            'ln_invoice_address',
        )
        mock_set_text.assert_called_once_with(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'ln_invoice_info', None,
            ).format('24', 'hours'),
        )

        # Test case 3: Copy Lightning invoice translation
        assert QCoreApplication.translate(
            IRIS_WALLET_TRANSLATIONS_CONTEXT, 'copy_ln_invoice', None,
        )


def test_show_receive_rgb_loading(receive_rgb_asset_widget: ReceiveRGBAssetWidget):
    """Test that the loading screen is shown correctly."""
    receive_rgb_asset_widget.receive_rgb_asset_page.label.hide = MagicMock()
    receive_rgb_asset_widget.receive_rgb_asset_page.receiver_address.hide = MagicMock()

    receive_rgb_asset_widget.show_receive_rgb_loading()

    receive_rgb_asset_widget.receive_rgb_asset_page.label.hide.assert_called_once()
    receive_rgb_asset_widget.receive_rgb_asset_page.receiver_address.hide.assert_called_once()


def test_hide_loading_screen(receive_rgb_asset_widget: ReceiveRGBAssetWidget):
    """Test that the loading screen is hidden correctly."""
    receive_rgb_asset_widget.receive_rgb_asset_page.label.show = MagicMock()
    receive_rgb_asset_widget.receive_rgb_asset_page.receiver_address.show = MagicMock()

    receive_rgb_asset_widget.hide_loading_screen()

    receive_rgb_asset_widget.receive_rgb_asset_page.label.show.assert_called_once()
    receive_rgb_asset_widget.receive_rgb_asset_page.receiver_address.show.assert_called_once()


def test_handle_message(receive_rgb_asset_widget):
    """Test handle_message calls the correct ToastManager method."""
    with patch.object(ToastManager, 'error') as mock_error, patch.object(ToastManager, 'success') as mock_success:
        # Test case 1: msg_type is ERROR
        receive_rgb_asset_widget.handle_message(
            ToastPreset.ERROR, 'This is an error message',
        )
        mock_error.assert_called_once_with('This is an error message')
        mock_success.assert_not_called()

        # Reset mocks
        mock_error.reset_mock()
        mock_success.reset_mock()

        # Test case 2: msg_type is not ERROR
        receive_rgb_asset_widget.handle_message(
            ToastPreset.SUCCESS, 'This is a success message',
        )
        mock_success.assert_called_once_with('This is a success message')
        mock_error.assert_not_called()
