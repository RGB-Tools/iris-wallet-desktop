# pylint: disable=too-many-instance-attributes, too-many-statements, unused-import
"""This module contains the RestoreMnemonicWidget class,
which represents the UI for restore page.
"""
from __future__ import annotations

from PySide6.QtCore import QCoreApplication
from PySide6.QtCore import QSize
from PySide6.QtCore import Qt
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QDialog
from PySide6.QtWidgets import QFrame
from PySide6.QtWidgets import QGridLayout
from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QLineEdit
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtWidgets import QSpacerItem
from PySide6.QtWidgets import QVBoxLayout

from accessible_constant import RESTORE_CONTINUE_BUTTON
from accessible_constant import RESTORE_DIALOG_BOX
from accessible_constant import RESTORE_MNEMONIC_INPUT
from accessible_constant import RESTORE_PASSWORD_INPUT
from src.utils.constant import IRIS_WALLET_TRANSLATIONS_CONTEXT
from src.utils.helpers import load_stylesheet
from src.viewmodels.main_view_model import MainViewModel
from src.views.components.toast import ToastManager


class RestoreMnemonicWidget(QDialog):
    """This class represents all the  elements of the restore dialog box."""
    on_continue = Signal(str, str)

    def __init__(self, parent=None, view_model: MainViewModel | None = None, origin_page: str = 'restore_page', mnemonic_visibility: bool = True):
        super().__init__(parent)
        self.setObjectName('self')
        self.setAccessibleName(RESTORE_DIALOG_BOX)
        self._view_model = view_model
        self.origin_page: str = origin_page
        self.mnemonic_visibility = mnemonic_visibility
        # Hide the title bar and close button
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.resize(370, 340)
        self.setStyleSheet(
            load_stylesheet(
                'views/qss/restore_mnemonic_style.qss',
            ),
        )
        self.grid_layout = QGridLayout(self)
        self.grid_layout.setObjectName('gridLayout')
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.mnemonic_frame = QFrame(self)
        self.mnemonic_frame.setObjectName('mnemonic_frame')
        self.mnemonic_frame.setMinimumSize(QSize(335, 292))
        self.mnemonic_frame.setFrameShape(QFrame.StyledPanel)
        self.mnemonic_frame.setFrameShadow(QFrame.Raised)
        self.vertical_layout_frame = QVBoxLayout(self.mnemonic_frame)
        self.vertical_layout_frame.setSpacing(20)
        self.vertical_layout_frame.setObjectName('vertical_layout_frame')
        self.vertical_layout_frame.setContentsMargins(25, -1, 25, -1)
        self.mnemonic_detail_text_label = QLabel(self.mnemonic_frame)
        self.mnemonic_detail_text_label.setObjectName(
            'mnemonic_detail_text_label',
        )
        self.mnemonic_detail_text_label.setMinimumSize(QSize(295, 84))

        self.mnemonic_detail_text_label.setWordWrap(True)

        self.vertical_layout_frame.addWidget(self.mnemonic_detail_text_label)

        self.mnemonic_input = QLineEdit(self.mnemonic_frame)
        self.mnemonic_input.setObjectName('mnemonic_input')
        self.mnemonic_input.setAccessibleName(RESTORE_MNEMONIC_INPUT)
        self.mnemonic_input.setMinimumSize(QSize(295, 56))

        self.vertical_layout_frame.addWidget(self.mnemonic_input)

        self.password_input = QLineEdit(self.mnemonic_frame)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setObjectName('password_input')
        self.password_input.setAccessibleName(RESTORE_PASSWORD_INPUT)
        self.password_input.setMinimumSize(QSize(295, 56))

        self.vertical_layout_frame.addWidget(self.password_input)

        self.horizontal_button_layout_restore = QHBoxLayout()
        self.horizontal_button_layout_restore.setSpacing(20)
        self.horizontal_button_layout_restore.setObjectName(
            'horizontal_button_layout',
        )
        self.horizontal_button_spacer = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum,
        )

        self.horizontal_button_layout_restore.addItem(
            self.horizontal_button_spacer,
        )

        self.cancel_button = QPushButton(self.mnemonic_frame)
        self.cancel_button.setObjectName('cancel_button')
        self.cancel_button.setMinimumSize(QSize(74, 38))
        self.cancel_button.setMaximumSize(QSize(74, 38))

        self.horizontal_button_layout_restore.addWidget(self.cancel_button)

        self.continue_button = QPushButton(self.mnemonic_frame)
        self.continue_button.setObjectName('continue_button')
        self.continue_button.setAccessibleName(RESTORE_CONTINUE_BUTTON)
        self.continue_button.setMinimumSize(QSize(74, 38))
        self.continue_button.setMaximumSize(QSize(74, 38))

        self.horizontal_button_layout_restore.addWidget(self.continue_button)

        self.vertical_layout_frame.addLayout(
            self.horizontal_button_layout_restore,
        )
        self.continue_button.setEnabled(False)
        self.grid_layout.addWidget(self.mnemonic_frame, 0, 0, 1, 1)
        self.setup_ui_connection()
        self.retranslate_ui()
        self.handle_mnemonic_input_visibility()

    def setup_ui_connection(self):
        """Set up connections for UI elements."""
        self.cancel_button.clicked.connect(self.on_click_cancel)
        self.continue_button.clicked.connect(self.on_continue_button_click)
        self.password_input.textChanged.connect(self.handle_button_enable)
        self.mnemonic_input.textChanged.connect(self.handle_button_enable)

    def handle_button_enable(self):
        """Handles the enable/disable state of the continue button."""
        if self.mnemonic_visibility:
            is_ready = bool(self.password_input.text()) and bool(
                self.mnemonic_input.text(),
            )
        else:
            is_ready = bool(self.password_input.text())

        self.continue_button.setEnabled(is_ready)

    def retranslate_ui(self):
        """Retranslate the UI elements."""
        self.mnemonic_detail_text_label.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'enter_mnemonic_phrase_info', None,
            ),
        )
        self.mnemonic_input.setPlaceholderText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'input_phrase', None,
            ),
        )
        self.cancel_button.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'cancel', None,
            ),
        )
        self.continue_button.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'continue', None,
            ),
        )
        self.password_input.setPlaceholderText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'enter_wallet_password', None,
            ),
        )

    def handle_on_keyring_toggle_enable(self):
        """Handle when user enable toggle from setting page"""
        mnemonic = str(self.mnemonic_input.text())
        password = str(self.password_input.text())
        self._view_model.setting_view_model.enable_keyring(
            mnemonic=mnemonic, password=password,
        )
        self.close()

    def on_continue_button_click(self):
        """Handle on continue"""
        mnemonic = str(self.mnemonic_input.text())
        password = str(self.password_input.text())
        if self.origin_page == 'restore_page':
            self.restore_wallet()
        elif self.origin_page == 'setting_page':
            self.handle_on_keyring_toggle_enable()
        elif self.origin_page == 'backup_page':
            self._view_model.backup_view_model.backup_when_keyring_unaccessible(
                mnemonic=mnemonic, password=password,
            )
            self.close()
        elif self.origin_page == 'on_close':
            self.on_continue.emit(mnemonic, password)
            self.close()
        elif self.origin_page == 'setting_card':
            self.accept()
        else:
            ToastManager.error('Unknown origin page')

    def restore_wallet(self):
        """This method restore the wallet"""
        self.accept()
        mnemonic = self.mnemonic_input.text()
        password = self.password_input.text()
        self._view_model.restore_view_model.restore(
            mnemonic=mnemonic, password=password,
        )

    def on_click_cancel(self):
        """The `on_click_cancel` method closes the dialog when the cancel button is clicked."""
        self.close()

    def handle_mnemonic_input_visibility(self):
        """handle mnemonic visibility for Qdialog"""
        if not self.mnemonic_visibility:
            self.mnemonic_input.hide()
            self.setMaximumSize(QSize(370, 220))
        else:
            self.setMaximumSize(QSize(370, 292))
            self.mnemonic_input.show()
