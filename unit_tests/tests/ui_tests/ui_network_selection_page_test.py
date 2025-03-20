"""Unit test for network selection page ui."""
# Disable the redefined-outer-name warning as
# it's normal to pass mocked objects in test functions
# pylint: disable=redefined-outer-name,unused-argument,protected-access
from __future__ import annotations

from unittest.mock import MagicMock
from unittest.mock import patch

import pytest
from PySide6.QtCore import QSize
from PySide6.QtCore import Qt

from src.data.repository.setting_repository import SettingRepository
from src.model.enums.enums_model import NetworkEnumModel
from src.utils.custom_exception import CommonException
from src.viewmodels.main_view_model import MainViewModel
from src.views.ui_network_selection_page import NetworkSelectionWidget


@pytest.fixture
def network_selection_page_page_navigation():
    """Fixture to create a mocked page navigation object."""
    mock_navigation = MagicMock()
    return mock_navigation


@pytest.fixture
def mock_network_selection_page_view_model(network_selection_page_page_navigation: MagicMock):
    """Fixture to create a MainViewModel instance with mocked page navigation."""
    view_model = MagicMock(
        MainViewModel(
            network_selection_page_page_navigation,
        ),
    )
    view_model.wallet_transfer_selection_view_model = MagicMock()
    view_model.wallet_transfer_selection_view_model.ln_node_process_status = MagicMock()
    view_model.wallet_transfer_selection_view_model.prev_ln_node_stopping = MagicMock()
    # Ensure start_node_for_embedded_option is mocked
    view_model.wallet_transfer_selection_view_model.start_node_for_embedded_option = MagicMock()
    return view_model


@pytest.fixture
def network_selection_page_widget(mock_network_selection_page_view_model: MainViewModel):
    """Fixture to initialize NetworkSelectionWidget."""
    return NetworkSelectionWidget(
        view_model=mock_network_selection_page_view_model,
        originating_page='wallet_selection_page',
        network='testnet',
    )


def test_initial_widget_setup(network_selection_page_widget: NetworkSelectionWidget):
    """Test initial setup of NetworkSelectionWidget."""
    assert network_selection_page_widget.wallet_logo is not None
    assert network_selection_page_widget.title_text_1.text() == 'select_network_type'
    assert network_selection_page_widget.regtest_text_label.text() == 'regtest'
    assert network_selection_page_widget.testnet_text_label.text() == 'testnet'
    assert network_selection_page_widget.mainnet_text_label.text() == 'mainnet'
    assert network_selection_page_widget.regtest_note_label.text() == 'regtest_note'
    assert network_selection_page_widget.mainnet_frame.isHidden()


def test_frame_click_event(network_selection_page_widget: NetworkSelectionWidget, qtbot):
    """Test the frame click event."""
    qtbot.mouseClick(
        network_selection_page_widget.regtest_frame, Qt.LeftButton,
    )

    qtbot.mouseClick(
        network_selection_page_widget.testnet_frame, Qt.LeftButton,
    )
    network_selection_page_widget.view_model.wallet_transfer_selection_view_model.start_node_for_embedded_option.assert_called_with(
        network=NetworkEnumModel.TESTNET,
        prev_network='testnet',
    )


def test_close_button_navigation(network_selection_page_widget: NetworkSelectionWidget, qtbot):
    """Test the close button navigation."""
    qtbot.mouseClick(
        network_selection_page_widget.select_network_close_btn, Qt.LeftButton,
    )
    network_selection_page_widget.view_model.page_navigation.wallet_method_page.assert_called()

    network_selection_page_widget.originating_page = 'settings_page'
    qtbot.mouseClick(
        network_selection_page_widget.select_network_close_btn, Qt.LeftButton,
    )
    network_selection_page_widget.view_model.page_navigation.settings_page.assert_called()


def test_hide_mainnet_frame(network_selection_page_widget: NetworkSelectionWidget):
    """Test hiding of the mainnet frame."""
    network_selection_page_widget.hide_mainnet_frame()
    assert network_selection_page_widget.mainnet_frame.isHidden()
    assert network_selection_page_widget.network_selection_widget.minimumSize() == QSize(696, 400)
    assert network_selection_page_widget.network_selection_widget.maximumSize() == QSize(696, 400)


def test_set_frame_click(network_selection_page_widget):
    """Test the frame click setup based on current network."""
    # Mock the network to 'regtest'
    mock_network = MagicMock(value='regtest')
    SettingRepository.get_wallet_network = MagicMock(return_value=mock_network)
    SettingRepository.is_wallet_initialized = MagicMock(
        return_value=MagicMock(is_wallet_initialized=True),
    )

    # Set the current network and frame click setup
    network_selection_page_widget.set_current_network()
    network_selection_page_widget.set_frame_click()

    # Ensure the frames are enabled/disabled based on the current network
    assert network_selection_page_widget.regtest_frame.isEnabled() is False  # Disabled ✅
    assert network_selection_page_widget.testnet_frame.isEnabled() is True    # Enabled ✅
    assert network_selection_page_widget.mainnet_frame.isEnabled() is True    # Enabled ✅


@patch('src.views.ui_network_selection_page.LoadingTranslucentScreen')
def test_show_loading_screen_start(mock_loading_screen, network_selection_page_widget: NetworkSelectionWidget, qtbot):
    """Test that the loading screen is shown correctly when status is True."""
    mock_loading_screen.return_value = MagicMock()
    network_selection_page_widget.show_wallet_loading_screen(
        True, 'Loading...',
    )

    # Check if frames are disabled
    assert not network_selection_page_widget.regtest_frame.isEnabled()
    assert not network_selection_page_widget.testnet_frame.isEnabled()

    # Verify that the loading screen is started
    mock_loading_screen.assert_called_once_with(
        parent=network_selection_page_widget, description_text='Loading...', dot_animation=True,
    )
    mock_loading_screen.return_value.start.assert_called_once()


def test_handle_close_button_visibility(network_selection_page_widget: NetworkSelectionWidget, qtbot):
    """Test that the close button is hidden when current_network equals _prev_network."""
    # Set up the initial state where current_network matches _prev_network
    network_selection_page_widget.current_network = 'testnet'
    # Assuming _prev_network is accessible for the test
    network_selection_page_widget._prev_network = 'testnet'

    # Mock the close button
    network_selection_page_widget.select_network_close_btn = MagicMock()

    # Call the method
    network_selection_page_widget.handle_close_button_visibility()

    # Check if the close button is hidden
    network_selection_page_widget.select_network_close_btn.hide.assert_called_once()


def test_show_wallet_loading_screen_disable_loading(network_selection_page_widget: NetworkSelectionWidget, qtbot, mocker):
    """Test the show_wallet_loading_screen method when status is False."""

    # Mock regtest_frame and testnet_frame to track changes
    mocker.patch.object(
        network_selection_page_widget,
        'regtest_frame', MagicMock(),
    )
    mocker.patch.object(
        network_selection_page_widget,
        'testnet_frame', MagicMock(),
    )

    # Mock the LoadingTranslucentScreen
    mock_loading_screen = MagicMock()
    mocker.patch.object(
        network_selection_page_widget,
        '_NetworkSelectionWidget__loading_translucent_screen',
        mock_loading_screen,
    )

    # Mock the handle_close_button_visibility function
    mock_handle_close = mocker.patch.object(
        network_selection_page_widget,
        'handle_close_button_visibility',
    )

    # Call the method with status=False
    network_selection_page_widget.show_wallet_loading_screen(False)

    # Assert the regtest_frame and testnet_frame are enabled
    network_selection_page_widget.regtest_frame.setDisabled.assert_called_with(
        False,
    )
    network_selection_page_widget.testnet_frame.setDisabled.assert_called_with(
        False,
    )

    # Assert that stop is called exactly twice
    assert mock_loading_screen.stop.call_count == 2

    # Assert that make_parent_disabled_during_loading was called with False
    mock_loading_screen.make_parent_disabled_during_loading.assert_called_with(
        False,
    )

    # Check that handle_close_button_visibility is called twice
    mock_handle_close.assert_called_with()
    assert mock_handle_close.call_count == 2


def test_set_current_network_success(network_selection_page_widget: NetworkSelectionWidget):
    """Test the set_current_network method when the network is retrieved successfully."""

    # Mock the SettingRepository.get_wallet_network method to return a mock object with the 'value' attribute
    with patch('src.data.repository.setting_repository.SettingRepository.get_wallet_network') as mock_get_wallet_network:
        mock_get_wallet_network.return_value.value = 'TestNetwork'
        # Call the method to set the current network
        network_selection_page_widget.set_current_network()

        # Assert that current_network is set correctly (in lowercase)
        assert network_selection_page_widget.current_network == 'testnetwork', f"Expected 'testnetwork', but got {
            network_selection_page_widget.current_network
        }"


def test_set_current_network_exception(network_selection_page_widget: NetworkSelectionWidget):
    """Test the set_current_network method when a CommonException is raised."""

    # Mock the SettingRepository.get_wallet_network method to raise a CommonException
    with patch('src.data.repository.setting_repository.SettingRepository.get_wallet_network') as mock_get_wallet_network:
        mock_get_wallet_network.side_effect = CommonException(
            'Error retrieving network',
        )

        # Call the method to set the current network
        network_selection_page_widget.set_current_network()

        # Assert that current_network is set to None in case of an exception
        assert network_selection_page_widget.current_network is None, f"Expected 'None', but got {
            network_selection_page_widget.current_network
        }"
