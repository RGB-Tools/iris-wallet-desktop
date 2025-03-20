# pylint: disable=too-many-instance-attributes, too-many-statements, unused-import
"""This module contains the ReceiveAssetWidget class,
 which represents the UI for receive asset.
 """
from __future__ import annotations

from PySide6.QtCore import QCoreApplication
from PySide6.QtCore import QSize
from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor
from PySide6.QtGui import QIcon
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QFrame
from PySide6.QtWidgets import QGridLayout
from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtWidgets import QSpacerItem
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QWidget

import src.resources_rc
from accessible_constant import INVOICE_COPY_BUTTON
from accessible_constant import RECEIVE_ASSET_CLOSE_BUTTON
from accessible_constant import RECEIVER_ADDRESS
from src.utils.common_utils import set_qr_code
from src.utils.constant import IRIS_WALLET_TRANSLATIONS_CONTEXT
from src.utils.helpers import load_stylesheet
from src.viewmodels.main_view_model import MainViewModel
from src.views.components.wallet_logo_frame import WalletLogoFrame


class ReceiveAssetWidget(QWidget):
    """This class represents all the UI elements of the Receive asset page."""

    def __init__(
        self, view_model: MainViewModel,
        page_name: str,
        address_info: str,
    ):
        super().__init__()
        self.setStyleSheet(
            load_stylesheet(
                'views/qss/receive_asset_style.qss',
            ),
        )
        self._view_model: MainViewModel = view_model
        self.address_info = address_info
        self.page_name = page_name
        self.get_receive_address = None
        self.receive_asset_grid_layout = QGridLayout(self)
        self.receive_asset_grid_layout.setObjectName(
            'receive_asset_grid_layout',
        )
        self.wallet_logo_frame = WalletLogoFrame()

        self.receive_asset_grid_layout.addWidget(
            self.wallet_logo_frame, 0, 0, 1, 1,
        )

        self.receive_vertical_spacer = QSpacerItem(
            20, 61, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding,
        )

        self.receive_asset_grid_layout.addItem(
            self.receive_vertical_spacer, 0, 1, 1, 1,
        )

        self.receive_horizontal_spacer = QSpacerItem(
            337, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum,
        )

        self.receive_asset_grid_layout.addItem(
            self.receive_horizontal_spacer, 1, 0, 1, 1,
        )

        self.receive_asset_page = QWidget(self)
        self.receive_asset_page.setObjectName(self.page_name)
        self.receive_asset_page.setMinimumSize(QSize(499, 760))
        self.receive_asset_page.setMaximumSize(QSize(499, 760))

        self.vertical_layout_2 = QVBoxLayout(self.receive_asset_page)
        self.vertical_layout_2.setObjectName('vertical_layout_2')
        self.vertical_layout_2.setContentsMargins(-1, -1, -1, 32)
        self.horizontal_layout_1 = QHBoxLayout()
        self.horizontal_layout_1.setSpacing(6)
        self.horizontal_layout_1.setObjectName('horizontal_layout_1')
        self.horizontal_layout_1.setContentsMargins(35, 5, 40, 0)
        self.asset_title = QLabel(self.receive_asset_page)
        self.asset_title.setObjectName('asset_title')
        self.asset_title.setMinimumSize(QSize(415, 63))

        self.horizontal_layout_1.addWidget(self.asset_title)

        self.receive_asset_close_button = QPushButton(self.receive_asset_page)
        self.receive_asset_close_button.setObjectName('close_btn_3')
        self.receive_asset_close_button.setAccessibleName(
            RECEIVE_ASSET_CLOSE_BUTTON,
        )
        self.receive_asset_close_button.setCursor(
            QCursor(Qt.CursorShape.PointingHandCursor),
        )
        self.receive_asset_close_button.setMinimumSize(QSize(24, 24))
        self.receive_asset_close_button.setMaximumSize(QSize(24, 24))
        self.receive_asset_close_button.setAutoFillBackground(False)

        icon = QIcon()
        icon.addFile(':/assets/x_circle.png', QSize(), QIcon.Normal, QIcon.Off)
        self.receive_asset_close_button.setIcon(icon)
        self.receive_asset_close_button.setIconSize(QSize(24, 24))
        self.receive_asset_close_button.setCheckable(False)
        self.receive_asset_close_button.setChecked(False)

        self.horizontal_layout_1.addWidget(
            self.receive_asset_close_button, 0, Qt.AlignHCenter,
        )

        self.vertical_layout_2.addLayout(self.horizontal_layout_1)

        self.vertical_layout = QVBoxLayout()
        self.vertical_layout.setObjectName('verticalLayout')
        self.btc_balance_layout = QVBoxLayout()
        self.btc_balance_layout.setObjectName('btc_balance_layout')
        self.btc_balance_layout.setContentsMargins(-1, 25, -1, 35)
        self.label = QLabel(self.receive_asset_page)
        self.label.setObjectName('label')
        self.label.setMinimumSize(QSize(335, 335))
        self.label.setStyleSheet('border:none')

        self.btc_balance_layout.addWidget(self.label, 0, Qt.AlignHCenter)

        self.vertical_layout.addLayout(self.btc_balance_layout)

        self.address_label = QLabel(self.receive_asset_page)
        self.address_label.setObjectName('asset_name_label_25')
        self.address_label.setMinimumSize(QSize(335, 0))
        self.address_label.setMaximumSize(QSize(335, 16777215))

        self.vertical_layout.addWidget(
            self.address_label, 0, Qt.AlignHCenter,
        )

        self.receiver_address = QLabel(self.receive_asset_page)
        self.receiver_address.setObjectName('label_2')
        self.receiver_address.setAccessibleDescription(RECEIVER_ADDRESS)
        self.receiver_address.setMinimumSize(QSize(334, 40))
        self.receiver_address.setMaximumSize(QSize(334, 40))

        self.vertical_layout.addWidget(
            self.receiver_address, 0, Qt.AlignHCenter,
        )

        self.wallet_address_description_text = QLabel(
            self.receive_asset_page,
        )
        self.wallet_address_description_text.setWordWrap(True)
        self.wallet_address_description_text.setObjectName(
            'wallet_address_description_text',
        )
        self.wallet_address_description_text.setMinimumSize(QSize(334, 60))
        self.wallet_address_description_text.setMaximumSize(QSize(334, 60))

        self.vertical_layout.addWidget(
            self.wallet_address_description_text, 0, Qt.AlignHCenter,
        )

        self.vertical_layout_2.addLayout(self.vertical_layout)

        self.vertical_spacer_5 = QSpacerItem(
            20, 17, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding,
        )

        self.vertical_layout_2.addItem(self.vertical_spacer_5)

        self.footer_line = QFrame(self.receive_asset_page)
        self.footer_line.setObjectName('line_8')

        self.footer_line.setFrameShape(QFrame.Shape.HLine)
        self.footer_line.setFrameShadow(QFrame.Shadow.Sunken)

        self.vertical_layout_2.addWidget(self.footer_line)

        self.vertical_spacer_3 = QSpacerItem(
            35, 25, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed,
        )

        self.vertical_layout_2.addItem(self.vertical_spacer_3)

        self.copy_button = QPushButton(self.receive_asset_page)
        self.copy_button.setObjectName('copy_button')
        self.copy_button.setAccessibleName(INVOICE_COPY_BUTTON)
        self.copy_button.setMinimumSize(QSize(402, 40))
        self.copy_button.setMaximumSize(QSize(402, 16777215))
        self.copy_button.setCursor(
            QCursor(Qt.CursorShape.PointingHandCursor),
        )
        self.vertical_layout_2.addWidget(
            self.copy_button, 0, Qt.AlignHCenter,
        )

        self.receive_asset_grid_layout.addWidget(
            self.receive_asset_page, 1, 1, 1, 1,
        )

        self.receive_horizontal_spacer_2 = QSpacerItem(
            336, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum,
        )

        self.receive_asset_grid_layout.addItem(
            self.receive_horizontal_spacer_2, 1, 2, 1, 1,
        )

        self.receive_vertical_spacer_2 = QSpacerItem(
            20, 77, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding,
        )

        self.receive_asset_grid_layout.addItem(
            self.receive_vertical_spacer_2, 2, 1, 1, 1,
        )

        self.retranslate_ui()

    def retranslate_ui(self):
        """Retranslate the UI elements."""
        self.asset_title.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'receive', None,
            ),
        )
        self.receive_asset_close_button.setText('')
        self.label.setText('')
        self.address_label.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'address', None,
            ),
        )
        self.wallet_address_description_text.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT,
                self.address_info,
                None,
            ),
        )
        self.copy_button.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'copy_address', None,
            ),
        )

        self.copy_button.clicked.connect(
            lambda: self.copy_button.setText(
                QCoreApplication.translate(
                    IRIS_WALLET_TRANSLATIONS_CONTEXT, 'copied', None,
                ),
            ),
        )

    def update_qr_and_address(self, address: str):
        """This method used to set qr and address"""
        qr_image = set_qr_code(str(address))
        pixmap = QPixmap.fromImage(qr_image)
        self.label.setPixmap(pixmap)
        self.receiver_address.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, str(
                    address,
                ), None,
            ),
        )
