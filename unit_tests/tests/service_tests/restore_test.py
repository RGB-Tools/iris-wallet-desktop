"""Unit tests for restore method of restore service"""
# pylint: disable=redefined-outer-name,unused-argument,too-many-arguments
from __future__ import annotations

import os
import shutil
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest

from src.data.service.restore_service import RestoreService
from src.model.common_operation_model import RestoreResponseModel
from src.utils.custom_exception import CommonException
from src.utils.error_message import ERROR_NOT_BACKUP_FILE
from src.utils.error_message import ERROR_UNABLE_GET_MNEMONIC
from src.utils.error_message import ERROR_UNABLE_TO_GET_HASHED_MNEMONIC
from src.utils.error_message import ERROR_UNABLE_TO_GET_PASSWORD
from src.utils.error_message import ERROR_WHILE_RESTORE_DOWNLOAD_FROM_DRIVE
from unit_tests.service_test_resources.mocked_fun_return_values.backup_service import mock_password
from unit_tests.service_test_resources.mocked_fun_return_values.backup_service import mock_valid_mnemonic

# Setup function


@pytest.fixture(scope='function')
def setup_directory():
    """Set up method for test"""
    test_dir = os.path.join(os.path.dirname(__file__), 'iris-wallet-test')

    restore_dir = os.path.join(test_dir, 'restore')

    # Create the iris-wallet-test directory
    os.makedirs(test_dir, exist_ok=True)

    # Create the restore directory inside iris-wallet-test
    os.makedirs(restore_dir, exist_ok=True)

    return test_dir, restore_dir

# Teardown function


@pytest.fixture(scope='function', autouse=True)
def teardown_directory_after_test():
    """Clean up function after test"""
    yield
    demo_dir = os.path.join(os.path.dirname(__file__), 'iris-wallet-test')
    if os.path.exists(demo_dir):
        shutil.rmtree(demo_dir)
    assert not os.path.exists(demo_dir)

# Test function


@patch('src.data.service.restore_service.COMPATIBLE_RLN_NODE_COMMITS', ['abc'])
@patch('src.data.service.restore_service.read_ln_node_commit_id_file')
@patch('src.data.service.restore_service.SettingRepository.set_rln_node_commit_id')
@patch('src.data.service.common_operation_service.CommonOperationService.get_hashed_mnemonic')
@patch('src.utils.local_store.local_store.get_path')
@patch('src.data.repository.common_operations_repository.CommonOperationRepository.restore')
@patch('src.data.service.restore_service.GoogleDriveManager')
def test_restore(mock_google_drive_manager, mock_restore, mock_app_paths, mock_get_hashed_mnemonic, mock_set_commit_id, mock_read_commit_id, setup_directory):
    """Case 1: Test restore service"""
    test_dir, restore_dir = setup_directory

    # Setup mocks
    mock_get_hashed_mnemonic.return_value = 'e23ddff3cc'
    mock_app_paths.restore_folder_path = restore_dir
    mock_app_paths.iriswallet_temp_folder_path = test_dir
    mock_read_commit_id.return_value = 'abc'

    mock_restore_instance = MagicMock()
    mock_restore.return_value = RestoreResponseModel(status=True)
    mock_restore_instance.return_value = None
    mock_google_drive_manager.return_value = mock_restore_instance
    # Two downloads: commit id file, then backup file
    mock_restore_instance.download_from_drive.side_effect = [True, True]

    result = RestoreService.restore(mock_valid_mnemonic, mock_password)

    # Assert the result
    assert result.status is True

# Test function


@patch('src.data.service.restore_service.COMPATIBLE_RLN_NODE_COMMITS', ['abc'])
@patch('src.data.service.restore_service.read_ln_node_commit_id_file')
@patch('src.data.service.restore_service.SettingRepository.set_rln_node_commit_id')
@patch('src.data.service.common_operation_service.CommonOperationService.get_hashed_mnemonic')
@patch('src.utils.local_store.local_store.get_path')
@patch('src.data.repository.common_operations_repository.CommonOperationRepository.restore')
@patch('src.data.service.restore_service.GoogleDriveManager')
def test_restore_when_file_not_exists(
    mock_google_drive_manager, mock_restore,
    mock_app_paths, mock_get_hashed_mnemonic, mock_set_commit_id, mock_read_commit_id, setup_directory,
):
    """Case 2: When restore file does not exist after download"""
    test_dir, restore_dir = setup_directory

    # Setup mocks
    mock_get_hashed_mnemonic.return_value = 'e23ddff3cc'
    mock_app_paths.restore_folder_path = restore_dir
    mock_app_paths.iriswallet_temp_folder_path = test_dir
    mock_read_commit_id.return_value = 'abc'

    mock_restore_instance = MagicMock()
    mock_restore.return_value = RestoreResponseModel(status=True)
    mock_restore_instance.return_value = None
    mock_google_drive_manager.return_value = mock_restore_instance
    # First: commit id download succeeds, Second: backup download returns None
    mock_restore_instance.download_from_drive.side_effect = [True, None]

    error_message = ERROR_NOT_BACKUP_FILE
    with pytest.raises(CommonException, match=error_message):
        RestoreService.restore(mock_valid_mnemonic, mock_password)


@patch('src.data.service.common_operation_service.CommonOperationService.get_hashed_mnemonic')
@patch('src.data.service.restore_service.app_paths')
@patch('src.data.service.restore_service.GoogleDriveManager')
@patch('src.data.repository.common_operations_repository.CommonOperationRepository.restore')
def test_restore_no_mnemonic(mock_restore, mock_google_drive_manager, mock_app_paths, mock_get_hashed_mnemonic):
    """Case 3: Test restore service with missing mnemonic"""
    # Setup mocks
    mock_get_hashed_mnemonic.side_effect = CommonException(
        ERROR_UNABLE_GET_MNEMONIC,
    )
    mock_app_paths.restore_folder_path = os.path.join(
        os.path.dirname(__file__), 'some_path',
    )
    mock_app_paths.iriswallet_temp_folder_path = os.path.join(
        os.path.dirname(__file__), 'some_path',
    )
    mock_google_drive_manager.return_value = MagicMock()
    mock_google_drive_manager.return_value.download_from_drive.return_value = True
    mock_restore.return_value = RestoreResponseModel(status=True)

    # Call the RestoreService.restore method
    mnemonic = None
    password = 'test_password'

    with pytest.raises(CommonException, match=ERROR_UNABLE_GET_MNEMONIC):
        RestoreService.restore(mnemonic, password)


@patch('src.data.service.common_operation_service.CommonOperationService.get_hashed_mnemonic')
@patch('src.data.service.restore_service.app_paths')
def test_restore_no_password(mock_app_paths, mock_get_hashed_mnemonic):
    """Case 4: Test restore service with missing password"""

    # Setup mocks
    mock_get_hashed_mnemonic.return_value = 'e23ddff3cc'
    mock_app_paths.restore_folder_path = os.path.join(
        os.path.dirname(__file__), 'some_path',
    )
    mock_app_paths.iriswallet_temp_folder_path = os.path.join(
        os.path.dirname(__file__), 'some_path',
    )

    # Call the RestoreService.restore method
    mnemonic = 'test_mnemonic'
    password = None

    with pytest.raises(CommonException, match=ERROR_UNABLE_TO_GET_PASSWORD):
        RestoreService.restore(mnemonic, password)


@patch('src.data.service.common_operation_service.CommonOperationService.get_hashed_mnemonic')
@patch('src.data.service.restore_service.app_paths')
@patch('src.data.service.restore_service.GoogleDriveManager')
@patch('src.data.repository.common_operations_repository.CommonOperationRepository.restore')
def test_restore_no_hashed_value(mock_restore, mock_google_drive_manager, mock_app_paths, mock_get_hashed_mnemonic):
    """Case 5: Test restore service with missing hashed value"""

    # Setup mocks
    mock_get_hashed_mnemonic.side_effect = CommonException(
        ERROR_UNABLE_TO_GET_HASHED_MNEMONIC,
    )
    mock_app_paths.restore_folder_path = os.path.join(
        os.path.dirname(__file__), 'some_path',
    )
    mock_app_paths.iriswallet_temp_folder_path = os.path.join(
        os.path.dirname(__file__), 'some_path',
    )
    mock_google_drive_manager.return_value = MagicMock()
    mock_google_drive_manager.return_value.download_from_drive.return_value = True
    mock_restore.return_value = RestoreResponseModel(status=True)

    # Call the RestoreService.restore method
    with pytest.raises(CommonException, match=ERROR_UNABLE_TO_GET_HASHED_MNEMONIC):
        RestoreService.restore(mock_valid_mnemonic, mock_password)


@patch('src.data.service.restore_service.COMPATIBLE_RLN_NODE_COMMITS', ['abc'])
@patch('src.data.service.restore_service.read_ln_node_commit_id_file')
@patch('src.data.service.common_operation_service.CommonOperationService.get_hashed_mnemonic')
@patch('src.data.service.restore_service.app_paths')
@patch('src.data.service.restore_service.GoogleDriveManager')
def test_restore_download_error(mock_google_drive_manager, mock_app_paths, mock_get_hashed_mnemonic, mock_read_commit_id):
    """Case 6: Test restore service with download failure"""

    # Setup mocks
    mock_get_hashed_mnemonic.return_value = 'e23ddff3cc'
    mock_app_paths.restore_folder_path = os.path.join(
        os.path.dirname(__file__), 'some_path',
    )
    mock_app_paths.iriswallet_temp_folder_path = os.path.join(
        os.path.dirname(__file__), 'some_path',
    )
    mock_read_commit_id.return_value = 'abc'
    drive = MagicMock()
    mock_google_drive_manager.return_value = drive
    # First commit id download ok, second backup download fails
    drive.download_from_drive.side_effect = [True, False]

    # Call the RestoreService.restore method
    with pytest.raises(CommonException, match=ERROR_WHILE_RESTORE_DOWNLOAD_FROM_DRIVE):
        RestoreService.restore(mock_valid_mnemonic, mock_password)
