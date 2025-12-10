"""Unit test for Issue CFA UI."""
# Disable the redefined-outer-name warning as
# it's normal to pass mocked objects in test functions
# pylint: disable=redefined-outer-name,unused-argument,protected-access
from __future__ import annotations

from unittest.mock import MagicMock
from unittest.mock import patch

import pytest
from PySide6.QtCore import QCoreApplication
from PySide6.QtCore import QSize
from PySide6.QtGui import QPixmap

from src.model.common_operation_model import NodeInfoResponseModel
from src.utils.constant import IRIS_WALLET_TRANSLATIONS_CONTEXT
from src.viewmodels.main_view_model import MainViewModel
from src.views.ui_issue_cfa import IssueCFAWidget
from unit_tests.tests.ui_tests.ui_helper_test.issue_asset_helper_test import assert_success_page_called


@pytest.fixture
def issue_cfa_page_navigation():
    """Fixture to create a mocked page navigation object."""
    mock_navigation = MagicMock()
    return mock_navigation


@pytest.fixture
def mock_issue_cfa_view_model(issue_cfa_page_navigation: MagicMock):
    """Fixture to create a MainViewModel instance with mocked page navigation."""
    return MainViewModel(issue_cfa_page_navigation)


@pytest.fixture
def issue_cfa_widget(mock_issue_cfa_view_model: MainViewModel):
    """Fixture to create a IssueCFAWidget instance."""

    return IssueCFAWidget(mock_issue_cfa_view_model)


def test_retranslate_ui(issue_cfa_widget: IssueCFAWidget):
    """Test that the UI strings are correctly translated."""
    issue_cfa_widget.retranslate_ui()
    assert issue_cfa_widget.total_supply_label.text() == 'total_supply'
    assert issue_cfa_widget.asset_name_label.text() == 'asset_name'


def test_on_issue_cfa(issue_cfa_widget: IssueCFAWidget, qtbot):
    """Test the on_issue_cfa method."""
    widget = issue_cfa_widget

    # Mock the view model method
    widget._view_model.issue_cfa_asset_view_model.issue_cfa_asset = MagicMock()

    # Set input values
    widget.asset_description_input.setText('Description')
    widget.name_of_the_asset_input.setText('Asset Name')
    widget.amount_input.setText('1000')

    # Simulate the button click
    widget.on_issue_cfa()

    # Verify that the view model method is called with the correct arguments
    widget._view_model.issue_cfa_asset_view_model.issue_cfa_asset.assert_called_once_with(
        'Description', 'Asset Name', '1000',
    )


def test_on_upload_asset_file(issue_cfa_widget: IssueCFAWidget, qtbot):
    """Test the on_upload_asset_file method."""
    widget = issue_cfa_widget

    # Mock the view model method
    widget._view_model.issue_cfa_asset_view_model.open_file_dialog = MagicMock()

    # Simulate the button click
    widget.on_upload_asset_file()

    # Verify that the file dialog is opened
    widget._view_model.issue_cfa_asset_view_model.open_file_dialog.assert_called_once()


def test_on_close(issue_cfa_widget: IssueCFAWidget, qtbot):
    """Test the on_close method."""
    widget = issue_cfa_widget

    # Mock the page navigation method
    widget._view_model.page_navigation.collectibles_asset_page = MagicMock()

    # Simulate the button click
    widget.on_close()

    # Verify that the page navigation method is called
    widget._view_model.page_navigation.collectibles_asset_page.assert_called_once()


def test_handle_button_enabled(issue_cfa_widget: IssueCFAWidget, qtbot):
    """Test the handle_button_enabled method."""
    widget = issue_cfa_widget

    # Mock the inputs and button
    widget.amount_input = MagicMock()
    widget.asset_description_input = MagicMock()
    widget.name_of_the_asset_input = MagicMock()
    widget.issue_cfa_button = MagicMock()

    # Case when all fields are filled
    widget.amount_input.text.return_value = '1000'
    widget.asset_description_input.text.return_value = 'Description'
    widget.name_of_the_asset_input.text.return_value = 'Asset Name'

    widget.handle_button_enabled()
    widget.issue_cfa_button.setDisabled.assert_called_once_with(False)

    # Case when one of the fields is empty
    widget.name_of_the_asset_input.text.return_value = ''

    widget.handle_button_enabled()
    assert widget.issue_cfa_button.isEnabled()


def test_update_loading_state(issue_cfa_widget: IssueCFAWidget, qtbot):
    """Test the update_loading_state method."""
    widget = issue_cfa_widget

    # Mock the button's loading methods
    widget.issue_cfa_button.start_loading = MagicMock()
    widget.issue_cfa_button.stop_loading = MagicMock()

    # Test loading state true
    widget.update_loading_state(True)
    widget.issue_cfa_button.start_loading.assert_called_once()
    widget.issue_cfa_button.stop_loading.assert_not_called()

    # Test loading state false
    widget.update_loading_state(False)
    # still called once from previous
    widget.issue_cfa_button.start_loading.assert_called_once()
    widget.issue_cfa_button.stop_loading.assert_called_once()


def test_show_asset_issued(issue_cfa_widget: IssueCFAWidget, qtbot):
    """Test the show_asset_issued method."""
    widget = issue_cfa_widget

    # Mock the success page method
    widget._view_model.page_navigation.show_success_page = MagicMock()
    widget._view_model.page_navigation.collectibles_asset_page = MagicMock()

    # Simulate asset issuance
    asset_name = 'Asset Name'
    widget.show_asset_issued(asset_name)

    # Verify that the success page is shown with correct parameters
    widget._view_model.page_navigation.show_success_page.assert_called_once()

    params = widget._view_model.page_navigation.show_success_page.call_args[0][0]
    assert_success_page_called(widget, asset_name)
    assert params.callback == widget._view_model.page_navigation.collectibles_asset_page


@patch('src.views.ui_issue_cfa.os.path.getsize')
@patch('src.views.ui_issue_cfa.resize_image')
@patch('src.views.ui_issue_cfa.QPixmap')
@patch('src.views.ui_issue_cfa.NodeInfoModel')
def test_show_file_preview(mock_node_info_model, mock_qpix_map, mock_resize_image, mock_getsize, issue_cfa_widget):
    """Test the show_file_preview method."""

    # Mock the NodeInfoModel to return a max file size of 10MB
    mock_node_info = MagicMock()
    mock_node_info_model.return_value = mock_node_info
    mock_node_info.node_info = MagicMock(spec=NodeInfoResponseModel)
    mock_node_info.node_info.max_media_upload_size_mb = 10  # 10MB max size

    issue_cfa_widget.file_path = MagicMock()
    issue_cfa_widget.issue_cfa_button = MagicMock()
    issue_cfa_widget.issue_cfa_card = MagicMock()
    issue_cfa_widget.upload_file = MagicMock()

    # Mock the file size returned by os.path.getsize
    # 15MB (larger than the allowed 10MB)
    mock_getsize.return_value = 15 * 1024 * 1024

    # Set up mock behavior for resize_image and QPixmap
    mock_resize_image.return_value = 'dummy_resized_image_path'
    mock_qpix_map.return_value = MagicMock(spec=QPixmap)

    # Simulate a file upload message
    file_upload_message = 'path/to/file.jpg'

    # Call the method under test
    issue_cfa_widget.show_file_preview(file_upload_message)

    # Assert that the validation message is shown for large files
    expected_validation_text = QCoreApplication.translate(
        IRIS_WALLET_TRANSLATIONS_CONTEXT, 'image_validation', None,
    ).format(mock_node_info.node_info.max_media_upload_size_mb)
    issue_cfa_widget.file_path.setText.assert_called_once_with(
        expected_validation_text,
    )

    issue_cfa_widget.issue_cfa_button.setDisabled.assert_any_call(
        True,
    )  # Assert it was disabled first

    # Assert that the card's maximum size is set to (499, 608)
    issue_cfa_widget.issue_cfa_card.setMaximumSize.assert_called_once_with(
        QSize(499, 608),
    )

    # Now test for a valid file size scenario (smaller than 10MB)
    mock_getsize.return_value = 5 * 1024 * 1024  # 5MB (valid size)

    # Call the method again with a smaller file size
    issue_cfa_widget.show_file_preview(file_upload_message)

    # Assert that the file path is displayed as the uploaded file
    issue_cfa_widget.file_path.setText.assert_called_with(
        file_upload_message,
    )

    issue_cfa_widget.issue_cfa_button.setDisabled.assert_any_call(
        False,
    )  # Assert it was enabled later

    # Assert that the card's maximum size is set to (499, 808)
    issue_cfa_widget.issue_cfa_card.setMaximumSize.assert_called_with(
        QSize(499, 808),
    )

    # Assert that the image is resized
    mock_resize_image.assert_called_once_with(file_upload_message, 242, 242)

    # Assert that the resized image is set to the file path as a pixmap
    issue_cfa_widget.file_path.setPixmap.assert_called_once_with(
        mock_qpix_map.return_value,
    )

    # Assert that the "change uploaded file" text is set
    issue_cfa_widget.upload_file.setText.assert_called_once_with(
        QCoreApplication.translate(
            IRIS_WALLET_TRANSLATIONS_CONTEXT, 'change_uploaded_file', 'CHANGE UPLOADED FILE',
        ),
    )
