# pylint: disable=too-many-instance-attributes, too-many-statements, unused-import
"""This module contains the BitcoinTransactionDetail class,
 which represents the UI for list of the bitcoin transactions.
 """
from __future__ import annotations

from PySide6.QtCore import QCoreApplication
from PySide6.QtCore import QSize
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
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
from accessible_constant import BITCOIN_AMOUNT_VALUE
from accessible_constant import BITCOIN_TX_ID
from accessible_constant import BITCOIN_TX_PAGE_CLOSE_BUTTON
from src.data.repository.setting_repository import SettingRepository
from src.model.enums.enums_model import NetworkEnumModel
from src.model.enums.enums_model import TransferStatusEnumModel
from src.model.transaction_detail_page_model import TransactionDetailPageModel
from src.utils.common_utils import get_bitcoin_explorer_url
from src.utils.common_utils import insert_zero_width_spaces
from src.utils.common_utils import network_info
from src.utils.constant import IRIS_WALLET_TRANSLATIONS_CONTEXT
from src.utils.helpers import load_stylesheet
from src.viewmodels.main_view_model import MainViewModel
from src.views.components.wallet_logo_frame import WalletLogoFrame


class BitcoinTransactionDetail(QWidget):
    """This class represents all the UI elements of the bitcoin transaction detail page."""

    def __init__(self, view_model, _params: TransactionDetailPageModel):
        super().__init__()
        self._view_model: MainViewModel = view_model
        self.network: str = ''
        self.params: TransactionDetailPageModel = _params
        self.tx_id: str = insert_zero_width_spaces(self.params.tx_id)
        self.setStyleSheet(
            load_stylesheet(
                'views/qss/bitcoin_transaction_style.qss',
            ),
        )
        self.grid_layout = QGridLayout(self)
        self.grid_layout.setObjectName('BitcoinTransactionDetail')
        self.vertical_spacer = QSpacerItem(
            20, 295, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding,
        )

        self.grid_layout.addItem(self.vertical_spacer, 0, 2, 1, 1)

        self.bitcoin_single_transaction_detail_widget = QWidget(self)
        self.bitcoin_single_transaction_detail_widget.setObjectName(
            'bitcoin_single_transaction_detail_widget',
        )
        self.bitcoin_single_transaction_detail_widget.setMinimumSize(
            QSize(515, 450),
        )
        self.bitcoin_single_transaction_detail_widget.setMaximumSize(
            QSize(515, 450),
        )
        self.bitcoin_grid_layout = QGridLayout(
            self.bitcoin_single_transaction_detail_widget,
        )
        self.bitcoin_grid_layout.setObjectName('bitcoin_grid_ayout')
        self.bitcoin_grid_layout.setContentsMargins(-1, -1, -1, 15)
        self.line_detail_tx = QFrame(
            self.bitcoin_single_transaction_detail_widget,
        )
        self.line_detail_tx.setObjectName('line_detail_tx')

        self.line_detail_tx.setFrameShape(QFrame.Shape.HLine)
        self.line_detail_tx.setFrameShadow(QFrame.Shadow.Sunken)

        self.bitcoin_grid_layout.addWidget(self.line_detail_tx, 1, 0, 1, 1)

        self.bitcoin_transaction_layout = QVBoxLayout()
        self.bitcoin_transaction_layout.setSpacing(0)
        self.bitcoin_transaction_layout.setObjectName('transaction_layout')
        self.bitcoin_transaction_layout.setContentsMargins(0, 7, 0, 50)
        self.transaction_detail_frame = QFrame(
            self.bitcoin_single_transaction_detail_widget,
        )
        self.transaction_detail_frame.setObjectName('transaction_detail_frame')
        self.transaction_detail_frame.setMinimumSize(QSize(340, 190))
        self.transaction_detail_frame.setMaximumSize(QSize(345, 190))

        self.transaction_detail_frame.setFrameShape(QFrame.StyledPanel)
        self.transaction_detail_frame.setFrameShadow(QFrame.Raised)
        self.vertical_layout_tx_frame = QVBoxLayout(
            self.transaction_detail_frame,
        )
        self.vertical_layout_tx_frame.setSpacing(0)
        self.vertical_layout_tx_frame.setObjectName('verticalLayout')
        self.vertical_layout_tx_frame.setContentsMargins(15, -1, -1, -1)
        self.tx_id_label = QLabel(self.transaction_detail_frame)
        self.tx_id_label.setObjectName('tx_id_label')
        self.tx_id_label.setMinimumSize(QSize(295, 20))
        self.tx_id_label.setMaximumSize(QSize(295, 20))

        self.vertical_layout_tx_frame.addWidget(self.tx_id_label)

        self.bitcoin_tx_id_value = QLabel(self.transaction_detail_frame)
        self.bitcoin_tx_id_value.setWordWrap(True)
        self.bitcoin_tx_id_value.setObjectName('tx_id_value')
        self.bitcoin_tx_id_value.setAccessibleDescription(BITCOIN_TX_ID)
        self.bitcoin_tx_id_value.setTextInteractionFlags(
            Qt.TextBrowserInteraction,
        )
        self.bitcoin_tx_id_value.setOpenExternalLinks(True)
        self.bitcoin_tx_id_value.setMinimumSize(QSize(295, 60))
        self.bitcoin_tx_id_value.setMaximumSize(QSize(305, 60))

        self.bitcoin_tx_id_value.setInputMethodHints(Qt.ImhMultiLine)

        self.vertical_layout_tx_frame.addWidget(self.bitcoin_tx_id_value)

        self.date_label = QLabel(self.transaction_detail_frame)
        self.date_label.setObjectName('date_label')
        self.date_label.setMinimumSize(QSize(295, 20))
        self.date_label.setMaximumSize(QSize(295, 20))

        self.vertical_layout_tx_frame.addWidget(self.date_label)

        self.date_value = QLabel(self.transaction_detail_frame)
        self.date_value.setObjectName('date_value')
        self.date_value.setMinimumSize(QSize(295, 25))
        self.date_value.setMaximumSize(QSize(295, 25))

        self.vertical_layout_tx_frame.addWidget(self.date_value)

        self.bitcoin_transaction_layout.addWidget(
            self.transaction_detail_frame, 0, Qt.AlignHCenter,
        )

        self.bitcoin_grid_layout.addLayout(
            self.bitcoin_transaction_layout, 3, 0, 1, 1,
        )

        self.header_layout = QHBoxLayout()
        self.header_layout.setObjectName('header_layout')
        self.header_layout.setContentsMargins(35, 9, 40, 0)
        self.bitcoin_title_value = QLabel(
            self.bitcoin_single_transaction_detail_widget,
        )
        self.bitcoin_title_value.setObjectName('bitcoin_title_value')
        self.bitcoin_title_value.setMinimumSize(QSize(415, 52))
        self.bitcoin_title_value.setMaximumSize(QSize(16777215, 52))

        self.header_layout.addWidget(self.bitcoin_title_value)

        self.close_btn_bitcoin_tx_page = QPushButton(
            self.bitcoin_single_transaction_detail_widget,
        )
        self.close_btn_bitcoin_tx_page.setObjectName('close_btn')
        self.close_btn_bitcoin_tx_page.setAccessibleName(
            BITCOIN_TX_PAGE_CLOSE_BUTTON,
        )
        self.close_btn_bitcoin_tx_page.setMinimumSize(QSize(24, 24))
        self.close_btn_bitcoin_tx_page.setMaximumSize(QSize(50, 65))
        self.close_btn_bitcoin_tx_page.setAutoFillBackground(False)

        icon = QIcon()
        icon.addFile(':/assets/x_circle.png', QSize(), QIcon.Normal, QIcon.Off)
        self.close_btn_bitcoin_tx_page.setIcon(icon)
        self.close_btn_bitcoin_tx_page.setIconSize(QSize(24, 24))
        self.close_btn_bitcoin_tx_page.setCheckable(False)
        self.close_btn_bitcoin_tx_page.setChecked(False)

        self.header_layout.addWidget(self.close_btn_bitcoin_tx_page)

        self.bitcoin_grid_layout.addLayout(self.header_layout, 0, 0, 1, 1)

        self.amount_layout = QVBoxLayout()
        self.amount_layout.setObjectName('amount_layout')
        self.amount_layout.setContentsMargins(-1, 17, -1, -1)
        self.btc_amount_label = QLabel(
            self.bitcoin_single_transaction_detail_widget,
        )
        self.btc_amount_label.setObjectName('amount_label')

        self.amount_layout.addWidget(self.btc_amount_label, 0, Qt.AlignHCenter)

        self.bitcoin_amount_value = QLabel(
            self.bitcoin_single_transaction_detail_widget,
        )
        self.bitcoin_amount_value.setObjectName('amount_value')
        self.bitcoin_amount_value.setAccessibleDescription(
            BITCOIN_AMOUNT_VALUE,
        )
        self.bitcoin_amount_value.setMinimumSize(QSize(0, 60))

        self.amount_layout.addWidget(
            self.bitcoin_amount_value, 0, Qt.AlignHCenter,
        )

        self.bitcoin_grid_layout.addLayout(self.amount_layout, 2, 0, 1, 1)

        self.grid_layout.addWidget(
            self.bitcoin_single_transaction_detail_widget, 1, 1, 2, 2,
        )

        self.horizontal_spacer_btc = QSpacerItem(
            362, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum,
        )

        self.grid_layout.addItem(self.horizontal_spacer_btc, 2, 0, 1, 1)

        self.horizontal_spacer_btc_2 = QSpacerItem(
            361, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum,
        )

        self.grid_layout.addItem(self.horizontal_spacer_btc_2, 2, 3, 1, 1)

        self.vertical_spacer_2 = QSpacerItem(
            20, 294, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding,
        )

        self.grid_layout.addItem(self.vertical_spacer_2, 3, 1, 1, 1)

        self.wallet_logo_frame = WalletLogoFrame(self)
        self.grid_layout.addWidget(self.wallet_logo_frame, 0, 0, 1, 1)

        network_info(self)
        self.retranslate_ui()
        self.set_btc_tx_value()
        self.setup_ui_connection()

    def setup_ui_connection(self):
        """Set up connections for UI elements."""
        self.close_btn_bitcoin_tx_page.clicked.connect(self.handle_close)

    def retranslate_ui(self):
        """Set up connections for UI elements."""
        self.url = get_bitcoin_explorer_url(self.params.tx_id)
        self.bitcoin_text = f'{
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, "bitcoin", None
            )
        } ({self.network})'
        self.tx_id_label.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'transaction_id', None,
            ),
        )
        if SettingRepository.get_wallet_network() != NetworkEnumModel.REGTEST:
            self.bitcoin_tx_id_value.setText(
                f"<a style='color: #03CA9B;' href='{self.url}'>"
                f"{self.tx_id}</a>",
            )
        else:
            self.bitcoin_tx_id_value.setText(self.tx_id)
        self.btc_amount_label.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'amount', None,
            ),
        )
        self.date_label.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'date', None,
            ),
        )
        self.bitcoin_title_value.setText(self.bitcoin_text)

    def set_btc_tx_value(self):
        """
        Set the values of various UI components based on the provided bitcoin transaction details.

        """
        if self.params.transfer_status in (TransferStatusEnumModel.SENT, TransferStatusEnumModel.INTERNAL):
            self.bitcoin_amount_value.setStyleSheet(
                load_stylesheet('views/qss/q_label.qss'),
            )

        if self.params.transfer_status == TransferStatusEnumModel.ON_GOING_TRANSFER:
            self.bitcoin_amount_value.setStyleSheet(
                """QLabel#amount_value{
                font: 24px "Inter";
                color: #959BAE;
                background: transparent;
                border: none;
                font-weight: 600;
                }""",
            )

        self.bitcoin_amount_value.setText(self.params.amount)

        if self.params.confirmation_date and self.params.confirmation_time:
            date_time_concat = f'{self.params.confirmation_date} | {
                self.params.confirmation_time
            }'
            self.date_value.setText(date_time_concat)
        else:
            self.date_label.setText(
                QCoreApplication.translate(
                    IRIS_WALLET_TRANSLATIONS_CONTEXT, 'status', None,
                ),
            )
            self.date_value.setText(self.params.transaction_status)

    def handle_close(self):
        """Handle close button"""
        self._view_model.page_navigation.bitcoin_page()
