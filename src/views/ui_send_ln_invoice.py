# pylint: disable=too-many-instance-attributes, too-many-statements, unused-import
"""This module contains the SendLnInvoiceWidget class,
which represents the UI for send ln invoice page.
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
from PySide6.QtWidgets import QPlainTextEdit
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtWidgets import QSpacerItem
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QWidget

import src.resources_rc
from accessible_constant import LN_INVOICE_INPUT
from accessible_constant import SEND_LN_INVOICE_BUTTON
from accessible_constant import SEND_LN_INVOICE_CLOSE_BUTTON
from src.model.enums.enums_model import AssetType
from src.model.enums.enums_model import ChannelFetchingModel
from src.model.invoices_model import DecodeInvoiceResponseModel
from src.utils.constant import IRIS_WALLET_TRANSLATIONS_CONTEXT
from src.utils.helpers import load_stylesheet
from src.utils.render_timer import RenderTimer
from src.viewmodels.main_view_model import MainViewModel
from src.views.components.buttons import PrimaryButton
from src.views.components.loading_screen import LoadingTranslucentScreen
from src.views.components.wallet_logo_frame import WalletLogoFrame


class SendLnInvoiceWidget(QWidget):
    """This class represents all the UI elements of the send ln invoice page."""

    def __init__(self, view_model, asset_type):
        super().__init__()
        self.render_timer = RenderTimer(task_name='SendLNInvoice Rendering')
        self._view_model: MainViewModel = view_model
        self.asset_type = asset_type
        self.invoice_detail = None
        self.is_invoice_valid = None
        self.max_asset_local_balance = None
        self.setStyleSheet(
            load_stylesheet(
                'views/qss/send_ln_invoice_style.qss',
            ),
        )
        self.grid_layout = QGridLayout(self)
        self.grid_layout.setObjectName('grid_layout')
        self.wallet_logo_frame = WalletLogoFrame(self)
        self.grid_layout.addWidget(self.wallet_logo_frame, 0, 0, 1, 1)

        self.enter_ln_invoice_vertical_spacer_1 = QSpacerItem(
            20, 61, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding,
        )

        self.grid_layout.addItem(
            self.enter_ln_invoice_vertical_spacer_1, 0, 2, 1, 1,
        )

        self.enter_ln_invoice_widget = QWidget(self)
        self.enter_ln_invoice_widget.setObjectName('enter_ln_invoice_widget')
        self.enter_ln_invoice_widget.setMinimumSize(QSize(800, 729))
        self.enter_ln_invoice_widget.setMaximumSize(QSize(800, 16777215))
        self.vertical_layout = QVBoxLayout(self.enter_ln_invoice_widget)
        self.vertical_layout.setObjectName('verticalLayout')
        self.enter_ln_invoice_title_layout = QHBoxLayout()
        self.enter_ln_invoice_title_layout.setObjectName(
            'enter_ln_invoice_title_layout',
        )
        self.enter_ln_invoice_title_layout.setContentsMargins(10, -1, 6, -1)
        self.enter_ln_invoice_title_label = QLabel(self)
        self.enter_ln_invoice_title_label.setObjectName(
            'enter_ln_invoice_title_label',
        )
        self.enter_ln_invoice_title_label.setMinimumSize(QSize(415, 63))
        self.enter_ln_invoice_title_label.setMaximumSize(QSize(16777215, 63))

        self.enter_ln_invoice_title_layout.addWidget(
            self.enter_ln_invoice_title_label,
        )

        self.close_btn_send_ln_invoice_page = QPushButton(
            self.enter_ln_invoice_widget,
        )
        self.close_btn_send_ln_invoice_page.setObjectName('close_btn')
        self.close_btn_send_ln_invoice_page.setAccessibleName(
            SEND_LN_INVOICE_CLOSE_BUTTON,
        )
        self.close_btn_send_ln_invoice_page.setMinimumSize(QSize(24, 24))
        self.close_btn_send_ln_invoice_page.setMaximumSize(QSize(50, 65))
        self.close_btn_send_ln_invoice_page.setAutoFillBackground(False)

        icon = QIcon()
        icon.addFile(
            ':/assets/x_circle.png', QSize(),
            QIcon.Mode.Normal, QIcon.State.Off,
        )
        self.close_btn_send_ln_invoice_page.setIcon(icon)
        self.close_btn_send_ln_invoice_page.setIconSize(QSize(24, 24))
        self.close_btn_send_ln_invoice_page.setCheckable(False)
        self.close_btn_send_ln_invoice_page.setChecked(False)
        self.close_btn_send_ln_invoice_page.setCursor(
            QCursor(Qt.CursorShape.PointingHandCursor),
        )

        self.enter_ln_invoice_title_layout.addWidget(
            self.close_btn_send_ln_invoice_page,
        )

        self.vertical_layout.addLayout(self.enter_ln_invoice_title_layout)

        self.header_line = QFrame(self.enter_ln_invoice_widget)
        self.header_line.setObjectName('line_1')

        self.header_line.setFrameShape(QFrame.Shape.HLine)
        self.header_line.setFrameShadow(QFrame.Shadow.Sunken)

        self.vertical_layout.addWidget(self.header_line)

        self.ln_invoice_label = QLabel(self.enter_ln_invoice_widget)
        self.ln_invoice_label.setObjectName('ln_invoice_label')
        self.ln_invoice_label.setMinimumSize(QSize(0, 25))
        self.ln_invoice_label.setMaximumSize(QSize(16777215, 25))
        self.ln_invoice_label.setBaseSize(QSize(0, 0))
        self.ln_invoice_label.setAutoFillBackground(False)

        self.ln_invoice_label.setFrameShadow(QFrame.Plain)
        self.ln_invoice_label.setLineWidth(1)

        self.vertical_layout.addWidget(self.ln_invoice_label)

        self.ln_invoice_input = QPlainTextEdit(self.enter_ln_invoice_widget)
        self.ln_invoice_input.setObjectName('ln_invoice_input')
        self.ln_invoice_input.setAccessibleName(LN_INVOICE_INPUT)
        self.ln_invoice_input.setMinimumSize(QSize(550, 50))
        self.ln_invoice_input.setMaximumSize(QSize(550, 155))

        self.vertical_layout.addWidget(
            self.ln_invoice_input, 0, Qt.AlignHCenter,
        )

        self.invoice_detail_label = QLabel(self.enter_ln_invoice_widget)
        self.invoice_detail_label.setObjectName('invoice_detail_label')
        self.invoice_detail_label.setMinimumSize(QSize(0, 25))
        self.invoice_detail_label.setMaximumSize(QSize(16777215, 25))
        self.invoice_detail_label.setBaseSize(QSize(0, 0))
        self.invoice_detail_label.setAutoFillBackground(False)

        self.invoice_detail_label.setFrameShadow(QFrame.Plain)
        self.invoice_detail_label.setLineWidth(1)

        self.vertical_layout.addWidget(self.invoice_detail_label)

        self.invoice_detail_frame = QFrame(self.enter_ln_invoice_widget)
        self.invoice_detail_frame.setObjectName('invoice_detail_frame')
        self.invoice_detail_frame.setMinimumSize(QSize(700, 300))
        self.invoice_detail_frame.setMaximumSize(QSize(740, 300))

        self.invoice_detail_frame.setFrameShape(QFrame.StyledPanel)
        self.invoice_detail_frame.setFrameShadow(QFrame.Raised)
        self.invoice_detail_frame_layout = QVBoxLayout(
            self.invoice_detail_frame,
        )
        self.invoice_detail_frame_layout.setObjectName('verticalLayout_2')
        self.amount_horizontal_layout = QHBoxLayout()
        self.amount_horizontal_layout.setObjectName('amount_horizontal_layout')
        self.amount_label = QLabel(self.invoice_detail_frame)
        self.amount_label.setObjectName('amount_label')
        self.amount_label.setMinimumSize(QSize(120, 0))
        self.amount_label.setMaximumSize(QSize(120, 16777215))
        self.amount_label.setStyleSheet('color:white')

        self.amount_horizontal_layout.addWidget(self.amount_label)

        self.amount_value = QLabel(self.invoice_detail_frame)
        self.amount_value.setObjectName('amount_value')

        self.amount_horizontal_layout.addWidget(self.amount_value)

        self.invoice_detail_frame_layout.addLayout(
            self.amount_horizontal_layout,
        )

        self.expiry_horizontal_layout = QHBoxLayout()
        self.expiry_horizontal_layout.setObjectName('expiry_horizontal_layout')
        self.expiry_label = QLabel(self.invoice_detail_frame)
        self.expiry_label.setObjectName('expiry_label')
        self.expiry_label.setMaximumSize(QSize(120, 16777215))
        self.expiry_label.setStyleSheet('color:white')

        self.expiry_horizontal_layout.addWidget(self.expiry_label)

        self.expiry_value = QLabel(self.invoice_detail_frame)
        self.expiry_value.setObjectName('expiry_value')

        self.expiry_horizontal_layout.addWidget(self.expiry_value)

        self.invoice_detail_frame_layout.addLayout(
            self.expiry_horizontal_layout,
        )

        self.timestamp_horizontal_layout = QHBoxLayout()
        self.timestamp_horizontal_layout.setObjectName(
            'timestamp_horizontal_layout',
        )
        self.timestamp_label = QLabel(self.invoice_detail_frame)
        self.timestamp_label.setObjectName('timestamp_label')
        self.timestamp_label.setMaximumSize(QSize(120, 16777215))
        self.timestamp_label.setStyleSheet('color:white')

        self.timestamp_horizontal_layout.addWidget(self.timestamp_label)

        self.timestamp_value = QLabel(self.invoice_detail_frame)
        self.timestamp_value.setObjectName('timestamp_value')

        self.timestamp_horizontal_layout.addWidget(self.timestamp_value)

        self.invoice_detail_frame_layout.addLayout(
            self.timestamp_horizontal_layout,
        )

        self.asset_id_horizontal_layout = QHBoxLayout()
        self.asset_id_horizontal_layout.setObjectName(
            'asset_id_horizontal_layout',
        )
        self.asset_id_label = QLabel(self.invoice_detail_frame)
        self.asset_id_label.setObjectName('asset_id_label')
        self.asset_id_label.setMinimumSize(QSize(120, 0))
        self.asset_id_label.setMaximumSize(QSize(120, 16777215))
        self.asset_id_label.setStyleSheet('color:white')

        self.asset_id_horizontal_layout.addWidget(self.asset_id_label)

        self.asset_id_value = QLabel(self.invoice_detail_frame)
        self.asset_id_value.setObjectName('asset_id_value')

        self.asset_id_horizontal_layout.addWidget(self.asset_id_value)

        self.invoice_detail_frame_layout.addLayout(
            self.asset_id_horizontal_layout,
        )

        self.asset_amount_horizontal_layout = QHBoxLayout()
        self.asset_amount_horizontal_layout.setObjectName(
            'asset_amount_horizontal_layout',
        )
        self.asset_amount_label = QLabel(self.invoice_detail_frame)
        self.asset_amount_label.setObjectName('asset_amount_label')
        self.asset_amount_label.setMinimumSize(QSize(120, 0))
        self.asset_amount_label.setMaximumSize(QSize(120, 16777215))
        self.asset_amount_label.setStyleSheet('color:white')

        self.asset_amount_horizontal_layout.addWidget(self.asset_amount_label)

        self.asset_amount_value = QLabel(self.invoice_detail_frame)
        self.asset_amount_value.setObjectName('asset_amount_value')

        self.asset_amount_horizontal_layout.addWidget(self.asset_amount_value)

        self.invoice_detail_frame_layout.addLayout(
            self.asset_amount_horizontal_layout,
        )

        self.p_hash_horizontal_layout = QHBoxLayout()
        self.p_hash_horizontal_layout.setObjectName('p_hash_horizontal_layout')
        self.p_hash_label = QLabel(self.invoice_detail_frame)
        self.p_hash_label.setObjectName('p_hash_label')
        self.p_hash_label.setMinimumSize(QSize(120, 0))
        self.p_hash_label.setMaximumSize(QSize(120, 16777215))
        self.p_hash_label.setStyleSheet('color:white')

        self.p_hash_horizontal_layout.addWidget(self.p_hash_label)

        self.p_hash_value = QLabel(self.invoice_detail_frame)
        self.p_hash_value.setObjectName('p_hash_value')

        self.p_hash_horizontal_layout.addWidget(self.p_hash_value)

        self.invoice_detail_frame_layout.addLayout(
            self.p_hash_horizontal_layout,
        )

        self.p_secret_horizontal_layout = QHBoxLayout()
        self.p_secret_horizontal_layout.setObjectName(
            'p_secret_horizontal_layout',
        )
        self.p_secret_label = QLabel(self.invoice_detail_frame)
        self.p_secret_label.setObjectName('p_secret_label')
        self.p_secret_label.setMinimumSize(QSize(120, 0))
        self.p_secret_label.setMaximumSize(QSize(120, 16777215))
        self.p_secret_label.setStyleSheet('color:white')

        self.p_secret_horizontal_layout.addWidget(self.p_secret_label)

        self.p_secret_value = QLabel(self.invoice_detail_frame)
        self.p_secret_value.setObjectName('p_secret_value')

        self.p_secret_horizontal_layout.addWidget(self.p_secret_value)

        self.invoice_detail_frame_layout.addLayout(
            self.p_secret_horizontal_layout,
        )

        self.payee_pubkey_horizontal_layout = QHBoxLayout()
        self.payee_pubkey_horizontal_layout.setObjectName(
            'payee_pubkey_horizontal_layout',
        )
        self.p_pubkey_label = QLabel(self.invoice_detail_frame)
        self.p_pubkey_label.setObjectName('p_pubkey_label')
        self.p_pubkey_label.setMinimumSize(QSize(120, 0))
        self.p_pubkey_label.setMaximumSize(QSize(120, 16777215))
        self.p_pubkey_label.setStyleSheet('color:white')

        self.payee_pubkey_horizontal_layout.addWidget(self.p_pubkey_label)

        self.p_pubkey_value = QLabel(self.invoice_detail_frame)
        self.p_pubkey_value.setObjectName('p_pubkey_value')
        self.p_pubkey_value.setMinimumSize(QSize(0, 0))

        self.payee_pubkey_horizontal_layout.addWidget(self.p_pubkey_value)

        self.invoice_detail_frame_layout.addLayout(
            self.payee_pubkey_horizontal_layout,
        )

        self.network_horizontal_layout = QHBoxLayout()
        self.network_horizontal_layout.setObjectName(
            'network_horizontal_layout',
        )
        self.network_label = QLabel(self.invoice_detail_frame)
        self.network_label.setObjectName('network_label')
        self.network_label.setMinimumSize(QSize(120, 0))
        self.network_label.setMaximumSize(QSize(120, 16777215))
        self.network_label.setStyleSheet('color:white')

        self.network_horizontal_layout.addWidget(self.network_label)

        self.network_value = QLabel(self.invoice_detail_frame)
        self.network_value.setObjectName('network_value')

        self.network_horizontal_layout.addWidget(self.network_value)

        self.invoice_detail_frame_layout.addLayout(
            self.network_horizontal_layout,
        )

        self.vertical_layout.addWidget(
            self.invoice_detail_frame, 0, Qt.AlignHCenter,
        )

        self.amount_validation_error_label = QLabel(
            self.enter_ln_invoice_widget,
        )
        self.amount_validation_error_label.setObjectName(
            'amount_validation_error_label',
        )
        self.amount_validation_error_label.setFixedHeight(30)

        self.amount_validation_error_label.hide()

        self.vertical_spacer = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding,
        )

        self.vertical_layout.addItem(self.vertical_spacer)

        self.vertical_layout.addWidget(
            self.amount_validation_error_label, 0, Qt.AlignHCenter,
        )

        self.footer_line = QFrame(self.enter_ln_invoice_widget)
        self.footer_line.setObjectName('line_2')
        self.footer_line.setStyleSheet(
            '    border: none;\n'
            '    border-bottom: 1px solid rgb(27, 35, 59) ;\n'
            '',
        )
        self.footer_line.setFrameShape(QFrame.Shape.HLine)
        self.footer_line.setFrameShadow(QFrame.Shadow.Sunken)

        self.vertical_layout.addWidget(self.footer_line)

        self.send_button_horizontal_layout = QHBoxLayout()
        self.send_button_horizontal_layout.setObjectName(
            'send_button_horizontal_layout',
        )
        self.send_button_horizontal_layout.setContentsMargins(-1, 15, -1, 15)
        self.send_button = PrimaryButton()
        self.send_button.setAccessibleName(SEND_LN_INVOICE_BUTTON)
        self.send_button.setMinimumSize(QSize(0, 40))
        self.send_button.setMaximumSize(QSize(402, 16777215))
        self.send_button_horizontal_layout.addWidget(self.send_button)

        self.vertical_layout.addLayout(self.send_button_horizontal_layout)

        self.grid_layout.addWidget(self.enter_ln_invoice_widget, 1, 1, 2, 2)

        self.enter_ln_invoice_horizontal_spacer_2 = QSpacerItem(
            49, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum,
        )

        self.grid_layout.addItem(
            self.enter_ln_invoice_horizontal_spacer_2, 1, 3, 1, 1,
        )

        self.enter_ln_invoice_horizontal_spacer_1 = QSpacerItem(
            257, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum,
        )

        self.grid_layout.addItem(
            self.enter_ln_invoice_horizontal_spacer_1, 2, 0, 1, 1,
        )

        self.enter_ln_invoice_vertical_spacer_2 = QSpacerItem(
            20, 3, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding,
        )

        self.grid_layout.addItem(
            self.enter_ln_invoice_vertical_spacer_2, 3, 1, 1, 1,
        )
        self.invoice_detail_label.hide()
        self.invoice_detail_frame.hide()
        self.enter_ln_invoice_widget.setMinimumSize(QSize(650, 400))
        self.send_button.setDisabled(True)
        self.__loading_translucent_screen = LoadingTranslucentScreen(
            parent=self, description_text='Loading',
        )
        self.retranslate_ui()
        self.setup_ui_connection()

    def setup_ui_connection(self):
        """Set up connections for UI elements."""
        self.ln_invoice_input.textChanged.connect(self.get_invoice_detail)
        self._view_model.ln_offchain_view_model.invoice_detail.connect(
            self.store_invoice_details,
        )
        self.send_button.clicked.connect(self.send_asset)
        self.close_btn_send_ln_invoice_page.clicked.connect(
            self.on_click_close_button,
        )
        self._view_model.ln_offchain_view_model.is_loading.connect(
            self.update_loading_state,
        )
        self._view_model.ln_offchain_view_model.is_sent.connect(
            self.on_success_sent_navigation,
        )
        self._view_model.channel_view_model.is_channel_fetching.connect(
            self.is_channel_fetched,
        )
        self._view_model.ln_offchain_view_model.is_invoice_valid.connect(
            self.set_is_invoice_valid,
        )

    def set_is_invoice_valid(self, is_valid: bool):
        """this method checks if the invoice is valid and performs the necessary actions"""
        if is_valid:
            self.is_invoice_valid = True
            self._view_model.channel_view_model.available_channels()

        else:
            self.is_invoice_valid = False
            self.invoice_detail_frame.hide()
            self.invoice_detail_label.hide()
            self.amount_validation_error_label.hide()
            self.enter_ln_invoice_widget.setMinimumSize(QSize(650, 400))
            self.send_button.setDisabled(True)

    def store_invoice_details(self, details):
        """this method stores the invoice details"""
        self.invoice_detail = details

    def is_channel_fetched(self, is_loading, is_fetching):
        """this method displays the loading bar and display the invoice detail frame if there is a valid invoice"""
        if is_loading:
            self.__loading_translucent_screen.start()
            self.ln_invoice_input.setReadOnly(True)
            self.send_button.setDisabled(True)
            self.close_btn_send_ln_invoice_page.setDisabled(True)
        else:
            if self.is_invoice_valid:
                if is_fetching == ChannelFetchingModel.FETCHED.value:
                    self.show_invoice_detail(detail=self.invoice_detail)
                    self.__loading_translucent_screen.stop()
                    self.ln_invoice_input.setReadOnly(False)
                if is_fetching == ChannelFetchingModel.FAILED.value:
                    self.send_button.setDisabled(False)
                    self.__loading_translucent_screen.stop()
            else:
                self.__loading_translucent_screen.stop()
                self.send_button.setDisabled(True)
                self.invoice_detail_frame.hide()
                self.invoice_detail_label.hide()
            self.close_btn_send_ln_invoice_page.setDisabled(False)

    def retranslate_ui(self):
        """Retranslate the UI elements."""
        self.enter_ln_invoice_title_label.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'enter_ln_invoice_title_label', None,
            ),
        )
        self.ln_invoice_label.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'ln_invoice_label', None,
            ),
        )
        self.invoice_detail_label.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'invoice_detail_label', None,
            ),
        )
        self.amount_label.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'msat_amount_label', None,
            ),
        )
        self.expiry_label.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'expiry_label_sec', None,
            ),
        )
        self.timestamp_label.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'timestamp_label', None,
            ),
        )
        self.asset_id_label.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'asset_id', None,
            ),
        )
        self.asset_amount_label.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'asset_amount_label', None,
            ),
        )
        self.p_hash_label.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'p_hash_label', None,
            ),
        )
        self.p_secret_label.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'p_secret_label', None,
            ),
        )
        self.p_pubkey_label.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'p_pubkey_label', None,
            ),
        )
        self.network_label.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'network_label', None,
            ),
        )
        self.amount_validation_error_label.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'amount_validation_error_label', None,
            ),
        )
        self.send_button.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'send_button', None,
            ),
        )

    def show_invoice_detail(self, detail: DecodeInvoiceResponseModel):
        """Shows the invoice detail card."""
        self._display_invoice_detail(detail)
        self._update_max_asset_local_balance(detail)
        self._validate_asset_amount(detail)

    def _display_invoice_detail(self, detail):
        """Displays the invoice details on the UI."""
        self.invoice_detail_label.show()
        self.invoice_detail_frame.show()
        self.enter_ln_invoice_widget.setMinimumSize(QSize(800, 730))
        self.amount_value.setText(str(detail.amt_msat // 1000))
        self.expiry_value.setText(str(detail.expiry_sec))
        self.asset_id_value.setText(str(detail.asset_id or ''))
        self.asset_amount_value.setText(str(detail.asset_amount or ''))
        self.p_hash_value.setText(str(detail.payment_hash))
        self.p_secret_value.setText(str(detail.payment_secret))
        self.p_pubkey_value.setText(str(detail.payee_pubkey))
        self.network_value.setText(str(detail.network))
        self.timestamp_value.setText(str(detail.timestamp))
        self.send_button.setDisabled(True)

    def _update_max_asset_local_balance(self, detail):
        """Updates the maximum asset local balance for the given asset_id."""
        if detail.asset_id:
            max_balance = None
            for channel in self._view_model.channel_view_model.channels:
                if channel.asset_id == detail.asset_id and channel.is_usable and channel.ready:
                    max_balance = max(
                        max_balance or 0,
                        channel.asset_local_amount,
                    )
            self.max_asset_local_balance = max_balance

    def _validate_asset_amount(self, detail):
        """Validates the asset amount and updates the UI accordingly."""
        if detail.asset_id is None:
            self._hide_asset_fields()
            self.send_button.setDisabled(False)
            self.amount_validation_error_label.hide()
            return

        if detail.asset_amount is not None:
            if self.max_asset_local_balance is not None and detail.asset_amount > self.max_asset_local_balance:
                self.amount_validation_error_label.show()
                self.send_button.setDisabled(True)
            else:
                self.amount_validation_error_label.hide()
                self.send_button.setDisabled(False)

    def _hide_asset_fields(self):
        """Hides asset-related fields from the UI."""
        self.asset_id_value.hide()
        self.asset_id_label.hide()
        self.asset_amount_value.hide()
        self.asset_amount_label.hide()

    def get_invoice_detail(self):
        """This method is used to get invoice detail"""
        invoice = self.ln_invoice_input.toPlainText()
        if len(invoice) > 200:
            self._view_model.ln_offchain_view_model.decode_invoice(invoice)
        else:
            self.invoice_detail_frame.hide()
            self.invoice_detail_label.hide()
            self.enter_ln_invoice_widget.setMinimumSize(QSize(650, 400))
            self.send_button.setDisabled(True)

    def send_asset(self):
        """This method is used to send asset"""
        invoice = self.ln_invoice_input.toPlainText()
        self._view_model.ln_offchain_view_model.send_asset_offchain(invoice)

    def on_success_sent_navigation(self):
        """This method is used to navigate to collectibles or fungibles page when the originating page is create ln invoice"""
        if self.asset_type == AssetType.CFA.value:
            self._view_model.page_navigation.collectibles_asset_page()
        else:
            self._view_model.page_navigation.fungibles_asset_page()

    def handle_button_enable(self):
        """This method handled button states"""
        if self.ln_invoice_input.toPlainText():
            self.send_button.setDisabled(False)
        else:
            self.send_button.setDisabled(True)

    def update_loading_state(self, is_loading: bool):
        """Updates the loading state of the send button."""
        if is_loading:
            self.render_timer.start()
            self.send_button.start_loading()
        else:
            self.render_timer.stop()
            self.send_button.stop_loading()

    def on_click_close_button(self):
        """This method is used to navigate to fungibles or collectibles page based on asset type"""
        if self.asset_type == AssetType.CFA.value:
            self._view_model.page_navigation.collectibles_asset_page()
        else:
            self._view_model.page_navigation.fungibles_asset_page()
