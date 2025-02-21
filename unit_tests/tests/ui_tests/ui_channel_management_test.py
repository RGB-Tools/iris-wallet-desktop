"""Unit test for channel management UI"""
# Disable the redefined-outer-name warning as
# it's normal to pass mocked object in tests function
# pylint: disable=redefined-outer-name,unused-argument,protected-access
from __future__ import annotations

from unittest.mock import MagicMock
from unittest.mock import patch

import pytest
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QFrame
from PySide6.QtWidgets import QGraphicsBlurEffect
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QWidget

from src.model.channels_model import ChannelDetailDialogModel
from src.viewmodels.channel_management_viewmodel import ChannelManagementViewModel
from src.viewmodels.main_view_model import MainViewModel
from src.views.ui_channel_detail_dialog import ChannelDetailDialogBox
from src.views.ui_channel_management import ChannelManagement


@pytest.fixture
def channel_management_page_navigation():
    """Fixture to create a mocked page navigation object."""
    return MagicMock()


@pytest.fixture
def mock_channel_management_view_model(channel_management_page_navigation):
    """Fixture to create a MainViewModel instance."""
    mock_view_model = MagicMock(
        spec=MainViewModel(
            channel_management_page_navigation,
        ),
    )
    mock_view_model.channel_view_model = MagicMock(
        spec=ChannelManagementViewModel(channel_management_page_navigation),
    )
    return mock_view_model


@pytest.fixture
def channel_management_widget(mock_channel_management_view_model, qtbot):
    """Fixture to create the ChannelManagement instance."""
    widget = ChannelManagement(mock_channel_management_view_model)
    qtbot.addWidget(widget)
    return widget


def test_initial_ui_elements(channel_management_widget):
    """Test initial UI elements of ChannelManagement."""
    assert isinstance(
        channel_management_widget.vertical_layout_channel, QVBoxLayout,
    )
    assert channel_management_widget.header_frame is not None
    assert channel_management_widget.sort_combobox.currentText() == 'Counter party'
    assert isinstance(channel_management_widget.channel_list_widget, QWidget)


def test_show_available_channels_positive(channel_management_widget, qtbot):
    """Test show_available_channels with valid data."""
    # Mock channel data
    mock_channel = MagicMock()
    mock_channel.peer_pubkey = 'abc123'
    mock_channel.asset_local_amount = 1000
    mock_channel.asset_remote_amount = 500
    mock_channel.asset_id = 'asset123'
    mock_channel.ready = True
    channel_management_widget._view_model.channel_view_model.channels = [
        mock_channel,
    ]

    channel_management_widget.show_available_channels()

    assert channel_management_widget.list_v_box_layout.count() > 1
    assert isinstance(channel_management_widget.list_frame, QFrame)
    assert isinstance(channel_management_widget.local_balance_value, QLabel)
    assert isinstance(channel_management_widget.remote_balance_value, QLabel)
    assert channel_management_widget.local_balance_value.text() == '1000'
    assert channel_management_widget.remote_balance_value.text() == '500'


def test_show_available_channels_no_channels(channel_management_widget):
    """Test show_available_channels with no channels."""
    channel_management_widget._view_model.channel_view_model.channels = []

    channel_management_widget.show_available_channels()

    # Ensure that no channels are displayed
    assert channel_management_widget.list_v_box_layout.count() == 1  # Only spacer
    assert channel_management_widget.list_frame is None  # No frame created


def test_show_available_channels_invalid_data(channel_management_widget):
    """Test show_available_channels with invalid data (None for mandatory fields)."""
    # Mock channel with missing mandatory fields
    mock_channel = MagicMock()
    mock_channel.peer_pubkey = None
    mock_channel.asset_local_amount = None
    mock_channel.asset_remote_amount = None
    mock_channel.asset_id = None
    mock_channel.ready = None
    channel_management_widget._view_model.channel_view_model.channels = [
        mock_channel,
    ]

    channel_management_widget.show_available_channels()

    # Ensure that no information is displayed if mandatory fields are missing
    # Only spacer (no frame added)
    assert channel_management_widget.list_v_box_layout.count() == 1
    assert channel_management_widget.list_frame is None  # No frame created


def test_retranslate_ui(channel_management_widget):
    """Test retranslate_ui method."""
    channel_management_widget.retranslate_ui()
    assert channel_management_widget.header_frame.action_button.text() == 'create_channel'


def test_hide_loading_screen(channel_management_widget):
    """Test hide_loading_screen method."""

    channel_management_widget.channel_management_loading_screen = MagicMock()

    channel_management_widget.channel_management_loading_screen.isVisible.return_value = True

    channel_management_widget.hide_loading_screen()

    channel_management_widget.channel_management_loading_screen.stop.assert_called_once()
    channel_management_widget.channel_management_loading_screen.make_parent_disabled_during_loading.assert_called_once_with(
        False,
    )

    channel_management_widget.channel_management_loading_screen.isVisible.return_value = False
    assert not channel_management_widget.channel_management_loading_screen.isVisible()


@patch('src.utils.helpers.create_circular_pixmap')
def test_show_available_channels_with_none_asset_id(mock_create_pixmap, channel_management_widget):
    """Test `show_available_channels` with None asset_id method."""
    # Mock the return value of create_circular_pixmap to be a QPixmap instance
    mock_create_pixmap.return_value = QPixmap(16, 16)

    # Mock the channel data with asset_id set to None
    mock_channel = MagicMock()
    mock_channel.peer_pubkey = 'mock_pubkey'
    mock_channel.asset_local_amount = 1000
    mock_channel.asset_remote_amount = 500
    mock_channel.asset_id = None  # This triggers the special case
    mock_channel.ready = True
    mock_channel.channel_id = 'mock_channel_id'
    mock_channel.outbound_balance_msat = 1000000
    mock_channel.inbound_balance_msat = 500000
    channel_management_widget._view_model.channel_view_model.channels = [
        mock_channel,
    ]

    with patch('src.data.repository.setting_repository.SettingRepository.get_wallet_network') as mock_get_network, \
            patch('src.data.service.helpers.main_asset_page_helper.get_offline_asset_ticker') as mock_get_ticker:

        # Create a mock for NetworkEnumModel and set its 'value' attribute
        mock_network = MagicMock()
        mock_network.value = 'mainnet'  # Set the value you want to test

        # Set the mock return values
        mock_get_network.return_value = mock_network  # Return the mock network
        mock_get_ticker.return_value = 'mock_ticker'

        # Call the method that uses the network mock
        channel_management_widget.show_available_channels()

        # Assertions to verify the correct display of channel information
        # 1 for the channel, 1 for the spacer
        assert channel_management_widget.list_v_box_layout.count() == 2
        assert channel_management_widget.list_frame.findChild(
            QLabel, 'local_balance_value',
        ).text() == '1000'
        assert channel_management_widget.list_frame.findChild(
            QLabel, 'remote_balance_value',
        ).text() == '500'


@patch('src.utils.helpers.create_circular_pixmap')
def test_show_available_channels_with_invalid_channel(mock_create_pixmap, channel_management_widget):
    """Test `show_available_channels` with an invalid channel."""
    # Mock the return value of create_circular_pixmap to be a QPixmap instance
    mock_create_pixmap.return_value = QPixmap(16, 16)

    # Mock an invalid channel (missing mandatory fields)
    mock_channel = MagicMock()
    mock_channel.peer_pubkey = None  # Invalid peer_pubkey
    mock_channel.asset_local_amount = 1000
    mock_channel.asset_remote_amount = 500
    mock_channel.asset_id = None  # Invalid asset_id
    mock_channel.ready = False  # Not ready
    channel_management_widget._view_model.channel_view_model.channels = [
        mock_channel,
    ]

    channel_management_widget.show_available_channels()

    # Ensure that no information is displayed for an invalid channel
    assert channel_management_widget.list_v_box_layout.count() == 1  # Only spacer
    assert channel_management_widget.list_frame is None  # No frame created


@patch('src.utils.helpers.create_circular_pixmap')
def test_show_available_channels_with_asset_id(mock_create_pixmap, channel_management_widget):
    """Test `show_available_channels` with valid asset_id."""
    # Mock the return value of create_circular_pixmap to be a QPixmap instance
    mock_create_pixmap.return_value = QPixmap(16, 16)

    # Mock valid channel data with asset_id
    mock_channel = MagicMock()
    mock_channel.peer_pubkey = 'mock_pubkey'
    mock_channel.asset_local_amount = 777
    mock_channel.asset_remote_amount = 0
    mock_channel.asset_id = 'rgb:2dkSTbr-jFhznbPmo-TQafzswCN-av4gTsJjX-ttx6CNou5-M98k8Zd'
    mock_channel.ready = True
    channel_management_widget._view_model.channel_view_model.channels = [
        mock_channel,
    ]

    channel_management_widget.show_available_channels()

    # Assertions to verify the correct display of channel information
    # 1 for the channel, 1 for spacer
    assert channel_management_widget.list_v_box_layout.count() == 2
    assert channel_management_widget.list_frame.findChild(
        QLabel, 'local_balance_value',
    ).text() == '777'
    assert channel_management_widget.list_frame.findChild(
        QLabel, 'remote_balance_value',
    ).text() == '0'
    tooltip = channel_management_widget.list_frame.findChild(
        QLabel, 'status_pixmap',
    ).toolTip()
    assert tooltip == 'opening'
    asset_label = channel_management_widget.list_frame.findChild(
        QLabel, 'asset_id',
    )
    assert asset_label is not None
    assert asset_label.text() == 'rgb:2dkSTbr-jFhznbPmo-TQafzswCN-av4gTsJjX-ttx6CNou5-M98k8Zd'


def test_show_available_channels_empty_data(channel_management_widget):
    """Test show_available_channels with empty channel data."""
    # Mock a channel with empty fields
    mock_channel = MagicMock()
    mock_channel.peer_pubkey = ''
    mock_channel.asset_local_amount = ''
    mock_channel.asset_remote_amount = ''
    mock_channel.asset_id = ''
    mock_channel.ready = None
    channel_management_widget._view_model.channel_view_model.channels = [
        mock_channel,
    ]

    channel_management_widget.show_available_channels()

    # Ensure that no information is displayed for an empty channel
    assert channel_management_widget.list_v_box_layout.count() == 1  # Only spacer
    assert channel_management_widget.list_frame is None  # No frame created


def test_create_channel_button_click(channel_management_widget):
    """Test the create_channel_button click functionality."""
    channel_management_widget.header_frame.action_button.clicked.emit()
    assert channel_management_widget._view_model.channel_view_model.navigate_to_create_channel_page.call_count == 1


def test_channel_creation_button_click(channel_management_widget):
    """Test the create channel button."""
    channel_management_widget.header_frame.action_button.clicked.emit()
    assert channel_management_widget._view_model.channel_view_model.navigate_to_create_channel_page.call_count == 1


def test_trigger_render_and_refresh(channel_management_widget):
    """Test the trigger_render_and_refresh method."""
    # Mock the channel_ui_render_timer and view model methods
    channel_management_widget.channel_ui_render_timer = MagicMock()
    channel_management_widget._view_model.channel_view_model.available_channels = MagicMock()
    channel_management_widget._view_model.channel_view_model.get_asset_list = MagicMock()

    # Call the method that triggers the render and refresh
    channel_management_widget.trigger_render_and_refresh()

    # Ensure that the channel UI render timer starts
    channel_management_widget.channel_ui_render_timer.start.assert_called_once()

    # Ensure that the available_channels and get_asset_list methods are called
    channel_management_widget._view_model.channel_view_model.available_channels.assert_called_once()
    channel_management_widget._view_model.channel_view_model.get_asset_list.assert_called_once()


@patch('src.views.ui_channel_management.LoadingTranslucentScreen')
def test_show_channel_management_loading(mock_loading_screen, channel_management_widget):
    """Test the show_channel_management_loading method."""

    # Mock the LoadingTranslucentScreen class to avoid actual UI rendering
    mock_loading_screen_instance = MagicMock()
    mock_loading_screen.return_value = mock_loading_screen_instance

    # Mock the header_frame to be a MagicMock object
    channel_management_widget.header_frame = MagicMock()

    # Call the method that shows the loading screen
    channel_management_widget.show_channel_management_loading()

    # Ensure that LoadingTranslucentScreen is created with the correct parameters
    mock_loading_screen.assert_called_once_with(
        parent=channel_management_widget, description_text='Loading', dot_animation=True,
    )

    # Ensure set_description_label_direction is called with 'Bottom'
    mock_loading_screen_instance.set_description_label_direction.assert_called_once_with(
        'Bottom',
    )

    # Ensure the start method is called
    mock_loading_screen_instance.start.assert_called_once()

    # Ensure make_parent_disabled_during_loading is called with True
    mock_loading_screen_instance.make_parent_disabled_during_loading.assert_called_once_with(
        True,
    )

    # Ensure that the header frame is disabled
    channel_management_widget.header_frame.setDisabled.assert_called_once_with(
        True,
    )


def test_show_available_channels_status_change(channel_management_widget, qtbot):
    """Test UI updates when channel status changes."""
    # Create mock channel
    mock_channel = MagicMock()
    mock_channel.peer_pubkey = 'abc123'
    mock_channel.asset_local_amount = 1000
    mock_channel.asset_remote_amount = 500
    mock_channel.asset_id = 'asset123'
    mock_channel.ready = True
    mock_channel.status = 'Closing'  # Initially "Closing"

    channel_management_widget._view_model.channel_view_model.channels = [
        mock_channel,
    ]

    channel_management_widget.show_available_channels()

    # Assert status color and tooltip for "Closing"
    assert channel_management_widget.list_frame.findChild(
        QLabel, 'status_pixmap',
    ).toolTip() == 'closing'

    # Change channel status
    mock_channel.status = 'Opening'
    channel_management_widget.show_available_channels()

    # Assert status color and tooltip for "Opening"
    assert channel_management_widget.list_frame.findChild(
        QLabel, 'status_pixmap',
    ).toolTip() == 'opening'


def test_channel_detail_event(channel_management_widget):
    """Test the channel_detail_event method."""

    # Mock the required parameters
    channel_id = 'mock_channel_id'
    pub_key = 'mock_pub_key'
    bitcoin_local_balance = 1000
    bitcoin_remote_balance = 500

    # Mock the view model's page_navigation
    channel_management_widget._view_model.page_navigation = MagicMock()

    # Patch ChannelDetailDialogBox and ChannelDetailDialogModel to avoid actual dialog instantiation
    with patch('src.views.ui_channel_management.ChannelDetailDialogBox') as mock_channel_detail_dialog_box, \
            patch('src.views.ui_channel_management.ChannelDetailDialogModel') as mock_channel_detail_dialog_model, \
            patch.object(channel_management_widget, 'setGraphicsEffect') as mock_set_graphics_effect:

        # Set up the mock return values
        mock_channel_detail_dialog_model.return_value = MagicMock(
            spec=ChannelDetailDialogModel,
        )
        mock_channel_detail_dialog_box.return_value = MagicMock(
            spec=ChannelDetailDialogBox,
        )

        # Call the method
        channel_management_widget.channel_detail_event(
            channel_id, pub_key, bitcoin_local_balance, bitcoin_remote_balance,
        )

        # Assertions

        # Assert that ChannelDetailDialogModel was initialized with correct parameters
        mock_channel_detail_dialog_model.assert_called_once_with(
            pub_key=pub_key,
            channel_id=channel_id,
            bitcoin_local_balance=bitcoin_local_balance,
            bitcoin_remote_balance=bitcoin_remote_balance,
        )

        # Assert that ChannelDetailDialogBox was initialized with the correct parameters
        mock_channel_detail_dialog_box.assert_called_once_with(
            page_navigate=channel_management_widget._view_model.page_navigation,
            param=mock_channel_detail_dialog_model.return_value,
            parent=channel_management_widget,
        )

        # Assert that the QGraphicsBlurEffect was applied to the widget
        # Ensure that setGraphicsEffect was called
        mock_set_graphics_effect.assert_called_once()
        # Get the first argument passed to setGraphicsEffect
        blur_effect = mock_set_graphics_effect.call_args[0][0]
        assert isinstance(blur_effect, QGraphicsBlurEffect)
        assert blur_effect.blurRadius() == 10  # Check if blur radius is set to 10

        # Assert that the exec method was called on the dialog box
        mock_channel_detail_dialog_box.return_value.exec.assert_called_once()


@patch('src.utils.helpers.create_circular_pixmap')
def test_show_available_channels_with_asset_id_lookup(mock_create_pixmap, channel_management_widget):
    """Test show_available_channels with asset lookup functionality."""
    # Mock the return value of create_circular_pixmap to be a QPixmap instance
    mock_create_pixmap.return_value = QPixmap(16, 16)

    # Mock valid channel data with asset_id
    mock_channel = MagicMock()
    mock_channel.peer_pubkey = 'mock_pubkey'
    mock_channel.asset_local_amount = 777
    mock_channel.asset_remote_amount = 0
    mock_channel.asset_id = 'test_asset_123'
    mock_channel.ready = True

    # Set up the asset lookup dictionary
    channel_management_widget._view_model.channel_view_model.total_asset_lookup_list = {
        'test_asset_123': 'Test Asset Name',
    }

    channel_management_widget._view_model.channel_view_model.channels = [
        mock_channel,
    ]

    channel_management_widget.show_available_channels()

    # Assertions to verify the correct display of channel information
    assert channel_management_widget.list_v_box_layout.count() == 2
    assert channel_management_widget.list_frame.findChild(
        QLabel, 'asset_name',
    ).text() == 'Test Asset Name'
    assert channel_management_widget.list_frame.findChild(
        QLabel, 'asset_id',
    ).text() == 'test_asset_123'
