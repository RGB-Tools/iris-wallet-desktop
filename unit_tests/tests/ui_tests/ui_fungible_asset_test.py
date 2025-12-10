"""Unit test for FungibleAsset UI"""
# Unit test for Enter Fungible Asset UI.
# Disable the redefined-outer-name warning as
# it's normal to pass mocked objects in test functions
# pylint: disable=redefined-outer-name,unused-argument,protected-access
from __future__ import annotations

from unittest.mock import MagicMock
from unittest.mock import patch

import pytest
from PySide6.QtCore import QCoreApplication
from PySide6.QtCore import QSize
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QSpacerItem
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QWidget

from src.model.enums.enums_model import AssetType
from src.model.enums.enums_model import NetworkEnumModel
from src.model.enums.enums_model import ToastPreset
from src.model.enums.enums_model import TokenSymbol
from src.model.enums.enums_model import WalletType
from src.model.rgb_model import RgbAssetPageLoadModel
from src.utils.constant import IRIS_WALLET_TRANSLATIONS_CONTEXT
from src.utils.info_message import INFO_FAUCET_NOT_AVAILABLE
from src.views.ui_fungible_asset import FungibleAssetWidget


@pytest.fixture
def mock_fungible_asset_view_model():
    """Fixture to create a mock view model."""
    mock_view_model = MagicMock()
    mock_view_model.main_asset_view_model.asset_loaded = MagicMock()
    mock_view_model.main_asset_view_model.assets.vanilla = MagicMock(
        asset_id='1',
        name='Bitcoin',
        ticker=TokenSymbol.BITCOIN.value,
        balance=MagicMock(future=0.5),
    )
    mock_view_model.main_asset_view_model.assets.nia = []
    return mock_view_model


@pytest.fixture
def create_fungible_asset_widget(qtbot, mock_fungible_asset_view_model):
    """Fixture to create the FungibleAssetWidget."""
    with patch('src.data.service.common_operation_service.CommonOperationRepository.node_info', return_value=MagicMock()):
        widget = FungibleAssetWidget(mock_fungible_asset_view_model)
        qtbot.addWidget(widget)
        return widget


def test_fungible_asset_widget_initialization(create_fungible_asset_widget):
    """Test the initialization of the FungibleAssetWidget."""
    widget = create_fungible_asset_widget

    # Check if the widget is properly initialized
    assert isinstance(widget, FungibleAssetWidget)
    assert widget.objectName() == 'my_assets_page'

    # Check if the title frame is created
    assert widget.title_frame is not None

    # Check if the refresh button is present
    assert isinstance(widget.title_frame.refresh_page_button, QPushButton)
    assert widget.title_frame.refresh_page_button.objectName() == 'refresh_page_button'

    # Check if the issue new assets button is present
    assert isinstance(widget.title_frame.action_button, QPushButton)
    assert widget.title_frame.action_button.text() == QCoreApplication.translate(
        IRIS_WALLET_TRANSLATIONS_CONTEXT, 'issue_new_asset', None,
    )


def test_fungible_asset_widget_show_assets(create_fungible_asset_widget: FungibleAssetWidget, qtbot):
    """Test the display of assets in the FungibleAssetWidget."""
    widget = create_fungible_asset_widget

    # Mock the assets
    bitcoin_mock = MagicMock()
    bitcoin_mock.name = 'bitcoin'
    bitcoin_mock.balance.future = '0.5'
    bitcoin_mock.ticker = 'BTC'
    bitcoin_mock.asset_id = 'rBTC'

    # Set the mock assets in the view model
    widget._view_model.main_asset_view_model.assets.vanilla = bitcoin_mock
    widget._view_model.main_asset_view_model.assets.nia = []

    # Simulate asset loading
    widget.show_assets()

    # Check that the asset name was set correctly
    assert widget.asset_name.text() == 'bitcoin'
    assert widget.address.text() == 'rBTC'
    assert widget.amount.text() == '0.5'
    assert widget.asset_logo.pixmap() is not None


def test_issue_new_assets_button_click(create_fungible_asset_widget, qtbot):
    """Test clicking the issue new assets button."""
    widget = create_fungible_asset_widget

    # Simulate clicking the issue new assets button
    qtbot.mouseClick(widget.title_frame.action_button, Qt.LeftButton)

    # Ensure the view model method is called with the correct argument
    widget._view_model.main_asset_view_model.navigate_issue_asset.assert_called_once()


def test_ui_update_after_asset_loading(create_fungible_asset_widget: FungibleAssetWidget, qtbot):
    """Test UI updates after assets are loaded."""
    widget = create_fungible_asset_widget

    # Mock Bitcoin asset
    bitcoin_mock = MagicMock()
    bitcoin_mock.asset_id = 'btc_asset_id'
    bitcoin_mock.name = 'bitcoin'  # Set as string
    bitcoin_mock.balance = MagicMock()
    bitcoin_mock.balance.future = '0.5'

    # Mock assets in the view model
    widget._view_model.main_asset_view_model.assets.vanilla = bitcoin_mock

    # Mock the create_fungible_card method to integrate the mock data into the widget
    with patch.object(widget, 'create_fungible_card') as mock_create_fungible_card:
        mock_create_fungible_card.side_effect = lambda asset, img_path=None: setattr(
            widget, 'asset_name', QLabel(str(asset.name)),
        )

        # Simulate asset loading
        widget.show_assets()

        # Check if the asset details UI is updated
        assert widget.asset_name.text() == 'bitcoin'


def test_show_assets_with_various_assets(create_fungible_asset_widget, qtbot):
    """Test the `show_assets` method with various asset configurations."""
    widget = create_fungible_asset_widget

    # Mock Bitcoin asset
    bitcoin_mock = MagicMock()
    bitcoin_mock.asset_id = 'btc_asset_id'
    bitcoin_mock.name = 'Bitcoin'
    bitcoin_mock.balance.future = '0.5'
    bitcoin_mock.ticker = 'BTC'

    # Mock NIA asset
    nia_mock = MagicMock()
    nia_mock.asset_id = 'nia_asset_id'
    nia_mock.name = 'NIA'
    nia_mock.balance.future = '1.0'
    nia_mock.ticker = 'NIA'

    # Mock assets in the view model
    widget._view_model.main_asset_view_model.assets.vanilla = bitcoin_mock
    widget._view_model.main_asset_view_model.assets.nia = [nia_mock]

    # Mock the get_bitcoin_address call
    widget._view_model.receive_bitcoin_view_model.get_bitcoin_address = MagicMock()

    # Mock the `create_fungible_card` method
    with patch.object(widget, 'create_fungible_card', wraps=widget.create_fungible_card) as mock_create_fungible_card:
        # Simulate asset loading
        widget.show_assets()

        # Assertions for Bitcoin card creation
        mock_create_fungible_card.assert_any_call(
            bitcoin_mock, img_path=':/assets/regtest_bitcoin.png',
        )

        # Assertions for NIA card creation
        mock_create_fungible_card.assert_any_call(nia_mock)

    # Check headers text
    assert widget.name_header.text() == QCoreApplication.translate(
        IRIS_WALLET_TRANSLATIONS_CONTEXT, 'asset_name', None,
    )
    assert widget.address_header.text() == QCoreApplication.translate(
        IRIS_WALLET_TRANSLATIONS_CONTEXT, 'asset_id', None,
    )
    assert widget.amount_header.text() == QCoreApplication.translate(
        IRIS_WALLET_TRANSLATIONS_CONTEXT, 'on_chain_balance', None,
    )
    assert widget.outbound_amount_header.text() == QCoreApplication.translate(
        IRIS_WALLET_TRANSLATIONS_CONTEXT, 'lightning_balance', None,
    )
    assert widget.symbol_header.text() == QCoreApplication.translate(
        IRIS_WALLET_TRANSLATIONS_CONTEXT, 'symbol_header', None,
    )

    # Ensure the spacer was added
    spacer_item = widget.vertical_layout_scroll_content.itemAt(
        widget.vertical_layout_scroll_content.count() - 1,
    )
    assert isinstance(spacer_item, QSpacerItem)


def test_update_faucet_availability_when_unavailable(create_fungible_asset_widget: FungibleAssetWidget, qtbot):
    """Test update_faucet_availability method when faucet is unavailable."""
    widget = create_fungible_asset_widget

    # Mock the view model and sidebar
    sidebar_mock = MagicMock()
    # Mocking the faucet button (QPushButton)
    faucet_mock = MagicMock(spec=QPushButton)

    # Simulate the sidebar having a faucet
    sidebar_mock.faucet = faucet_mock
    widget._view_model.page_navigation.sidebar = MagicMock(
        return_value=sidebar_mock,
    )

    # Call the method with available=False
    widget.update_faucet_availability(available=False)

    # Check if faucet.setCheckable(False) was called
    faucet_mock.setCheckable.assert_called_once_with(False)

    # Check if the stylesheet was set correctly
    faucet_mock.setStyleSheet.assert_called_once_with(
        'Text-align:left;font: 15px "Inter";color: rgb(120, 120, 120);padding: 17.5px 16px;'
        'background-image: url(:/assets/right_small.png);background-repeat: no-repeat;'
        'background-position: right center;background-origin: content;',
    )

    # Check if the click event handler was disconnected
    faucet_mock.clicked.disconnect.assert_called_once()

    # Check if the faucet click handler was connected to `show_faucet_unavailability_message`
    faucet_mock.clicked.connect.assert_called_once_with(
        widget.show_faucet_unavailability_message,
    )


def test_update_faucet_availability_when_available(create_fungible_asset_widget: FungibleAssetWidget, qtbot):
    """Test update_faucet_availability method when faucet is available."""
    widget = create_fungible_asset_widget

    # Mock the view model and sidebar
    sidebar_mock = MagicMock()
    # Mocking the faucet button (QPushButton)
    faucet_mock = MagicMock(spec=QPushButton)

    # Simulate the sidebar having a faucet
    sidebar_mock.faucet = faucet_mock
    widget._view_model.page_navigation.sidebar = MagicMock(
        return_value=sidebar_mock,
    )

    # Call the method with available=True
    widget.update_faucet_availability(available=True)

    # Verify that faucet.setCheckable(True) is called when available is True
    faucet_mock.setCheckable.assert_called_once_with(True)

    # Ensure that no stylesheet is applied when the faucet is available
    faucet_mock.setStyleSheet.assert_not_called()

    # Ensure the faucet's click event handler is not disconnected
    faucet_mock.clicked.disconnect.assert_not_called()

    # Ensure the faucet click handler is not connected to `show_faucet_unavailability_message`
    faucet_mock.clicked.connect.assert_not_called()


def test_show_faucet_unavailability_message(mocker, mock_fungible_asset_view_model):
    """Test that the show_faucet_unavailability_message method displays the correct toast message."""
    # Mock the ToastManager
    toast_manager_mock = mocker.patch(
        'src.views.ui_fungible_asset.ToastManager.info',
    )

    # Create an instance of the widget
    widget = FungibleAssetWidget(mock_fungible_asset_view_model)

    # Call the method
    widget.show_faucet_unavailability_message()

    # Verify the ToastManager.info method is called with the correct argument
    toast_manager_mock.assert_called_once_with(
        description=INFO_FAUCET_NOT_AVAILABLE,
    )


def test_stop_fungible_loading_screen(create_fungible_asset_widget):
    """Test that the stop_fungible_loading_screen method stops the loading screen and enables refresh button."""
    widget = create_fungible_asset_widget

    # Mock render_timer and translucent screen
    widget.render_timer = MagicMock()
    # Correct mangled name
    widget._FungibleAssetWidget__loading_translucent_screen = MagicMock()
    widget.title_frame = MagicMock()

    # Call the method
    widget.stop_fungible_loading_screen()

    # Verify the render_timer and translucent screen are stopped
    widget.render_timer.stop.assert_called_once()
    widget._FungibleAssetWidget__loading_translucent_screen.stop.assert_called_once()

    # Verify the refresh button is enabled
    widget.title_frame.refresh_page_button.setDisabled.assert_called_once_with(
        False,
    )


def test_fungible_show_message_success(create_fungible_asset_widget):
    """Test the show_message method for success scenario."""
    message = 'Success message'

    with patch('src.views.ui_fungible_asset.ToastManager.success') as mock_success:
        create_fungible_asset_widget.show_message(ToastPreset.SUCCESS, message)
        mock_success.assert_called_once_with(description=message)


def test_fungible_show_message_error(create_fungible_asset_widget):
    """Test the show_message method for error scenario."""
    message = 'Error message'

    with patch('src.views.ui_fungible_asset.ToastManager.error') as mock_error:
        create_fungible_asset_widget.show_message(ToastPreset.ERROR, message)
        mock_error.assert_called_once_with(description=message)


def test_fungible_show_message_information(create_fungible_asset_widget):
    """Test the show_message method for information scenario."""
    message = 'Information message'

    with patch('src.views.ui_fungible_asset.ToastManager.info') as mock_info:
        create_fungible_asset_widget.show_message(
            ToastPreset.INFORMATION, message,
        )
        mock_info.assert_called_once_with(description=message)


def test_fungible_show_message_warning(create_fungible_asset_widget):
    """Test the show_message method for warning scenario."""
    message = 'Warning message'

    with patch('src.views.ui_fungible_asset.ToastManager.warning') as mock_warning:
        create_fungible_asset_widget.show_message(ToastPreset.WARNING, message)
        mock_warning.assert_called_once_with(description=message)


def test_handle_backup_visibility(create_fungible_asset_widget):
    """Test that handle_backup_visibility shows or hides the backup button based on wallet type."""
    widget = create_fungible_asset_widget

    # Mock the view model and sidebar
    sidebar_mock = MagicMock()
    backup_mock = MagicMock()
    sidebar_mock.backup = backup_mock
    widget._view_model.page_navigation.sidebar = MagicMock(
        return_value=sidebar_mock,
    )

    # Mock the SettingRepository to return CONNECT_TYPE_WALLET
    with patch('src.views.ui_fungible_asset.SettingRepository.get_wallet_type') as mock_get_wallet_type:
        # Test for CONNECT_TYPE_WALLET
        mock_get_wallet_type.return_value = WalletType.REMOTE_TYPE_WALLET

        # Call the method
        widget.handle_backup_visibility()

        # Verify that the backup button is hidden
        sidebar_mock.backup.hide.assert_called_once()
        sidebar_mock.backup.show.assert_not_called()

        # Reset mocks for the next scenario
        sidebar_mock.backup.hide.reset_mock()
        sidebar_mock.backup.show.reset_mock()

        # Test for EMBEDDED_TYPE_WALLET
        mock_get_wallet_type.return_value = WalletType.EMBEDDED_TYPE_WALLET

        # Call the method
        widget.handle_backup_visibility()

        # Verify that the backup button is shown
        sidebar_mock.backup.show.assert_called_once()
        sidebar_mock.backup.hide.assert_not_called()


def test_refresh_asset(create_fungible_asset_widget):
    """Test that refresh_asset starts the render timer and refreshes the asset list."""
    widget = create_fungible_asset_widget

    # Mock the render timer and the main asset view model
    widget.render_timer = MagicMock()
    widget._view_model.main_asset_view_model = MagicMock()

    # Call the method
    widget.refresh_asset()

    # Verify that the render timer is started
    widget.render_timer.start.assert_called_once()

    # Verify that the asset list is refreshed with a hard refresh
    widget._view_model.main_asset_view_model.get_assets.assert_called_once_with(
        rgb_asset_hard_refresh=True,
    )


def test_handle_asset_frame_click(create_fungible_asset_widget):
    """Test that handle_asset_frame_click navigates correctly based on asset type."""
    widget = create_fungible_asset_widget

    # Mock the view model and navigation methods
    widget._view_model.page_navigation = MagicMock()
    widget._view_model.cfa_view_model = MagicMock()

    # Test for Bitcoin asset type
    bitcoin_asset_id = 'btc_asset_id'
    bitcoin_asset_name = 'Bitcoin'
    bitcoin_image_path = ':/assets/bitcoin.png'
    bitcoin_asset_type = AssetType.BITCOIN.value

    widget.handle_asset_frame_click(
        asset_id=bitcoin_asset_id,
        asset_name=bitcoin_asset_name,
        image_path=bitcoin_image_path,
        asset_type=bitcoin_asset_type,
    )

    # Verify navigation to Bitcoin page
    widget._view_model.page_navigation.bitcoin_page.assert_called_once()
    widget._view_model.cfa_view_model.asset_info.emit.assert_not_called()
    widget._view_model.page_navigation.cfa_detail_page.assert_not_called()

    # Reset mocks for the next scenario
    widget._view_model.page_navigation.bitcoin_page.reset_mock()

    # Test for RGB asset type
    rgb_asset_id = 'rgb_asset_id'
    rgb_asset_name = 'RGB Asset'
    rgb_image_path = ':/assets/rgb.png'
    rgb_asset_type = AssetType.CFA.value

    widget.handle_asset_frame_click(
        asset_id=rgb_asset_id,
        asset_name=rgb_asset_name,
        image_path=rgb_image_path,
        asset_type=rgb_asset_type,
    )

    # Verify asset_info signal is emitted with correct parameters
    widget._view_model.cfa_view_model.asset_info.emit.assert_called_once_with(
        rgb_asset_id, rgb_asset_name, rgb_image_path, rgb_asset_type,
    )

    # Verify navigation to RGB detail page
    widget._view_model.page_navigation.cfa_detail_page.assert_called_once_with(
        RgbAssetPageLoadModel(asset_type=rgb_asset_type),
    )

    # Verify Bitcoin page navigation is not triggered
    widget._view_model.page_navigation.bitcoin_page.assert_not_called()


def test_create_fungible_card(create_fungible_asset_widget, qtbot):
    """Test that create_fungible_card creates and configures the fungible card correctly."""
    widget = create_fungible_asset_widget

    # Mock the dependencies
    widget.fungibles_widget = MagicMock()
    widget.vertical_layout_3 = MagicMock()
    widget._view_model = MagicMock()

    # Create a sample asset
    asset = MagicMock()
    asset.asset_id = 'sample_asset_id'
    asset.name = 'Sample Asset'
    asset.balance.future = 1000
    asset.balance.offchain_outbound = 200
    asset.ticker = 'SAMPLE'

    widget.create_fungible_card(asset)

    # Verify the fungible_frame is created with the correct settings
    assert widget.fungible_frame is not None
    assert widget.fungible_frame.objectName() == 'frame_4'
    assert widget.fungible_frame.minimumSize() == QSize(900, 70)
    assert widget.fungible_frame.maximumSize() == QSize(16777215, 70)

    # Verify asset_name is set correctly
    assert widget.asset_name.text() == asset.name
    assert widget.asset_name.minimumSize() == QSize(135, 40)

    # Verify address is set correctly for NIA
    assert widget.address.text() == asset.asset_id

    # Verify amount is set
    assert widget.amount.text() == str(asset.balance.future)

    # Verify outbound_balance is set for NIA
    assert widget.outbound_balance.text() == str(asset.balance.offchain_outbound)

    # Verify token_symbol is set
    assert widget.token_symbol.text() == asset.ticker

    widget.create_fungible_card(asset, img_path=':/assets/sample_icon.png')

    # Verify that the fungible frame is added to the layout
    widget.vertical_layout_3.addWidget.assert_called()

    # Test for Bitcoin-specific behavior
    asset.name = 'Bitcoin'

    # Test for BTC (mainnet Bitcoin)
    asset.ticker = TokenSymbol.BITCOIN.value
    widget.create_fungible_card(asset)
    assert widget.token_symbol.text() == TokenSymbol.SAT.value
    assert widget.asset_name.text() == AssetType.BITCOIN.value.lower()

    # Test for TESTNET4_BITCOIN
    with patch('src.views.ui_fungible_asset.SettingRepository.get_wallet_network', return_value=NetworkEnumModel.TESTNET4):
        asset.ticker = TokenSymbol.TESTNET4_BITCOIN.value
        widget.create_fungible_card(asset)
        assert widget.token_symbol.text() == TokenSymbol.SAT.value
        assert widget.asset_name.text() == f'{NetworkEnumModel.TESTNET4.value} {
            AssetType.BITCOIN.value.lower()
        }'

    # Test for TESTNET_BITCOIN
    with patch('src.views.ui_fungible_asset.SettingRepository.get_wallet_network', return_value=NetworkEnumModel.TESTNET):
        asset.ticker = TokenSymbol.TESTNET_BITCOIN.value
        widget.create_fungible_card(asset)
        assert widget.token_symbol.text() == TokenSymbol.SAT.value
        assert widget.asset_name.text() == f'{NetworkEnumModel.TESTNET.value} {
            AssetType.BITCOIN.value.lower()
        }'

    # Test for REGTEST_BITCOIN
    with patch('src.views.ui_fungible_asset.SettingRepository.get_wallet_network', return_value=NetworkEnumModel.REGTEST):
        asset.ticker = TokenSymbol.REGTEST_BITCOIN.value
        widget.create_fungible_card(asset)
        assert widget.token_symbol.text() == TokenSymbol.SAT.value
        assert widget.asset_name.text() == f'{NetworkEnumModel.REGTEST.value} {
            AssetType.BITCOIN.value.lower()
        }'


def test_show_assets(create_fungible_asset_widget, qtbot):
    """Test the show_assets method to ensure assets are cleared and the Bitcoin address signal is managed correctly."""

    widget = create_fungible_asset_widget

    # Mock dependencies
    widget._view_model = MagicMock()
    widget._view_model.receive_bitcoin_view_model = MagicMock()
    widget._view_model.receive_bitcoin_view_model.get_bitcoin_address = MagicMock()
    widget._view_model.receive_bitcoin_view_model.address = MagicMock()

    # Set up a vertical layout with real widgets (instead of MagicMock) to test deletion
    widget.vertical_layout_3 = QVBoxLayout()
    widget1 = QWidget()  # Use a real QWidget
    widget2 = QWidget()  # Use a real QWidget

    # Add widgets to the layout
    widget.vertical_layout_3.addWidget(widget1)
    widget.vertical_layout_3.addWidget(widget2)

    # Initial state assertions
    assert widget.vertical_layout_3.count() == 2  # Two widgets added

    # Set the signal_connected flag to True to test signal disconnection
    widget.signal_connected = True

    # Mock asset with proper attributes
    asset = MagicMock()
    asset.name = 'Bitcoin'  # Mock the 'name' attribute to return a string
    asset.asset_id = 'asset123'  # Mock the 'asset_id' attribute
    asset.ticker = 'BTC'

    # Mock the assets in the view model (if needed)
    widget._view_model.main_asset_view_model.assets.vanilla = asset

    # Call show_assets
    widget.show_assets()
