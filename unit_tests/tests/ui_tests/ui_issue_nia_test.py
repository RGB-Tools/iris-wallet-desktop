"""Unit test for Issue NIA UI."""
# Disable the redefined-outer-name warning as
# it's normal to pass mocked objects in test functions
# pylint: disable=redefined-outer-name,unused-argument,protected-access
from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from src.viewmodels.main_view_model import MainViewModel
from src.views.ui_issue_nia import IssueNIAWidget
from unit_tests.tests.ui_tests.ui_helper_test.issue_asset_helper_test import assert_success_page_called


@pytest.fixture
def issue_nia_page_navigation():
    """Fixture to create a mocked page navigation object."""
    mock_navigation = MagicMock()
    return mock_navigation


@pytest.fixture
def mock_issue_nia_view_model(issue_nia_page_navigation: MagicMock):
    """Fixture to create a MainViewModel instance with mocked page navigation."""
    return MainViewModel(issue_nia_page_navigation)


@pytest.fixture
def issue_nia_widget(mock_issue_nia_view_model: MainViewModel):
    """Fixture to create a IssueNIAWidget instance."""
    return IssueNIAWidget(mock_issue_nia_view_model)


def test_retranslate_ui(issue_nia_widget: IssueNIAWidget):
    """Test that the UI strings are correctly translated."""
    issue_nia_widget.retranslate_ui()

    assert issue_nia_widget.asset_ticker_label.text() == 'asset_ticker'
    assert issue_nia_widget.asset_name_label.text() == 'asset_name'


def test_on_issue_nia_click(issue_nia_widget: IssueNIAWidget, qtbot):
    """Test the on_issue_nia_click method."""
    widget = issue_nia_widget

    # Mock the input fields
    widget.short_identifier_input = MagicMock()
    widget.short_identifier_input.text.return_value = 'TTK'

    widget.asset_name_input = MagicMock()
    widget.asset_name_input.text.return_value = 'NIA'

    widget.amount_input = MagicMock()
    widget.amount_input.text.return_value = '100'

    # Mock the view model method
    widget._view_model.issue_nia_asset_view_model.on_issue_click = MagicMock()

    # Simulate the click event
    widget.on_issue_nia_click()

    # Verify that the view model method was called with the correct arguments
    widget._view_model.issue_nia_asset_view_model.on_issue_click.assert_called_once_with(
        'TTK', 'NIA', '100',
    )


def test_handle_button_enabled(issue_nia_widget: IssueNIAWidget, qtbot):
    """Test the handle_button_enabled method."""
    widget = issue_nia_widget

    # Mock the input fields
    widget.short_identifier_input = MagicMock()
    widget.amount_input = MagicMock()
    widget.asset_name_input = MagicMock()
    widget.issue_nia_btn = MagicMock()

    # Case when all fields are filled
    widget.short_identifier_input.text.return_value = 'TTK'
    widget.amount_input.text.return_value = '100'
    widget.asset_name_input.text.return_value = 'NIA'

    widget.handle_button_enabled()
    widget.issue_nia_btn.setDisabled.assert_called_once_with(False)

    # Case when one of the fields is empty
    widget.short_identifier_input.text.return_value = ''

    widget.handle_button_enabled()
    widget.issue_nia_btn.setDisabled.assert_called_with(True)


def test_asset_issued(issue_nia_widget: IssueNIAWidget, qtbot):
    """Test the asset_issued method."""
    widget = issue_nia_widget

    # Mock the view model's navigation
    widget._view_model.page_navigation.show_success_page = MagicMock()
    widget._view_model.page_navigation.fungibles_asset_page = MagicMock()

    # Simulate asset issuance
    asset_name = 'NIA'
    widget.asset_issued(asset_name)

    # Verify that the success page is shown with correct parameters
    widget._view_model.page_navigation.show_success_page.assert_called_once()

    params = widget._view_model.page_navigation.show_success_page.call_args[0][0]
    assert_success_page_called(widget, asset_name)
    assert params.callback == widget._view_model.page_navigation.fungibles_asset_page


def test_update_loading_state_true(issue_nia_widget: IssueNIAWidget):
    """Test the update_loading_state method when is_loading is True."""

    issue_nia_widget.render_timer = MagicMock()
    issue_nia_widget.issue_nia_btn = MagicMock()
    issue_nia_widget.nia_close_btn = MagicMock()

    # Call the method with is_loading=True
    issue_nia_widget.update_loading_state(True)

    # Assert that the render_timer starts
    issue_nia_widget.render_timer.start.assert_called_once()

    # Assert that the issue_nia_btn starts loading
    issue_nia_widget.issue_nia_btn.start_loading.assert_called_once()

    # Assert that the nia_close_btn is disabled
    issue_nia_widget.nia_close_btn.setDisabled.assert_called_once_with(
        True,
    )


def test_update_loading_state_false(issue_nia_widget: IssueNIAWidget):
    """Test the update_loading_state method when is_loading is False."""

    issue_nia_widget.render_timer = MagicMock()
    issue_nia_widget.issue_nia_btn = MagicMock()
    issue_nia_widget.nia_close_btn = MagicMock()

    # Call the method with is_loading=False
    issue_nia_widget.update_loading_state(False)

    # Assert that the render_timer stops
    issue_nia_widget.render_timer.stop.assert_called_once()

    # Assert that the issue_nia_btn stops loading
    issue_nia_widget.issue_nia_btn.stop_loading.assert_called_once()

    # Assert that the nia_close_btn is enabled
    issue_nia_widget.nia_close_btn.setDisabled.assert_called_once_with(
        False,
    )
