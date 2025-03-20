# pylint: disable=too-many-instance-attributes, too-many-statements, unused-import
"""This module contains the SendAssetWidget class,
 which represents the UI for send asset.
 """
from __future__ import annotations

from PySide6.QtCore import QCoreApplication
from PySide6.QtCore import QSize
from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor
from PySide6.QtGui import QIcon
from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import QCheckBox
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
from accessible_constant import ASSET_ADDRESS_VALIDATION_LABEL
from accessible_constant import ASSET_AMOUNT_VALIDATION
from accessible_constant import CUSTOM_CHECKBOX
from accessible_constant import ENTER_RECEIVER_ADDRESS
from accessible_constant import FAST_CHECKBOX
from accessible_constant import FEE_RATE_INPUT
from accessible_constant import MEDIUM_CHECKBOX
from accessible_constant import PAY_AMOUNT
from accessible_constant import SEND_ASSET_BUTTON
from accessible_constant import SEND_ASSET_CLOSE_BUTTON
from accessible_constant import SEND_ASSET_REFRESH_BUTTON
from accessible_constant import SLOW_CHECKBOX
from src.utils.common_utils import extract_amount
from src.utils.common_utils import set_number_validator
from src.utils.common_utils import set_placeholder_value
from src.utils.constant import IRIS_WALLET_TRANSLATIONS_CONTEXT
from src.utils.helpers import load_stylesheet
from src.viewmodels.main_view_model import MainViewModel
from src.views.components.buttons import PrimaryButton
from src.views.components.wallet_logo_frame import WalletLogoFrame


class SendAssetWidget(QWidget):
    """This class represents all the UI elements of the send asset."""

    def __init__(self,  view_model: MainViewModel, address: str):
        super().__init__()
        self.address = address
        self.spendable_amount = None
        self.pay_amount = None
        self._view_model: MainViewModel = view_model
        self.grid_layout = QGridLayout(self)
        self.grid_layout.setObjectName('grid_layout')
        self.wallet_logo = QFrame(self)
        self.wallet_logo = WalletLogoFrame()
        self.grid_layout.addWidget(self.wallet_logo, 0, 0, 1, 1)
        self.setStyleSheet(
            load_stylesheet(
                'views/qss/send_asset.qss',
            ),
        )

        self.vertical_spacer_1 = QSpacerItem(
            20, 78, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding,
        )

        self.grid_layout.addItem(self.vertical_spacer_1, 0, 1, 1, 1)

        self.horizontal_spacer_1 = QSpacerItem(
            337, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum,
        )

        self.grid_layout.addItem(self.horizontal_spacer_1, 1, 0, 1, 1)

        self.send_asset_page = QWidget(self)
        self.send_asset_page.setObjectName('send_asset_page')
        self.send_asset_page.setMaximumSize(QSize(499, 790))
        self.send_asset_widget_layout = QVBoxLayout(self.send_asset_page)
        self.send_asset_widget_layout.setObjectName('vertical_layout')
        self.send_asset_widget_layout.setContentsMargins(1, 9, 1, 35)
        self.send_asset_title_layout = QHBoxLayout()
        self.send_asset_title_layout.setSpacing(6)
        self.send_asset_title_layout.setObjectName('horizontal_layout')
        self.send_asset_title_layout.setContentsMargins(35, 5, 40, 0)
        self.asset_title = QLabel(self.send_asset_page)
        self.asset_title.setObjectName('asset_title')
        self.asset_title.setMinimumSize(QSize(415, 63))
        self.send_asset_title_layout.addWidget(self.asset_title)

        self.scan_button = QPushButton(self.send_asset_page)
        self.scan_button.setObjectName('asset_close_btn_4')
        self.scan_button.setMinimumSize(QSize(31, 24))
        self.scan_button.setCursor(
            QCursor(Qt.CursorShape.PointingHandCursor),
        )
        self.scan_button.setMaximumSize(QSize(24, 24))
        self.scan_button.setAutoFillBackground(False)
        self.scan_button.setStyleSheet(
            'background: transparent;\n'
            'border: none;',
        )
        icon = QIcon()
        icon.addFile(':/assets/scan.png', QSize(), QIcon.Normal, QIcon.Off)
        self.scan_button.setIcon(icon)
        self.scan_button.setIconSize(QSize(24, 24))
        self.scan_button.setCheckable(False)
        self.scan_button.setChecked(False)

        self.send_asset_title_layout.addWidget(self.scan_button)
        self.scan_button.hide()
        self.refresh_button = QPushButton(self.send_asset_page)
        self.refresh_button.setObjectName('refresh_button')
        self.refresh_button.setAccessibleName(SEND_ASSET_REFRESH_BUTTON)
        self.refresh_button.setCursor(
            QCursor(Qt.CursorShape.PointingHandCursor),
        )
        self.refresh_button.setMinimumSize(QSize(24, 24))
        self.refresh_button.setMaximumSize(QSize(24, 24))
        self.refresh_button.setAutoFillBackground(False)
        refresh_icon = QIcon()
        refresh_icon.addFile(
            ':/assets/refresh.png',
            QSize(), QIcon.Normal, QIcon.Off,
        )
        self.refresh_button.setIcon(refresh_icon)
        self.refresh_button.setIconSize(QSize(24, 24))
        self.send_asset_title_layout.addWidget(self.refresh_button)

        self.close_button = QPushButton(self.send_asset_page)
        self.close_button.setObjectName('asset_close_btn_3')
        self.close_button.setAccessibleName(SEND_ASSET_CLOSE_BUTTON)
        self.close_button.setCursor(
            QCursor(Qt.CursorShape.PointingHandCursor),
        )
        self.close_button.setMinimumSize(QSize(24, 24))
        self.close_button.setMaximumSize(QSize(24, 24))
        self.close_button.setAutoFillBackground(False)
        icon1 = QIcon()
        icon1.addFile(
            ':/assets/x_circle.png',
            QSize(), QIcon.Normal, QIcon.Off,
        )
        self.close_button.setIcon(icon1)
        self.close_button.setIconSize(QSize(24, 24))
        self.close_button.setCheckable(False)
        self.close_button.setChecked(False)

        self.send_asset_title_layout.addWidget(
            self.close_button, 0, Qt.AlignHCenter,
        )

        self.send_asset_widget_layout.addLayout(self.send_asset_title_layout)

        self.header_line = QFrame(self.send_asset_page)
        self.header_line.setObjectName('line_9')

        self.header_line.setFrameShape(QFrame.Shape.HLine)
        self.header_line.setFrameShadow(QFrame.Shadow.Sunken)

        self.send_asset_widget_layout.addWidget(self.header_line)

        self.balance_value_spendable = QLabel(self.send_asset_page)
        self.balance_value_spendable.setObjectName('balance_value_spendable')
        self.balance_value_spendable.setText('BALANCE VALUE')

        self.asset_balance_label_spendable = QLabel(self.send_asset_page)
        self.asset_balance_label_spendable.setObjectName('label_11')

        self.btc_balance_layout = QVBoxLayout()
        self.btc_balance_layout.setObjectName('btc_balance_layout')
        self.btc_balance_layout.setSpacing(10)
        self.btc_balance_layout.setContentsMargins(-1, 25, -1, 35)
        self.balance_value = QLabel(self.send_asset_page)
        self.balance_value.setObjectName('balance_value')

        self.asset_balance_label_total = QLabel(self.send_asset_page)
        self.asset_balance_label_total.setObjectName('label_11')

        self.btc_balance_layout.addWidget(
            self.balance_value, 0, Qt.AlignHCenter,
        )

        self.btc_balance_layout.addWidget(
            self.asset_balance_label_total, 0, Qt.AlignHCenter,
        )
        self.btc_balance_layout.addWidget(
            self.balance_value_spendable, 0, Qt.AlignHCenter,
        )
        self.btc_balance_layout.addWidget(
            self.asset_balance_label_spendable, 0, Qt.AlignHCenter,
        )
        self.send_asset_widget_layout.addLayout(self.btc_balance_layout)

        self.send_asset_details_layout = QVBoxLayout()
        self.send_asset_details_layout.setSpacing(11)
        self.send_asset_details_layout.setObjectName('verticalLayout')
        self.send_asset_details_layout.setContentsMargins(80, -1, 80, -1)
        self.pay_to_label = QLabel(self.send_asset_page)
        self.pay_to_label.setObjectName('asset_name_label_25')
        self.pay_to_label.setMinimumSize(QSize(335, 0))
        self.pay_to_label.setMaximumSize(QSize(335, 16777215))
        self.pay_to_label.setStyleSheet(
            load_stylesheet('views/qss/q_label.qss'),
        )

        self.send_asset_details_layout.addWidget(self.pay_to_label)

        self.asset_address_value = QLineEdit(self.send_asset_page)
        self.asset_address_value.setObjectName('name_of_the_asset_input_25')
        self.asset_address_value.setAccessibleName(ENTER_RECEIVER_ADDRESS)
        self.asset_address_value.setMinimumSize(QSize(335, 40))
        self.asset_address_value.setMaximumSize(QSize(335, 16777215))
        self.asset_address_value.setClearButtonEnabled(True)

        self.send_asset_details_layout.addWidget(
            self.asset_address_value, 0, Qt.AlignHCenter,
        )
        self.asset_address_validation_label = QLabel(self)
        self.asset_address_validation_label.setObjectName(
            'address_validation_label',
        )
        self.asset_address_validation_label.setAccessibleDescription(
            ASSET_ADDRESS_VALIDATION_LABEL,
        )
        self.asset_address_validation_label.setMinimumSize(QSize(335, 0))
        self.asset_address_validation_label.setMaximumSize(
            QSize(335, 16777215),
        )
        self.asset_address_validation_label.setWordWrap(True)
        self.send_asset_details_layout.addWidget(
            self.asset_address_validation_label, 0, Qt.AlignHCenter,
        )
        self.asset_address_validation_label.setStyleSheet(
            load_stylesheet('views/qss/q_label.qss'),
        )
        self.asset_address_validation_label.hide()

        self.total_supply_label = QLabel(self.send_asset_page)
        self.total_supply_label.setObjectName('total_supply_label')
        self.total_supply_label.setMinimumSize(QSize(335, 0))
        self.total_supply_label.setMaximumSize(QSize(335, 16777215))
        self.total_supply_label.setStyleSheet(
            load_stylesheet('views/qss/q_label.qss'),
        )

        self.send_asset_details_layout.addWidget(self.total_supply_label)

        self.asset_amount_value = QLineEdit(self.send_asset_page)
        self.asset_amount_value.setObjectName('amount_input_25')
        self.asset_amount_value.setAccessibleName(PAY_AMOUNT)
        set_number_validator(self.asset_amount_value)

        self.asset_amount_value.setMinimumSize(QSize(335, 40))
        self.asset_amount_value.setMaximumSize(QSize(335, 16777215))
        self.asset_amount_value.setClearButtonEnabled(True)
        self.send_asset_details_layout.addWidget(
            self.asset_amount_value, 0, Qt.AlignHCenter,
        )

        self.asset_amount_validation = QLabel(self.send_asset_page)
        self.asset_amount_validation.setObjectName('asset_amount_validation')
        self.asset_amount_validation.setAccessibleDescription(
            ASSET_AMOUNT_VALIDATION,
        )
        self.asset_amount_validation.setMinimumSize(QSize(335, 0))
        self.asset_amount_validation.setMaximumSize(QSize(335, 16777215))
        self.asset_amount_validation.setStyleSheet(
            load_stylesheet('views/qss/q_label.qss'),
        )
        self.asset_amount_validation.setWordWrap(True)
        self.send_asset_details_layout.addWidget(self.asset_amount_validation)
        self.asset_amount_validation.hide()

        self.fee_rate_checkbox_layout = QHBoxLayout()
        self.fee_rate_checkbox_layout.setObjectName('horizontalLayout_2')
        self.fee_rate_checkbox_layout.setContentsMargins(1, 4, 1, 4)
        self.txn_label = QLabel(self.send_asset_page)
        self.txn_label.setObjectName('txn_label')
        self.slow_checkbox = QCheckBox(self.send_asset_page)
        self.slow_checkbox.setObjectName('slow_checkBox')
        self.slow_checkbox.setAccessibleName(SLOW_CHECKBOX)
        self.slow_checkbox.setAutoExclusive(True)

        self.fee_rate_checkbox_layout.addWidget(self.slow_checkbox)
        self.medium_checkbox = QCheckBox(self.send_asset_page)
        self.medium_checkbox.setObjectName('medium_checkBox')
        self.medium_checkbox.setAccessibleName(MEDIUM_CHECKBOX)
        self.medium_checkbox.setAutoExclusive(True)

        self.fee_rate_checkbox_layout.addWidget(self.medium_checkbox)

        self.fast_checkbox = QCheckBox(self.send_asset_page)
        self.fast_checkbox.setObjectName('fast_checkBox')
        self.fast_checkbox.setAccessibleName(FAST_CHECKBOX)
        self.fast_checkbox.setAutoExclusive(True)

        self.fee_rate_checkbox_layout.addWidget(self.fast_checkbox)

        self.custom_checkbox = QCheckBox(self.send_asset_page)
        self.custom_checkbox.setObjectName('custom_checkBox')
        self.custom_checkbox.setAccessibleName(CUSTOM_CHECKBOX)
        self.custom_checkbox.setCheckState(Qt.Checked)
        self.custom_checkbox.clicked.connect(
            self.enable_fee_rate_line_edit,
        )
        self.custom_checkbox.setAutoExclusive(True)

        self.fee_rate_checkbox_layout.addWidget(self.custom_checkbox)

        self.send_asset_details_layout.addWidget(self.txn_label)
        self.send_asset_details_layout.addLayout(self.fee_rate_checkbox_layout)

        self.fee_rate_label = QLabel(self.send_asset_page)
        self.fee_rate_label.setObjectName('fee_rate_label')
        self.fee_rate_label.setMinimumSize(QSize(335, 0))
        self.fee_rate_label.setMaximumSize(QSize(335, 16777215))
        self.fee_rate_label.setStyleSheet(
            load_stylesheet('views/qss/q_label.qss'),
        )

        self.send_asset_details_layout.addWidget(self.fee_rate_label)

        self.fee_rate_value = QLineEdit(self.send_asset_page)
        self.fee_rate_value.setObjectName('amount_input_25')
        self.fee_rate_value.setAccessibleName(FEE_RATE_INPUT)
        self.fee_rate_value.setValidator(QIntValidator())
        self.fee_rate_value.setMinimumSize(QSize(335, 40))
        self.fee_rate_value.setMaximumSize(QSize(335, 16777215))
        self.fee_rate_value.setClearButtonEnabled(False)

        self.send_asset_details_layout.addWidget(
            self.fee_rate_value, 0, Qt.AlignHCenter,
        )

        self.estimate_fee_error_label = QLabel(self.send_asset_page)
        self.estimate_fee_error_label.setObjectName(
            'estimation_fee_error_label',
        )
        self.estimate_fee_error_label.setWordWrap(True)
        self.estimate_fee_error_label.hide()

        self.send_asset_details_layout.addWidget(self.estimate_fee_error_label)

        self.spendable_balance_validation = QLabel(self.send_asset_page)
        self.spendable_balance_validation.setObjectName(
            'spendable_balance_validation',
        )
        self.spendable_balance_validation.setStyleSheet(
            load_stylesheet('views/qss/q_label.qss'),
        )
        self.spendable_balance_validation.setMinimumSize(QSize(335, 0))
        self.spendable_balance_validation.setMaximumSize(QSize(335, 16777215))
        self.spendable_balance_validation.setWordWrap(True)
        self.send_asset_details_layout.addWidget(
            self.spendable_balance_validation,
        )
        self.spendable_balance_validation.hide()
        self.vertical_spacer_3 = QSpacerItem(
            20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred,
        )

        self.send_asset_details_layout.addItem(self.vertical_spacer_3)

        self.send_asset_widget_layout.addLayout(self.send_asset_details_layout)

        self.footer_line = QFrame(self.send_asset_page)
        self.footer_line.setObjectName('line_8')
        self.footer_line.setFrameShape(QFrame.Shape.HLine)
        self.footer_line.setFrameShadow(QFrame.Shadow.Sunken)

        self.send_asset_widget_layout.addWidget(self.footer_line)

        self.vertical_spacer_4 = QSpacerItem(
            20, 30, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred,
        )

        self.send_asset_widget_layout.addItem(self.vertical_spacer_4)

        self.send_btn = PrimaryButton()
        self.send_btn.setAccessibleName(SEND_ASSET_BUTTON)
        self.send_btn.setMinimumSize(QSize(402, 40))
        self.send_btn.setMaximumSize(QSize(402, 16777215))

        self.send_asset_widget_layout.addWidget(
            self.send_btn, 0, Qt.AlignCenter,
        )

        self.grid_layout.addWidget(self.send_asset_page, 1, 1, 1, 1)

        self.horizontal_spacer_send = QSpacerItem(
            336, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum,
        )

        self.grid_layout.addItem(self.horizontal_spacer_send, 1, 2, 1, 1)

        self.vertical_spacer_2 = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding,
        )

        self.grid_layout.addItem(self.vertical_spacer_2, 2, 1, 1, 1)
        self.retranslate_ui()

        # signal connections
        self.slow_checkbox.clicked.connect(
            lambda: self.disable_fee_rate_line_edit(
                self.slow_checkbox.objectName(),
            ),
        )
        self.fast_checkbox.clicked.connect(
            lambda: self.disable_fee_rate_line_edit(
                self.fast_checkbox.objectName(),
            ),
        )
        self.medium_checkbox.clicked.connect(
            lambda: self.disable_fee_rate_line_edit(
                self.medium_checkbox.objectName(),
            ),
        )

        self._view_model.estimate_fee_view_model.fee_estimation_success.connect(
            self.set_fee_rate,
        )
        self._view_model.estimate_fee_view_model.fee_estimation_error.connect(
            self.show_fee_estimation_error,
        )
        self.asset_amount_value.textChanged.connect(
            self.validate_amount,
        )
        self.asset_amount_value.textChanged.connect(
            lambda: set_placeholder_value(self.asset_amount_value),
        )
        self.fee_rate_value.textChanged.connect(
            lambda: set_placeholder_value(self.fee_rate_value),
        )

    def retranslate_ui(self):
        """Retranslate the UI elements."""
        self.asset_title.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'send', None,
            ),
        )
        self.balance_value.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'total_balance', None,
            ),
        )
        self.pay_to_label.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'pay_to', None,
            ),
        )
        self.asset_address_value.setPlaceholderText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, self.address, None,
            ),
        )
        self.total_supply_label.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'amount_to_pay', None,
            ),
        )
        self.fee_rate_label.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'fee_rate', None,
            ),
        )
        self.fee_rate_value.setPlaceholderText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, '0', None,
            ),
        )
        self.asset_amount_value.setPlaceholderText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, '0', None,
            ),
        )
        self.asset_amount_validation.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'asset_amount_validation',
            ),
        )
        self.send_btn.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'send', None,
            ),
        )
        self.asset_balance_label_spendable.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, '0 SATS', None,
            ),
        )
        self.balance_value_spendable.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'spendable_balance', None,
            ),
        )
        self.spendable_balance_validation.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'spendable_balance_validation', None,
            ),
        )
        self.txn_label.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'transaction_fees', None,
            ),
        )

        self.slow_checkbox.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'slow', None,
            ),
        )

        self.medium_checkbox.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'medium', None,
            ),
        )

        self.fast_checkbox.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'fast', None,
            ),
        )

        self.custom_checkbox.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'custom', None,
            ),
        )

        self.estimate_fee_error_label.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'estimation_error',
            ),
        )

        self.slow_checkbox.setToolTip(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'slow_transaction_speed',
            ),
        )

        self.medium_checkbox.setToolTip(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'medium_transaction_speed',
            ),
        )

        self.fast_checkbox.setToolTip(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'fast_transaction_speed',
            ),
        )

    def disable_fee_rate_line_edit(self, txn_speed):
        """Disables the fee rate input field and triggers fee rate estimation based on the selected transaction speed."""
        self.fee_rate_value.setReadOnly(True)
        self.get_transaction_fee_rate(txn_speed)

    def enable_fee_rate_line_edit(self):
        """Enables the fee rate input field, sets the focus, and positions the cursor at the end of the text in the fee rate field."""
        self.fee_rate_value.setReadOnly(False)
        self.fee_rate_value.setFocus()
        self.fee_rate_value.setCursorPosition(len(self.fee_rate_value.text()))

    def get_transaction_fee_rate(self, txn_fee_speed):
        """
        Calls the fee estimation function for the selected transaction speed
        (slow, medium, or fast) based on the corresponding checkbox.
        """

        if txn_fee_speed == self.slow_checkbox.objectName():
            self._view_model.estimate_fee_view_model.get_fee_rate(
                self.slow_checkbox.objectName(),
            )

        if txn_fee_speed == self.medium_checkbox.objectName():
            self._view_model.estimate_fee_view_model.get_fee_rate(
                self.medium_checkbox.objectName(),
            )

        if txn_fee_speed == self.fast_checkbox.objectName():
            self._view_model.estimate_fee_view_model.get_fee_rate(
                self.fast_checkbox.objectName(),
            )

    def set_fee_rate(self, fee_rate: float):
        """Sets the fee rate in the input field as an integer, removing decimal places entirely."""
        fee_rate_int = int(fee_rate)
        self.fee_rate_value.setText(str(fee_rate_int))

    def show_fee_estimation_error(self):
        """
        Displays an error message for fee estimation and switches to custom fee input mode.
        Hides the speed checkboxes and enables fee rate input.
        """
        self.estimate_fee_error_label.show()
        self.fast_checkbox.hide()
        self.slow_checkbox.hide()
        self.medium_checkbox.hide()
        self.layout().update()
        self.custom_checkbox.setChecked(True)
        self.fee_rate_value.setReadOnly(False)
        self.fee_rate_value.setCursorPosition(-1)

    def validate_amount(self):
        """
        Validates that the pay amount does not exceed the spendable balance.

        This method compares the user-specified pay amount with the available spendable balance.
        If the pay amount exceeds the spendable amount, an error message is displayed, and the
        layout is adjusted accordingly. If the pay amount is valid, the error message is hidden,
        and the layout is reset.

        Behavior:
        - Shows `asset_amount_validation` error if pay amount > spendable balance.
        - Adjusts `send_asset_page` layout size based on validation result.
        """

        try:
            self.spendable_amount = extract_amount(
                self.asset_balance_label_spendable.text(),
            )
            self.pay_amount = extract_amount(
                self.asset_amount_value.text(), unit='',
            )

            # Perform validation by comparing pay amount and spendable balance.
            if self.pay_amount > self.spendable_amount:
                self.asset_amount_validation.show()
                self.send_btn.setDisabled(True)
            else:
                self.asset_amount_validation.hide()
                self.send_btn.setDisabled(False)

        except ValueError:
            # Handle invalid integer conversion, typically due to non-numeric input.
            self.send_btn.setDisabled(True)
            self.asset_amount_validation.show()
