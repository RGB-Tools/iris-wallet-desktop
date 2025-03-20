# pylint: disable=too-many-instance-attributes, too-many-statements, unused-import
"""This module contains the WelcomeWidget class,
which represents the UI for welcome page.
"""
from __future__ import annotations

from PySide6.QtCore import QCoreApplication
from PySide6.QtCore import QSize
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame
from PySide6.QtWidgets import QGraphicsBlurEffect
from PySide6.QtWidgets import QGridLayout
from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QPlainTextEdit
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtWidgets import QSpacerItem
from PySide6.QtWidgets import QWidget

import src.resources_rc
from accessible_constant import CREATE_BUTTON
from accessible_constant import RESTORE_BUTTON
from src.model.enums.enums_model import ToastPreset
from src.utils.constant import IRIS_WALLET_TRANSLATIONS_CONTEXT
from src.utils.helpers import load_stylesheet
from src.viewmodels.main_view_model import MainViewModel
from src.views.components.buttons import PrimaryButton
from src.views.components.buttons import SecondaryButton
from src.views.components.toast import ToastManager
from src.views.components.wallet_logo_frame import WalletLogoFrame
from src.views.ui_restore_mnemonic import RestoreMnemonicWidget


class WelcomeWidget(QWidget):
    """This class represents all the UI elements of the welcome page."""

    def __init__(self, view_model):
        super().__init__()
        self.setStyleSheet(
            load_stylesheet('views/qss/welcome_style.qss'),
        )
        self._view_model: MainViewModel = view_model
        self.setObjectName('welcome_Page')
        self.grid_layout_welcome = QGridLayout(self)
        self.grid_layout_welcome.setObjectName('gridLayout')
        self.welcome_horizontal_spacer = QSpacerItem(
            135,
            20,
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Minimum,
        )
        self.grid_layout_welcome.addItem(
            self.welcome_horizontal_spacer,
            1,
            0,
            1,
            1,
        )
        self.horizontal_spacer_welcome = QSpacerItem(
            135,
            20,
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Minimum,
        )
        self.grid_layout_welcome.addItem(
            self.horizontal_spacer_welcome,
            2,
            4,
            1,
            1,
        )
        self.vertical_spacer_tnc = QSpacerItem(
            20,
            178,
            QSizePolicy.Policy.Minimum,
            QSizePolicy.Policy.Expanding,
        )
        self.grid_layout_welcome.addItem(self.vertical_spacer_tnc, 0, 2, 1, 1)
        self.vertical_spacer_1 = QSpacerItem(
            20,
            177,
            QSizePolicy.Policy.Minimum,
            QSizePolicy.Policy.Expanding,
        )
        self.grid_layout_welcome.addItem(self.vertical_spacer_1, 3, 3, 1, 1)

        self.welcome_widget = QWidget(self)
        self.welcome_widget.setObjectName('welcome_widget')
        self.welcome_widget.setMinimumSize(QSize(696, 526))
        self.welcome_widget.setMaximumSize(QSize(696, 526))

        self.grid_layout_1 = QGridLayout(self.welcome_widget)
        self.grid_layout_1.setObjectName('grid_layout_1')
        self.grid_layout_1.setContentsMargins(1, -1, 1, 25)

        self.header_line = QFrame(self.welcome_widget)
        self.header_line.setObjectName('TnC_line')
        self.header_line.setMinimumSize(QSize(690, 0))

        self.header_line.setFrameShape(QFrame.Shape.HLine)
        self.header_line.setFrameShadow(QFrame.Sunken)

        self.grid_layout_1.addWidget(self.header_line, 1, 0, 1, 1)

        self.welcome_text_desc = QPlainTextEdit(self.welcome_widget)
        self.welcome_text_desc.setObjectName('welcome_text_desc')
        self.welcome_text_desc.setMinimumSize(QSize(644, 348))
        self.welcome_text_desc.setMaximumSize(QSize(644, 348))
        self.welcome_text_desc.setStyleSheet(
            load_stylesheet('views/qss/q_label.qss'),
        )
        self.welcome_text_desc.setReadOnly(True)

        self.grid_layout_1.addWidget(
            self.welcome_text_desc, 2, 0, 1, 1, Qt.AlignHCenter,
        )

        self.grid_layout_2 = QGridLayout()
        self.grid_layout_2.setObjectName('grid_layout_2')
        self.grid_layout_2.setContentsMargins(25, -1, 27, -1)

        self.welcome_text = QLabel(self.welcome_widget)
        self.welcome_text.setObjectName('welcome_text')
        self.welcome_text.setStyleSheet(
            load_stylesheet('views/qss/q_label.qss'),
        )

        self.grid_layout_2.addWidget(self.welcome_text, 0, 0, 1, 1)

        self.grid_layout_1.addLayout(self.grid_layout_2, 0, 0, 1, 1)

        self.welcome_horizontal_layout = QHBoxLayout()
        self.welcome_horizontal_layout.setSpacing(0)
        self.welcome_horizontal_layout.setObjectName(
            'welcome_horizontal_layout',
        )
        self.welcome_horizontal_layout.setContentsMargins(8, -1, 8, -1)

        self.restore_btn = SecondaryButton()
        self.restore_btn.setAccessibleName(RESTORE_BUTTON)
        self.restore_btn.setMinimumSize(QSize(318, 40))
        self.restore_btn.setMaximumSize(QSize(318, 40))
        self.welcome_horizontal_layout.addWidget(self.restore_btn)

        self.create_btn = PrimaryButton()
        self.create_btn.setAccessibleName(CREATE_BUTTON)
        self.create_btn.setMinimumSize(QSize(318, 40))
        self.create_btn.setMaximumSize(QSize(318, 40))

        self.welcome_horizontal_layout.addWidget(self.create_btn)

        self.grid_layout_1.addLayout(
            self.welcome_horizontal_layout,
            4,
            0,
            1,
            1,
        )

        self.vertical_spacer_12 = QSpacerItem(
            20,
            40,
            QSizePolicy.Policy.Minimum,
            QSizePolicy.Policy.Expanding,
        )
        self.grid_layout_1.addItem(self.vertical_spacer_12, 3, 0, 1, 1)

        self.grid_layout_welcome.addWidget(self.welcome_widget, 1, 1, 2, 3)

        self.wallet_logo = WalletLogoFrame()
        self.grid_layout_welcome.addWidget(self.wallet_logo, 0, 0, 1, 2)

        self.retranslate_ui()
        self.setup_ui_connection()

    # setupUi

    def setup_ui_connection(self):
        """Set up connections for UI elements."""
        self.create_btn.clicked.connect(
            self._view_model.welcome_view_model.on_create_click,
        )
        self.restore_btn.clicked.connect(
            self.restore_wallet,
        )
        self._view_model.welcome_view_model.create_button_clicked.connect(
            self.update_create_status,
        )
        self._view_model.restore_view_model.is_loading.connect(
            self.update_loading_state,
        )
        self._view_model.restore_view_model.message.connect(
            self.handle_message,
        )

    def retranslate_ui(self):
        """Retranslate the UI elements."""
        self.wallet_logo.logo_text.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT,
                'iris_wallet',
                None,
            ),
        )
        self.welcome_text.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT,
                'welcome_label',
                None,
            ),
        )
        self.welcome_text_desc.setPlainText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT,
                'welcome_text_description',
                None,
            ),
        )
        self.restore_btn.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT,
                'restore_button',
                None,
            ),
        )
        self.create_btn.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT,
                'create_button',
                None,
            ),
        )

    # retranslateUi
    def update_create_status(self, is_created):
        """This method handles create button status."""
        if is_created:
            self.create_btn.setText('Creating...')
            self.create_btn.setEnabled(not is_created)
        else:
            self.create_btn.setText(
                QCoreApplication.translate(
                    IRIS_WALLET_TRANSLATIONS_CONTEXT,
                    'create_button',
                    None,
                ),
            )
            self.create_btn.setEnabled(not is_created)

    def restore_wallet(self):
        """This method handles update button status."""
        blur_effect = QGraphicsBlurEffect()
        blur_effect.setBlurRadius(10)
        self.setGraphicsEffect(blur_effect)
        dialog = RestoreMnemonicWidget(
            view_model=self._view_model, parent=self,
        )
        dialog.exec()

    def update_loading_state(self, is_loading: bool):
        """
        Updates the loading state of the proceed_wallet_password object.

        This method prints the loading state and starts or stops the loading animation
        of the proceed_wallet_password object based on the value of is_loading.
        """
        if is_loading:
            self.create_btn.setEnabled(False)
            self.restore_btn.start_loading()
        else:
            self.create_btn.setEnabled(True)
            self.restore_btn.stop_loading()

    def handle_message(self, msg_type: ToastPreset, message: str):
        """This method handled to show message."""
        if msg_type == ToastPreset.ERROR:
            ToastManager.error(message)
        else:
            ToastManager.success(message)
