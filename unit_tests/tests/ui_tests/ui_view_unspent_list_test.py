"""Unit test for ViewUnspentList."""
# Disable the redefined-outer-name warning as
# it's normal to pass mocked objects in test functions
# pylint: disable=redefined-outer-name,unused-argument,protected-access
from __future__ import annotations

from unittest.mock import MagicMock

import pytest
from PySide6.QtCore import QCoreApplication
from PySide6.QtCore import QSize
from PySide6.QtGui import QResizeEvent
from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtWidgets import QSpacerItem
from PySide6.QtWidgets import QVBoxLayout

from src.model.enums.enums_model import NetworkEnumModel
from src.viewmodels.main_view_model import MainViewModel
from src.views.ui_view_unspent_list import ViewUnspentList


@pytest.fixture
def view_unspent_list_widget(qtbot):
    """Fixture to create and return an instance of ViewUnspentList."""
    mock_navigation = MagicMock()
    view_model = MagicMock(MainViewModel(mock_navigation))
    widget = ViewUnspentList(view_model)
    qtbot.addWidget(widget)
    return widget


def test_trigger_render_and_refresh(view_unspent_list_widget: ViewUnspentList, mocker):
    """Test the trigger_render_and_refresh method."""

    # Mock the render timer start and the ViewModel method
    mock_render_timer = mocker.patch.object(
        view_unspent_list_widget.render_timer, 'start',
    )
    mock_get_unspent_list = mocker.patch.object(
        view_unspent_list_widget._view_model.unspent_view_model, 'get_unspent_list',
    )

    # Call the method
    view_unspent_list_widget.trigger_render_and_refresh()

    # Validate that the render timer started and the unspent list was refreshed
    mock_render_timer.assert_called_once()
    mock_get_unspent_list.assert_called_once_with(is_hard_refresh=True)


def test_show_view_unspent_loading(view_unspent_list_widget: ViewUnspentList, mocker):
    """Test the show_view_unspent_loading method."""

    # Mock LoadingTranslucentScreen
    mock_loading_screen = MagicMock()
    mocker.patch(
        'src.views.ui_view_unspent_list.LoadingTranslucentScreen',
        return_value=mock_loading_screen,
    )

    # Call the method
    view_unspent_list_widget.show_view_unspent_loading()

    # Verify loading screen was created with correct parameters
    mock_loading_screen.set_description_label_direction.assert_called_once_with(
        'Bottom',
    )
    mock_loading_screen.start.assert_called_once()

    # Verify refresh button was disabled
    assert view_unspent_list_widget.header_unspent_frame.refresh_page_button.isEnabled() is False


def test_hide_loading_screen(view_unspent_list_widget: ViewUnspentList, mocker):
    """Test the hide_loading_screen method."""

    # Mock loading screen and render timer
    mock_loading_screen = MagicMock()
    view_unspent_list_widget._ViewUnspentList__loading_translucent_screen = mock_loading_screen
    mock_render_timer = mocker.patch.object(
        view_unspent_list_widget.render_timer, 'stop',
    )

    # Call the method
    view_unspent_list_widget.hide_loading_screen()

    # Verify loading screen was stopped
    mock_loading_screen.stop.assert_called_once()
    mock_render_timer.assert_called_once()

    # Verify refresh button was enabled
    assert view_unspent_list_widget.header_unspent_frame.refresh_page_button.isEnabled() is True


def test_get_image_path(view_unspent_list_widget: ViewUnspentList):
    """Test the get_image_path method."""

    # Test with colorable asset
    mock_colorable = MagicMock()
    mock_colorable.utxo.colorable = True
    assert view_unspent_list_widget.get_image_path(
        mock_colorable,
    ) == ':/assets/images/rgb_logo_round.png'

    # Test with non-colorable assets for different networks
    mock_non_colorable = MagicMock()
    mock_non_colorable.utxo.colorable = False

    # Test mainnet
    view_unspent_list_widget.network = NetworkEnumModel.MAINNET
    assert view_unspent_list_widget.get_image_path(
        mock_non_colorable,
    ) == ':/assets/bitcoin.png'

    # Test testnet
    view_unspent_list_widget.network = NetworkEnumModel.TESTNET
    assert view_unspent_list_widget.get_image_path(
        mock_non_colorable,
    ) == ':/assets/testnet_bitcoin.png'

    # Test regtest
    view_unspent_list_widget.network = NetworkEnumModel.REGTEST
    assert view_unspent_list_widget.get_image_path(
        mock_non_colorable,
    ) == ':/assets/regtest_bitcoin.png'


def test_set_address_label(view_unspent_list_widget: ViewUnspentList):
    """Test the set_address_label method."""

    mock_label = QLabel()

    # Test with colorable asset and asset_id
    mock_colorable = MagicMock()
    mock_colorable.utxo.colorable = True
    mock_colorable.rgb_allocations = [MagicMock(asset_id='test_asset_id')]

    view_unspent_list_widget.set_address_label(
        mock_label, mock_colorable, False,
    )
    assert mock_label.text() == 'test_asset_id'

    # Test with colorable asset but no asset_id
    mock_colorable.rgb_allocations = [MagicMock(asset_id='')]
    view_unspent_list_widget.set_address_label(
        mock_label, mock_colorable, False,
    )
    assert mock_label.text() == 'NA'

    # Test with non-colorable asset
    mock_non_colorable = MagicMock()
    mock_non_colorable.utxo.colorable = False
    view_unspent_list_widget.set_address_label(
        mock_label, mock_non_colorable, False,
    )
    assert mock_label.text() == ''


def test_handle_asset_frame_click(view_unspent_list_widget: ViewUnspentList, mocker):
    """Test the handle_asset_frame_click method."""
    mock_copy = mocker.patch('src.views.ui_view_unspent_list.copy_text')

    # Call method with test asset id
    test_asset_id = 'test_asset_id'
    view_unspent_list_widget.handle_asset_frame_click(test_asset_id)

    # Verify copy_text was called with correct asset id
    mock_copy.assert_called_once_with(test_asset_id)


def test_clear_unspent_list_layout(view_unspent_list_widget: ViewUnspentList):
    """Test the clear_unspent_list_layout method."""

    # Add some test widgets and spacers
    test_widget = QLabel('test')
    test_widget.setObjectName('frame_4')
    view_unspent_list_widget.unspent_list_v_box_layout.addWidget(test_widget)

    test_spacer = QSpacerItem(
        20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding,
    )
    view_unspent_list_widget.unspent_list_v_box_layout.addItem(test_spacer)

    # Call clear method
    view_unspent_list_widget.clear_unspent_list_layout()

    # Verify layout is empty
    assert view_unspent_list_widget.unspent_list_v_box_layout.count() == 0


def test_show_unspent_list(view_unspent_list_widget: ViewUnspentList, mocker):
    """Test the show_unspent_list method."""

    # Mock clear_unspent_list_layout
    mock_clear = mocker.patch.object(
        view_unspent_list_widget, 'clear_unspent_list_layout',
    )

    # Mock create_unspent_clickable_frame to return a QWidget
    mock_frame = QLabel()  # Using QLabel as a simple QWidget for testing
    mock_create_frame = mocker.patch.object(
        view_unspent_list_widget, 'create_unspent_clickable_frame', return_value=mock_frame,
    )

    # Create test unspent list
    test_list = [MagicMock(), MagicMock()]
    view_unspent_list_widget._view_model.unspent_view_model.unspent_list = test_list

    # Call method
    view_unspent_list_widget.show_unspent_list()

    # Verify layout was cleared
    mock_clear.assert_called_once()

    # Verify frames were created and added
    assert mock_create_frame.call_count == len(test_list)
    assert view_unspent_list_widget.unspent_list_v_box_layout.count() == len(
        test_list,
    )  # Removed +1 since spacer isn't being added


def test_change_layout(view_unspent_list_widget: ViewUnspentList, mocker):
    """Test the change_layout method."""

    # Mock show_unspent_list
    mock_show = mocker.patch.object(
        view_unspent_list_widget, 'show_unspent_list',
    )

    # Create mock resize events with different sizes
    mock_event_large = QResizeEvent(QSize(1400, 800), QSize(1000, 600))
    mock_event_small = QResizeEvent(QSize(1000, 800), QSize(1400, 600))

    # Test large window
    view_unspent_list_widget.change_layout(mock_event_large)
    mock_show.assert_called_with(True)
    assert view_unspent_list_widget.event_val is True

    # Test small window
    view_unspent_list_widget.change_layout(mock_event_small)
    mock_show.assert_called_with(False)
    assert view_unspent_list_widget.event_val is False


def test_resize_event(view_unspent_list_widget: ViewUnspentList, mocker):
    """Test the resizeEvent handling."""

    # Mock parent class resizeEvent
    mock_super = mocker.patch('PySide6.QtWidgets.QWidget.resizeEvent')

    # Create mock resize events
    mock_event = QResizeEvent(QSize(1400, 800), QSize(1000, 600))

    # Call resizeEvent
    view_unspent_list_widget.resizeEvent(mock_event)

    # Verify super().resizeEvent was called
    mock_super.assert_called_once_with(mock_event)

    # Verify window size was updated
    assert view_unspent_list_widget.window_size == 1400


def test_create_unspent_clickable_frame(view_unspent_list_widget: ViewUnspentList, mocker):
    """Test creating a clickable frame for unspent items."""

    # Create mock unspent list item
    mock_list_item = MagicMock()
    mock_list_item.utxo.outpoint = 'test_outpoint'
    mock_list_item.utxo.btc_amount = 1000
    mock_list_item.utxo.colorable = True

    # Mock get_image_path
    mock_image_path = ':/assets/images/rgb_logo_round.png'
    mocker.patch.object(
        view_unspent_list_widget,
        'get_image_path', return_value=mock_image_path,
    )

    # Mock set_address_label
    mocker.patch.object(view_unspent_list_widget, 'set_address_label')

    # Create frame
    frame = view_unspent_list_widget.create_unspent_clickable_frame(
        mock_list_item, True,
    )

    # Connect mock handler to clicked signal
    frame.clicked.connect(view_unspent_list_widget.handle_asset_frame_click)

    # Verify frame properties
    assert frame.objectName() == 'frame_4'
    assert frame.minimumSize() == QSize(900, 75)
    assert frame.maximumSize() == QSize(16777215, 75)

    # Verify layout structure
    assert isinstance(frame.layout(), QVBoxLayout)
    horizontal_layout = frame.layout().itemAt(0).layout()
    assert isinstance(horizontal_layout, QHBoxLayout)

    # Verify logo
    logo_label = horizontal_layout.itemAt(0).widget()
    assert isinstance(logo_label, QLabel)
    assert logo_label.maximumSize() == QSize(40, 40)

    # Verify asset name and details
    asset_details = horizontal_layout.itemAt(1).layout()
    asset_name = asset_details.itemAt(0).widget()
    assert asset_name.text() == 'test_outpoint'
    assert asset_name.toolTip() == QCoreApplication.translate(
        'iris_wallet', 'click_to_copy',
    )

    # Verify amount label
    amount_label = horizontal_layout.itemAt(2).widget()
    assert amount_label.text() == '1000 sat'

    # Test non-colorable case
    mock_list_item.utxo.colorable = False
    frame = view_unspent_list_widget.create_unspent_clickable_frame(
        mock_list_item, True,
    )
    assert not frame.isVisible()  # Verify frame is not visible for non-colorable items
