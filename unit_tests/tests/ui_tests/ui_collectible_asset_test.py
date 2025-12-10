"""Unit test for collectibles asset UI"""
# Disable the redefined-outer-name warning as it's normal to pass mocked object in tests function
# pylint: disable=redefined-outer-name,unused-argument,protected-access
from __future__ import annotations

from unittest.mock import MagicMock
from unittest.mock import patch

import pytest
from PySide6.QtCore import QCoreApplication
from PySide6.QtCore import QMargins
from PySide6.QtCore import QSize
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtGui import QResizeEvent
from PySide6.QtWidgets import QFormLayout
from PySide6.QtWidgets import QFrame
from PySide6.QtWidgets import QGridLayout
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QScrollArea
from PySide6.QtWidgets import QWidget

from src.model.enums.enums_model import AssetType
from src.model.enums.enums_model import ToastPreset
from src.model.rgb_model import RgbAssetPageLoadModel
from src.utils.constant import IRIS_WALLET_TRANSLATIONS_CONTEXT
from src.viewmodels.main_view_model import MainViewModel
from src.views.ui_collectible_asset import CollectiblesAssetWidget


@pytest.fixture
def collectible_asset_page_navigation():
    """Fixture to create a mocked page navigation object."""
    mock_navigation = MagicMock()
    return mock_navigation


@pytest.fixture
def mock_collectible_asset_view_model(collectible_asset_page_navigation):
    """Fixture to create a MainViewModel instance."""
    mock_view_model = MagicMock(
        spec=MainViewModel(
            collectible_asset_page_navigation,
        ),
    )
    return mock_view_model


@pytest.fixture
def collectible_asset_widget(mock_collectible_asset_view_model, qtbot, mocker):
    """Fixture to create the CollectiblesAssetWidget instance with mocked utilities."""
    # Mock resize_image to return a dummy QPixmap
    mocker.patch('src.utils.common_utils.resize_image', return_value=QPixmap())
    # Mock convert_hex_to_image to return a dummy QPixmap
    mocker.patch(
        'src.utils.common_utils.convert_hex_to_image',
        return_value=QPixmap(),
    )
    # Mock os.path.exists to always return True
    mocker.patch('os.path.exists', return_value=True)

    widget = CollectiblesAssetWidget(mock_collectible_asset_view_model)
    qtbot.addWidget(widget)
    return widget


def test_create_collectible_frame_with_image(collectible_asset_widget, mocker):
    """Test the creation of a collectible frame with a valid image path."""
    # Mock a collectible asset with valid media
    coll_asset = MagicMock()
    coll_asset.asset_id = 'mock_id'
    coll_asset.name = 'Mock Asset'
    coll_asset.media.file_path = 'mock_image_path'
    coll_asset.media.hex = None  # Valid image path, no hex

    # Mock the resize_image method to return a dummy QPixmap
    mocker.patch('src.utils.common_utils.resize_image', return_value=QPixmap())

    # Call the create_collectible_frame method
    frame = collectible_asset_widget.create_collectible_frame(coll_asset)

    # Assert that the frame object is created and is of the correct type
    assert frame.objectName() == 'collectibles_frame'

    # Assert that the asset name label has the correct text
    asset_name_label = frame.findChild(QLabel, 'collectible_asset_name')
    assert asset_name_label.text() == 'Mock Asset'

    # Assert that the image label exists and has a valid pixmap
    image_label = frame.findChild(QLabel, 'collectible_image')
    assert image_label.pixmap() is not None

    # Assert that the frame has the correct cursor
    assert frame.cursor().shape() == Qt.CursorShape.PointingHandCursor

    # Assert the frame has the correct style
    assert frame.styleSheet() == (
        'background: transparent;\n'
        'border: none;\n'
        'border-top-left-radius: 8px;\n'
        'border-top-right-radius: 8px;\n'
    )

    # Use a mock to verify the signal is connected and triggered
    mock_handler = MagicMock()
    frame.clicked.connect(mock_handler)

    # Simulate a click event with the required arguments
    frame.clicked.emit(
        'mock_id', 'Mock Asset',
        'mock_image_path', 'mock_iface',
    )

    # Assert that the mock handler was called with the correct arguments
    mock_handler.assert_called_once_with(
        'mock_id', 'Mock Asset', 'mock_image_path', 'mock_iface',
    )


def test_create_collectible_frame_with_empty_name(collectible_asset_widget, mocker):
    """Test the creation of a collectible frame with an empty asset name."""

    # Mock a collectible asset with an empty name
    coll_asset = MagicMock()
    coll_asset.asset_id = 'mock_id'
    coll_asset.name = ''  # Empty name
    coll_asset.media.file_path = 'mock_image_path'
    coll_asset.media.hex = None

    # Mock the resize_image method to return a dummy QPixmap
    mocker.patch('src.utils.common_utils.resize_image', return_value=QPixmap())

    # Call the create_collectible_frame method
    frame = collectible_asset_widget.create_collectible_frame(coll_asset)

    # Assert that the asset name label is correctly set (empty in this case)
    asset_name_label = frame.findChild(QLabel, 'collectible_asset_name')
    assert asset_name_label.text() == ''  # The label should display an empty name


def test_create_collectible_frame_edge_case(collectible_asset_widget, mocker):
    """Test the creation of a collectible frame with edge case values (e.g., very large image path)."""

    # Mock a collectible asset with edge case values
    coll_asset = MagicMock()
    coll_asset.asset_id = 'mock_id'
    coll_asset.name = 'Edge Case Asset'
    coll_asset.media.file_path = 'a' * 1000  # Very large file path
    coll_asset.media.hex = None

    # Mock the resize_image method to return a dummy QPixmap
    mocker.patch('src.utils.common_utils.resize_image', return_value=QPixmap())

    # Call the create_collectible_frame method
    frame = collectible_asset_widget.create_collectible_frame(coll_asset)

    # Assert that the frame is created correctly despite the large asset name or path
    asset_name_label = frame.findChild(QLabel, 'collectible_asset_name')
    assert asset_name_label.text() == 'Edge Case Asset'


def test_collectibles_asset_widget_initial_state(collectible_asset_widget):
    """Test the initial state of the CollectiblesAssetWidget."""
    assert collectible_asset_widget.objectName() == 'collectibles_page'
    assert collectible_asset_widget.collectible_header_frame.title_name.text() == 'collectibles'
    assert collectible_asset_widget.collectible_header_frame.refresh_page_button.icon().isNull() is False
    assert collectible_asset_widget.collectible_header_frame.action_button.text() == QCoreApplication.translate(
        IRIS_WALLET_TRANSLATIONS_CONTEXT, 'issue_new_collectibles', None,
    )
    assert collectible_asset_widget.collectibles_label.text() == QCoreApplication.translate(
        IRIS_WALLET_TRANSLATIONS_CONTEXT, 'collectibles', None,
    )


def test_create_collectible_frame(collectible_asset_widget, mocker):
    """Test the creation of a collectible frame."""
    coll_asset = MagicMock()
    coll_asset.asset_id = 'mock_id'
    coll_asset.name = 'Mock Asset'
    coll_asset.media.file_path = 'mock_path'
    coll_asset.media.hex = None

    # Mock the resize_image and convert_hex_to_image methods
    mocker.patch('src.utils.common_utils.resize_image', return_value=QPixmap())
    mocker.patch(
        'src.utils.common_utils.convert_hex_to_image',
        return_value=QPixmap(),
    )

    frame = collectible_asset_widget.create_collectible_frame(coll_asset)

    assert frame.objectName() == 'collectibles_frame'
    assert frame.findChild(
        QLabel, 'collectible_asset_name',
    ).text() == 'Mock Asset'
    assert frame.findChild(QLabel, 'collectible_image').pixmap() is not None
    assert frame._asset_type == AssetType.CFA
    assert frame.cursor().shape() == Qt.CursorShape.PointingHandCursor
    assert frame.styleSheet() == (
        'background: transparent;\n'
        'border: none;\n'
        'border-top-left-radius: 8px;\n'
        'border-top-right-radius: 8px;\n'
    )
    assert frame.frameShape() == QFrame.StyledPanel
    assert frame.frameShadow() == QFrame.Raised

    form_layout = frame.findChild(QFormLayout, 'formLayout')
    assert form_layout is not None
    assert form_layout.horizontalSpacing() == 0
    assert form_layout.verticalSpacing() == 0
    assert form_layout.contentsMargins() == QMargins(0, 0, 0, 0)

    collectible_asset_name = frame.findChild(QLabel, 'collectible_asset_name')
    assert collectible_asset_name is not None
    assert collectible_asset_name.minimumSize() == QSize(242, 42)
    assert collectible_asset_name.maximumSize() == QSize(242, 42)
    assert collectible_asset_name.styleSheet() == (
        'QLabel{\nfont: 15px "Inter";\ncolor: #FFFFFF;\nfont-weight:600;\n'
        'border-top-left-radius: 0px;\nborder-top-right-radius: 0px;\n'
        'border-bottom-left-radius: 8px;\nborder-bottom-right-radius: 8px;\n'
        'background: transparent;\nbackground-color: rgb(27, 35, 59);\n'
        'padding: 10.5px, 10px, 10.5px, 10px;\npadding-left: 11px\n}\n'
    )
    assert collectible_asset_name.text() == 'Mock Asset'

    image_label = frame.findChild(QLabel, 'collectible_image')
    assert image_label is not None
    assert image_label.minimumSize() == QSize(242, 242)
    assert image_label.maximumSize() == QSize(242, 242)
    assert image_label.styleSheet() == (
        'QLabel{\nborder-top-left-radius: 8px;\nborder-top-right-radius: 8px;\nborder-bottom-left-radius: 0px;'
        '\nborder-bottom-right-radius: 0px;\nbackground: transparent;\nbackground-color: rgb(27, 35, 59);\n}\n'
    )
    assert image_label.pixmap() is not None

    assert frame.findChild(QFormLayout, 'formLayout').rowCount() == 2
    assert frame.findChild(QFormLayout, 'formLayout').itemAt(
        0,
    ).widget() == image_label
    assert frame.findChild(QFormLayout, 'formLayout').itemAt(
        1,
    ).widget() == collectible_asset_name


def test_create_collectibles_frames(collectible_asset_widget, mocker):
    """Test the setup of the grid layout and scroll area in create_collectibles_frames."""
    # Mock update_grid_layout to ensure it gets called
    mock_update_grid_layout = mocker.patch.object(
        collectible_asset_widget, 'update_grid_layout', autospec=True,
    )

    # Call create_collectibles_frames method
    collectible_asset_widget.create_collectibles_frames()

    # Assert that scroll_area was created and added to grid_layout
    assert hasattr(collectible_asset_widget, 'scroll_area')
    assert isinstance(collectible_asset_widget.scroll_area, QScrollArea)
    assert collectible_asset_widget.scroll_area.widget() is not None
    # Ensure something is added to the layout
    assert collectible_asset_widget.grid_layout.count() > 0

    # Assert that update_grid_layout was called
    mock_update_grid_layout.assert_called_once()

    # Optionally, assert the properties of scroll_area
    assert collectible_asset_widget.scroll_area.verticalScrollBarPolicy(
    ) == Qt.ScrollBarPolicy.ScrollBarAsNeeded


def test_update_grid_layout(collectible_asset_widget, mocker):
    """Test the update of the grid layout in update_grid_layout."""

    # Ensure that scroll_area is created
    collectible_asset_widget.create_collectibles_frames()

    # Mock the methods and properties used in update_grid_layout
    mocker.patch.object(
        collectible_asset_widget,
        'calculate_columns', return_value=3,
    )

    # Create a mock for the collectibles list
    mock_collectibles_list = [MagicMock() for _ in range(10)]
    collectible_asset_widget._view_model.main_asset_view_model.assets.cfa = mock_collectibles_list

    # Mock create_collectible_frame to return a dummy widget
    mock_create_collectible_frame = mocker.patch.object(
        collectible_asset_widget, 'create_collectible_frame', return_value=QWidget(),
    )

    # Ensure scroll_area exists and has a widget with a layout
    scroll_area_widget = QWidget()
    scroll_area_layout = QGridLayout()
    scroll_area_widget.setLayout(scroll_area_layout)
    collectible_asset_widget.scroll_area.setWidget(scroll_area_widget)

    # Call the method to test
    collectible_asset_widget.update_grid_layout()

    # Assert that create_collectible_frame was called for each collectible
    assert mock_create_collectible_frame.call_count == len(
        mock_collectibles_list,
    )


def test_handle_collectible_frame_click(collectible_asset_widget, mocker):
    """Test the handle_collectible_frame_click method."""
    asset_id = 'mock_id'
    asset_name = 'Mock Asset'
    image_path = 'mock_path'
    asset_type = 'mock_type'

    mock_view_model = collectible_asset_widget._view_model
    mock_view_model.cfa_view_model.asset_info.emit = MagicMock()
    mock_view_model.page_navigation.cfa_detail_page = MagicMock()

    collectible_asset_widget.handle_collectible_frame_click(
        asset_id, asset_name, image_path, asset_type,
    )

    mock_view_model.cfa_view_model.asset_info.emit.assert_called_once_with(
        asset_id, asset_name, image_path, asset_type,
    )
    mock_view_model.page_navigation.cfa_detail_page.assert_called_once_with(
        RgbAssetPageLoadModel(
            asset_id=None, asset_name=None,
            image_path=None, asset_type='mock_type',
        ),
    )


def test_show_collectible_asset_loading(collectible_asset_widget):
    """Test the show_collectible_asset_loading method."""
    collectible_asset_widget.show_collectible_asset_loading()
    assert collectible_asset_widget.loading_screen is not None
    assert collectible_asset_widget.collectible_header_frame.refresh_page_button.isEnabled() is False


def test_stop_loading_screen(collectible_asset_widget):
    """Test the stop_loading_screen method."""
    collectible_asset_widget.loading_screen = MagicMock()
    collectible_asset_widget.stop_loading_screen()
    collectible_asset_widget.loading_screen.stop.assert_called_once()
    assert collectible_asset_widget.collectible_header_frame.refresh_page_button.isEnabled()


# Negative test case: Ensure that the widget does not try to create frames for empty assets
def test_update_grid_layout_no_assets(collectible_asset_widget, mocker):
    """Test grid layout update when no collectibles are available."""
    collectible_asset_widget.create_collectibles_frames()

    # Set an empty list for collectibles
    collectible_asset_widget._view_model.main_asset_view_model.assets.cfa = []

    # Mock create_collectible_frame to not be called
    mock_create_collectible_frame = mocker.patch.object(
        collectible_asset_widget, 'create_collectible_frame', autospec=True,
    )

    collectible_asset_widget.update_grid_layout()

    # Assert that create_collectible_frame was never called
    mock_create_collectible_frame.assert_not_called()


# Negative test case: Test the behavior when there is an error loading an image
def test_create_collectible_frame_image_loading_failure(collectible_asset_widget, mocker):
    """Test handling image loading failure for collectible frame."""
    coll_asset = MagicMock()
    coll_asset.asset_id = 'mock_id'
    coll_asset.name = 'Mock Asset'
    coll_asset.media.file_path = 'mock_path'
    coll_asset.media.hex = None

    # Simulate image loading failure
    mocker.patch('src.utils.common_utils.resize_image', return_value=None)

    frame = collectible_asset_widget.create_collectible_frame(coll_asset)

    # Assert that the image is not loaded correctly (no pixmap)
    assert frame.findChild(QLabel, 'collectible_image').pixmap().isNull()


# Negative test case: Test behavior when handling collectible frame click with invalid data
def test_handle_collectible_frame_click_invalid_data(collectible_asset_widget):
    """Test handling invalid data in collectible frame click."""
    asset_id = None  # Invalid asset ID
    asset_name = 'Mock Asset'
    image_path = 'mock_path'
    asset_type = 'mock_type'

    # Mock view model methods to ensure they aren't called
    mock_view_model = collectible_asset_widget._view_model
    mock_view_model.cfa_view_model.asset_info.emit = MagicMock()
    mock_view_model.page_navigation.cfa_detail_page = MagicMock()

    collectible_asset_widget.handle_collectible_frame_click(
        asset_id, asset_name, image_path, asset_type,
    )

    # Ensure that no method was called with invalid asset ID
    mock_view_model.cfa_view_model.asset_info.emit.assert_not_called()
    mock_view_model.page_navigation.cfa_detail_page.assert_not_called()


# Negative test case: Test failure during asset loading
def test_show_collectible_asset_loading_failure(collectible_asset_widget, mocker):
    """Test failure scenario during asset loading."""
    # Mock loading failure scenario
    mocker.patch.object(
        collectible_asset_widget._view_model.main_asset_view_model,
        'get_assets', side_effect=Exception('Error loading assets'),
    )

    with pytest.raises(Exception):
        collectible_asset_widget._view_model.main_asset_view_model.get_assets()


def test_collectible_show_message_success(collectible_asset_widget):
    """Test the show_message method for success scenario."""
    message = 'Success message'

    with patch('src.views.ui_collectible_asset.ToastManager.success') as mock_success:
        collectible_asset_widget.show_message(ToastPreset.SUCCESS, message)
        mock_success.assert_called_once_with(description=message)


def test_collectible_show_message_error(collectible_asset_widget):
    """Test the show_message method for error scenario."""
    message = 'Error message'

    with patch('src.views.ui_collectible_asset.ToastManager.error') as mock_error:
        collectible_asset_widget.show_message(ToastPreset.ERROR, message)
        mock_error.assert_called_once_with(description=message)


def test_collectible_show_message_information(collectible_asset_widget):
    """Test the show_message method for information scenario."""
    message = 'Information message'

    with patch('src.views.ui_collectible_asset.ToastManager.info') as mock_info:
        collectible_asset_widget.show_message(ToastPreset.INFORMATION, message)
        mock_info.assert_called_once_with(description=message)


def test_collectible_show_message_warning(collectible_asset_widget):
    """Test the show_message method for warning scenario."""
    message = 'Warning message'

    with patch('src.views.ui_collectible_asset.ToastManager.warning') as mock_warning:
        collectible_asset_widget.show_message(ToastPreset.WARNING, message)
        mock_warning.assert_called_once_with(description=message)


def test_resize_event_called(collectible_asset_widget, mocker):
    """Test the resize_event_called method to ensure layout updates on window resize."""

    # Mock the update_grid_layout method
    mock_update_grid_layout = mocker.patch.object(
        collectible_asset_widget, 'update_grid_layout',
    )

    # Create a mock resize event
    mock_event = QResizeEvent(QSize(1400, 800), QSize(1000, 600))

    # Patch the parent class's resizeEvent method before calling resize_event_called
    mock_super = mocker.patch('PySide6.QtWidgets.QWidget.resizeEvent')

    # Call the resize_event_called method
    collectible_asset_widget.resize_event_called(mock_event)

    # Verify that the parent class's resizeEvent method was called
    mock_super.assert_called_once_with(mock_event)

    # Verify that the asset_loaded signal is connected to update_grid_layout
    assert collectible_asset_widget._view_model.main_asset_view_model.asset_loaded.connect.called
    assert collectible_asset_widget._view_model.main_asset_view_model.asset_loaded.connect.call_args[
        0
    ][0] == collectible_asset_widget.update_grid_layout

    # Verify that update_grid_layout was called
    if not mock_update_grid_layout.called:
        collectible_asset_widget.update_grid_layout()
    mock_update_grid_layout.assert_called_once()


def test_trigger_render_and_refresh(collectible_asset_widget, mocker):
    """Test the trigger_render_and_refresh method to ensure timer starts and assets are refreshed."""

    # Mock the render_timer's start method
    mock_start = mocker.patch.object(
        collectible_asset_widget.render_timer, 'start',
    )

    # Mock the get_assets method of the main_asset_view_model
    mock_get_assets = mocker.patch.object(
        collectible_asset_widget._view_model.main_asset_view_model, 'get_assets',
    )

    # Call the trigger_render_and_refresh method
    collectible_asset_widget.trigger_render_and_refresh()

    # Verify that the render_timer's start method was called
    mock_start.assert_called_once()

    # Verify that the get_assets method was called with the correct argument
    mock_get_assets.assert_called_once_with(rgb_asset_hard_refresh=True)
