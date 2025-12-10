"""
This module provides the service for backup.
"""
from __future__ import annotations

import os
import shutil

from src.data.repository.common_operations_repository import CommonOperationRepository
from src.data.service.common_operation_service import CommonOperationService
from src.model.common_operation_model import BackupRequestModel
from src.utils.build_app_path import app_paths
from src.utils.custom_exception import CommonException
from src.utils.error_message import ERROR_BACKUP_FILE_NOT_EXITS
from src.utils.error_message import ERROR_UNABLE_TO_GET_PASSWORD
from src.utils.gdrive_operation import GoogleDriveManager
from src.utils.handle_exception import handle_exceptions
from src.utils.helpers import write_ln_node_commit_id_file
from src.utils.logging import logger


class BackupService:
    """
    Service class to handle the backup operations.
    """
    @staticmethod
    def backup_file_exists(file_path: str) -> bool:
        """
        Check if a file exists at the given path.

        :param file_path: Path of the file to check.
        :return: True if file exists, False otherwise.
        """
        return os.path.exists(file_path)

    @staticmethod
    def backup(mnemonic: str, password: str) -> bool:
        """
        Creates a temporary backup of the node's data, uploads it to Google Drive,
        and deletes the local backup after a successful upload.

        Returns:
            bool: True if the backup and upload were successful, False otherwise.

        Raises:
            CommonException: If any operation fails during the backup process.
        """
        try:
            logger.info('Back up process started...')

            backup_folder_path = app_paths.backup_folder_path

            hashed_mnemonic = CommonOperationService.get_hashed_mnemonic(
                mnemonic=mnemonic,
            )

            backup_file_name: str = f'{hashed_mnemonic}.rgb_backup'

            # Ensure the backup folder exists
            if not os.path.exists(backup_folder_path):
                logger.info('Creating backup folder')
                os.makedirs(backup_folder_path, exist_ok=True)

            backup_file_path = os.path.join(
                backup_folder_path, backup_file_name,
            )

            # Remove if old backup file available at local store of application
            if os.path.exists(backup_file_path):
                os.remove(backup_file_path)

            if not password:
                raise CommonException(
                    ERROR_UNABLE_TO_GET_PASSWORD,
                )

            # Perform the backup operation
            logger.info('Calling backup api')
            CommonOperationRepository.backup(
                BackupRequestModel(
                    backup_path=backup_file_path, password=password,
                ),
            )

            # Verify the backup file exists
            if not BackupService.backup_file_exists(backup_file_path):
                error_message = ERROR_BACKUP_FILE_NOT_EXITS+' '+backup_file_path
                raise CommonException(
                    error_message,
                )

            # Upload the backup to Google Drive
            backup = GoogleDriveManager()
            success: bool = backup.upload_to_drive(
                file_path=backup_file_path, file_name=backup_file_name,
            )

            commit_id_file_path, commit_id_file_name = write_ln_node_commit_id_file(
                hashed_mnemonic,
            )
            commit_id_success: bool = backup.upload_to_drive(
                file_path=commit_id_file_path, file_name=commit_id_file_name,
            )
            return success and commit_id_success
        except Exception as exc:
            return handle_exceptions(exc)
        finally:
            if os.path.exists(app_paths.iriswallet_temp_folder_path):
                shutil.rmtree(
                    app_paths.iriswallet_temp_folder_path, ignore_errors=True,
                )
                logger.info('Deleting backup folder')
