# pylint: disable=too-many-instance-attributes, too-many-statements, unused-import
"""This module contains the CreateLnInvoiceWidget class,
which represents the UI for create ln invoice page.
"""
from __future__ import annotations

from PySide6.QtCore import QCoreApplication
from PySide6.QtCore import QSize
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import QComboBox
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

from accessible_constant import ASSET_AMOUNT_LN
from accessible_constant import CREATE_LN_INVOICE_AMOUNT_VALIDATION
from accessible_constant import CREATE_LN_INVOICE_BUTTON
from accessible_constant import CREATE_LN_INVOICE_CLOSE_BUTTON
from accessible_constant import EXPIRY_TIME
from accessible_constant import EXPIRY_TIME_COMBO_BOX
from accessible_constant import MSAT_AMOUNT
from src.data.repository.setting_card_repository import SettingCardRepository
from src.model.common_operation_model import NodeInfoResponseModel
from src.model.enums.enums_model import AssetType
from src.model.enums.enums_model import UnitType
from src.model.invoices_model import LnInvoiceRequestModel
from src.model.node_info_model import NodeInfoModel
from src.model.selection_page_model import AssetDataModel
from src.model.setting_model import DefaultExpiryTime
from src.utils.common_utils import extract_amount
from src.utils.common_utils import sat_to_msat
from src.utils.common_utils import set_placeholder_value
from src.utils.constant import IRIS_WALLET_TRANSLATIONS_CONTEXT
from src.utils.helpers import load_stylesheet
from src.utils.render_timer import RenderTimer
from src.viewmodels.main_view_model import MainViewModel
from src.views.components.buttons import PrimaryButton
from src.views.components.loading_screen import LoadingTranslucentScreen
from src.views.components.wallet_logo_frame import WalletLogoFrame


class CreateLnInvoiceWidget(QWidget):
    """This class represents all the UI elements of the create ln invoice page."""

    def __init__(self, view_model, asset_id, asset_name, asset_type):
        super().__init__()
        get_node_info = NodeInfoModel()
        self.node_info: NodeInfoResponseModel = get_node_info.node_info
        self.amt_msat_value = self.node_info.rgb_htlc_min_msat
        self.value_default_expiry_time: DefaultExpiryTime = SettingCardRepository.get_default_expiry_time()
        self.render_timer = RenderTimer(task_name='CreateLnInvoice Rendering')
        self._view_model: MainViewModel = view_model
        self.setStyleSheet(
            load_stylesheet(
                'views/qss/create_ln_invoice_style.qss',
            ),
        )
        self.grid_layout = QGridLayout(self)
        self.asset_id = asset_id
        self.asset_name = asset_name
        self.asset_type = asset_type
        self.max_asset_local_amount = None
        self.__loading_translucent_screen = LoadingTranslucentScreen(
            parent=self, description_text='Loading', dot_animation=True,
        )
        self.grid_layout.setObjectName('grid_layout')
        self.vertical_spacer_2 = QSpacerItem(
            20, 85, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding,
        )

        self.grid_layout.addItem(self.vertical_spacer_2, 4, 1, 1, 1)

        self.wallet_logo_frame = WalletLogoFrame(self)

        self.grid_layout.addWidget(self.wallet_logo_frame, 0, 0, 1, 1)

        self.vertical_spacer = QSpacerItem(
            20, 86, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding,
        )

        self.grid_layout.addItem(self.vertical_spacer, 0, 1, 1, 1)

        self.horizontal_spacer_2 = QSpacerItem(
            277, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum,
        )

        self.grid_layout.addItem(self.horizontal_spacer_2, 2, 2, 1, 1)

        self.horizontal_spacer = QSpacerItem(
            277, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum,
        )

        self.grid_layout.addItem(self.horizontal_spacer, 3, 0, 1, 1)

        self.ln_invoice_card = QWidget(self)
        self.ln_invoice_card.setObjectName('ln_invoice_card')
        self.ln_invoice_card.setMinimumSize(QSize(499, 650))
        self.ln_invoice_card.setMaximumSize(QSize(499, 650))

        self.ln_invoice_card_layout = QVBoxLayout(self.ln_invoice_card)
        self.ln_invoice_card_layout.setObjectName('vertical_layout')
        self.ln_invoice_card_layout.setContentsMargins(1, -1, 1, -1)
        self.title_layout = QGridLayout()
        self.title_layout.setObjectName('tittle_layout')
        self.title_layout.setContentsMargins(40, -1, 40, -1)
        self.create_ln_invoice_label = QLabel(self.ln_invoice_card)
        self.create_ln_invoice_label.setObjectName('create_ln_invoice_label')

        self.title_layout.addWidget(self.create_ln_invoice_label, 0, 0, 1, 1)

        self.close_btn_ln_invoice_page = QPushButton(self.ln_invoice_card)
        self.close_btn_ln_invoice_page.setObjectName('close_btn')
        self.close_btn_ln_invoice_page.setAccessibleName(
            CREATE_LN_INVOICE_CLOSE_BUTTON,
        )
        self.close_btn_ln_invoice_page.setMinimumSize(QSize(24, 24))
        self.close_btn_ln_invoice_page.setMaximumSize(QSize(50, 65))
        self.close_btn_ln_invoice_page.setAutoFillBackground(False)

        icon = QIcon()
        icon.addFile(':/assets/x_circle.png', QSize(), QIcon.Normal, QIcon.Off)
        self.close_btn_ln_invoice_page.setIcon(icon)
        self.close_btn_ln_invoice_page.setIconSize(QSize(24, 24))
        self.close_btn_ln_invoice_page.setCheckable(False)
        self.close_btn_ln_invoice_page.setChecked(False)

        self.title_layout.addWidget(
            self.close_btn_ln_invoice_page, 0, 1, 1, 1,
        )

        self.ln_invoice_card_layout.addLayout(self.title_layout)

        self.header_line = QFrame(self.ln_invoice_card)
        self.header_line.setObjectName('line')

        self.header_line.setFrameShape(QFrame.Shape.HLine)
        self.header_line.setFrameShadow(QFrame.Shadow.Sunken)

        self.ln_invoice_card_layout.addWidget(self.header_line)

        self.asset_input_layout = QVBoxLayout()
        self.asset_input_layout.setSpacing(16)
        self.asset_input_layout.setObjectName('asset_input_layout')
        self.asset_input_layout.setContentsMargins(0, 10, 0, -1)

        self.asset_name_label = QLabel(self.ln_invoice_card)
        self.asset_name_label.setObjectName('asset_name_label')
        self.asset_name_label.setMinimumSize(QSize(370, 0))
        self.asset_name_label.setAutoFillBackground(False)

        self.asset_name_label.setFrameShadow(QFrame.Plain)
        self.asset_name_label.setLineWidth(1)

        self.asset_input_layout.addWidget(
            self.asset_name_label, 0, Qt.AlignHCenter,
        )

        self.asset_name_value = QLineEdit(self.ln_invoice_card)
        self.asset_name_value.setObjectName('asset_name_value')
        self.asset_name_value.setMinimumSize(QSize(370, 40))
        self.asset_name_value.setReadOnly(True)
        self.asset_name_value.setText(self.asset_name)
        self.asset_input_layout.addWidget(
            self.asset_name_value, 0, Qt.AlignHCenter,
        )

        self.amount_label = QLabel(self.ln_invoice_card)
        self.amount_label.setObjectName('amount_label')
        self.amount_label.setMinimumSize(QSize(370, 0))

        self.asset_input_layout.addWidget(
            self.amount_label, 0, Qt.AlignHCenter,
        )

        self.amount_input = QLineEdit(self.ln_invoice_card)
        self.amount_input.setObjectName('amount_input')
        self.amount_input.setMinimumSize(QSize(370, 40))
        self.amount_input.setAccessibleName(ASSET_AMOUNT_LN)

        self.amount_input.setValidator(QIntValidator())

        self.amount_input.setClearButtonEnabled(True)

        self.asset_input_layout.addWidget(
            self.amount_input, 0, Qt.AlignHCenter,
        )

        self.asset_balance_validation_label = QLabel(self.ln_invoice_card)
        self.asset_balance_validation_label.setObjectName(
            'asset_balance_validation_label',
        )
        self.asset_balance_validation_label.setAccessibleDescription(
            CREATE_LN_INVOICE_AMOUNT_VALIDATION,
        )
        self.asset_balance_validation_label.setMinimumSize(QSize(370, 35))
        self.asset_balance_validation_label.setWordWrap(True)
        self.asset_balance_validation_label.hide()
        self.asset_input_layout.addWidget(
            self.asset_balance_validation_label, 0, Qt.AlignHCenter,
        )

        self.msat_amount_label = QLabel(self.ln_invoice_card)
        self.msat_amount_label.setObjectName('msat_amount_label')
        self.msat_amount_label.setMinimumSize(QSize(370, 0))
        self.msat_amount_label.setAutoFillBackground(False)

        self.msat_amount_label.setFrameShadow(QFrame.Plain)
        self.msat_amount_label.setLineWidth(1)

        self.asset_input_layout.addWidget(
            self.msat_amount_label, 0, Qt.AlignHCenter,
        )

        self.msat_amount_value = QLineEdit(self.ln_invoice_card)
        self.msat_amount_value.setObjectName('msat_amount_value')
        self.msat_amount_value.setAccessibleName(MSAT_AMOUNT)
        self.msat_amount_value.setMinimumSize(QSize(370, 40))
        self.msat_amount_value.setValidator(QIntValidator())

        self.asset_input_layout.addWidget(
            self.msat_amount_value, 0, Qt.AlignHCenter,
        )

        self.msat_error_label = QLabel(self.ln_invoice_card)
        self.msat_error_label.setObjectName('msat_error_label')
        self.msat_error_label.setMinimumSize(QSize(370, 35))
        self.msat_error_label.setWordWrap(True)
        self.msat_error_label.hide()

        self.asset_input_layout.addWidget(
            self.msat_error_label, 0, Qt.AlignHCenter,
        )
        self.expiry_label = QLabel(self.ln_invoice_card)
        self.expiry_label.setObjectName('expiry_label')
        self.expiry_label.setMinimumSize(QSize(370, 0))

        self.asset_input_layout.addWidget(
            self.expiry_label, 0, Qt.AlignHCenter,
        )

        self.expiry_time_grid_layout = QGridLayout()
        self.expiry_time_grid_layout.setContentsMargins(0, 0, 0, 0)

        self.expiry_input = QLineEdit(self.ln_invoice_card)
        self.expiry_input.setObjectName('expiry_input')
        self.expiry_input.setMinimumSize(QSize(250, 40))
        self.expiry_input.setMaximumSize(QSize(370, 40))
        self.expiry_input.setAccessibleName(EXPIRY_TIME)
        self.expiry_input.setAccessibleDescription(self.expiry_input.text())

        self.expiry_input.setValidator(QIntValidator())
        self.expiry_time_grid_layout.addWidget(
            self.expiry_input, 0, 0, Qt.AlignHCenter,
        )
        self.expiry_input.setText(
            str(self.value_default_expiry_time.time),
        )
        self.time_unit_combobox = QComboBox()
        self.time_unit_combobox.setMinimumSize(QSize(100, 40))
        self.time_unit_combobox.setMaximumSize(QSize(160, 40))
        self.time_unit_combobox.setAccessibleDescription(EXPIRY_TIME_COMBO_BOX)

        self.expiry_time_grid_layout.addWidget(
            self.time_unit_combobox, 0, 1, Qt.AlignHCenter,
        )

        self.asset_input_layout.addLayout(self.expiry_time_grid_layout)
        self.asset_input_layout.setAlignment(
            self.expiry_time_grid_layout, Qt.AlignHCenter,
        )

        self.ln_invoice_card_layout.addLayout(self.asset_input_layout)

        self.vertical_spacer_4 = QSpacerItem(
            20, 148, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding,
        )

        self.ln_invoice_card_layout.addItem(self.vertical_spacer_4)

        self.footer_line = QFrame(self.ln_invoice_card)
        self.footer_line.setObjectName('line_2')

        self.footer_line.setFrameShape(QFrame.Shape.HLine)
        self.footer_line.setFrameShadow(QFrame.Shadow.Sunken)

        self.ln_invoice_card_layout.addWidget(self.footer_line)

        self.button_layout = QHBoxLayout()
        self.button_layout.setObjectName('button_layout')
        self.button_layout.setContentsMargins(-1, 20, -1, 20)
        self.horizontal_spacer_3 = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum,
        )

        self.button_layout.addItem(self.horizontal_spacer_3)

        self.create_button = PrimaryButton()
        self.create_button.setAccessibleName(CREATE_LN_INVOICE_BUTTON)
        self.create_button.setMinimumSize(QSize(370, 40))
        self.create_button.setMaximumSize(QSize(370, 40))
        self.create_button.setEnabled(False)
        self.button_layout.addWidget(self.create_button)

        self.horizontal_spacer_4 = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum,
        )

        self.button_layout.addItem(self.horizontal_spacer_4)

        self.ln_invoice_card_layout.addLayout(self.button_layout)

        self.grid_layout.addWidget(self.ln_invoice_card, 1, 1, 3, 1)

        self.setup_ui_connection()
        self.retranslate_ui()
        self.handle_bitcoin_layout()
        self.msat_value_change()

    def handle_bitcoin_layout(self):
        """This method change the layout according the asset value"""
        if self.asset_id == AssetType.BITCOIN.value:
            self.asset_name_label.hide()
            self.asset_name_value.hide()
            self.msat_amount_label.hide()
            self.msat_amount_value.hide()
            self.msat_error_label.hide()
            self.asset_balance_validation_label.hide()
            self.hide_create_ln_invoice_loader()
        else:
            self._view_model.channel_view_model.available_channels()
            self._view_model.channel_view_model.channel_loaded.connect(
                self.get_max_asset_remote_balance,
            )
            self._view_model.channel_view_model.channel_loaded.connect(
                self.hide_create_ln_invoice_loader,
            )
            self.amount_label.setText(
                QCoreApplication.translate(
                    IRIS_WALLET_TRANSLATIONS_CONTEXT, 'asset_amount', None,
                ),
            )
            self.amount_input.setPlaceholderText(
                QCoreApplication.translate(
                    IRIS_WALLET_TRANSLATIONS_CONTEXT, 'asset_amount', None,
                ),
            )

    def setup_ui_connection(self):
        """Set up connections for UI elements."""
        self.show_create_ln_invoice_loader()
        self.asset_name_value.textChanged.connect(self.handle_button_enable)
        self.amount_input.textChanged.connect(self.handle_button_enable)
        self.expiry_input.textChanged.connect(self.handle_button_enable)
        self.create_button.clicked.connect(self.get_ln_invoice)
        self.close_btn_ln_invoice_page.clicked.connect(self.on_close)
        self.msat_amount_value.textChanged.connect(
            self.msat_value_change,
        )
        self.msat_amount_value.textChanged.connect(
            self.handle_button_enable,
        )
        self.amount_input.textChanged.connect(self.validate_asset_amount)
        self.amount_input.textChanged.connect(
            lambda: set_placeholder_value(self.amount_input),
        )
        self.msat_amount_value.textChanged.connect(
            lambda: set_placeholder_value(self.msat_amount_value),
        )
        self.expiry_input.textChanged.connect(
            lambda: set_placeholder_value(self.expiry_input),
        )

    def retranslate_ui(self):
        """Retranslate the UI elements."""
        self.create_ln_invoice_label.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'create_ln_invoice', None,
            ),
        )
        self.asset_name_label.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'asset_name', None,
            ),
        )
        self.amount_label.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'amount', None,
            ),
        )
        self.amount_input.setPlaceholderText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'amount', None,
            ),
        )
        self.expiry_label.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'expiry', None,
            ),
        )
        self.expiry_input.setPlaceholderText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'expiry_in_second', None,
            ),
        )
        self.create_button.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'create_button', None,
            ),
        )
        self.msat_amount_label.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'msat_amount_label', None,
            ),
        )
        self.msat_amount_value.setPlaceholderText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'msat_amount_label', None,
            ),
        )
        self.add_translated_item('minutes')
        self.add_translated_item('hours')
        self.add_translated_item('days')
        self.asset_balance_validation_label.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'asset_amount_validation_invoice', None,
            ),
        )

    def on_close(self):
        """Navigate to the fungibles page."""
        if self.asset_type == AssetType.CFA.value:
            self._view_model.page_navigation.collectibles_asset_page()
        else:
            self._view_model.page_navigation.fungibles_asset_page()

    def handle_button_enable(self):
        """Handles button states."""
        if not self.is_amount_valid() or not self.is_expiry_valid():
            self.create_button.setDisabled(True)
            return

        if self.asset_id == AssetType.BITCOIN.value:
            self.create_button.setDisabled(False)
            return

        if not self.is_msat_valid():
            self.create_button.setDisabled(True)
            return

        if self.is_amount_within_limit():
            self.create_button.setDisabled(False)
        else:
            self.create_button.setDisabled(True)

    def is_expiry_valid(self):
        """Returns True if the expiry field has a valid value."""
        expiry_text = self.expiry_input.text()
        return bool(expiry_text) and expiry_text != '0'

    def is_amount_valid(self):
        """Returns True if the amount field has a valid value."""
        amount_text = self.amount_input.text()
        return bool(amount_text) and amount_text != '0'

    def is_msat_valid(self):
        """Checks the validity of msat values."""
        return not self.msat_amount_value.text() or self.msat_value_is_valid()

    def is_amount_within_limit(self):
        """Checks if the amount is within the allowed limit."""
        if self.max_asset_local_amount is None:
            return True
        return int(self.amount_input.text()) <= self.max_asset_local_amount

    def get_ln_invoice(self):
        """This method get the ln invoice data"""
        if self.msat_amount_value.text() != '':
            push_msat = sat_to_msat(int(self.msat_amount_value.text()))
        else:
            invoice_detail = LnInvoiceRequestModel()
            push_msat = invoice_detail.amt_msat
        self.render_timer.start()
        expiry_time = self.get_expiry_time_in_seconds()
        if self.asset_id == AssetType.BITCOIN.value:
            self._view_model.ln_offchain_view_model.get_invoice(
                amount_msat=self.amount_input.text(), expiry=expiry_time,
            )

        else:
            self._view_model.ln_offchain_view_model.get_invoice(
                asset_id=self.asset_id, amount=self.amount_input.text(), expiry=expiry_time, amount_msat=push_msat,
            )
        self.render_timer.stop()
        self._view_model.page_navigation.receive_cfa_page(
            params=AssetDataModel(
                asset_type='create_invoice',
                close_page_navigation=self.asset_type,
                expiry_time=int(self.expiry_input.text()),
                expiry_unit=self.time_unit_combobox.currentText(),
            ),
        )

    def msat_value_change(self):
        """
        Handles changes to the MSAT input field.

        This method checks if the MSAT value is empty or zero. If it is, the create button is enabled.
        If there's a valid MSAT value, it checks if it's within allowed limits (min 3,000,000 and less than total inbound balance).
        It then updates the button state and error messages accordingly, calling `handle_button_enable` to check the overall form.
        """
        if self.asset_id == AssetType.BITCOIN.value:
            self.msat_error_label.hide()
            return

        if not self._view_model.channel_view_model.channels:
            return

        # Extract the MSAT value from the text input field
        self.amt_msat_value = extract_amount(
            self.msat_amount_value.text(), unit='',
        )

        # If MSAT is empty, hide the error label
        if not self.msat_amount_value.text():
            self.msat_error_label.hide()
        else:
            # Check if MSAT is valid
            self.msat_value_is_valid()

    def msat_value_is_valid(self):
        """
        Validates the MSAT value.

        Checks if the MSAT value is at least 3,000,000 and does not exceed the available inbound balance for the selected asset.
        Shows an error message if invalid and returns `True` if valid, otherwise `False`.
        """
        max_inbound_balance = 0
        push_amount = sat_to_msat(self.amt_msat_value)
        # Loop through all channels and sum inbound_balance_msat for matching asset_id
        for channel in self._view_model.channel_view_model.channels:
            if channel.asset_id == self.asset_id:
                if channel.is_usable and channel.ready:
                    max_inbound_balance = max(
                        channel.inbound_balance_msat, max_inbound_balance,
                    )

        # Check if MSAT is within valid bounds
        if push_amount < self.node_info.rgb_htlc_min_msat:

            self.msat_error_label.setText(
                QCoreApplication.translate(
                    IRIS_WALLET_TRANSLATIONS_CONTEXT, 'msat_lower_bound_limit', None,
                ).format(self.node_info.rgb_htlc_min_msat//1000),
            )
            self.msat_error_label.show()
            return False
        if push_amount > max_inbound_balance:
            self.msat_error_label.setText(
                QCoreApplication.translate(
                    IRIS_WALLET_TRANSLATIONS_CONTEXT, 'msat_uper_bound_limit', None,
                ).format(max_inbound_balance//1000),
            )
            self.msat_error_label.show()
            return False
        self.msat_error_label.hide()  # Hide the error label if valid
        return True

    def get_expiry_time_in_seconds(self):
        """Returns the expiry time in seconds based on user input."""
        value = extract_amount(
            self.expiry_input.text(), unit='',
        )
        unit = self.time_unit_combobox.currentText()
        unit = unit.lower()

        if unit == UnitType.MINUTES.value:
            return value * 60
        if unit == UnitType.HOURS.value:
            return value * 3600
        if unit == UnitType.DAYS.value:
            return value * 86400
        return None

    def add_translated_item(self, text: str):
        """Adds a translated item to the time unit combo box."""
        translated_text = QCoreApplication.translate(
            IRIS_WALLET_TRANSLATIONS_CONTEXT, text, None,
        )
        self.time_unit_combobox.addItem(translated_text)
        self.time_unit_combobox.setCurrentText(
            str(self.value_default_expiry_time.unit),
        )

    def get_max_asset_remote_balance(self):
        """This function gets the maximum remote balance among all online channels of the asset"""
        for channel in self._view_model.channel_view_model.channels:
            if channel.asset_id == self.asset_id:
                if channel.is_usable and channel.ready:
                    if self.max_asset_local_amount is None:
                        self.max_asset_local_amount = channel.asset_remote_amount
                        continue
                    self.max_asset_local_amount = max(
                        channel.asset_remote_amount, self.max_asset_local_amount,
                    )

    def validate_asset_amount(self):
        """This function checks the entered asset amount and shows or hides the validation error label"""

        if self.asset_id != AssetType.BITCOIN.value:
            if self.amount_input.text() != '' and self.max_asset_local_amount is not None:
                if int(self.amount_input.text()) > self.max_asset_local_amount:
                    self.asset_balance_validation_label.show()
                else:
                    self.asset_balance_validation_label.hide()
            else:
                self.asset_balance_validation_label.hide()

    def show_create_ln_invoice_loader(self):
        """Shows the loader on screen"""
        self.__loading_translucent_screen.start()
        self.__loading_translucent_screen.make_parent_disabled_during_loading(
            True,
        )

    def hide_create_ln_invoice_loader(self):
        """hides the loader on screen"""
        self.__loading_translucent_screen.stop()
        self.__loading_translucent_screen.make_parent_disabled_during_loading(
            False,
        )
