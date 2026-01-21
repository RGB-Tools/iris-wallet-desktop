# pylint: disable=too-many-instance-attributes, too-many-statements, unused-import
"""This module contains the RGBAssetTransactionDetail class,
 which represents the UI for rgb asset transaction details.
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
from accessible_constant import AMOUNT_VALUE
from accessible_constant import ASSET_TRANSACTION_DETAIL_CLOSE_BUTTON
from accessible_constant import ASSET_TX_ID
from src.data.repository.setting_repository import SettingRepository
from src.model.enums.enums_model import NetworkEnumModel
from src.model.enums.enums_model import PaymentStatus
from src.model.enums.enums_model import TransferStatusEnumModel
from src.model.rgb_model import RgbAssetPageLoadModel
from src.model.transaction_detail_page_model import TransactionDetailPageModel
from src.utils.common_utils import get_bitcoin_explorer_url
from src.utils.common_utils import insert_zero_width_spaces
from src.utils.constant import IRIS_WALLET_TRANSLATIONS_CONTEXT
from src.utils.helpers import load_stylesheet
from src.viewmodels.main_view_model import MainViewModel
from src.views.components.wallet_logo_frame import WalletLogoFrame


class RGBAssetTransactionDetail(QWidget):
    """This class represents all the UI elements of the rgb asset transaction detail page."""

    def __init__(self, view_model, params: TransactionDetailPageModel):
        super().__init__()
        self._view_model: MainViewModel = view_model
        self.params: TransactionDetailPageModel = params
        self.tx_id: str = insert_zero_width_spaces(self.params.tx_id)

        self.setStyleSheet(
            load_stylesheet(
                'views/qss/rgb_asset_transaction_detail.qss',
            ),
        )
        self.grid_layout = QGridLayout(self)
        self.grid_layout.setObjectName('gridLayout')
        self.vertical_spacer_2 = QSpacerItem(
            20, 68, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred,
        )

        self.grid_layout.addItem(self.vertical_spacer_2, 0, 2, 1, 1)

        self.horizontal_spacer = QSpacerItem(
            362, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum,
        )

        self.grid_layout.addItem(self.horizontal_spacer, 2, 0, 1, 1)

        self.horizontal_spacer_2 = QSpacerItem(
            361, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum,
        )

        self.grid_layout.addItem(self.horizontal_spacer_2, 2, 3, 1, 1)

        self.rgb_asset_single_transaction_detail_widget = QWidget(self)
        self.rgb_asset_single_transaction_detail_widget.setObjectName(
            'rgb_single_transaction_detail_widget',
        )
        self.rgb_asset_single_transaction_detail_widget.setMinimumSize(
            QSize(515, 790),
        )
        self.rgb_asset_single_transaction_detail_widget.setMaximumSize(
            QSize(515, 790),
        )

        self.transaction_detail_layout = QGridLayout(
            self.rgb_asset_single_transaction_detail_widget,
        )
        self.transaction_detail_layout.setObjectName('gridLayout_25')
        self.transaction_detail_layout.setContentsMargins(-1, -1, -1, 15)
        self.line_detail_tx = QFrame(
            self.rgb_asset_single_transaction_detail_widget,
        )
        self.line_detail_tx.setObjectName('line_detail_tx')

        self.line_detail_tx.setFrameShape(QFrame.Shape.HLine)
        self.line_detail_tx.setFrameShadow(QFrame.Shadow.Sunken)

        self.transaction_detail_layout.addWidget(
            self.line_detail_tx, 1, 0, 1, 1,
        )

        self.rgb_transaction_layout = QVBoxLayout()
        self.rgb_transaction_layout.setSpacing(0)
        self.rgb_transaction_layout.setObjectName('transaction_layout')
        self.rgb_transaction_layout.setContentsMargins(0, 7, 0, 50)
        self.transaction_detail_frame = QFrame(
            self.rgb_asset_single_transaction_detail_widget,
        )
        self.transaction_detail_frame.setObjectName('transaction_detail_frame')
        self.transaction_detail_frame.setMinimumSize(QSize(340, 520))
        self.transaction_detail_frame.setMaximumSize(QSize(345, 530))

        self.transaction_detail_frame.setFrameShape(QFrame.StyledPanel)
        self.transaction_detail_frame.setFrameShadow(QFrame.Raised)
        self.vertical_layout_tx_detail_frame = QVBoxLayout(
            self.transaction_detail_frame,
        )
        self.vertical_layout_tx_detail_frame.setSpacing(15)
        self.vertical_layout_tx_detail_frame.setObjectName('verticalLayout')
        self.vertical_layout_tx_detail_frame.setContentsMargins(19, 25, -1, 9)
        self.tx_id_label = QLabel(self.transaction_detail_frame)
        self.tx_id_label.setObjectName('tx_id_label')
        self.tx_id_label.setMinimumSize(QSize(295, 20))
        self.tx_id_label.setMaximumSize(QSize(295, 20))

        self.vertical_layout_tx_detail_frame.addWidget(self.tx_id_label)

        self.tx_id_value = QLabel(self.transaction_detail_frame)
        self.tx_id_value.setAccessibleDescription(ASSET_TX_ID)
        self.tx_id_value.setWordWrap(True)
        self.tx_id_value.setTextInteractionFlags(
            Qt.TextBrowserInteraction,
        )
        self.tx_id_value.setOpenExternalLinks(True)
        self.tx_id_value.setObjectName('tx_id_value')
        self.tx_id_value.setMinimumSize(QSize(295, 48))
        self.tx_id_value.setMaximumSize(QSize(305, 48))

        self.tx_id_value.setInputMethodHints(Qt.ImhMultiLine)

        self.vertical_layout_tx_detail_frame.addWidget(self.tx_id_value)

        self.date_label = QLabel(self.transaction_detail_frame)
        self.date_label.setObjectName('date_label')
        self.date_label.setMinimumSize(QSize(295, 20))
        self.date_label.setMaximumSize(QSize(295, 20))

        self.vertical_layout_tx_detail_frame.addWidget(self.date_label)

        self.date_value = QLabel(self.transaction_detail_frame)
        self.date_value.setObjectName('date_value')
        self.date_value.setMinimumSize(QSize(295, 25))
        self.date_value.setMaximumSize(QSize(295, 25))

        self.vertical_layout_tx_detail_frame.addWidget(self.date_value)

        self.blinded_utxo_label = QLabel(self.transaction_detail_frame)
        self.blinded_utxo_label.setObjectName('blinded_utxo_label')
        self.blinded_utxo_label.setMinimumSize(QSize(295, 20))
        self.blinded_utxo_label.setMaximumSize(QSize(295, 20))

        self.vertical_layout_tx_detail_frame.addWidget(self.blinded_utxo_label)

        self.blinded_utxo_value = QLabel(self.transaction_detail_frame)
        self.blinded_utxo_value.setObjectName('blinded_utxo_value')
        self.blinded_utxo_value.setWordWrap(True)
        self.blinded_utxo_value.setMinimumSize(QSize(320, 6))
        self.blinded_utxo_value.setMaximumSize(QSize(320, 65))

        self.vertical_layout_tx_detail_frame.addWidget(self.blinded_utxo_value)

        self.unblinded_and_change_utxo_label = QLabel(
            self.transaction_detail_frame,
        )
        self.unblinded_and_change_utxo_label.setObjectName(
            'unblinded_and_change_utxo_label',
        )
        self.unblinded_and_change_utxo_label.setMinimumSize(QSize(295, 20))
        self.unblinded_and_change_utxo_label.setMaximumSize(QSize(295, 20))

        self.vertical_layout_tx_detail_frame.addWidget(
            self.unblinded_and_change_utxo_label,
        )

        self.unblinded_and_change_utxo_value = QLabel(
            self.transaction_detail_frame,
        )
        self.unblinded_and_change_utxo_value.setWordWrap(True)
        self.unblinded_and_change_utxo_value.setTextInteractionFlags(
            Qt.TextBrowserInteraction,
        )
        self.unblinded_and_change_utxo_value.setOpenExternalLinks(True)
        self.unblinded_and_change_utxo_value.setObjectName(
            'unblinded_and_change_utxo_value',
        )
        self.unblinded_and_change_utxo_value.setMinimumSize(QSize(320, 60))
        self.unblinded_and_change_utxo_value.setMaximumSize(QSize(320, 60))

        self.vertical_layout_tx_detail_frame.addWidget(
            self.unblinded_and_change_utxo_value,
        )

        self.consignment_endpoints_label = QLabel(
            self.transaction_detail_frame,
        )
        self.consignment_endpoints_label.setObjectName(
            'consignment_endpoints_label',
        )
        self.consignment_endpoints_label.setMinimumSize(QSize(295, 20))
        self.consignment_endpoints_label.setMaximumSize(QSize(295, 20))

        self.vertical_layout_tx_detail_frame.addWidget(
            self.consignment_endpoints_label,
        )

        self.consignment_endpoints_value = QLabel(
            self.transaction_detail_frame,
        )
        self.consignment_endpoints_value.setWordWrap(True)
        self.consignment_endpoints_value.setObjectName(
            'consignment_endpoints_value',
        )
        self.consignment_endpoints_value.setMinimumSize(QSize(295, 48))
        self.consignment_endpoints_value.setMaximumSize(QSize(295, 48))

        self.vertical_layout_tx_detail_frame.addWidget(
            self.consignment_endpoints_value,
        )

        self.rgb_transaction_layout.addWidget(
            self.transaction_detail_frame, 0, Qt.AlignHCenter,
        )

        self.transaction_detail_layout.addLayout(
            self.rgb_transaction_layout, 3, 0, 1, 1,
        )

        self.header_layout = QHBoxLayout()
        self.header_layout.setObjectName('header_layout')
        self.header_layout.setContentsMargins(35, 9, 40, 0)
        self.rgb_asset_name_value = QLabel(
            self.rgb_asset_single_transaction_detail_widget,
        )
        self.rgb_asset_name_value.setObjectName('rgb_asset_name_value')
        self.rgb_asset_name_value.setMinimumSize(QSize(415, 52))
        self.rgb_asset_name_value.setMaximumSize(QSize(16777215, 52))

        self.header_layout.addWidget(self.rgb_asset_name_value)

        self.close_btn_rgb_asset_tx_page = QPushButton(
            self.rgb_asset_single_transaction_detail_widget,
        )
        self.close_btn_rgb_asset_tx_page.setObjectName('close_btn')
        self.close_btn_rgb_asset_tx_page.setAccessibleName(
            ASSET_TRANSACTION_DETAIL_CLOSE_BUTTON,
        )
        self.close_btn_rgb_asset_tx_page.setMinimumSize(QSize(24, 24))
        self.close_btn_rgb_asset_tx_page.setMaximumSize(QSize(50, 65))
        self.close_btn_rgb_asset_tx_page.setAutoFillBackground(False)

        icon = QIcon()
        icon.addFile(':/assets/x_circle.png', QSize(), QIcon.Normal, QIcon.Off)
        self.close_btn_rgb_asset_tx_page.setIcon(icon)
        self.close_btn_rgb_asset_tx_page.setIconSize(QSize(24, 24))
        self.close_btn_rgb_asset_tx_page.setCheckable(False)
        self.close_btn_rgb_asset_tx_page.setChecked(False)

        self.header_layout.addWidget(self.close_btn_rgb_asset_tx_page)

        self.transaction_detail_layout.addLayout(
            self.header_layout, 0, 0, 1, 1,
        )

        self.amount_layout = QVBoxLayout()
        self.amount_layout.setObjectName('amount_layout')
        self.amount_layout.setContentsMargins(-1, 17, -1, -1)
        self.rgb_amount_label = QLabel(
            self.rgb_asset_single_transaction_detail_widget,
        )
        self.rgb_amount_label.setObjectName('amount_label')

        self.amount_layout.addWidget(self.rgb_amount_label, 0, Qt.AlignHCenter)

        self.amount_value = QLabel(
            self.rgb_asset_single_transaction_detail_widget,
        )
        self.amount_value.setObjectName('amount_value')
        self.amount_value.setAccessibleDescription(AMOUNT_VALUE)
        self.amount_value.setMinimumSize(QSize(0, 60))

        self.amount_layout.addWidget(self.amount_value, 0, Qt.AlignHCenter)

        self.transaction_detail_layout.addLayout(
            self.amount_layout, 2, 0, 1, 1,
        )

        self.grid_layout.addWidget(
            self.rgb_asset_single_transaction_detail_widget, 2, 1, 1, 2,
        )

        self.vertical_spacer = QSpacerItem(
            20, 100, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred,
        )

        self.grid_layout.addItem(self.vertical_spacer, 3, 1, 1, 1)

        self.wallet_logo = WalletLogoFrame(self)
        self.grid_layout.addWidget(self.wallet_logo, 1, 0, 1, 1)
        self.retranslate_ui()
        self.set_rgb_asset_value()
        self.setup_ui_connection()

    def setup_ui_connection(self):
        """Set up connections for UI elements."""
        self.close_btn_rgb_asset_tx_page.clicked.connect(self.handle_close)

    def retranslate_ui(self):
        """Retranslate the UI elements."""
        self.date_label.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'date', None,
            ),
        )
        self.blinded_utxo_label.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'blinded_utxo', None,
            ),
        )
        self.unblinded_and_change_utxo_label.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'unblinded_utxo', None,
            ),
        )
        self.consignment_endpoints_label.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'consignment_endpoints', None,
            ),
        )
        self.rgb_amount_label.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'amount', None,
            ),
        )

    def set_rgb_asset_value(self):
        """
        Set the values of various UI components based on the provided RGB transaction details.
        """
        self.tx_id_label.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'transaction_id', None,
            ),
        )
        self.rgb_asset_name_value.setText(self.params.asset_name)
        self.amount_value.setText(self.params.amount)
        if self.params.transfer_status == TransferStatusEnumModel.SENT:
            self.amount_value.setStyleSheet(
                load_stylesheet('views/qss/q_label.qss'),
            )

        if self.params.transfer_status == TransferStatusEnumModel.INTERNAL:
            self.consignment_endpoints_value.setText('N/A')
            date_time_concat = f'{self.params.confirmation_date} | {
                self.params.confirmation_time
            }'
            self.date_value.setText(date_time_concat)
            self.blinded_utxo_label.hide()
            self.blinded_utxo_value.hide()
            self.unblinded_and_change_utxo_label.hide()
            self.unblinded_and_change_utxo_value.hide()
            self.tx_id_label.hide()
            self.tx_id_value.hide()
            self.rgb_asset_single_transaction_detail_widget.setMinimumHeight(
                450,
            )
            self.rgb_asset_single_transaction_detail_widget.setMaximumHeight(
                450,
            )
            self.transaction_detail_frame.setMinimumHeight(190)
            self.transaction_detail_frame.setMaximumHeight(190)
            self.grid_layout.addWidget(self.wallet_logo, 0, 0, 1, 1)
            self.vertical_spacer = QSpacerItem(
                40, 250, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred,
            )
            self.grid_layout.addItem(self.vertical_spacer, 3, 1, 1, 1)
        if self.params.is_off_chain:
            self.handle_lightning_detail()

        else:
            unblinded_and_change_utxo_value = None
            self.url = get_bitcoin_explorer_url(self.params.tx_id)
            if self.params.receive_utxo is not None:
                self.url = get_bitcoin_explorer_url(self.params.receive_utxo)
                unblinded_and_change_utxo_value = insert_zero_width_spaces(
                    self.params.receive_utxo,
                )
            if self.params.change_utxo is not None:
                self.url = get_bitcoin_explorer_url(self.params.change_utxo)
                unblinded_and_change_utxo_value = insert_zero_width_spaces(
                    self.params.change_utxo,
                )
            if SettingRepository.get_wallet_network() != NetworkEnumModel.REGTEST:
                self.unblinded_and_change_utxo_value.setText(
                    f"<a style='color: #03CA9B;' href='{self.url}'>"
                    f"{unblinded_and_change_utxo_value}</a>",
                )
                self.tx_id_value.setText(
                    f"<a style='color: #03CA9B;' href='{self.url}'>"
                    f"{self.tx_id}</a>",
                )
            else:
                self.unblinded_and_change_utxo_value.setText(
                    unblinded_and_change_utxo_value,
                )
                self.tx_id_value.setText(self.tx_id)
            self.blinded_utxo_value.setText(self.params.recipient_id)
            if self.params.consignment_endpoints:
                consignment_endpoint = self.params.consignment_endpoints[0].endpoint or 'N/A'
            else:
                consignment_endpoint = 'N/A'
            self.consignment_endpoints_value.setText(consignment_endpoint)
            if self.params.confirmation_date and self.params.confirmation_time:
                date_time_concat = f'{self.params.confirmation_date} | {
                    self.params.confirmation_time
                }'
                self.date_value.setText(date_time_concat)
            else:
                self.amount_value.setStyleSheet(
                    "font: 24px \"Inter\";\n"
                    'color: #798094;\n'
                    'background: transparent;\n'
                    'border: none;\n'
                    'font-weight: 600;\n',
                )
                self.date_label.setText(
                    QCoreApplication.translate(
                        IRIS_WALLET_TRANSLATIONS_CONTEXT, 'status', None,
                    ),
                )
                self.date_value.setText(self.params.transaction_status)

    def handle_close(self):
        """
        Handle the close action for the transaction detail view.

        This method emits a signal with the asset information and navigates to the CFA detail page.

        Attributes:
            self (object): The instance of the class containing the view model and navigation logic.
        """
        self._view_model.cfa_view_model.asset_info.emit(
            self.params.asset_id,
            self.params.asset_name,
            self.params.image_path,
            self.params.asset_type,
        )
        self._view_model.page_navigation.cfa_detail_page(
            RgbAssetPageLoadModel(asset_type=self.params.asset_type),
        )

    def handle_lightning_detail(self):
        """
        Updates UI for Lightning Network transactions:
        - Sets amount color based on status (success, pending).
        - Displays payment hash as transaction ID.
        - Hides irrelevant fields and adjusts widget sizes.
        """
        self.vertical_layout_tx_detail_frame.setSpacing(4)
        self.tx_id_label.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'payee_pubkey', None,
            ),
        )
        if self.params.transaction_status == PaymentStatus.SUCCESS.value:
            if self.params.inbound:
                # Green color for successful received transactions
                self.amount_value.setStyleSheet(
                    'color:#01A781;font-weight: 600',
                )
            else:
                # Red color for successful sent transactions
                self.amount_value.setStyleSheet(
                    'color:#EB5A5A;font-weight: 600',
                )
        elif self.params.transaction_status == PaymentStatus.PENDING.value:
            # Grey color for pending transactions (both sent and received)
            self.amount_value.setStyleSheet(
                'color:#959BAE;font-weight: 600',
            )
        self.tx_id_value.setText(self.tx_id)
        self.tx_id_value.setStyleSheet(
            'color:#01A781;',
        )
        self.date_label.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'confirmation_date', None,
            ),
        )
        date_time_concat = f'{self.params.confirmation_date} | {
            self.params.confirmation_time
        }'
        self.date_value.setText(date_time_concat)

        self.blinded_utxo_label.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'update_date', None,
            ),
        )
        date_time_concat = f'{self.params.updated_date} | {
            self.params.updated_time
        }'
        self.blinded_utxo_label.setMinimumSize(QSize(295, 20))
        self.blinded_utxo_label.setMaximumSize(QSize(295, 20))
        self.blinded_utxo_value.setMinimumSize(QSize(295, 25))
        self.blinded_utxo_value.setMaximumSize(QSize(295, 25))
        self.blinded_utxo_value.setText(date_time_concat)

        self.unblinded_and_change_utxo_label.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'status', None,
            ),
        )
        self.unblinded_and_change_utxo_label.setMinimumSize(QSize(295, 20))
        self.unblinded_and_change_utxo_label.setMaximumSize(QSize(295, 20))
        self.unblinded_and_change_utxo_value.setMinimumSize(QSize(295, 25))
        self.unblinded_and_change_utxo_value.setMaximumSize(QSize(295, 25))
        self.unblinded_and_change_utxo_value.setText(
            self.params.transaction_status,
        )
        self.consignment_endpoints_label.hide()
        self.consignment_endpoints_value.hide()
        self.rgb_asset_single_transaction_detail_widget.setMinimumHeight(
            650,
        )
        self.rgb_asset_single_transaction_detail_widget.setMaximumHeight(
            650,
        )
        self.transaction_detail_frame.setMinimumHeight(400)
        self.transaction_detail_frame.setMaximumHeight(400)
        self.grid_layout.addWidget(self.wallet_logo, 0, 0, 1, 1)
        self.vertical_spacer = QSpacerItem(
            40, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred,
        )
        self.grid_layout.addItem(self.vertical_spacer, 3, 1, 1, 1)
