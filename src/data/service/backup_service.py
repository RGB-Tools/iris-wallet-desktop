"""
This module provides the service for backup.
"""
from __future__ import annotations

import os

from src.data.repository.common_operations_repository import CommonOperationRepository
from src.model.common_operation_model import BackupRequestModel
from src.utils.custom_exception import CommonException
from src.utils.error_message import ERROR_BACKUP_FILE_NOT_EXITS
from src.utils.error_message import ERROR_UNABLE_GET_MNEMONIC
from src.utils.error_message import ERROR_UNABLE_TO_GET_HASHED_MNEMONIC
from src.utils.error_message import ERROR_UNABLE_TO_GET_PASSWORD
from src.utils.gdrive_operation import GoogleDriveManager
from src.utils.handle_exception import handle_exceptions
from src.utils.helpers import hash_mnemonic
from src.utils.local_store import local_store
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
        Creates a backup of the node's data and uploads it to Google Drive.

        Returns:
            bool: True if the backup and upload were successful, False otherwise.

        Raises:
            CommonException: If any operation fails during the backup process.
        """
        try:
            logger.info('Back up process started...')
            if not mnemonic:
                raise CommonException(ERROR_UNABLE_GET_MNEMONIC)

            hashed_mnemonic = hash_mnemonic(mnemonic_phrase=mnemonic)

            if not hashed_mnemonic:
                raise CommonException(ERROR_UNABLE_TO_GET_HASHED_MNEMONIC)

            backup_file_name: str = f'{hashed_mnemonic}.rgb_backup'

            local_store_base_path = local_store.get_path()
            backup_folder_path = os.path.join(local_store_base_path, 'backup')

            # Ensure the backup folder exists
            if not os.path.exists(backup_folder_path):
                logger.info('Creating backup folder')
                local_store.create_folder('backup')

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
            return success
        except Exception as exc:
            return handle_exceptions(exc)
