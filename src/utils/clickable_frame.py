# pylint: disable=invalid-name,too-few-public-methods
# This class is intentionally designed as a data container (DTO / model).
# It stores structured data only and does not require additional public methods.
"""This module contains the ClickableFrame class, which represents a clickable frame widget.

This class inherits from QFrame and emits a clicked signal when a mouse press event occurs.

Attributes:
    clicked (Signal): A signal emitted when the frame is clicked, containing the frame ID.

Example:
    Creating a ClickableFrame instance:

        clickable_frame = ClickableFrame(_id='frame1', _name='Frame 1', image_path='path/to/image')
        clickable_frame.clicked.connect(handle_frame_click)

    Handling the click event:

        def handle_frame_click(frame_id, frame_name, image_path):
            print("Clicked Frame ID:", frame_id)
            print("Frame Name:", frame_name)
            print("Image Path:", image_path)

        clickable_frame = ClickableFrame(_id='frame1', _name='Frame 1', image_path='path/to/image')
        clickable_frame.clicked.connect(handle_frame_click)
"""
from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtCore import Signal
from PySide6.QtGui import QCursor
from PySide6.QtWidgets import QFrame


class ClickableFrame(QFrame):
    """This class represents a clickable frame."""

    # Signal emits ID, name, and image path
    clicked = Signal(str, str, str, str)

    def __init__(self, _id=None, _name=None, image_path=None, asset_type=None, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self._id = _id
        self._name = _name
        self._image_path = image_path
        self._asset_type = asset_type
        self.setCursor(
            QCursor(Qt.CursorShape.PointingHandCursor),
        )

    def mousePressEvent(self, event):
        """Handles the mouse press event to emit the clicked signal."""
        self.clicked.emit(
            self._id, self._name,
            self._image_path, self._asset_type,
        )
        super().mousePressEvent(event)
