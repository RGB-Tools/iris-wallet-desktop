# pylint: disable=too-many-instance-attributes, too-many-statements, unused-import
"""This module contains the ChannelDetailDialogBox which contains UI for
channel detail dialog box
"""
from __future__ import annotations

from PySide6.QtCore import QCoreApplication
from PySide6.QtCore import QSize
from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QDialog
from PySide6.QtWidgets import QFrame
from PySide6.QtWidgets import QGraphicsBlurEffect
from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtWidgets import QSpacerItem
from PySide6.QtWidgets import QVBoxLayout

import src.resources_rc
from accessible_constant import BTC_LOCAL_VALUE_LABEL
from accessible_constant import BTC_REMOTE_VALUE_LABEL
from accessible_constant import CHANNEL_DETAIL_CLOSE_BUTTON
from accessible_constant import CHANNEL_DETAIL_DIALOG
from accessible_constant import CHANNEL_PEER_PUBKEY_COPY_BUTTON
from accessible_constant import CLOSE_CHANNEL_BUTTON
from src.utils.common_utils import copy_text
from src.utils.constant import IRIS_WALLET_TRANSLATIONS_CONTEXT
from src.utils.helpers import load_stylesheet
from src.viewmodels.main_view_model import MainViewModel
from src.views.ui_close_channel_dialog import CloseChannelDialog


class ChannelDetailDialogBox(QDialog):
    """This class represents all the UI element of channel detail dialog box"""

    def __init__(self, page_navigate, param, parent=None):
        super().__init__(parent)
        self.setObjectName('Dialog')
        self.setAccessibleName(CHANNEL_DETAIL_DIALOG)
        self.setStyleSheet(
            load_stylesheet(
                'views/qss/channel_detail.qss',
            ),
        )
        self.parent_widget = parent
        self._param = param
        self.pub_key = self._param.pub_key
        self.bitcoin_local_balance = self._param.bitcoin_local_balance
        self.bitcoin_remote_balance = self._param.bitcoin_remote_balance
        self._page_navigate = page_navigate
        self._view_model = MainViewModel(page_navigate)
        self.channel_id = self._param.channel_id

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.channel_detail_frame = QFrame(self)
        self.channel_detail_frame.setObjectName('channel_detail_frame')
        self.channel_detail_frame.setMinimumWidth(850)

        self.vertical_layout_3 = QVBoxLayout(self.channel_detail_frame)
        self.vertical_layout_3.setObjectName('vertical_layout_3')
        self.vertical_layout_3.setContentsMargins(0, 0, 0, 5)
        self.horizontal_layout_2 = QHBoxLayout()
        self.horizontal_layout_2.setObjectName('horizontal_layout_2')
        self.channel_detail_title_label = QLabel(self.channel_detail_frame)
        self.channel_detail_title_label.setObjectName(
            'channel_detail_title_label',
        )
        self.channel_detail_title_label.setMinimumSize(QSize(0, 0))
        self.horizontal_layout_2.addWidget(self.channel_detail_title_label)

        self.horizontal_spacer = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum,
        )

        self.horizontal_layout_2.addItem(self.horizontal_spacer)

        self.close_button = QPushButton(self.channel_detail_frame)
        self.close_button.setObjectName('close_button')
        self.close_button.setAccessibleName(CHANNEL_DETAIL_CLOSE_BUTTON)
        self.close_button.setMinimumSize(QSize(0, 24))
        self.close_button.setMaximumSize(QSize(16777215, 16777215))
        self.close_button.setLayoutDirection(Qt.LayoutDirection.LeftToRight)

        icon = QIcon()
        icon.addFile(
            ':/assets/x_circle.png', QSize(),
            QIcon.Mode.Normal, QIcon.State.Off,
        )
        self.close_button.setIcon(icon)
        self.close_button.setIconSize(QSize(24, 24))
        self.close_button.setCursor(
            QCursor(Qt.CursorShape.PointingHandCursor),
        )

        self.horizontal_layout_2.addWidget(self.close_button)

        self.vertical_layout_3.addLayout(self.horizontal_layout_2)

        self.header_line = QFrame(self.channel_detail_frame)
        self.header_line.setObjectName('header_line')
        self.header_line.setFrameShape(QFrame.Shape.VLine)
        self.header_line.setFrameShadow(QFrame.Shadow.Sunken)
        self.header_line.setMaximumSize(QSize(16777215, 16777215))

        self.vertical_layout_3.addWidget(self.header_line)

        self.vertical_spacer_5 = QSpacerItem(
            20, 15, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred,
        )

        self.vertical_layout_3.addItem(self.vertical_spacer_5)

        self.btc_balance_frame = QFrame(self.channel_detail_frame)
        self.btc_balance_frame.setObjectName('btc_balance_frame')
        self.btc_balance_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.btc_balance_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontal_layout = QHBoxLayout(self.btc_balance_frame)
        self.horizontal_layout.setObjectName('horizontal_layout')
        self.vertical_layout = QVBoxLayout()
        self.vertical_layout.setObjectName('vertical_layout')

        self.btc_local_balance_label = QLabel(self.btc_balance_frame)
        self.btc_local_balance_label.setObjectName('btc_local_balance_label')

        self.btc_local_balance_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.vertical_layout.addWidget(self.btc_local_balance_label)

        self.btc_local_balance_value_label = QLabel(self.btc_balance_frame)
        self.btc_local_balance_value_label.setObjectName(
            'btc_local_balance_value_label',
        )
        self.btc_local_balance_value_label.setAccessibleDescription(
            BTC_LOCAL_VALUE_LABEL,
        )
        size_policy = QSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred,
        )
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(
            self.btc_local_balance_value_label.sizePolicy().hasHeightForWidth(),
        )
        self.btc_local_balance_value_label.setSizePolicy(size_policy)
        self.btc_local_balance_value_label.setMinimumSize(QSize(0, 0))
        self.btc_local_balance_value_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter,
        )
        self.btc_local_balance_value_label.setText(
            str(int(self.bitcoin_local_balance/1000)),
        )

        self.vertical_layout.addWidget(self.btc_local_balance_value_label)

        self.horizontal_layout.addLayout(self.vertical_layout)

        self.balance_separator_line = QFrame(self.btc_balance_frame)
        self.balance_separator_line.setObjectName('line')
        self.balance_separator_line.setFrameShape(QFrame.Shape.VLine)
        self.balance_separator_line.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontal_layout.addWidget(self.balance_separator_line)

        self.vertical_layout_2 = QVBoxLayout()
        self.vertical_layout_2.setObjectName('vertical_layout_2')
        self.btc_remote_balance_label = QLabel(self.btc_balance_frame)
        self.btc_remote_balance_label.setObjectName('btc_remote_balance_label')

        self.btc_remote_balance_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter,
        )

        self.vertical_layout_2.addWidget(self.btc_remote_balance_label)

        self.btc_remote_balance_value_label = QLabel(self.btc_balance_frame)
        self.btc_remote_balance_value_label.setObjectName(
            'btc_remote_balance_value_label',
        )
        self.btc_remote_balance_value_label.setAccessibleDescription(
            BTC_REMOTE_VALUE_LABEL,
        )
        self.btc_remote_balance_value_label.setMinimumSize(QSize(0, 0))

        self.btc_remote_balance_value_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter,
        )
        self.btc_remote_balance_value_label.setText(
            str(int(self.bitcoin_remote_balance/1000)),
        )

        self.vertical_layout_2.addWidget(self.btc_remote_balance_value_label)

        self.horizontal_layout.addLayout(self.vertical_layout_2)

        self.vertical_layout_3.addWidget(
            self.btc_balance_frame, alignment=Qt.AlignCenter,
        )
        self.vertical_spacer_2 = QSpacerItem(
            20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred,
        )

        self.vertical_layout_3.addItem(self.vertical_spacer_2)

        self.horizontal_layout_3 = QHBoxLayout()
        self.horizontal_layout_3.setContentsMargins(40, 0, 0, 0)
        self.horizontal_layout_3.setObjectName('horizontal_layout_3')
        self.pub_key_label = QLabel(self.channel_detail_frame)
        self.pub_key_label.setObjectName('pub_key_label')

        self.horizontal_layout_3.addWidget(
            self.pub_key_label, alignment=Qt.AlignRight,
        )

        self.pub_key_value_label = QLabel(self.channel_detail_frame)
        self.pub_key_value_label.setObjectName('pub_key_value_label')
        self.pub_key_value_label.setMinimumWidth(575)
        self.pub_key_value_label.setMaximumSize(QSize(16777215, 16777215))
        self.pub_key_value_label.setText(str(self.pub_key))

        self.horizontal_layout_3.addWidget(
            self.pub_key_value_label, alignment=Qt.AlignRight,
        )

        self.copy_button = QPushButton(self.channel_detail_frame)
        self.copy_button.setObjectName('copy_button')
        self.copy_button.setAccessibleName(CHANNEL_PEER_PUBKEY_COPY_BUTTON)
        self.copy_button.setMaximumSize(QSize(24, 24))
        self.copy_button.setCursor(
            QCursor(Qt.CursorShape.PointingHandCursor),
        )

        icon1 = QIcon()
        icon1.addFile(
            ':/assets/copy.png', QSize(),
            QIcon.Mode.Normal, QIcon.State.Off,
        )
        self.copy_button.setIcon(icon1)
        self.copy_button.setIconSize(QSize(24, 24))

        self.horizontal_layout_3.addWidget(
            self.copy_button, alignment=Qt.AlignRight,
        )

        self.horizontal_spacer_2 = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum,
        )

        self.horizontal_layout_3.addItem(self.horizontal_spacer_2)

        self.vertical_layout_3.addLayout(self.horizontal_layout_3)

        self.vertical_spacer = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred,
        )

        self.vertical_layout_3.addItem(self.vertical_spacer)

        self.footer_line = QFrame(self.channel_detail_frame)
        self.footer_line.setObjectName('footer_line')
        self.footer_line.setFrameShape(QFrame.Shape.VLine)
        self.footer_line.setFrameShadow(QFrame.Shadow.Sunken)
        self.footer_line.setMaximumSize(QSize(16777215, 16777215))
        self.vertical_layout_3.addWidget(self.footer_line)

        self.vertical_spacer_4 = QSpacerItem(
            20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred,
        )

        self.vertical_layout_3.addItem(self.vertical_spacer_4)

        self.close_channel_button = QPushButton(self.channel_detail_frame)
        self.close_channel_button.setObjectName('close_channel_button')
        self.close_channel_button.setAccessibleName(CLOSE_CHANNEL_BUTTON)
        size_policy_1 = QSizePolicy(
            QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed,
        )
        size_policy_1.setHorizontalStretch(0)
        size_policy_1.setVerticalStretch(0)
        size_policy_1.setHeightForWidth(
            self.close_channel_button.sizePolicy().hasHeightForWidth(),
        )
        self.close_channel_button.setSizePolicy(size_policy_1)
        self.close_channel_button.setMinimumSize(QSize(150, 40))
        self.close_channel_button.setMaximumSize(QSize(150, 16777215))

        self.close_channel_button.setFlat(False)
        self.close_channel_button.setCursor(
            QCursor(Qt.CursorShape.PointingHandCursor),
        )

        self.vertical_layout_3.addWidget(
            self.close_channel_button, alignment=Qt.AlignCenter,
        )
        self.vertical_spacer_4 = QSpacerItem(
            20, 13, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding,
        )

        self.vertical_layout_3.addItem(self.vertical_spacer_4)
        self.channel_detail_frame.adjustSize()
        self.btc_balance_frame.setMinimumSize(
            QSize(self.channel_detail_frame.size().width()-85, 70),
        )
        self.header_line.setMinimumSize(
            QSize(self.channel_detail_frame.size().width()-2, 1),
        )
        self.footer_line.setMinimumSize(
            QSize(self.channel_detail_frame.size().width()-2, 1),
        )
        self.retranslate_ui()
        self.setup_ui_connections()

    def retranslate_ui(self):
        """Retranslate the UI elements."""
        self.channel_detail_title_label.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'channel_details', None,
            ),
        )
        self.btc_local_balance_label.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'bitcoin_local_balance', None,
            ),
        )
        self.btc_remote_balance_label.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'bitcoin_remote_balance', None,
            ),
        )
        self.pub_key_label.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'peer_pubkey', None,
            ),
        )
        self.close_channel_button.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'close_channel', None,
            ),
        )

    def setup_ui_connections(self):
        """Ui connections for channel detail dialog"""
        self.close_button.clicked.connect(
            self.close,
        )
        self.copy_button.clicked.connect(
            lambda: copy_text(self.pub_key_value_label),
        )
        self.close_channel_button.clicked.connect(
            self.close_channel,
        )

    def close_channel(self):
        """This function would close the channel detail dialog and show the close channel prompt"""
        self.close()
        close_channel_dialog = CloseChannelDialog(
            page_navigate=self._view_model.page_navigation,
            pub_key=self.pub_key,
            channel_id=self.channel_id,
            parent=self.parent_widget,
        )
        blur_effect = QGraphicsBlurEffect()
        blur_effect.setBlurRadius(10)
        self.setGraphicsEffect(blur_effect)
        close_channel_dialog.exec()
