# pylint: disable=too-many-instance-attributes, too-many-statements, unused-import
"""This module contains the BtcWidget class,
 which represents the UI for Bitcoin transactions.
 """
from __future__ import annotations

from PySide6.QtCore import QCoreApplication
from PySide6.QtCore import QRect
from PySide6.QtCore import QSize
from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QFrame
from PySide6.QtWidgets import QGridLayout
from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QScrollArea
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtWidgets import QSpacerItem
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QWidget

import src.resources_rc
from accessible_constant import BITCOIN_BALANCE
from accessible_constant import BITCOIN_CLOSE_BUTTON
from accessible_constant import BITCOIN_REFRESH_BUTTON
from accessible_constant import BITCOIN_SPENDABLE_BALANCE
from accessible_constant import BITCOIN_TRANSACTION_DETAIL_FRAME
from accessible_constant import RECEIVE_BITCOIN_BUTTON
from accessible_constant import SEND_BITCOIN_BUTTON
from src.model.btc_model import TransactionListResponse
from src.model.enums.enums_model import AssetType
from src.model.enums.enums_model import TransactionStatusEnumModel
from src.model.enums.enums_model import TransferStatusEnumModel
from src.model.enums.enums_model import TransferType
from src.model.selection_page_model import SelectionPageModel
from src.model.transaction_detail_page_model import TransactionDetailPageModel
from src.utils.common_utils import network_info
from src.utils.constant import IRIS_WALLET_TRANSLATIONS_CONTEXT
from src.utils.helpers import load_stylesheet
from src.utils.render_timer import RenderTimer
from src.viewmodels.main_view_model import MainViewModel
from src.views.components.buttons import AssetTransferButton
from src.views.components.loading_screen import LoadingTranslucentScreen
from src.views.components.transaction_detail_frame import TransactionDetailFrame
from src.views.components.wallet_logo_frame import WalletLogoFrame


class BtcWidget(QWidget):
    """This class represents all the UI elements of the bitcoin page."""

    def __init__(self, view_model):
        self.render_timer = RenderTimer(task_name='BtcWidget Rendering')
        self.render_timer.start()
        super().__init__()
        self._view_model: MainViewModel = view_model
        self.network = ''
        self.__loading_translucent_screen = None
        self.setStyleSheet(load_stylesheet('views/qss/bitcoin_style.qss'))
        self.btc_grid_layout_main = QGridLayout(self)
        self.btc_grid_layout_main.setObjectName('btc_grid_layout_main')
        self.btc_vertical_spacer = QSpacerItem(
            20, 121, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding,
        )

        self.btc_grid_layout_main.addItem(self.btc_vertical_spacer, 0, 2, 1, 1)

        self.bitcoin_page = QWidget(self)
        self.bitcoin_page.setObjectName('bitcoin_page')
        self.bitcoin_page.setMinimumSize(QSize(499, 558))
        self.bitcoin_page.setMaximumSize(QSize(499, 670))
        self.btc_grid_layout = QGridLayout(self.bitcoin_page)
        self.btc_grid_layout.setSpacing(6)
        self.btc_grid_layout.setObjectName('btc_grid_layout')
        self.btc_grid_layout.setContentsMargins(1, 9, 1, -1)
        self.btc_horizontal_layout = QHBoxLayout()
        self.btc_horizontal_layout.setSpacing(6)
        self.btc_horizontal_layout.setObjectName('btc_horizontal_layout')
        self.btc_horizontal_layout.setContentsMargins(35, 5, 40, 0)
        self.bitcoin_title = QLabel(self.bitcoin_page)
        self.bitcoin_title.setObjectName('bitcoin_title')
        self.bitcoin_title.setMinimumSize(QSize(415, 63))

        self.btc_horizontal_layout.addWidget(self.bitcoin_title)
        self.refresh_button = QPushButton(self.bitcoin_page)
        self.refresh_button.setObjectName('refresh_button')
        self.refresh_button.setAccessibleName(BITCOIN_REFRESH_BUTTON)
        self.refresh_button.setCursor(
            QCursor(Qt.CursorShape.PointingHandCursor),
        )
        self.refresh_button.setMinimumSize(QSize(24, 24))

        icon = QIcon()
        icon.addFile(
            ':/assets/refresh_2x.png',
            QSize(), QIcon.Normal, QIcon.Off,
        )
        self.refresh_button.setIcon(icon)
        self.btc_horizontal_layout.addWidget(
            self.refresh_button, 0, Qt.AlignHCenter,
        )

        self.bitcoin_close_btn = QPushButton(self.bitcoin_page)
        self.bitcoin_close_btn.setObjectName('bitcoin_close_btn')
        self.bitcoin_close_btn.setAccessibleDescription(BITCOIN_CLOSE_BUTTON)
        self.bitcoin_close_btn.setCursor(
            QCursor(Qt.CursorShape.PointingHandCursor),
        )
        self.bitcoin_close_btn.setMinimumSize(QSize(40, 35))
        self.bitcoin_close_btn.setAutoFillBackground(False)

        icon = QIcon()
        icon.addFile(':/assets/x_circle.png', QSize(), QIcon.Normal, QIcon.Off)
        self.bitcoin_close_btn.setIcon(icon)
        self.bitcoin_close_btn.setIconSize(QSize(24, 24))
        self.bitcoin_close_btn.setCheckable(False)
        self.bitcoin_close_btn.setChecked(False)

        self.btc_horizontal_layout.addWidget(
            self.bitcoin_close_btn, 0, Qt.AlignHCenter,
        )
        self.btc_grid_layout.addLayout(
            self.btc_horizontal_layout, 0, 0, 1, 1,
        )

        self.line_btc = QFrame(self.bitcoin_page)
        self.line_btc.setObjectName('line_btc')

        self.line_btc.setFrameShape(QFrame.Shape.HLine)
        self.line_btc.setFrameShadow(QFrame.Shadow.Sunken)

        self.btc_grid_layout.addWidget(self.line_btc, 1, 0, 1, 1)

        self.btc_horizontal_layout_1 = QHBoxLayout()
        self.btc_horizontal_layout_1.setObjectName('btc_horizontal_layout_1')
        self.btc_horizontal_layout_1.setContentsMargins(82, 0, -1, -1)
        self.transactions = QLabel(self.bitcoin_page)
        self.transactions.setObjectName('transactions')
        self.transactions.setMinimumSize(QSize(97, 22))

        self.transactions.setMargin(0)

        self.btc_horizontal_layout_1.addWidget(self.transactions)

        self.btc_grid_layout.addLayout(
            self.btc_horizontal_layout_1, 3, 0, 1, 1,
        )

        self.btc_balance_layout = QVBoxLayout()
        self.btc_balance_layout.setObjectName('btc_balance_layout')
        self.btc_balance_layout.setContentsMargins(-1, 17, -1, -1)
        self.btc_balance_layout.setSpacing(10)
        self.balance_value = QLabel(self.bitcoin_page)
        self.balance_value.setObjectName('balance_value')

        self.btc_balance_layout.addWidget(
            self.balance_value, 0, Qt.AlignHCenter,
        )

        self.bitcoin_balance = QLabel(self.bitcoin_page)
        self.bitcoin_balance.setObjectName('bitcoin_balance')
        self.bitcoin_balance.setAccessibleDescription(BITCOIN_BALANCE)
        self.btc_balance_layout.addWidget(
            self.bitcoin_balance, 0, Qt.AlignHCenter,
        )

        self.spendable_balance_label = QLabel(self.bitcoin_page)
        self.spendable_balance_label.setObjectName('spendable_balance_label')

        self.btc_balance_layout.addWidget(
            self.spendable_balance_label, 0, Qt.AlignHCenter,
        )

        self.spendable_balance_value = QLabel(self.bitcoin_page)
        self.spendable_balance_value.setObjectName('spendable_balance_value')
        self.spendable_balance_value.setAccessibleDescription(
            BITCOIN_SPENDABLE_BALANCE,
        )
        self.btc_balance_layout.addWidget(
            self.spendable_balance_value, 0, Qt.AlignHCenter,
        )

        self.button_layout = QHBoxLayout()
        self.button_layout.setSpacing(20)
        self.button_layout.setObjectName('button_layout')
        self.button_layout.setContentsMargins(0, 22, 0, 7)
        self.btc_horizontal_spacer_17 = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum,
        )
        self.button_layout.addItem(self.btc_horizontal_spacer_17)
        self.receive_asset_btn = AssetTransferButton(
            'receive_assets', ':/assets/bottom_left.png',
        )
        self.receive_asset_btn.setAccessibleName('receive_assets')
        self.receive_asset_btn.setAccessibleName(RECEIVE_BITCOIN_BUTTON)
        self.receive_asset_btn.setCursor(
            QCursor(Qt.CursorShape.PointingHandCursor),
        )
        self.button_layout.addWidget(self.receive_asset_btn)
        self.send_asset_btn = AssetTransferButton(
            'send_assets', ':/assets/top_right.png',
        )
        self.send_asset_btn.setAccessibleName(SEND_BITCOIN_BUTTON)
        self.send_asset_btn.setCursor(
            QCursor(Qt.CursorShape.PointingHandCursor),
        )
        self.button_layout.addWidget(self.send_asset_btn)
        self.btc_horizontal_spacer_18 = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum,
        )
        self.button_layout.addItem(self.btc_horizontal_spacer_18)
        self.btc_balance_layout.addLayout(self.button_layout)
        self.btc_grid_layout.addLayout(self.btc_balance_layout, 2, 0, 1, 1)
        self.btc_horizontal_layout_11 = QHBoxLayout()
        self.btc_horizontal_layout_11.setSpacing(0)
        self.btc_horizontal_layout_11.setObjectName('btc_horizontal_layout_11')
        self.btc_horizontal_layout_11.setContentsMargins(-1, 0, -1, 25)
        self.btc_horizontal_spacer_19 = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum,
        )

        self.btc_horizontal_layout_11.addItem(self.btc_horizontal_spacer_19)

        self.btc_scroll_area = QScrollArea(self.bitcoin_page)
        self.btc_scroll_area.setObjectName('btc_scroll_area')
        self.btc_scroll_area.setMinimumSize(QSize(335, 236))
        self.btc_scroll_area.setMaximumSize(QSize(335, 236))
        self.btc_scroll_area.setLineWidth(-1)
        self.btc_scroll_area.setMidLineWidth(0)
        self.btc_scroll_area.setWidgetResizable(True)
        self.btc_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.btc_scroll_area.setWidgetResizable(True)
        self.btc_scroll_area_widget_contents = QWidget()
        self.btc_scroll_area_widget_contents.setObjectName(
            'btc_scroll_area_widget_contents',
        )
        self.btc_scroll_area_widget_contents.setGeometry(QRect(0, 0, 335, 240))
        self.btc_grid_layout_20 = QGridLayout(
            self.btc_scroll_area_widget_contents,
        )
        self.btc_grid_layout_20.setObjectName('btc_grid_layout_20')
        self.btc_grid_layout_20.setHorizontalSpacing(6)
        self.btc_grid_layout_20.setVerticalSpacing(9)
        self.btc_grid_layout_20.setContentsMargins(0, 0, 0, 0)
        self.set_transaction_detail_frame()

        self.btc_scroll_area.setWidget(self.btc_scroll_area_widget_contents)

        self.btc_horizontal_layout_11.addWidget(self.btc_scroll_area)

        self.btc_horizontal_spacer_20 = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum,
        )

        self.btc_horizontal_layout_11.addItem(self.btc_horizontal_spacer_20)

        self.btc_grid_layout.addLayout(
            self.btc_horizontal_layout_11, 4, 0, 1, 1,
        )

        self.btc_grid_layout_main.addWidget(self.bitcoin_page, 1, 2, 2, 1)

        self.btc_horizontal_pacer = QSpacerItem(
            337, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum,
        )

        self.btc_grid_layout_main.addItem(
            self.btc_horizontal_pacer, 2, 1, 1, 1,
        )

        self.btc_horizontal_spacer_2 = QSpacerItem(
            336, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum,
        )

        self.btc_grid_layout_main.addItem(
            self.btc_horizontal_spacer_2, 2, 3, 1, 1,
        )

        self.btc_vertical_spacer_2 = QSpacerItem(
            20, 120, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding,
        )

        self.btc_grid_layout_main.addItem(
            self.btc_vertical_spacer_2, 3, 2, 1, 1,
        )

        self.wallet_logo = WalletLogoFrame()

        self.btc_grid_layout_main.addWidget(self.wallet_logo, 0, 1, 1, 1)
        network_info(self)
        self.retranslate_ui()
        self.setup_ui_connection()

    def retranslate_ui(self):
        """Retranslate the UI elements."""
        self.bitcoin_text = f'{
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, "bitcoin", None
            )
        } ({self.network})'
        self.bitcoin_title.setText(self.bitcoin_text)
        self.transactions.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'transfers', None,
            ),
        )
        self.balance_value.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'total_balance', None,
            ),
        )
        self.bitcoin_balance.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'SAT', None,
            ),
        )
        self.spendable_balance_label.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'spendable_balance', None,
            ),
        )
        self.spendable_balance_value.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'SAT', None,
            ),
        )

    def setup_ui_connection(self):
        """Set up connections for UI elements."""
        self.show_bitcoin_loading_screen()
        self.receive_asset_btn.clicked.connect(
            self.select_receive_transfer_type,
        )
        self.send_asset_btn.clicked.connect(self.select_send_transfer_type)
        self.bitcoin_close_btn.clicked.connect(
            self.fungible_page_navigation,
        )
        self.refresh_button.clicked.connect(self.refresh_bitcoin_page)
        self._view_model.bitcoin_view_model.transaction_loaded.connect(
            self.set_transaction_detail_frame,
        )
        self._view_model.bitcoin_view_model.transaction_loaded.connect(
            self.set_bitcoin_balance,
        )
        self._view_model.bitcoin_view_model.get_transaction_list()
        self._view_model.bitcoin_view_model.loading_started.connect(
            self.show_bitcoin_loading_screen,
        )
        self._view_model.bitcoin_view_model.loading_finished.connect(
            self.hide_loading_screen,
        )

    def handle_asset_frame_click(self, signal_value: TransactionDetailPageModel):
        """
        Handle the click event on an asset frame.

        This method is triggered when an asset frame is clicked. It navigates to the
        Bitcoin transaction detail page, passing the provided transaction details.

        Parameters:
            signal_value (TransactionDetailPageModel): The transaction details to be passed
                                                    to the Bitcoin transaction detail page.

        Attributes:
            self (object): The instance of the class containing the view model and navigation logic.
        """
        self._view_model.page_navigation.bitcoin_transaction_detail_page(
            params=signal_value,
        )

    def refresh_bitcoin_page(self):
        """Refresh the bitcoin page."""
        self.render_timer.start()
        self._view_model.bitcoin_view_model.on_hard_refresh()

    def fungible_page_navigation(self):
        """Navigate to the fungibles asset page."""
        self._view_model.page_navigation.fungibles_asset_page()

    def receive_asset(self):
        """This method is triggered when the user clicks the 'Receive Asset' button.
        It calls the 'on_receive_bitcoin_click' method in the Bitcoin ViewModel
        to handle the logic for receiving bitcoin.
        """
        self._view_model.bitcoin_view_model.on_receive_bitcoin_click()

    def send_bitcoin(self):
        """This method is triggered when the user clicks the 'Send Bitcoin' button.
        It calls the 'on_send_bitcoin_click' method in the Bitcoin ViewModel
        to handle the logic for sending bitcoin.
        """
        self._view_model.bitcoin_view_model.on_send_bitcoin_click()

    def navigate_to_selection_page(self, callback):
        """This method is navigate to the selection page"""
        title = 'Select transfer type'
        btc_on_chain_logo_path = ':/assets/on_chain.png'
        btc_on_chain_title = TransferType.ON_CHAIN.value
        btc_off_chain_logo_path = ':/assets/off_chain.png'
        btc_off_chain_title = TransferType.LIGHTNING.value
        params = SelectionPageModel(
            title=title,
            logo_1_path=btc_on_chain_logo_path,
            logo_1_title=btc_on_chain_title,
            logo_2_path=btc_off_chain_logo_path,
            logo_2_title=btc_off_chain_title,
            asset_id=AssetType.BITCOIN.value,
            callback=callback,
            back_page_navigation=self._view_model.page_navigation.bitcoin_page,
        )
        self._view_model.page_navigation.wallet_method_page(params)

    def select_receive_transfer_type(self):
        """This method navigates the receive page"""
        self.navigate_to_selection_page(
            TransferStatusEnumModel.RECEIVE_BTC.value,
        )

    def select_send_transfer_type(self):
        """This method navigates the send asset page according to the condition"""
        self.navigate_to_selection_page(TransferStatusEnumModel.SEND_BTC.value)

    def set_bitcoin_balance(self):
        """This method updates the displayed bitcoin balance in the UI.
        It retrieves the current bitcoin balance from the Bitcoin ViewModel
        and sets the text of the 'bitcoin_balance' label to the retrieved balance.
        """
        btc_balance = self._view_model.bitcoin_view_model

        self.bitcoin_balance.setText(
            btc_balance.total_bitcoin_balance_with_suffix,
        )
        self.spendable_balance_value.setText(
            btc_balance.spendable_bitcoin_balance_with_suffix,
        )

    def set_transaction_detail_frame(self):
        """This method sets up the transaction detail frame in the UI.
        It retrieves sorted transactions from the Bitcoin ViewModel and updates the UI
        by adding a widget for each transaction.
        If there are no transactions, it shows a 'no transfer' widget.
        """
        view_model = self._view_model.bitcoin_view_model
        sorted_transactions: TransactionListResponse = view_model.transaction
        # Clear any existing items in the layout
        for i in reversed(range(self.btc_grid_layout_20.count())):
            widget_to_remove = self.btc_grid_layout_20.itemAt(i).widget()
            if widget_to_remove is not None:
                widget_to_remove.setParent(None)

        if not sorted_transactions:
            self.transaction_detail_frame = TransactionDetailFrame(
                self.btc_scroll_area_widget_contents,
            )
            self.transaction_detail_frame.close_button.hide()
            self.transaction_detail_frame.setCursor(
                QCursor(Qt.CursorShape.PointingHandCursor),
            )
            self.transactions.hide()
            no_transaction_widget = self.transaction_detail_frame.no_transaction_frame()
            self.btc_grid_layout_20.addWidget(
                no_transaction_widget, 0, 0, 1, 1,
            )
            return

        # Initialize the row index for the grid layout
        row_index = 0

        self.transactions.show()
        for transaction_detail in sorted_transactions:
            tx_id = str(transaction_detail.txid)
            amount = str(transaction_detail.amount)
            self.transaction_detail_frame = TransactionDetailFrame(
                self.btc_scroll_area_widget_contents,
                TransactionDetailPageModel(
                    tx_id=tx_id, amount=amount, confirmation_date=transaction_detail.confirmation_date,
                    confirmation_time=transaction_detail.confirmation_normal_time, transaction_status=transaction_detail.transaction_status,
                    transfer_status=transaction_detail.transfer_status,
                ),
            )
            self.transaction_detail_frame.setAccessibleName(
                BITCOIN_TRANSACTION_DETAIL_FRAME,
            )
            self.transaction_detail_frame.setCursor(
                QCursor(Qt.CursorShape.PointingHandCursor),
            )
            self.transaction_detail_frame.close_button.hide()
            transaction_date = str(transaction_detail.confirmation_date)
            transaction_time = str(transaction_detail.confirmation_normal_time)
            transfer_status = str(transaction_detail.transfer_status.value)
            transfer_amount = amount
            transaction_type = str(transaction_detail.transaction_type)
            transaction_status = str(
                transaction_detail.transaction_status.value,
            )
            if transfer_status == TransferStatusEnumModel.SENT:
                self.transaction_detail_frame.transaction_amount.setStyleSheet(
                    'color:#EB5A5A;font-weight: 600;border:none',
                )
            if transfer_status == TransferStatusEnumModel.RECEIVED:
                self.transaction_detail_frame.transaction_amount.setStyleSheet(
                    'color:#01A781;font-weight: 600;border:none',
                )
            if transaction_status == TransactionStatusEnumModel.WAITING_CONFIRMATIONS:
                self.transaction_detail_frame.transaction_amount.setStyleSheet(
                    'color:#959BAE;font-weight: 600',
                )

            self.transaction_detail_frame.transaction_time.setText(
                transaction_time,
            )
            self.transaction_detail_frame.transaction_date.setText(
                transaction_date,
            )
            if transaction_date == 'None':
                self.transaction_detail_frame.transaction_time.setStyleSheet(
                    'color:#959BAE;font-weight: 400; font-size:14px',
                )
                self.transaction_detail_frame.transaction_time.setText(
                    transaction_status,
                )
                self.transaction_detail_frame.transaction_date.setText(
                    transfer_status,
                )
            self.transaction_detail_frame.transaction_amount.setText(
                transfer_amount,
            )

            if transfer_status == TransferStatusEnumModel.SENT or TransferStatusEnumModel.RECEIVED:
                if transaction_type == TransferType.CREATEUTXOS.value:
                    self.transaction_detail_frame.transaction_type.setText(
                        TransferStatusEnumModel.INTERNAL.value,
                    )

                    self.transaction_detail_frame.transaction_type.show()
                else:
                    self.transaction_detail_frame.transaction_type.hide()

            self.transaction_detail_frame.transfer_type.hide()

            # Add the transaction detail frame to the grid layout at the current row index
            self.btc_grid_layout_20.addWidget(
                self.transaction_detail_frame, row_index, 0, 1, 1,
            )
            row_index += 1
            self.transaction_detail_frame.click_frame.connect(
                self.handle_asset_frame_click,
            )

        # Create and add the spacer item at the next available row index
        self.btc_vertical_spacer_25 = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding,
        )

        self.btc_grid_layout_20.addItem(
            self.btc_vertical_spacer_25, row_index, 0, 1, 1,
        )

    def show_bitcoin_loading_screen(self):
        """This method handled show loading screen on main asset page"""
        self.__loading_translucent_screen = LoadingTranslucentScreen(
            parent=self, description_text='Loading',
        )
        self.render_timer.start()
        self.__loading_translucent_screen.start()
        self.refresh_button.setDisabled(True)
        self.send_asset_btn.setDisabled(True)
        self.receive_asset_btn.setDisabled(True)

    def hide_loading_screen(self):
        """This method handled stop loading screen on main asset page"""
        self.__loading_translucent_screen.stop()
        self.render_timer.stop()
        self.refresh_button.setDisabled(False)
        self.send_asset_btn.setDisabled(False)
        self.receive_asset_btn.setDisabled(False)
