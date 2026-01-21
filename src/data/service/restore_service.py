# pylint:disable = too-few-public-methods
"""
This module provides the service for restore.
"""
from __future__ import annotations

import os
import shutil

from src.data.repository.common_operations_repository import CommonOperationRepository
from src.data.repository.setting_repository import SettingRepository
from src.data.service.common_operation_service import CommonOperationService
from src.model.common_operation_model import RestoreRequestModel
from src.model.common_operation_model import RestoreResponseModel
from src.utils.build_app_path import app_paths
from src.utils.constant import COMPATIBLE_RLN_NODE_COMMITS
from src.utils.custom_exception import CommonException
from src.utils.error_message import ERROR_NOT_BACKUP_FILE
from src.utils.error_message import ERROR_UNABLE_TO_GET_PASSWORD
from src.utils.error_message import ERROR_WHILE_RESTORE_DOWNLOAD_FROM_DRIVE
from src.utils.gdrive_operation import GoogleDriveManager
from src.utils.handle_exception import handle_exceptions
from src.utils.helpers import read_ln_node_commit_id_file
from src.utils.logging import logger


class RestoreService:
    """
    Service class to handle the backup operations.
    """

    @staticmethod
    def restore(mnemonic: str, password: str) -> RestoreResponseModel:
        """
        Creates a temporary backup of the node's data, uploads it to Google Drive, and deletes the temporary copy afterward.

        Returns:
            bool: True if the backup and upload were successful, False otherwise.

        Raises:
            CommonException: If any operation fails during the backup process.
        """
        try:
            restore_folder_path = app_paths.restore_folder_path
            hashed_mnemonic = CommonOperationService.get_hashed_mnemonic(
                mnemonic=mnemonic,
            )

            restore_file_name: str = f'{hashed_mnemonic}.rgb_backup'

            # Ensure the backup folder exists
            if not os.path.exists(restore_folder_path):
                logger.info('Creating backup folder')
                os.makedirs(restore_folder_path, exist_ok=True)

            restore_file_path = os.path.join(
                restore_folder_path, restore_file_name,
            )

            # Remove if old backup file available at local store of application
            if os.path.exists(restore_file_path):
                os.remove(restore_file_path)

            if not password:
                raise CommonException(
                    ERROR_UNABLE_TO_GET_PASSWORD,
                )

            # Download restore zip from Google Drive
            logger.info('Downloading restore zip from drive')
            restore = GoogleDriveManager()
            commit_id_file_name = f'{hashed_mnemonic}.commit'
            restore.download_from_drive(
                file_name=commit_id_file_name, destination_dir=restore_folder_path,
            )

            commit_id = read_ln_node_commit_id_file(commit_id_file_name)
            if commit_id not in COMPATIBLE_RLN_NODE_COMMITS:
                raise CommonException('RGB_LIB_INCOMPATIBLE')
            SettingRepository.set_rln_node_commit_id(
                commit_id,
            )
            success: bool | None = restore.download_from_drive(
                file_name=restore_file_name, destination_dir=restore_folder_path,
            )

            if success is None:
                raise CommonException(ERROR_NOT_BACKUP_FILE)

            if not success:
                raise CommonException(ERROR_WHILE_RESTORE_DOWNLOAD_FROM_DRIVE)

            # Perform the Restore operation
            logger.info('Calling restore api')
            response: RestoreResponseModel = CommonOperationRepository.restore(
                RestoreRequestModel(
                    backup_path=restore_file_path, password=password,
                ),
            )
            return response
        except Exception as exc:
            return handle_exceptions(exc)
        finally:
            if os.path.exists(app_paths.iriswallet_temp_folder_path):
                shutil.rmtree(app_paths.iriswallet_temp_folder_path)
                logger.info('Deleting restore folder')
