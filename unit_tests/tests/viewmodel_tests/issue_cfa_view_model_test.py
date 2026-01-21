"""Unit test for Issue CFA view model.

This module contains tests for the IssueCFAViewModel class, which represents the view model
for the Issue CFA Asset page activities.
"""
# Disable the redefined-outer-name warning as
# it's normal to pass mocked object in tests function
# pylint: disable=redefined-outer-name,unused-argument
from __future__ import annotations

from unittest.mock import MagicMock
from unittest.mock import Mock
from unittest.mock import patch

import pytest
from PySide6.QtWidgets import QFileDialog

from src.model.rgb_model import AssetBalanceResponseModel
from src.model.rgb_model import IssueAssetResponseModel
from src.utils.custom_exception import CommonException
from src.utils.error_message import ERROR_AUTHENTICATION
from src.utils.error_message import ERROR_FIELD_MISSING
from src.utils.error_message import ERROR_SOMETHING_WENT_WRONG
from src.utils.info_message import INFO_ASSET_ISSUED
from src.utils.info_message import INFO_NO_FILE
from src.viewmodels.issue_cfa_view_model import IssueCFAViewModel


@pytest.fixture
def mock_page_navigation(mocker):
    """Fixture to create a mock page navigation object."""
    return mocker.MagicMock()


@pytest.fixture
def issue_cfa_view_model(mock_page_navigation):
    """Fixture to create an instance of the IssueCFAViewModel class."""
    return IssueCFAViewModel(mock_page_navigation)


@patch('src.views.components.toast.ToastManager')
def test_open_file_dialog_normal_execution(mock_toast_manager, issue_cfa_view_model):
    """Test open_file_dialog method when a file is selected"""
    with patch.object(QFileDialog, 'exec_', return_value=True), \
            patch.object(QFileDialog, 'selectedFiles', return_value=['/path/to/file.png']):

        # Create a mock signal to check if the file_upload_message signal is emitted
        mock_signal = Mock()
        issue_cfa_view_model.file_upload_message.connect(mock_signal)

        issue_cfa_view_model.open_file_dialog()

        # Verify that the signal is emitted with the correct file path
        mock_signal.assert_called_once_with('/path/to/file.png')


@patch('src.views.components.toast.ToastManager.error')
@patch('src.data.repository.rgb_repository.RgbRepository.issue_asset_cfa')
@patch('src.utils.worker.ThreadManager.run_in_thread')
def test_issue_cfa_asset_failure(
    mock_run_in_thread, mock_issue_asset_cfa, mock_toast_error,
    issue_cfa_view_model, mock_page_navigation,
):
    """Test for failure to issue CFA asset."""
    # Simulate failure in issuing the asset
    mock_issue_asset_cfa.side_effect = CommonException('Failed to issue asset')

    # Mock the worker
    mock_worker = MagicMock()
    issue_cfa_view_model.worker = mock_worker

    # Provide required input data
    issue_cfa_view_model.uploaded_file_path = 'path/to/file.png'

    # Perform the action
    issue_cfa_view_model.issue_cfa_asset('ticker', 'asset_name', '100')

    # Simulate the error callback
    mock_worker.error.emit(mock_issue_asset_cfa.side_effect)

    mock_page_navigation.collectibles_asset_page.assert_not_called()


@patch('src.views.components.toast.ToastManager')
def test_open_file_dialog_success(mock_toast_manager, issue_cfa_view_model, mocker):
    """Test for open_file_dialog method when file is successfully selected"""
    with patch('PySide6.QtWidgets.QFileDialog.exec_', return_value=True), \
            patch('PySide6.QtWidgets.QFileDialog.selectedFiles', return_value=['/path/to/selected/image.png']):
        issue_cfa_view_model.open_file_dialog()

        assert issue_cfa_view_model.uploaded_file_path == '/path/to/selected/image.png'


@patch('src.views.components.toast.ToastManager')
def test_open_file_dialog_no_selection(mock_toast_manager, issue_cfa_view_model, mocker):
    """Test for open_file_dialog method when no file is selected"""
    with patch('PySide6.QtWidgets.QFileDialog.exec_', return_value=False):
        issue_cfa_view_model.open_file_dialog()

        assert issue_cfa_view_model.uploaded_file_path is None


@patch('src.views.components.toast.ToastManager.error')
def test_open_file_dialog_exception(mock_toast_manager, issue_cfa_view_model, mocker):
    """Test for open_file_dialog method when an exception is raised"""
    with patch('PySide6.QtWidgets.QFileDialog.exec_', side_effect=CommonException('Test error')):
        issue_cfa_view_model.open_file_dialog()

        mock_toast_manager.assert_called_once_with(
            description='An unexpected error occurred: Test error',
        )


@patch('src.views.components.toast.ToastManager.error')
def test_on_success_native_auth_cfa_missing_fields(mock_toast_manager, issue_cfa_view_model):
    """Test on_success_native_auth_cfa with missing required fields"""
    issue_cfa_view_model.is_loading = MagicMock()

    issue_cfa_view_model.amount = None
    issue_cfa_view_model.asset_name = None
    issue_cfa_view_model.asset_ticker = None

    issue_cfa_view_model.on_success_native_auth_cfa(True)

    mock_toast_manager.assert_called_once_with(description=ERROR_FIELD_MISSING)
    issue_cfa_view_model.is_loading.emit.assert_called_with(False)


@patch('src.views.components.toast.ToastManager.error')
def test_on_error_native_auth_cfa(mock_toast_manager, issue_cfa_view_model):
    """Test on_error_native_auth_cfa with different error types"""
    # Test with CommonException
    common_error = CommonException('Test error')
    issue_cfa_view_model.on_error_native_auth_cfa(common_error)
    mock_toast_manager.assert_called_with(description='Test error')

    # Test with generic Exception
    generic_error = Exception('Generic error')
    issue_cfa_view_model.on_error_native_auth_cfa(generic_error)
    mock_toast_manager.assert_called_with(
        description=ERROR_SOMETHING_WENT_WRONG,
    )


@patch('src.views.components.toast.ToastManager.success')
def test_on_success(mock_toast_manager, issue_cfa_view_model):
    """Test on_success callback"""
    issue_cfa_view_model.success_page_message = MagicMock()
    issue_cfa_view_model.is_loading = MagicMock()

    response = IssueAssetResponseModel(
        asset_id='test_id',
        name='Test Asset',
        ticker='TEST',
        details='details',
        precision=2,
        issued_supply=1000,
        timestamp=123456789,
        added_at=123456789,
        balance=AssetBalanceResponseModel(
            spendable=10, future=10, settled=12, offchain_outbound=0, offchain_inbound=0,
        ),
    )

    issue_cfa_view_model.on_success(response)

    mock_toast_manager.assert_called_once_with(
        description=INFO_ASSET_ISSUED.format('test_id'),
    )
    issue_cfa_view_model.success_page_message.emit.assert_called_once_with(
        'Test Asset',
    )
    issue_cfa_view_model.is_loading.emit.assert_called_once_with(False)


@patch('src.views.components.toast.ToastManager.error')
def test_on_error(mock_toast_manager, issue_cfa_view_model):
    """Test on_error callback"""
    issue_cfa_view_model.is_loading = MagicMock()
    error = CommonException('Test error')

    issue_cfa_view_model.on_error(error)

    mock_toast_manager.assert_called_once_with(description='Test error')
    issue_cfa_view_model.is_loading.emit.assert_called_once_with(False)

    @patch('src.views.components.toast.ToastManager.error')
    def test_on_success_native_auth_cfa_with_generic_exception(mock_toast_manager, issue_cfa_view_model):
        """Test on_success_native_auth_cfa with generic exception"""
        issue_cfa_view_model.is_loading = MagicMock()
        issue_cfa_view_model.run_in_thread = MagicMock(
            side_effect=Exception('Unexpected error'),
        )

        # Set required attributes
        issue_cfa_view_model.amount = '100'
        issue_cfa_view_model.asset_name = 'Test Asset'
        issue_cfa_view_model.asset_ticker = 'TEST'
        issue_cfa_view_model.uploaded_file_path = '/path/to/file.png'

        issue_cfa_view_model.on_success_native_auth_cfa(True)

        mock_toast_manager.assert_called_once_with(
            description=ERROR_SOMETHING_WENT_WRONG,
        )
        issue_cfa_view_model.is_loading.emit.assert_called_once_with(False)


@patch('src.views.components.toast.ToastManager.error')
def test_on_success_native_auth_cfa_auth_failed(mock_toast_manager, issue_cfa_view_model):
    """Test on_success_native_auth_cfa when authentication fails"""
    issue_cfa_view_model.is_loading = MagicMock()

    # Set required attributes
    issue_cfa_view_model.amount = '100'
    issue_cfa_view_model.asset_name = 'Test Asset'
    issue_cfa_view_model.asset_ticker = 'TEST'

    issue_cfa_view_model.on_success_native_auth_cfa(False)

    mock_toast_manager.assert_called_once_with(
        description=ERROR_AUTHENTICATION,
    )
    issue_cfa_view_model.is_loading.emit.assert_called_once_with(False)


@patch('src.views.components.toast.ToastManager.error')
def test_on_success_native_auth_cfa_no_file(mock_toast_manager, issue_cfa_view_model):
    """Test on_success_native_auth_cfa when no file is uploaded"""
    issue_cfa_view_model.is_loading = MagicMock()

    # Set required attributes except file path
    issue_cfa_view_model.amount = '100'
    issue_cfa_view_model.asset_name = 'Test Asset'
    issue_cfa_view_model.asset_ticker = 'TEST'
    issue_cfa_view_model.uploaded_file_path = None

    issue_cfa_view_model.on_success_native_auth_cfa(True)

    mock_toast_manager.assert_called_once_with(description=INFO_NO_FILE)
    issue_cfa_view_model.is_loading.emit.assert_called_once_with(False)


@patch('src.viewmodels.issue_cfa_view_model.IssueAssetService')
def test_on_success_native_auth_cfa_success(mock_issue_asset_service, issue_cfa_view_model):
    """Test on_success_native_auth_cfa successful execution"""
    issue_cfa_view_model.run_in_thread = MagicMock()

    # Set all required attributes
    issue_cfa_view_model.amount = '100'
    issue_cfa_view_model.asset_name = 'Test Asset'
    issue_cfa_view_model.asset_ticker = 'TEST'
    issue_cfa_view_model.uploaded_file_path = '/path/to/file.png'

    issue_cfa_view_model.on_success_native_auth_cfa(True)

    # Verify run_in_thread was called with correct arguments
    issue_cfa_view_model.run_in_thread.assert_called_once()
    call_args = issue_cfa_view_model.run_in_thread.call_args[0][1]

    assert call_args['callback'] == issue_cfa_view_model.on_success
    assert call_args['error_callback'] == issue_cfa_view_model.on_error
    assert len(call_args['args']) == 1

    request_model = call_args['args'][0]
    assert request_model.amounts == [100]
    assert request_model.ticker == 'TEST'
    assert request_model.name == 'Test Asset'
    assert request_model.file_path == '/path/to/file.png'


@patch('src.views.components.toast.ToastManager.error')
def test_on_success_native_auth_cfa_exception(mock_toast_manager, issue_cfa_view_model):
    """Test on_success_native_auth_cfa when an unexpected exception occurs"""
    issue_cfa_view_model.is_loading = MagicMock()

    # Set all required attributes
    # This will cause an exception when converting to int
    issue_cfa_view_model.amount = 'invalid_amount'
    issue_cfa_view_model.asset_name = 'Test Asset'
    issue_cfa_view_model.asset_ticker = 'TEST'
    issue_cfa_view_model.uploaded_file_path = '/path/to/file.png'

    issue_cfa_view_model.on_success_native_auth_cfa(True)

    mock_toast_manager.assert_called_once_with(
        description=ERROR_SOMETHING_WENT_WRONG,
    )
    issue_cfa_view_model.is_loading.emit.assert_called_once_with(False)
