# pylint: disable=too-many-instance-attributes, too-many-statements, unused-import, disable=too-few-public-methods
"""This module contains the CreateChannelWidget class,
which represents the UI for open channel page.
"""
from __future__ import annotations

from PySide6.QtCore import QCoreApplication
from PySide6.QtCore import QSize
from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor
from PySide6.QtGui import QIcon
from PySide6.QtGui import QPixmap
from PySide6.QtGui import QTextOption
from PySide6.QtWidgets import QFrame
from PySide6.QtWidgets import QGridLayout
from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QPlainTextEdit
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtWidgets import QSpacerItem
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QWidget

import src.resources_rc
from accessible_constant import SUCCESS_PAGE_CLOSE_BUTTON
from accessible_constant import SUCCESS_PAGE_HOME_BUTTON
from src.model.success_model import SuccessPageModel
from src.utils.constant import IRIS_WALLET_TRANSLATIONS_CONTEXT
from src.utils.helpers import load_stylesheet
from src.views.components.buttons import PrimaryButton
from src.views.components.wallet_logo_frame import WalletLogoFrame


class SuccessWidget(QWidget):
    """This class represents all the UI elements of the create channel page."""

    def __init__(self, params: SuccessPageModel):
        super().__init__()
        self._params = params
        self.setStyleSheet(load_stylesheet('views/qss/success_style.qss'))
        self.grid_layout = QGridLayout(self)
        self.grid_layout.setObjectName('gridLayout')
        self.wallet_logo = WalletLogoFrame()
        self.grid_layout.addWidget(self.wallet_logo, 0, 0, 1, 1)

        self.vertical_spacer_success_top = QSpacerItem(
            20,
            78,
            QSizePolicy.Policy.Minimum,
            QSizePolicy.Policy.Expanding,
        )

        self.grid_layout.addItem(self.vertical_spacer_success_top, 0, 1, 1, 1)

        self.horizontal_spacer_success_left = QSpacerItem(
            337,
            20,
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Minimum,
        )

        self.grid_layout.addItem(
            self.horizontal_spacer_success_left, 1, 0, 1, 1,
        )

        self.issue_new_ticker = QWidget()
        self.issue_new_ticker.setObjectName('issue_new_ticker')
        self.issue_new_ticker.setMinimumSize(QSize(499, 644))
        self.issue_new_ticker.setMaximumSize(QSize(499, 644))

        self.vertical_layout = QVBoxLayout(self.issue_new_ticker)
        self.vertical_layout.setObjectName('verticalLayout_2')
        self.vertical_layout.setContentsMargins(1, -1, 1, 9)
        self.header_horizontal_layout = QHBoxLayout()
        self.header_horizontal_layout.setSpacing(6)
        self.header_horizontal_layout.setObjectName('header_horizontal_layout')
        self.header_horizontal_layout.setContentsMargins(35, 5, 40, 0)
        self.success_page_header = QLabel(self.issue_new_ticker)
        self.success_page_header.setObjectName('issue_ticker_title')
        self.success_page_header.setMinimumSize(QSize(415, 63))

        self.header_horizontal_layout.addWidget(self.success_page_header)

        self.close_button = QPushButton(self.issue_new_ticker)
        self.close_button.setObjectName('close_button')
        self.close_button.setAccessibleName(SUCCESS_PAGE_CLOSE_BUTTON)
        self.close_button.setMinimumSize(QSize(24, 24))
        self.close_button.setMaximumSize(QSize(24, 24))
        self.close_button.setAutoFillBackground(False)
        self.close_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        icon = QIcon()
        icon.addFile(':/assets/x_circle.png', QSize(), QIcon.Normal, QIcon.Off)
        self.close_button.setIcon(icon)
        self.close_button.setIconSize(QSize(24, 24))
        self.close_button.setCheckable(False)
        self.close_button.setChecked(False)

        self.header_horizontal_layout.addWidget(
            self.close_button, 0, Qt.AlignHCenter,
        )

        self.vertical_layout.addLayout(self.header_horizontal_layout)

        self.top_line = QFrame(self.issue_new_ticker)
        self.top_line.setObjectName('top_line')

        self.top_line.setFrameShape(QFrame.Shape.HLine)
        self.top_line.setFrameShadow(QFrame.Shadow.Sunken)

        self.vertical_layout.addWidget(self.top_line)

        self.vertical_spacer_2 = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding,
        )

        self.vertical_layout.addItem(self.vertical_spacer_2)

        self.success_logo = QLabel(self.issue_new_ticker)
        self.success_logo.setObjectName('success_logo')

        self.success_logo.setPixmap(QPixmap(':/assets/tick_circle.png'))
        self.success_logo.setAlignment(Qt.AlignBottom | Qt.AlignHCenter)

        self.vertical_layout.addWidget(self.success_logo)

        self.bold_title = QLabel(self.issue_new_ticker)
        self.bold_title.setObjectName('bold_title')

        self.bold_title.setAlignment(Qt.AlignCenter)

        self.vertical_layout.addWidget(self.bold_title)

        self.desc_msg = QPlainTextEdit(self.issue_new_ticker)
        self.desc_msg.setObjectName('desc_msg')
        self.desc_msg.setReadOnly(True)

        text_option = QTextOption()
        text_option.setAlignment(Qt.AlignCenter)
        self.desc_msg.document().setDefaultTextOption(text_option)

        self.vertical_layout.addWidget(self.desc_msg)

        self.vertical_spacer = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding,
        )

        self.vertical_layout.addItem(self.vertical_spacer)

        self.bottom_line = QFrame(self.issue_new_ticker)
        self.bottom_line.setObjectName('bottom_line')

        self.bottom_line.setFrameShape(QFrame.Shape.HLine)
        self.bottom_line.setFrameShadow(QFrame.Shadow.Sunken)

        self.vertical_layout.addWidget(self.bottom_line)

        self.button_horizontal_layout = QHBoxLayout()
        self.button_horizontal_layout.setObjectName('horizontalLayout_5')
        self.button_horizontal_layout.setContentsMargins(-1, 24, -1, 24)
        self.home_button = PrimaryButton()
        self.home_button.setAccessibleName(SUCCESS_PAGE_HOME_BUTTON)
        self.home_button.setMinimumSize(QSize(402, 40))
        self.home_button.setMaximumSize(QSize(201, 16777215))
        self.home_button.setAutoRepeat(False)
        self.home_button.setAutoExclusive(False)
        self.home_button.setFlat(False)

        self.button_horizontal_layout.addWidget(
            self.home_button, 0, Qt.AlignHCenter | Qt.AlignVCenter,
        )

        self.vertical_layout.addLayout(self.button_horizontal_layout)

        self.grid_layout.addWidget(self.issue_new_ticker, 1, 1, 1, 1)
        self.success_horizontal_spacer_right = QSpacerItem(
            336, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum,
        )

        self.grid_layout.addItem(
            self.success_horizontal_spacer_right, 1, 2, 1, 1,
        )

        self.main_vertical_spacer_bottom = QSpacerItem(
            20,
            77,
            QSizePolicy.Policy.Minimum,
            QSizePolicy.Policy.Expanding,
        )

        self.grid_layout.addItem(self.main_vertical_spacer_bottom, 2, 1, 1, 1)

        self.retranslate_ui()

    def retranslate_ui(self):
        """This method retranslate the ui initially"""
        self.home_button.clicked.connect(self._params.callback)
        self.close_button.clicked.connect(self._params.callback)
        self.success_page_header.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, self._params.header, None,
            ),
        )

        self.bold_title.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, self._params.title, None,
            ),
        )
        self.desc_msg.setPlainText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, self._params.description, None,
            ),
        )
        self.home_button.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, self._params.button_text, None,
            ),
        )
