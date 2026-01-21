"""
Image utility functions.

Provides functions for copying images to the home directory.
"""
from __future__ import annotations

import shutil
from pathlib import Path


def copy_cfa_image_to_home_directory(current_working_directory):
    """
    Copies the sample.png image from the e2e_tests/assets directory to the home directory.

    Args:
        current_working_directory (str): The current working directory.

    Returns:
        Path: The path to the copied image in the home directory.
    """
    # Get the home directory
    home_directory = Path.home()

    # Set the target directory for the asset (image)
    image_source_path = Path(current_working_directory) / \
        'e2e_tests' / 'assets' / 'sample.png'

    # Set the destination directory inside the home directory
    image_destination_path = home_directory / 'sample.png'

    # Copy the image from target_directory to home_dir
    shutil.copy(str(image_source_path), str(image_destination_path))

    # Now set the asset path in home directory
    image_path_in_home = home_directory / 'sample.png'

    return image_path_in_home
