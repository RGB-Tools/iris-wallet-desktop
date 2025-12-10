"""Unit tests for backup method of back service"""
# pylint: disable=redefined-outer-name,unused-argument,too-many-arguments
from __future__ import annotations

import os
import shutil
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest

from src.data.service.backup_service import BackupService
from src.utils.custom_exception import CommonException
from src.utils.error_message import ERROR_BACKUP_FILE_NOT_EXITS
from src.utils.error_message import ERROR_UNABLE_GET_MNEMONIC
from src.utils.error_message import ERROR_UNABLE_TO_GET_HASHED_MNEMONIC
from src.utils.error_message import ERROR_UNABLE_TO_GET_PASSWORD
from unit_tests.service_test_resources.mocked_fun_return_values.backup_service import mock_password
from unit_tests.service_test_resources.mocked_fun_return_values.backup_service import mock_valid_mnemonic

# Setup function


@pytest.fixture(scope='function')
def setup_directory():
    """Set up method for test"""
    test_dir = os.path.join(os.path.dirname(__file__), 'iris-wallet-test')

    backup_dir = os.path.join(test_dir, 'backup')

    # Create the iris-wallet-test directory
    os.makedirs(test_dir, exist_ok=True)

    # Create the backup directory inside iris-wallet-test
    os.makedirs(backup_dir, exist_ok=True)

    return test_dir, backup_dir

# Teardown function


@pytest.fixture(scope='function', autouse=True)
def teardown_directory_after_test():
    """Clean up function after test"""
    yield
    test_dir = os.path.join(os.path.dirname(__file__), 'iris-wallet-test')
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    assert not os.path.exists(test_dir)

# Test function


@patch('src.data.service.common_operation_service.CommonOperationService.get_hashed_mnemonic')
@patch('src.data.service.backup_service.app_paths')
@patch('src.data.service.backup_service.BackupService.backup_file_exists')
@patch('src.data.repository.common_operations_repository.CommonOperationRepository.backup')
@patch('src.data.service.backup_service.write_ln_node_commit_id_file')
@patch('src.data.service.backup_service.GoogleDriveManager')
def test_backup(mock_google_drive_manager, mock_write_commit_file, mock_backup, mock_backup_file_exits, mock_app_paths, mock_get_hashed_mnemonic, setup_directory):
    """Case 1 : Test backup service"""
    test_dir, backup_dir = setup_directory

    # Setup mocks
    mock_get_hashed_mnemonic.return_value = 'e23ddff3cc'
    mock_app_paths.backup_folder_path = backup_dir
    mock_app_paths.iriswallet_temp_folder_path = test_dir

    mock_backup_instance = MagicMock()
    mock_backup.return_value = None
    mock_backup_file_exits.return_value = True
    mock_backup_instance.return_value = None
    mock_google_drive_manager.return_value = mock_backup_instance
    # Two uploads: backup file and commit id file
    mock_backup_instance.upload_to_drive.side_effect = [True, True]
    # commit id file path and name
    mock_write_commit_file.return_value = (
        os.path.join(
            backup_dir, 'e23ddff3cc.commit',
        ), 'e23ddff3cc.commit',
    )

    result = BackupService.backup(mock_valid_mnemonic, mock_password)

    # Assert the result
    assert result is True

# Test function


@patch('src.data.service.common_operation_service.CommonOperationService.get_hashed_mnemonic')
@patch('src.data.service.backup_service.app_paths')
@patch('src.data.service.backup_service.BackupService.backup_file_exists')
@patch('src.data.repository.common_operations_repository.CommonOperationRepository.backup')
@patch('src.data.service.backup_service.write_ln_node_commit_id_file')
@patch('src.data.service.backup_service.GoogleDriveManager')
def test_backup_when_backup_file_not_exits(
    mock_google_drive_manager, mock_write_commit_file,
    mock_backup, mock_backup_file_exits, mock_app_paths, mock_get_hashed_mnemonic, setup_directory,
):
    """Case  2: When backup not exits after api call"""
    test_dir, backup_dir = setup_directory

    # Setup mocks
    mock_get_hashed_mnemonic.return_value = 'e23ddff3cc'
    mock_app_paths.backup_folder_path = backup_dir
    mock_app_paths.iriswallet_temp_folder_path = test_dir

    mock_backup_instance = MagicMock()
    mock_backup.return_value = None
    mock_backup_file_exits.return_value = False
    mock_backup_instance.return_value = None
    mock_google_drive_manager.return_value = mock_backup_instance
    mock_backup_instance.upload_to_drive.side_effect = [True, True]
    mock_write_commit_file.return_value = (
        os.path.join(
            backup_dir, 'e23ddff3cc.commit',
        ), 'e23ddff3cc.commit',
    )
    error_message = ERROR_BACKUP_FILE_NOT_EXITS
    with pytest.raises(CommonException, match=error_message):
        BackupService.backup(mock_valid_mnemonic, mock_password)


@patch('src.data.service.common_operation_service.CommonOperationService.get_hashed_mnemonic')
@patch('src.data.service.backup_service.app_paths')
@patch('src.data.service.backup_service.BackupService.backup_file_exists')
@patch('src.data.repository.common_operations_repository.CommonOperationRepository.backup')
def test_backup_no_mnemonic(mock_backup, mock_backup_file_exits, mock_app_paths, mock_get_hashed_mnemonic):
    """Case 3 : Test backup service with missing mnemonic"""
    # Setup mocks
    mock_get_hashed_mnemonic.side_effect = CommonException(
        ERROR_UNABLE_GET_MNEMONIC,
    )
    mock_app_paths.backup_folder_path = os.path.join(
        os.path.dirname(__file__), 'some_path',
    )
    mock_app_paths.iriswallet_temp_folder_path = os.path.join(
        os.path.dirname(__file__), 'some_path',
    )
    mock_backup.return_value = None
    mock_backup_file_exits.return_value = True

    # Call the BackupService.backup method
    mnemonic = None
    password = 'demo_password'

    with pytest.raises(CommonException, match=ERROR_UNABLE_GET_MNEMONIC):
        BackupService.backup(mnemonic, password)


@patch('src.data.service.common_operation_service.CommonOperationService.get_hashed_mnemonic')
@patch('src.data.service.backup_service.app_paths')
def test_backup_no_password(mock_app_paths, mock_get_hashed_mnemonic):
    """Case 4 : Test backup service with missing password"""

    # Setup mocks
    mock_get_hashed_mnemonic.return_value = 'e23ddff3cc'
    mock_app_paths.backup_folder_path = os.path.join(
        os.path.dirname(__file__), 'some_path',
    )
    mock_app_paths.iriswallet_temp_folder_path = os.path.join(
        os.path.dirname(__file__), 'some_path',
    )

    # Call the BackupService.backup method
    mnemonic = 'demo_mnemonic'
    password = None

    with pytest.raises(CommonException, match=ERROR_UNABLE_TO_GET_PASSWORD):
        BackupService.backup(mnemonic, password)


@patch('src.data.service.common_operation_service.CommonOperationService.get_hashed_mnemonic')
@patch('src.data.service.backup_service.app_paths')
@patch('src.data.service.backup_service.BackupService.backup_file_exists')
@patch('src.data.repository.common_operations_repository.CommonOperationRepository.backup')
def test_backup_no_hashed_value(mock_backup, mock_backup_file_exits, mock_app_paths, mock_get_hashed_mnemonic):
    """Case 5 : Test backup service with missing hashed value"""

    # Setup mocks
    mock_get_hashed_mnemonic.side_effect = CommonException(
        ERROR_UNABLE_TO_GET_HASHED_MNEMONIC,
    )
    mock_app_paths.backup_folder_path = os.path.join(
        os.path.dirname(__file__), 'some_path',
    )
    mock_app_paths.iriswallet_temp_folder_path = os.path.join(
        os.path.dirname(__file__), 'some_path',
    )
    mock_backup.return_value = None
    mock_backup_file_exits.return_value = True

    # Call the BackupService.backup method
    with pytest.raises(CommonException, match=ERROR_UNABLE_TO_GET_HASHED_MNEMONIC):
        BackupService.backup(mock_valid_mnemonic, mock_password)


def test_backup_file_exists():
    """Case 6 : test backup_file_exists"""
    result = BackupService.backup_file_exists('./random_path')
    assert result is False
