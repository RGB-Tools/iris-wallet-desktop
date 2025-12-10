"""Unit test for WalletOrTransferSelectionWidget."""
# Disable the redefined-outer-name warning as
# it's normal to pass mocked objects in test functions
# pylint: disable=redefined-outer-name,unused-argument,protected-access
from __future__ import annotations

from unittest.mock import MagicMock
from unittest.mock import patch

import pytest

from src.data.repository.setting_repository import SettingRepository
from src.model.enums.enums_model import AssetType
from src.model.enums.enums_model import TransferStatusEnumModel
from src.model.enums.enums_model import TransferType
from src.model.enums.enums_model import WalletType
from src.model.selection_page_model import AssetDataModel
from src.model.selection_page_model import SelectionPageModel
from src.viewmodels.main_view_model import MainViewModel
from src.views.ui_wallet_or_transfer_selection import WalletOrTransferSelectionWidget

SELECTED_FRAME_STYLESHEET = """
                QFrame{
                font: 15px "Inter";
                border-radius: 8px;
                border: 1px solid white;
                }
                QLabel{
                border:none
                }
                """


@pytest.fixture
def wallet_or_transfer_selection_widget(qtbot):
    """Fixture to create and return an instance of WalletOrTransferSelectionWidget."""
    params = SelectionPageModel(
        title='connection_type',
        logo_1_title='embedded',
        logo_1_path=':/assets/embedded.png',
        logo_2_title='remote',
        logo_2_path=':/assets/remote.png',
        callback='None',
        asset_id='None',
    )
    mock_navigation = MagicMock()
    view_model = MagicMock(MainViewModel(mock_navigation))
    widget = WalletOrTransferSelectionWidget(view_model, params)
    widget._view_model.page_navigation.send_bitcoin_page = MagicMock()
    widget._view_model.page_navigation.receive_bitcoin_page = MagicMock()
    qtbot.addWidget(widget)
    return widget


def test_retranslate_ui(wallet_or_transfer_selection_widget: WalletOrTransferSelectionWidget):
    """Test the retranslation of UI elements in WalletOrTransferSelectionWidget."""
    wallet_or_transfer_selection_widget.retranslate_ui()

    assert wallet_or_transfer_selection_widget.option_1_text_label.text() == 'embedded'
    assert wallet_or_transfer_selection_widget.option_2_text_label.text() == 'remote'


def test_handle_frame_click_embedded_wallet(wallet_or_transfer_selection_widget, mocker):
    """Test handle_frame_click for embedded wallet option."""
    # Patch correctly
    mock_start_node = mocker.patch.object(
        wallet_or_transfer_selection_widget._view_model.wallet_transfer_selection_view_model, 'start_node_for_embedded_option',
    )
    mock_set_wallet_type = mocker.patch.object(
        SettingRepository, 'set_wallet_type',
    )

    # Simulate clicking the frame
    wallet_or_transfer_selection_widget.handle_frame_click(
        WalletType.EMBEDDED_TYPE_WALLET,
    )

    # Simulate clicking continue
    wallet_or_transfer_selection_widget.on_click_continue()

    # Assertions
    mock_set_wallet_type.assert_called_once_with(
        WalletType.EMBEDDED_TYPE_WALLET,
    )
    mock_start_node.assert_called_once()


def test_handle_frame_click_on_chain_receive(wallet_or_transfer_selection_widget: WalletOrTransferSelectionWidget, mocker):
    """Test handle_frame_click for on-chain receive option."""
    # Setup the parameters
    wallet_or_transfer_selection_widget._params.callback = TransferStatusEnumModel.RECEIVE.value
    wallet_or_transfer_selection_widget._params.asset_id = 'test_asset_id'

    # Mock asset_type if necessary
    # Ensure asset_type is set
    wallet_or_transfer_selection_widget.asset_type = AssetType.NIA.value

    # Mock the methods that should be called
    mock_receive_cfa_page = mocker.patch.object(
        wallet_or_transfer_selection_widget._view_model.page_navigation, 'receive_cfa_page',
    )

    # Call the method with the on-chain ID
    wallet_or_transfer_selection_widget.handle_frame_click(
        TransferType.ON_CHAIN.value,
    )

    # Assertions
    mock_receive_cfa_page.assert_called_once_with(
        params=AssetDataModel(
            asset_type=AssetType.NIA.value,  # Ensure asset_type is passed as expected
            asset_id='test_asset_id',
        ),
    )


def test_handle_frame_click_on_chain_send(wallet_or_transfer_selection_widget: WalletOrTransferSelectionWidget, mocker):
    """Test handle_frame_click for on-chain send option."""
    # Setup the parameters
    wallet_or_transfer_selection_widget._params.callback = TransferStatusEnumModel.SEND.value

    # Mock the methods that should be called
    mock_send_cfa_page = mocker.patch.object(
        wallet_or_transfer_selection_widget._view_model.page_navigation, 'send_cfa_page',
    )

    # Call the method with the on-chain ID
    wallet_or_transfer_selection_widget.handle_frame_click(
        TransferType.ON_CHAIN.value,
    )

    # Assertions
    mock_send_cfa_page.assert_called_once()


def test_handle_frame_click_off_chain_receive(wallet_or_transfer_selection_widget: WalletOrTransferSelectionWidget, mocker):
    """Test handle_frame_click for off-chain receive option."""
    # Setup the parameters
    wallet_or_transfer_selection_widget._params.callback = TransferStatusEnumModel.RECEIVE.value
    wallet_or_transfer_selection_widget._params.asset_id = 'test_asset_id'
    wallet_or_transfer_selection_widget._params.asset_name = 'test_asset_name'
    wallet_or_transfer_selection_widget.asset_type = 'test_asset_type'

    # Mock the methods that should be called
    mock_create_ln_invoice_page = mocker.patch.object(
        wallet_or_transfer_selection_widget._view_model.page_navigation, 'create_ln_invoice_page',
    )

    # Call the method with the off-chain ID
    wallet_or_transfer_selection_widget.handle_frame_click(
        TransferType.LIGHTNING.value,
    )

    # Assertions
    mock_create_ln_invoice_page.assert_called_once_with(
        'test_asset_id', 'test_asset_name', 'test_asset_type',
    )


def test_handle_frame_click_connect_wallet(wallet_or_transfer_selection_widget, mocker):
    """Test handle_frame_click for connect wallet option."""

    mock_set_wallet_type = mocker.patch(
        'src.data.repository.setting_repository.SettingRepository.set_wallet_type',
    )
    _ = mocker.patch.object(
        wallet_or_transfer_selection_widget._view_model.page_navigation, 'ln_endpoint_page',
    )

    wallet_or_transfer_selection_widget.handle_frame_click(
        WalletType.REMOTE_TYPE_WALLET,
    )

    wallet_or_transfer_selection_widget.on_click_continue()

    mock_set_wallet_type.assert_called_once_with(WalletType.REMOTE_TYPE_WALLET)


def test_show_wallet_loading_screen_true(wallet_or_transfer_selection_widget: WalletOrTransferSelectionWidget, mocker):
    """Test show_wallet_loading_screen when status is True."""
    # Call the method with status True
    wallet_or_transfer_selection_widget.show_wallet_loading_screen(True)

    # Assertions
    assert wallet_or_transfer_selection_widget.option_1_frame.isEnabled() is False
    assert wallet_or_transfer_selection_widget.option_2_frame.isEnabled() is False


def test_show_wallet_loading_screen_false(wallet_or_transfer_selection_widget: WalletOrTransferSelectionWidget, mocker):
    """Test show_wallet_loading_screen when status is False."""
    # Call the method with status False
    wallet_or_transfer_selection_widget.show_wallet_loading_screen(False)

    # Assertions
    assert wallet_or_transfer_selection_widget.option_1_frame.isEnabled() is True
    assert wallet_or_transfer_selection_widget.option_2_frame.isEnabled() is True


def test_handle_frame_click_send_btc(wallet_or_transfer_selection_widget):
    """Test handle_frame_click for sending BTC."""
    wallet_or_transfer_selection_widget._params.callback = TransferStatusEnumModel.SEND_BTC.value

    wallet_or_transfer_selection_widget.handle_frame_click(
        TransferType.ON_CHAIN.value,
    )

    print(wallet_or_transfer_selection_widget._view_model.page_navigation.send_bitcoin_page.call_args_list)

    wallet_or_transfer_selection_widget._view_model.page_navigation.send_bitcoin_page.assert_called_once_with()


def test_handle_frame_click_receive_btc(wallet_or_transfer_selection_widget):
    """Test handle_frame_click for receiving BTC."""

    wallet_or_transfer_selection_widget._params.callback = TransferStatusEnumModel.RECEIVE_BTC.value
    wallet_or_transfer_selection_widget.handle_frame_click(
        TransferType.ON_CHAIN.value,
    )

    wallet_or_transfer_selection_widget._view_model.page_navigation.receive_bitcoin_page.assert_called_once_with()


def test_close_button_navigation(wallet_or_transfer_selection_widget: WalletOrTransferSelectionWidget, mocker):
    """Test close_button_navigation for proper navigation and asset info emission."""

    # Mock the back_page_navigation method with a callable mock
    mock_back_page_navigation = mocker.Mock()
    wallet_or_transfer_selection_widget._params.back_page_navigation = mock_back_page_navigation

    # Mock the cfa_view_model object
    mock_cfa_view_model = mocker.patch.object(
        wallet_or_transfer_selection_widget._view_model, 'cfa_view_model', autospec=False,
    )

    # Create a MagicMock for asset_info and mock its emit method
    mock_asset_info = mocker.MagicMock()
    mock_cfa_view_model.asset_info = mock_asset_info

    # Set up rgb_asset_page_load_model with test values
    wallet_or_transfer_selection_widget._params.rgb_asset_page_load_model = mocker.Mock(
        asset_id='test_asset_id',
        asset_name='test_asset_name',
        image_path='test_image_path',
        asset_type='test_asset_type',
    )

    # Call the method
    wallet_or_transfer_selection_widget.close_button_navigation()

    # Assertions
    mock_back_page_navigation.assert_called_once()  # Ensure navigation was triggered
    mock_asset_info.emit.assert_called_once_with(
        'test_asset_id', 'test_asset_name', 'test_image_path', 'test_asset_type',
    )  # Ensure asset info emission was triggered with correct parameters


def test_handle_frame_click_toggle_info_frame(wallet_or_transfer_selection_widget):
    """Test toggle behavior when clicking the same frame again."""

    # Set the selected frame to SEND_BTC so that the condition matches
    wallet_or_transfer_selection_widget.selected_frame = TransferStatusEnumModel.SEND_BTC.value

    # Store initial visibility state
    initial_state = wallet_or_transfer_selection_widget.info_frame.isHidden()

    # Call handle_frame_click with the same _id
    wallet_or_transfer_selection_widget.handle_frame_click(
        TransferStatusEnumModel.SEND_BTC.value,
    )

    # Assert that info_frame visibility is toggled
    assert wallet_or_transfer_selection_widget.info_frame.isHidden() != initial_state


def test_on_click_frame_embedded_selected(wallet_or_transfer_selection_widget, mocker):
    """Test on_click_frame with embedded wallet selected (is_selected True)."""
    # Patch load_stylesheet even though it should not be used in the True branch.
    dummy_stylesheet = 'dummy stylesheet'
    mocker.patch(
        'src.views.ui_wallet_or_transfer_selection.load_stylesheet',
        return_value=SELECTED_FRAME_STYLESHEET,
    )

    widget = wallet_or_transfer_selection_widget
    # Set option_1_frame and option_2_frame as mocks
    widget.option_1_frame = MagicMock()
    widget.option_2_frame = MagicMock()

    # Call with embedded wallet ID and is_selected True
    widget.on_click_frame(WalletType.EMBEDDED_TYPE_WALLET.value, True)

    # Expect that option_1_frame gets the hard-coded options_stylesheet

    widget.option_1_frame.setStyleSheet.assert_called_once_with(
        SELECTED_FRAME_STYLESHEET,
    )
    widget.option_2_frame.setStyleSheet.assert_not_called()


def test_on_click_frame_embedded_not_selected(wallet_or_transfer_selection_widget, mocker):
    """Test on_click_frame with embedded wallet not selected (is_selected False)."""
    dummy_stylesheet = 'dummy stylesheet'
    # Patch load_stylesheet to return our dummy stylesheet.
    mocker.patch(
        'src.views.ui_wallet_or_transfer_selection.load_stylesheet',
        return_value=dummy_stylesheet,
    )

    widget = wallet_or_transfer_selection_widget
    widget.option_1_frame = MagicMock()
    widget.option_2_frame = MagicMock()

    widget.on_click_frame(WalletType.EMBEDDED_TYPE_WALLET.value, False)

    # In the not selected branch, the stylesheet is loaded via load_stylesheet.
    widget.option_1_frame.setStyleSheet.assert_called_once_with(
        dummy_stylesheet,
    )
    widget.option_2_frame.setStyleSheet.assert_not_called()


def test_on_click_frame_remote_selected(wallet_or_transfer_selection_widget, mocker):
    """Test on_click_frame with remote wallet selected (is_selected True)."""
    dummy_stylesheet = 'dummy stylesheet'
    mocker.patch(
        'src.views.ui_wallet_or_transfer_selection.load_stylesheet',
        return_value=SELECTED_FRAME_STYLESHEET,
    )

    widget = wallet_or_transfer_selection_widget
    widget.option_1_frame = MagicMock()
    widget.option_2_frame = MagicMock()

    widget.on_click_frame(WalletType.REMOTE_TYPE_WALLET.value, True)

    widget.option_2_frame.setStyleSheet.assert_called_once_with(
        SELECTED_FRAME_STYLESHEET,
    )
    widget.option_1_frame.setStyleSheet.assert_not_called()


def test_on_click_frame_remote_not_selected(wallet_or_transfer_selection_widget, mocker):
    """Test on_click_frame with remote wallet not selected (is_selected False)."""
    dummy_stylesheet = 'dummy stylesheet'
    mocker.patch(
        'src.views.ui_wallet_or_transfer_selection.load_stylesheet',
        return_value=dummy_stylesheet,
    )

    widget = wallet_or_transfer_selection_widget
    widget.option_1_frame = MagicMock()
    widget.option_2_frame = MagicMock()

    widget.on_click_frame(WalletType.REMOTE_TYPE_WALLET.value, False)

    widget.option_2_frame.setStyleSheet.assert_called_once_with(
        dummy_stylesheet,
    )
    widget.option_1_frame.setStyleSheet.assert_not_called()


@patch('src.views.ui_wallet_or_transfer_selection.SettingRepository.set_wallet_type')
def test_on_click_continue(mock_set_wallet_type, wallet_or_transfer_selection_widget):
    """Test on_click_continue handles wallet selection properly."""

    # Mock view model and navigation
    wallet_or_transfer_selection_widget._view_model = MagicMock()

    # Test Embedded Wallet
    wallet_or_transfer_selection_widget.selected_frame = WalletType.EMBEDDED_TYPE_WALLET.value
    wallet_or_transfer_selection_widget.on_click_continue()
    mock_set_wallet_type.assert_called_with(WalletType.EMBEDDED_TYPE_WALLET)
    wallet_or_transfer_selection_widget._view_model.wallet_transfer_selection_view_model.start_node_for_embedded_option.assert_called()

    # Test Remote Wallet
    wallet_or_transfer_selection_widget.selected_frame = WalletType.REMOTE_TYPE_WALLET.value
    wallet_or_transfer_selection_widget.on_click_continue()
    mock_set_wallet_type.assert_called_with(WalletType.REMOTE_TYPE_WALLET)
    wallet_or_transfer_selection_widget._view_model.page_navigation.ln_endpoint_page.assert_called_with(
        'wallet_selection_page',
    )
