"""Confirmation dialog box module"""
from __future__ import annotations

from PySide6.QtCore import QCoreApplication
from PySide6.QtCore import QSize
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog
from PySide6.QtWidgets import QGraphicsBlurEffect
from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QWidget

from accessible_constant import CONFIRMAION_DIALOG
from accessible_constant import CONFIRMATION_DIALOG_CANCEL_BUTTON
from accessible_constant import CONFIRMATION_DIALOG_CONTINUE_BUTTON
from src.utils.constant import IRIS_WALLET_TRANSLATIONS_CONTEXT
from src.utils.helpers import load_stylesheet
from src.views.components.buttons import PrimaryButton
from src.views.components.buttons import SecondaryButton


class ConfirmationDialog(QDialog):
    """
    A custom confirmation dialog with a message and two buttons: Continue and Cancel.

    This dialog is designed to display a message to the user and allow them to confirm
    or cancel an action. It uses a frameless window design with a blur effect and is modal.
    """

    def __init__(self, message: str, parent):
        super().__init__(parent)
        self.parent_widget = parent if parent else QWidget()
        self.blur_effect = QGraphicsBlurEffect()
        self.blur_effect.setBlurRadius(10)

        self.setObjectName('confirmation_dialog')
        self.setAccessibleName(CONFIRMAION_DIALOG)
        self.resize(300, 200)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setModal(True)
        self.setStyleSheet(
            load_stylesheet(
                'views/qss/confirmation_dialog.qss',
            ),
        )

        dialog_layout = QVBoxLayout(self)

        self.message_label = QLabel(message, self)
        self.message_label.setObjectName('message_label')
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.message_label.setWordWrap(True)

        dialog_layout.addWidget(self.message_label)

        self.button_layout = QHBoxLayout()
        self.button_layout.setObjectName('button_layout')
        self.button_layout.setContentsMargins(6, 6, 6, 12)

        self.confirmation_dialog_cancel_button = SecondaryButton()
        self.confirmation_dialog_cancel_button.setAccessibleName(
            CONFIRMATION_DIALOG_CANCEL_BUTTON,
        )
        self.confirmation_dialog_cancel_button.setMinimumSize(QSize(220, 35))
        self.confirmation_dialog_cancel_button.setMaximumSize(QSize(300, 35))
        self.button_layout.addWidget(self.confirmation_dialog_cancel_button)

        self.confirmation_dialog_continue_button = PrimaryButton()
        self.confirmation_dialog_continue_button.setAccessibleName(
            CONFIRMATION_DIALOG_CONTINUE_BUTTON,
        )
        self.confirmation_dialog_continue_button.setMinimumSize(QSize(220, 35))
        self.confirmation_dialog_continue_button.setMaximumSize(QSize(300, 35))
        self.button_layout.addWidget(self.confirmation_dialog_continue_button)

        dialog_layout.addLayout(self.button_layout)

        self.setup_ui_connection()
        self.retranslate_ui()

    def retranslate_ui(self):
        """Retranslate UI."""
        self.confirmation_dialog_continue_button.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'continue', None,
            ),
        )
        self.confirmation_dialog_cancel_button.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'cancel', None,
            ),
        )

    def setup_ui_connection(self):
        """Set up connections for UI elements."""
        self.confirmation_dialog_continue_button.clicked.connect(self.accept)
        self.confirmation_dialog_cancel_button.clicked.connect(self.reject)

    def showEvent(self, event):  # pylint:disable=invalid-name
        """Apply the blur effect to the parent widget when the dialog is shown."""
        if self.parent_widget:
            self.parent_widget.setGraphicsEffect(self.blur_effect)
        super().showEvent(event)

    def closeEvent(self, event):  # pylint:disable=invalid-name
        """Remove the blur effect from the parent widget when the dialog is closed."""
        if self.parent_widget:
            self.parent_widget.setGraphicsEffect(None)
        super().closeEvent(event)

    def accept(self):
        """Handle the Continue button click, remove blur, and accept the dialog."""
        if self.parent_widget:
            self.parent_widget.setGraphicsEffect(None)
        super().accept()
