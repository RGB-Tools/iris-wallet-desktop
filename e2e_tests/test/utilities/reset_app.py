"""This module contains the script to delete the wallet data"""
from __future__ import annotations

import os
import shutil


def delete_app_data(directory_path: str):
    """
    Delete all files and directories in the specified directory.

    Args:
        directory_path (str): The path to the directory from which files and directories will be deleted.

    Raises:
        Exception: If an error occurs during the deletion process.
    """
    try:
        # Check if the directory exists
        if not os.path.exists(directory_path):
            print(f'Directory does not exist: {directory_path}')
            return

        # Remove all files and directories in the path
        for item in os.listdir(directory_path):
            item_path = os.path.join(directory_path, item)
            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.remove(item_path)  # Remove file or symbolic link
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)  # Remove directory and its contents

        print(
            f'All files and directories in {
                directory_path
            } have been deleted.',
        )
    except Exception as e:
        print(f'An error occurred while deleting files: {e}')
