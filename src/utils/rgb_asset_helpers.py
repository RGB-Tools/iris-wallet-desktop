"""Helper utilities for RGB asset detail operations.

This module contains validation and image handling functions extracted from
the RGBAssetDetailWidget to improve code organization and testability.
"""
from __future__ import annotations

import re

from PySide6.QtCore import QSize
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel

from src.utils.common_utils import convert_hex_to_image
from src.utils.common_utils import resize_image


def is_path(file_path: str) -> bool:
    """Check if the string is a valid Unix-like file path.

    Args:
        file_path: String to validate as a file path.

    Returns:
        True if file_path matches Unix file path pattern, False otherwise.
    """
    if not isinstance(file_path, str):
        return False
    # Define a basic regex pattern for Unix-like file paths
    pattern = r'^(\/[a-zA-Z0-9_.-]+)+\/?$'
    # Check if the file_path matches the pattern
    return bool(re.match(pattern, file_path))


def is_hex_string(bytes_hex: str) -> bool:
    """Check if the string is a valid hex string.

    Args:
        bytes_hex: String to validate as hexadecimal.

    Returns:
        True if bytes_hex is a valid hex string with even length, False otherwise.
    """
    if len(bytes_hex) % 2 != 0:
        return False
    hex_pattern = re.compile(r'^[0-9a-fA-F]+$')
    return bool(hex_pattern.match(bytes_hex))


def set_asset_image(label_widget: QLabel, image_hex: str) -> None:
    """Set the asset image on a QLabel from hex string or file path.

    Args:
        label_widget: QLabel widget to set the image on.
        image_hex: Hex string or file path of the image.
    """
    if is_hex_string(image_hex):
        pixmap = convert_hex_to_image(image_hex)
        resized_image = resize_image(pixmap, 335, 335)
        label_widget.setPixmap(resized_image)
    else:
        resized_image = resize_image(image_hex, 335, 335)
        label_widget.setPixmap(resized_image)


def handle_img_path(
    widget, image_path: str, asset_image_layout,
    asset_id_frame, label_asset_name: QLabel | None = None,
) -> QLabel:
    """Configure the asset detail widget based on the provided image path.

    Adjusts the layout and styles, and sets the asset image.

    Args:
        widget: The parent widget to configure.
        image_path: Path or hex string of the asset image.
        asset_image_layout: Layout to add the image label to.
        asset_id_frame: Frame containing the asset ID.
        label_asset_name: Optional existing label, or None to create new one.

    Returns:
        The QLabel widget containing the asset image.
    """
    if not image_path:
        return label_asset_name

    widget.setMinimumSize(QSize(466, 848))
    widget.setFixedWidth(499)

    if label_asset_name is None:
        label_asset_name = QLabel(widget)
        label_asset_name.setObjectName('label_asset_name')

    label_asset_name.setMaximumSize(QSize(335, 335))
    asset_id_frame.setMinimumSize(QSize(335, 86))
    asset_id_frame.setMaximumSize(QSize(335, 86))
    label_asset_name.setStyleSheet(
        "font: 14px \"Inter\";\n"
        'color: #B3B6C3;\n'
        'background: transparent;\n'
        'border: none;\n'
        'border-radius: 8px;\n'
        'font-weight: 400;\n'
        '',
    )
    asset_image_layout.addWidget(
        label_asset_name, 0, Qt.AlignHCenter,
    )
    set_asset_image(label_asset_name, image_hex=image_path)

    return label_asset_name
