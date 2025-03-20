# pylint: disable=too-many-instance-attributes, too-many-statements, unused-import
"""This module contains the LnEndpointWidget class,
 which represents the UI for lightning node endpoint.
 """
from __future__ import annotations

from PySide6.QtCore import QCoreApplication
from PySide6.QtCore import QSize
from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QFrame
from PySide6.QtWidgets import QGridLayout
from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QLineEdit
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtWidgets import QSpacerItem
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QWidget

import src.resources_rc
from accessible_constant import LN_ENDPOINT_CLOSE_BUTTON
from accessible_constant import LN_NODE_URL
from accessible_constant import PROCEED_BUTTON
from src.data.repository.setting_repository import SettingRepository
from src.utils.common_utils import close_button_navigation
from src.utils.constant import BACKED_URL_LIGHTNING_NETWORK
from src.utils.constant import IRIS_WALLET_TRANSLATIONS_CONTEXT
from src.utils.helpers import load_stylesheet
from src.viewmodels.main_view_model import MainViewModel
from src.views.components.buttons import PrimaryButton
from src.views.components.wallet_logo_frame import WalletLogoFrame


class LnEndpointWidget(QWidget):
    """This class represents all the UI elements of the ln endpoint page."""

    def __init__(self, view_model, originating_page):
        super().__init__()
        self.view_model: MainViewModel = view_model
        self.originating_page = originating_page
        self.setObjectName('LnEndpointWidget')
        self.grid_layout_ln = QGridLayout(self)
        self.grid_layout_ln.setObjectName('grid_layout_ln')
        self.wallet_logo = WalletLogoFrame()
        self.setStyleSheet(load_stylesheet('views/qss/ln_endpoint_style.qss'))
        self.grid_layout_ln.addWidget(self.wallet_logo, 0, 0, 1, 1)

        self.vertical_spacer_1 = QSpacerItem(
            20, 325, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding,
        )

        self.grid_layout_ln.addItem(self.vertical_spacer_1, 0, 2, 1, 1)

        self.lightning_node_widget = QWidget(self)
        self.lightning_node_widget.setObjectName('lightning_node_widget')
        self.lightning_node_widget.setMinimumSize(QSize(499, 300))
        self.lightning_node_widget.setMaximumSize(QSize(466, 608))

        self.grid_layout_1 = QGridLayout(self.lightning_node_widget)
        self.grid_layout_1.setSpacing(6)
        self.grid_layout_1.setObjectName('grid_layout_1')
        self.grid_layout_1.setContentsMargins(1, 4, 1, 30)
        self.lightning_node_page_layout = QVBoxLayout()
        self.lightning_node_page_layout.setSpacing(6)
        self.lightning_node_page_layout.setObjectName(
            'lightning_node_page_layout',
        )
        self.horizontal_layout_ln = QHBoxLayout()
        self.horizontal_layout_ln.setObjectName('horizontal_layout_ln')
        self.horizontal_layout_ln.setContentsMargins(40, 9, 50, 0)
        self.ln_node_connection = QLabel(self.lightning_node_widget)
        self.ln_node_connection.setObjectName('ln_node_connection')
        self.ln_node_connection.setMinimumSize(QSize(385, 63))

        self.horizontal_layout_ln.addWidget(self.ln_node_connection)

        self.close_button = QPushButton(self.lightning_node_widget)
        self.close_button.setObjectName('close_button')
        self.close_button.setAccessibleName(LN_ENDPOINT_CLOSE_BUTTON)
        self.close_button.setCursor(
            QCursor(Qt.CursorShape.PointingHandCursor),
        )
        self.close_button.setMinimumSize(QSize(24, 24))
        self.close_button.setMaximumSize(QSize(50, 65))
        self.close_button.setAutoFillBackground(False)

        ln_endpoint_close_icon = QIcon()
        ln_endpoint_close_icon.addFile(
            ':/assets/x_circle.png', QSize(), QIcon.Normal, QIcon.Off,
        )
        self.close_button.setIcon(ln_endpoint_close_icon)
        self.close_button.setIconSize(QSize(24, 24))
        self.close_button.setCheckable(False)
        self.close_button.setChecked(False)

        self.horizontal_layout_ln.addWidget(self.close_button)

        self.lightning_node_page_layout.addLayout(self.horizontal_layout_ln)

        self.line_top = QFrame(self.lightning_node_widget)
        self.line_top.setObjectName('line_top')
        self.line_top.setFrameShape(QFrame.Shape.HLine)
        self.line_top.setFrameShadow(QFrame.Shadow.Sunken)

        self.lightning_node_page_layout.addWidget(self.line_top)

        self.node_endpoint_label = QLabel(self.lightning_node_widget)
        self.node_endpoint_label.setObjectName('node_endpoint_label')
        self.node_endpoint_label.setMinimumSize(QSize(0, 45))
        self.node_endpoint_label.setBaseSize(QSize(0, 0))
        self.node_endpoint_label.setAutoFillBackground(False)

        self.node_endpoint_label.setFrameShadow(QFrame.Plain)
        self.node_endpoint_label.setLineWidth(1)

        self.lightning_node_page_layout.addWidget(
            self.node_endpoint_label, 0, Qt.AlignTop,
        )

        self.enter_ln_node_url_layout = QHBoxLayout()
        self.enter_ln_node_url_layout.setSpacing(0)
        self.enter_ln_node_url_layout.setObjectName('enter_ln_node_url_layout')
        self.enter_ln_node_url_layout.setContentsMargins(40, -1, 40, -1)
        self.enter_ln_node_url_input = QLineEdit(self.lightning_node_widget)
        self.enter_ln_node_url_input.setObjectName('enter_ln_node_url_input')
        self.enter_ln_node_url_input.setAccessibleName(LN_NODE_URL)
        self.enter_ln_node_url_input.setMinimumSize(QSize(402, 40))
        self.enter_ln_node_url_input.setMaximumSize(QSize(370, 40))

        self.enter_ln_node_url_input.setFrame(False)
        self.enter_ln_node_url_input.setEchoMode(QLineEdit.Normal)
        self.enter_ln_node_url_input.setClearButtonEnabled(False)

        self.enter_ln_node_url_layout.addWidget(self.enter_ln_node_url_input)

        self.lightning_node_page_layout.addLayout(
            self.enter_ln_node_url_layout,
        )

        self.horizontal_layout_1 = QHBoxLayout()
        self.horizontal_layout_1.setSpacing(0)
        self.horizontal_layout_1.setObjectName('horizontal_layout_1')
        self.horizontal_layout_1.setContentsMargins(40, -1, 40, -1)

        self.lightning_node_page_layout.addLayout(self.horizontal_layout_1)

        self.label = QLabel()
        self.label.setObjectName('label')

        self.lightning_node_page_layout.addWidget(self.label)
        self.label.setContentsMargins(50, 5, 40, 5)

        self.vertical_spacer_2 = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding,
        )

        self.lightning_node_page_layout.addItem(self.vertical_spacer_2)

        self.line_bottom = QFrame(self.lightning_node_widget)
        self.line_bottom.setObjectName('line_bottom')

        self.line_bottom.setFrameShape(QFrame.Shape.HLine)
        self.line_bottom.setFrameShadow(QFrame.Shadow.Sunken)

        self.lightning_node_page_layout.addWidget(self.line_bottom)

        self.horizontal_layout_2 = QHBoxLayout()
        self.horizontal_layout_2.setObjectName('horizontal_layout_2')
        self.horizontal_layout_2.setContentsMargins(-1, 22, -1, -1)
        self.horizontal_spacer_1 = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum,
        )

        self.horizontal_layout_2.addItem(self.horizontal_spacer_1)

        self.proceed_button = PrimaryButton()
        self.proceed_button.setAccessibleName(PROCEED_BUTTON)
        size_policy_proceed_button = QSizePolicy(
            QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed,
        )
        size_policy_proceed_button.setHorizontalStretch(1)
        size_policy_proceed_button.setVerticalStretch(0)
        size_policy_proceed_button.setHeightForWidth(
            self.proceed_button.sizePolicy().hasHeightForWidth(),
        )
        self.proceed_button.setSizePolicy(size_policy_proceed_button)
        self.proceed_button.setMinimumSize(QSize(402, 40))
        self.proceed_button.setMaximumSize(QSize(402, 40))

        self.horizontal_layout_2.addWidget(self.proceed_button)

        self.horizontal_spacer_2 = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum,
        )

        self.horizontal_layout_2.addItem(self.horizontal_spacer_2)

        self.lightning_node_page_layout.addLayout(self.horizontal_layout_2)

        self.grid_layout_1.addLayout(
            self.lightning_node_page_layout, 0, 0, 1, 1,
        )
        self.grid_layout_ln.addWidget(self.lightning_node_widget, 1, 1, 2, 2)

        self.horizontal_spacer_3 = QSpacerItem(
            274, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum,
        )

        self.grid_layout_ln.addItem(self.horizontal_spacer_3, 1, 3, 1, 1)

        self.horizontal_spacer_4 = QSpacerItem(
            274, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum,
        )

        self.grid_layout_ln.addItem(self.horizontal_spacer_4, 2, 0, 1, 1)

        self.vertical_spacer_3 = QSpacerItem(
            20, 324, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding,
        )

        self.grid_layout_ln.addItem(self.vertical_spacer_3, 3, 1, 1, 1)

        self.setup_ui_connection()
        self.retranslate_ui()
        self.set_ln_placeholder_text()

    def setup_ui_connection(self):
        """Set up connections for UI elements."""
        self.close_button.clicked.connect(
            lambda: close_button_navigation(
                self, self.view_model.page_navigation.term_and_condition_page,
            ),
        )
        self.proceed_button.clicked.connect(self.set_ln_url)
        self.view_model.ln_endpoint_view_model.loading_message.connect(
            self.start_loading_connect,
        )
        self.view_model.ln_endpoint_view_model.stop_loading_message.connect(
            self.stop_loading_connect,
        )

    def retranslate_ui(self):
        """Retranslate the UI elements."""
        self.ln_node_connection.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'lightning_node_connection', None,
            ),
        )
        self.node_endpoint_label.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'rgb_lightning_node_url', None,
            ),
        )
        self.enter_ln_node_url_input.setPlaceholderText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'enter_lightning_node_url', None,
            ),
        )
        self.proceed_button.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'proceed', None,
            ),
        )

    def set_ln_url(self):
        """Set the lightning node url"""
        node_url = self.enter_ln_node_url_input.text()
        self.view_model.ln_endpoint_view_model.set_ln_endpoint(
            node_url, self.set_validation,
        )

    def set_validation(self):
        """Set the validation for lightning node URL"""
        self.label.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'invalid_url', None,
            ),
        )

    def start_loading_connect(self):
        """
        Updates the start loading state of the proceed_wallet_password object.
        """
        self.proceed_button.start_loading()

    def stop_loading_connect(self):
        """
        Updates the stop loading state of the proceed_wallet_password object.
        """
        self.proceed_button.stop_loading()

    def set_ln_placeholder_text(self):
        """This method set the ln endpoint in placeholder"""
        if self.originating_page == 'settings_page':
            ln_url = SettingRepository.get_ln_endpoint()
            self.enter_ln_node_url_input.setText(ln_url)
        else:
            self.enter_ln_node_url_input.setText(BACKED_URL_LIGHTNING_NETWORK)
