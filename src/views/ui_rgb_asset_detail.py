# pylint: disable=too-many-instance-attributes, too-many-statements
"""This module contains the RGBAssetDetailWidget class,
 which represents the UI for RGB asset detail.
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
from PySide6.QtWidgets import QPlainTextEdit
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QScrollArea
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtWidgets import QSpacerItem
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QWidget

from accessible_constant import ASSET_CLOSE_BUTTON
from accessible_constant import ASSET_ID_COPY_BUTTON
from accessible_constant import ASSET_LIGHTNING_SPENDABLE_BALANCE
from accessible_constant import ASSET_LIGHTNING_TOTAL_BALANCE
from accessible_constant import ASSET_ON_CHAIN_SPENDABLE_BALANCE
from accessible_constant import ASSET_ON_CHAIN_TOTAL_BALANCE
from accessible_constant import ASSET_RECEIVE_BUTTON
from accessible_constant import ASSET_REFRESH_BUTTON
from accessible_constant import ASSET_SEND_BUTTON
from accessible_constant import RGB_TRANSACTION_DETAIL_LIGHTNING_FRAME
from accessible_constant import RGB_TRANSACTION_DETAIL_ON_CHAIN_FRAME
from accessible_constant import TRANSACTION_DETAIL_CLOSE_BUTTON
from src.data.repository.setting_repository import SettingRepository
from src.model.enums.enums_model import AssetType
from src.model.enums.enums_model import NetworkEnumModel
from src.model.enums.enums_model import PaymentStatus
from src.model.enums.enums_model import TransactionStatusEnumModel
from src.model.enums.enums_model import TransferOptionModel
from src.model.enums.enums_model import TransferStatusEnumModel
from src.model.enums.enums_model import TransferType
from src.model.rgb_model import ListOnAndOffChainTransfersWithBalance
from src.model.rgb_model import RgbAssetPageLoadModel
from src.model.selection_page_model import AssetDataModel
from src.model.selection_page_model import SelectionPageModel
from src.model.transaction_detail_page_model import TransactionDetailPageModel
from src.utils.common_utils import copy_text
from src.utils.constant import IRIS_WALLET_TRANSLATIONS_CONTEXT
from src.utils.helpers import load_stylesheet
from src.utils.render_timer import RenderTimer
from src.utils.rgb_asset_helpers import handle_img_path
from src.viewmodels.main_view_model import MainViewModel
from src.views.components.buttons import AssetTransferButton
from src.views.components.confirmation_dialog import ConfirmationDialog
from src.views.components.loading_screen import LoadingTranslucentScreen
from src.views.components.transaction_detail_frame import TransactionDetailFrame
from src.views.components.wallet_logo_frame import WalletLogoFrame


class RGBAssetDetailWidget(QWidget):
    """This class represents the UI for RGB asset details."""

    def __init__(self, view_model: MainViewModel, params: RgbAssetPageLoadModel):
        """Initialize the RGBAssetDetailWidget class."""
        super().__init__()
        self.render_timer = RenderTimer(
            task_name='RGBAssetDetailWidget Rendering',
        )
        self.render_timer.start()
        self.setStyleSheet(
            load_stylesheet(
                'views/qss/rgb_asset_detail_style.qss',
            ),
        )
        self.asset_name = None
        self.transaction_date = None
        self.transaction_time = None
        self.transfer_status = None
        self.transfer_amount = None
        self.transaction_type = None
        self.transaction_status = None
        self.vertical_spacer_3 = None
        self.scroll_area_widget_layout = None
        self.label_asset_name = None
        self.filtered_lightning_transactions = None
        self.on_chain_icon = None
        self.lightning_icon = None
        self.transaction_detail_frame = None
        self.network: NetworkEnumModel = SettingRepository.get_wallet_network()
        self.bitcoin_img_path = {
            NetworkEnumModel.MAINNET.value: ':/assets/bitcoin.png',
            NetworkEnumModel.REGTEST.value: ':/assets/regtest_bitcoin.png',
            NetworkEnumModel.TESTNET.value: ':/assets/testnet_bitcoin.png',
            NetworkEnumModel.TESTNET4.value: ':/assets/testnet_bitcoin.png',
        }
        self.__loading_translucent_screen = LoadingTranslucentScreen(self)
        self.asset_type = params.asset_type
        self.image_path = params.image_path
        self._view_model: MainViewModel = view_model
        self.grid_layout_2 = QGridLayout(self)
        self.grid_layout_2.setObjectName('gridLayout_2')
        self.horizontal_spacer_3 = QSpacerItem(
            336, 14, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum,
        )
        self.grid_layout_2.addItem(self.horizontal_spacer_3, 1, 0, 1, 1)
        self.vertical_layout_2 = QVBoxLayout()
        self.vertical_layout_2.setObjectName('vertical_layout_2')
        self.vertical_spacer_2 = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding,
        )
        self.vertical_layout_2.addItem(self.vertical_spacer_2)
        self.rgb_asset_detail_widget = QWidget(self)
        self.rgb_asset_detail_widget.setObjectName(
            'rgb_asset_detail_widget',
        )
        self.rgb_asset_detail_widget.setMinimumSize(QSize(499, 770))
        self.rgb_asset_detail_widget_layout = QGridLayout(
            self.rgb_asset_detail_widget,
        )
        self.rgb_asset_detail_widget_layout.setObjectName('gridLayout')
        self.rgb_asset_detail_widget_layout.setVerticalSpacing(0)
        self.rgb_asset_detail_widget_layout.setContentsMargins(1, 0, 1, 9)
        self.top_line = QFrame(self.rgb_asset_detail_widget)
        self.top_line.setObjectName('top_line')
        self.top_line.setFrameShape(QFrame.Shape.HLine)
        self.top_line.setFrameShadow(QFrame.Shadow.Sunken)
        self.rgb_asset_detail_widget_layout.addWidget(
            self.top_line, 1, 0, 1, 1,
        )
        self.send_receive_button_layout = QHBoxLayout()
        self.send_receive_button_layout.setSpacing(18)
        self.send_receive_button_layout.setObjectName('horizontal_layout_11')
        self.send_receive_button_layout.setContentsMargins(0, 20, 0, -1)
        self.horizontal_spacer = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum,
        )
        self.send_receive_button_layout.addItem(self.horizontal_spacer)
        self.receive_rgb_asset = AssetTransferButton(
            'receive_assets', ':/assets/bottom_left.png',
        )
        self.receive_rgb_asset.setAccessibleName(ASSET_RECEIVE_BUTTON)
        self.receive_rgb_asset.setCursor(
            QCursor(Qt.CursorShape.PointingHandCursor),
        )
        self.send_receive_button_layout.addWidget(self.receive_rgb_asset)
        self.send_asset = AssetTransferButton(
            'send_assets', ':/assets/top_right.png',
        )
        self.send_asset.setAccessibleName(ASSET_SEND_BUTTON)
        self.send_asset.setCursor(
            QCursor(Qt.CursorShape.PointingHandCursor),
        )
        self.send_receive_button_layout.addWidget(self.send_asset)
        self.horizontal_spacer_2 = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum,
        )
        self.send_receive_button_layout.addItem(self.horizontal_spacer_2)
        self.rgb_asset_detail_widget_layout.addLayout(
            self.send_receive_button_layout, 4, 0, 1, 1,
        )
        self.asset_image_layout = QVBoxLayout()
        self.asset_image_layout.setSpacing(0)
        self.asset_image_layout.setObjectName('vertical_layout_7')
        self.asset_image_layout.setContentsMargins(-1, 15, -1, 18)
        self.rgb_asset_detail_widget_layout.addLayout(
            self.asset_image_layout, 2, 0, 1, 1,
        )
        self.vertical_layout_8 = QVBoxLayout()
        self.vertical_layout_8.setSpacing(0)
        self.vertical_layout_8.setObjectName('vertical_layout_8')
        self.vertical_layout_8.setContentsMargins(0, 9, 1, 12)
        self.transactions_label = QLabel(self.rgb_asset_detail_widget)
        self.transactions_label.setObjectName('transactions_label')
        self.transactions_label.setMaximumSize(QSize(97, 30))
        self.transactions_label.setMargin(0)
        self.vertical_layout_8.addWidget(self.transactions_label)
        self.scroll_area = QScrollArea(self.rgb_asset_detail_widget)
        self.scroll_area.setObjectName('scroll_area')
        self.scroll_area.setMinimumSize(QSize(350, 74))
        self.scroll_area.setMaximumSize(QSize(335, 74))
        self.scroll_area.setLineWidth(-1)
        self.scroll_area.setMidLineWidth(0)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area_widget_contents = QWidget()
        self.scroll_area_widget_contents.setObjectName(
            'scroll_area_widget_contents',
        )
        self.scroll_area_widget_contents.setGeometry(QRect(0, 0, 350, 240))
        self.scroll_area_widget_layout = QGridLayout(
            self.scroll_area_widget_contents,
        )
        self.scroll_area_widget_layout.setObjectName('gridLayout_20')
        self.scroll_area_widget_layout.setHorizontalSpacing(6)
        self.scroll_area_widget_layout.setContentsMargins(0, 0, 0, 0)
        self.horizontal_layout_balance_frames = QHBoxLayout()
        self.asset_balance_frame = QFrame(self.rgb_asset_detail_widget)
        self.scroll_area.setWidget(self.scroll_area_widget_contents)
        self.vertical_layout_8.addWidget(self.scroll_area)
        self.rgb_asset_detail_widget_layout.addLayout(
            self.vertical_layout_8, 5, 0, 1, 1, Qt.AlignCenter,
        )
        self.vertical_layout = QVBoxLayout()
        self.vertical_layout.setSpacing(20)
        self.vertical_layout.setObjectName('vertical_layout')
        self.asset_id_frame = QFrame(self.rgb_asset_detail_widget)
        self.asset_id_frame.setObjectName('frame_5')
        self.asset_id_frame.setMinimumSize(QSize(335, 86))
        self.asset_id_frame.setMaximumSize(QSize(335, 86))
        self.asset_id_frame.setFrameShape(QFrame.StyledPanel)
        self.asset_id_frame.setFrameShadow(QFrame.Raised)
        self.asset_id_frame_layout = QGridLayout(self.asset_id_frame)
        self.asset_id_frame_layout.setObjectName('gridLayout_23')
        self.asset_id_frame_layout.setVerticalSpacing(3)
        self.asset_id_frame_layout.setContentsMargins(15, 11, 15, 12)
        self.asset_id_label = QLabel(self.asset_id_frame)
        self.asset_id_label.setObjectName('asset_id_label')
        self.asset_id_label.setMinimumSize(QSize(83, 20))
        self.asset_id_frame_layout.addWidget(
            self.asset_id_label, 0, 0, 1, 1, Qt.AlignLeft,
        )
        self.asset_id_detail = QPlainTextEdit(self.asset_id_frame)
        self.asset_id_detail.setObjectName('asset_id_detail')
        self.asset_id_detail.setMinimumSize(QSize(289, 38))
        self.asset_id_detail.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.asset_id_detail.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff,
        )
        self.asset_id_detail.setTextInteractionFlags(
            Qt.TextSelectableByKeyboard | Qt.TextSelectableByMouse,
        )
        self.asset_id_frame_layout.addWidget(self.asset_id_detail, 1, 0, 1, 1)
        self.copy_button = QPushButton(self.asset_id_frame)
        self.copy_button.setObjectName('copy_button')
        self.copy_button.setAccessibleName(ASSET_ID_COPY_BUTTON)
        self.copy_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.copy_button.setStyleSheet('border:none;')
        icon2 = QIcon()
        icon2.addFile(':/assets/copy.png', QSize(), QIcon.Normal, QIcon.Off)
        self.copy_button.setIcon(icon2)
        self.asset_id_frame_layout.addWidget(self.copy_button, 0, 1, 1, 1)
        self.vertical_layout.addWidget(self.asset_id_frame, 0, Qt.AlignHCenter)
        self.asset_balance_frame.setObjectName('frame_4')
        self.asset_balance_frame.setMinimumSize(QSize(158, 66))
        self.asset_balance_frame.setFrameShape(QFrame.StyledPanel)
        self.asset_balance_frame.setFrameShadow(QFrame.Raised)
        self.asset_balance_frame_layout = QGridLayout(self.asset_balance_frame)
        self.asset_balance_frame_layout.setObjectName('gridLayout_8')
        self.asset_balance_frame_layout.setContentsMargins(15, -1, 15, 9)
        self.asset_balance_label = QLabel(self.asset_balance_frame)
        self.asset_balance_label.setObjectName('asset_balance_label')
        self.asset_balance_label.setMinimumSize(QSize(83, 20))
        self.asset_balance_frame_layout.addWidget(
            self.asset_balance_label, 0, 0, 1, 1, Qt.AlignLeft,
        )
        self.asset_total_amount_label = QLabel(self.asset_balance_frame)
        self.asset_total_amount_label.setObjectName('asset_total_amount_label')
        self.asset_balance_frame_layout.addWidget(
            self.asset_total_amount_label, 1, 0, 1, 1, Qt.AlignLeft,
        )
        self.asset_total_balance = QLabel(self.asset_balance_frame)
        self.asset_total_balance.setObjectName('asset_total_balance')
        self.asset_total_balance.setAccessibleDescription(
            ASSET_ON_CHAIN_TOTAL_BALANCE,
        )
        self.asset_total_balance.setMinimumSize(QSize(60, 18))
        self.asset_balance_frame_layout.addWidget(
            self.asset_total_balance, 2, 0, 1, 1, Qt.AlignLeft,
        )
        self.asset_spendable_amount_label = QLabel(self.asset_balance_frame)
        self.asset_spendable_amount_label.setObjectName(
            'asset_spendable_amount_label',
        )
        self.asset_balance_frame_layout.addWidget(
            self.asset_spendable_amount_label, 3, 0, 1, 1, Qt.AlignLeft,
        )
        self.asset_spendable_amount = QLabel(self.asset_balance_frame)
        self.asset_spendable_amount.setObjectName('asset_spendable_amount')
        self.asset_spendable_amount.setAccessibleDescription(
            ASSET_ON_CHAIN_SPENDABLE_BALANCE,
        )
        self.asset_balance_frame_layout.addWidget(
            self.asset_spendable_amount, 4, 0, 1, 1, Qt.AlignLeft,
        )
        self.horizontal_layout_balance_frames.addWidget(
            self.asset_balance_frame, 0, Qt.AlignRight,
        )
        self.vertical_layout_lightning_frame = QVBoxLayout()
        self.vertical_layout_lightning_frame.setContentsMargins(15, -1, 15, 9)
        self.lightning_balance_frame = QFrame(self.rgb_asset_detail_widget)
        self.lightning_balance_frame.setObjectName('frame_4')
        self.lightning_balance_frame.setMinimumSize(QSize(158, 66))
        self.lightning_balance_frame.setLayout(
            self.vertical_layout_lightning_frame,
        )
        self.lightning_balance_label = QLabel(self.lightning_balance_frame)
        self.lightning_balance_label.setObjectName('lightning_balance_label')
        self.vertical_layout_lightning_frame.addWidget(
            self.lightning_balance_label,
        )
        self.lightning_total_balance_label = QLabel(
            self.lightning_balance_frame,
        )
        self.lightning_total_balance_label.setObjectName(
            'lightning_total_balance_label',
        )
        self.vertical_layout_lightning_frame.addWidget(
            self.lightning_total_balance_label,
        )
        self.lightning_total_balance = QLabel(self.lightning_balance_frame)
        self.lightning_total_balance.setObjectName('lightning_total_balance')
        self.lightning_total_balance.setAccessibleDescription(
            ASSET_LIGHTNING_TOTAL_BALANCE,
        )
        self.vertical_layout_lightning_frame.addWidget(
            self.lightning_total_balance,
        )
        self.lightning_spendable_balance_label = QLabel(
            self.lightning_balance_frame,
        )
        self.lightning_spendable_balance_label.setObjectName(
            'lightning_spendable_balance_label',
        )
        self.vertical_layout_lightning_frame.addWidget(
            self.lightning_spendable_balance_label,
        )
        self.lightning_spendable_balance = QLabel(self.lightning_balance_frame)
        self.lightning_spendable_balance.setObjectName(
            'lightning_spendable_balance',
        )
        self.lightning_spendable_balance.setAccessibleDescription(
            ASSET_LIGHTNING_SPENDABLE_BALANCE,
        )
        self.vertical_layout_lightning_frame.addWidget(
            self.lightning_spendable_balance,
        )
        self.horizontal_layout_balance_frames.addWidget(
            self.lightning_balance_frame, 0, Qt.AlignLeft,
        )
        self.vertical_layout.addLayout(self.horizontal_layout_balance_frames)
        self.rgb_asset_detail_widget_layout.addLayout(
            self.vertical_layout, 3, 0, 1, 1,
        )
        self.rgb_asset_detail_title_layout = QHBoxLayout()
        self.rgb_asset_detail_title_layout.setSpacing(0)
        self.rgb_asset_detail_title_layout.setObjectName('horizontal_layout_1')
        self.rgb_asset_detail_title_layout.setContentsMargins(35, 0, 40, 5)
        self.widget_title_asset_name = QLabel(
            self.rgb_asset_detail_widget,
        )
        self.widget_title_asset_name.setObjectName(
            'set_wallet_password_label_3',
        )
        self.widget_title_asset_name.setMinimumSize(QSize(415, 0))
        self.widget_title_asset_name.setMaximumSize(QSize(16777215, 30))

        self.rgb_asset_detail_title_layout.addWidget(
            self.widget_title_asset_name,
        )
        self.asset_refresh_button = QPushButton(
            self.rgb_asset_detail_widget,
        )
        self.asset_refresh_button.setCursor(
            QCursor(Qt.CursorShape.PointingHandCursor),
        )
        self.asset_refresh_button.setObjectName('refresh_button')
        self.asset_refresh_button.setAccessibleName(ASSET_REFRESH_BUTTON)
        self.asset_refresh_button.setMinimumSize(QSize(50, 65))
        icon = QIcon()
        icon.addFile(
            ':/assets/refresh_2x.png',
            QSize(), QIcon.Normal, QIcon.Off,
        )
        self.asset_refresh_button.setIcon(icon)
        self.rgb_asset_detail_title_layout.addWidget(
            self.asset_refresh_button, 0, Qt.AlignHCenter,
        )
        self.close_btn = QPushButton(self.rgb_asset_detail_widget)
        self.close_btn.setObjectName('close_btn')
        self.close_btn.setAccessibleName(ASSET_CLOSE_BUTTON)
        self.close_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.close_btn.setMinimumSize(QSize(24, 24))
        self.close_btn.setMaximumSize(QSize(50, 65))
        self.close_btn.setAutoFillBackground(False)
        icon3 = QIcon()
        icon3.addFile(
            ':/assets/x_circle.png',
            QSize(), QIcon.Normal, QIcon.Off,
        )
        self.close_btn.setIcon(icon3)
        self.close_btn.setIconSize(QSize(24, 24))
        self.close_btn.setCheckable(False)
        self.close_btn.setChecked(False)
        self.rgb_asset_detail_title_layout.addWidget(
            self.close_btn, 0, Qt.AlignHCenter,
        )
        self.rgb_asset_detail_widget_layout.addLayout(
            self.rgb_asset_detail_title_layout, 0, 0, 1, 1,
        )
        self.vertical_layout_2.addWidget(self.rgb_asset_detail_widget)

        self.vertical_spacer = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding,
        )
        self.vertical_layout_2.addItem(self.vertical_spacer)
        self.grid_layout_2.addLayout(self.vertical_layout_2, 0, 1, 3, 1)
        self.horizontal_spacer_4 = QSpacerItem(
            335, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum,
        )
        self.grid_layout_2.addItem(self.horizontal_spacer_4, 2, 2, 1, 1)
        self.wallet_logo_frame = WalletLogoFrame(self)
        self.grid_layout_2.addWidget(self.wallet_logo_frame, 0, 0, 1, 1)
        self.setup_ui_connection()
        self.retranslate_ui()

    def retranslate_ui(self):
        """Retranslate the UI elements."""
        self.transactions_label.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'transfers', None,
            ),
        )
        self.asset_id_label.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'asset_id', None,
            ),
        )
        self.asset_balance_label.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'on_chain_balance', None,
            ),
        )
        self.asset_total_amount_label.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'total', None,
            ),
        )
        self.asset_spendable_amount_label.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'spendable_bal', None,
            ),
        )
        self.lightning_spendable_balance_label.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'spendable_bal', None,
            ),
        )
        self.lightning_total_balance_label.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'total', None,
            ),
        )
        self.lightning_balance_label.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'lightning_balance',
            ),
        )

    def navigate_to_selection_page(self, navigation):
        """This method is navigate to the selection page"""
        title = 'Select transfer type'
        rgb_on_chain_logo_path = ':/assets/on_chain.png'
        rgb_on_chain_logo_title = TransferType.ON_CHAIN.value
        rgb_off_chain_logo_path = ':/assets/off_chain.png'
        rgb_off_chain_logo_title = TransferType.LIGHTNING.value
        rgb_asset_page_load_model = RgbAssetPageLoadModel(
            asset_type=self.asset_type, asset_id=self.asset_id_detail.toPlainText(), asset_name=self.asset_name, image_path=self.image_path,
        )
        params = SelectionPageModel(
            title=title,
            logo_1_path=rgb_on_chain_logo_path,
            logo_1_title=rgb_on_chain_logo_title,
            logo_2_path=rgb_off_chain_logo_path,
            logo_2_title=rgb_off_chain_logo_title,
            asset_id=self.asset_id_detail.toPlainText(),
            asset_name=self.asset_name,
            callback=navigation,
            back_page_navigation=lambda: self._view_model.page_navigation.cfa_detail_page(
                RgbAssetPageLoadModel(asset_type=self.asset_type),
            ),
            rgb_asset_page_load_model=rgb_asset_page_load_model,
        )
        self._view_model.page_navigation.wallet_method_page(params)

    def select_receive_transfer_type(self):
        """This method handled after channel created"""
        if self.is_channel_open_for_asset():
            self.navigate_to_selection_page(
                TransferStatusEnumModel.RECEIVE.value,
            )
        else:
            self._view_model.page_navigation.receive_cfa_page(
                params=AssetDataModel(
                    asset_type=self.asset_type, asset_id=self.asset_id_detail.toPlainText(),
                ),
            )

    def select_send_transfer_type(self):
        """This method navigates the send asset page according to the condition"""
        if self.is_channel_open_for_asset():
            self.navigate_to_selection_page(
                TransferStatusEnumModel.SEND.value,
            )
        else:
            self._view_model.page_navigation.send_cfa_page()

    def setup_ui_connection(self):
        """Set up connections for UI elements."""
        self.show_loading_screen(True)
        self._view_model.channel_view_model.available_channels()
        self._view_model.channel_view_model.channel_loaded.connect(
            self.is_channel_open_for_asset,
        )
        self._view_model.channel_view_model.channel_loaded.connect(
            self.set_lightning_balance,
        )
        self.send_asset.clicked.connect(
            self.select_send_transfer_type,
        )
        self.receive_rgb_asset.clicked.connect(
            self.select_receive_transfer_type,
        )
        self.copy_button.clicked.connect(
            lambda: copy_text(self.asset_id_detail),
        )
        self._view_model.cfa_view_model.txn_list_loaded.connect(
            self.set_transaction_detail_frame,
        )
        self.close_btn.clicked.connect(
            self.handle_page_navigation,
        )
        self._view_model.cfa_view_model.is_loading.connect(
            self.show_loading_screen,
        )
        self.asset_refresh_button.clicked.connect(
            self._view_model.cfa_view_model.on_refresh_click,
        )

    def refresh_transaction(self):
        """Refresh the transaction of the assets"""
        self.render_timer.start()
        self._view_model.cfa_view_model.on_refresh_click()

    def set_transaction_detail_frame(self, asset_id, asset_name, image_path, asset_type):
        """This method sets up the transaction detail frame in the UI.
        It retrieves sorted transactions from the Bitcoin ViewModel and updates the UI
        by adding a widget for each transaction.
        """
        self.image_path = image_path
        self.asset_type = asset_type
        self.asset_name = asset_name
        self.handle_img_path(image_path=self.image_path)
        asset_transactions: ListOnAndOffChainTransfersWithBalance = self._view_model.cfa_view_model.txn_list
        self.asset_total_balance.setText(
            str(asset_transactions.asset_balance.future),
        )
        self.asset_id_detail.setPlainText(str(asset_id))
        self.widget_title_asset_name.setText(str(asset_name))
        self.asset_spendable_amount.setText(
            str(asset_transactions.asset_balance.spendable),
        )
        # Ensure asset_transactions is unpacked correctly if it's a tuple
        if isinstance(asset_transactions, tuple):
            asset_transactions, _ = asset_transactions
        # Clear any existing items in the layout
        for i in reversed(range(self.scroll_area_widget_layout.count())):
            widget_to_remove = self.scroll_area_widget_layout.itemAt(
                i,
            ).widget()
            if widget_to_remove is not None:
                widget_to_remove.setParent(None)
        if not asset_transactions or (
            not asset_transactions.onchain_transfers and not asset_transactions.off_chain_transfers
        ):
            transaction_detail_frame = TransactionDetailFrame(
                self.scroll_area_widget_contents,
            )
            self.transactions_label.hide()
            no_transaction_widget = transaction_detail_frame.no_transaction_frame()
            transaction_detail_frame.setCursor(
                QCursor(Qt.CursorShape.PointingHandCursor),
            )
            self.scroll_area_widget_layout.addWidget(
                no_transaction_widget, 0, 0, 1, 1,
            )
            return
        if asset_type == AssetType.NIA.value:
            self.rgb_asset_detail_widget.setMinimumSize(QSize(499, 730))
            self.rgb_asset_detail_widget.setMaximumSize(QSize(499, 730))
            self.scroll_area.setMaximumSize(QSize(335, 225))
            self.lightning_balance_frame.setMaximumSize(QSize(159, 120))
            self.asset_balance_frame.setMaximumSize(QSize(158, 120))
        # Initialize the row index for the grid layout
        row_index = 0
        self.filtered_lightning_transactions = [
            payment for payment in asset_transactions.off_chain_transfers
            if payment.asset_id == asset_id
        ]
        # Combine on-chain and off-chain transactions
        all_transactions = [
            (TransferOptionModel.LIGHTNING.value, tx) for tx in self.filtered_lightning_transactions
        ] + [(TransferOptionModel.ON_CHAIN.value, tx) for tx in asset_transactions.onchain_transfers]
        all_transactions = sorted(
            all_transactions, key=lambda x: x[1].updated_at, reverse=True,
        )
        for tx_type, transaction in all_transactions:
            if tx_type == TransferOptionModel.ON_CHAIN:
                self.set_on_chain_transaction_frame(
                    transaction, asset_name, asset_type, asset_id, image_path,
                )
            if tx_type == TransferOptionModel.LIGHTNING:
                self.set_lightning_transaction_frame(
                    transaction, asset_name, asset_type,
                )
            self.transaction_detail_frame.click_frame.connect(
                self.handle_asset_frame_click,
            )
            self.transaction_detail_frame.setCursor(
                QCursor(Qt.CursorShape.PointingHandCursor),
            )
            self.scroll_area_widget_layout.addWidget(
                self.transaction_detail_frame, row_index, 0, 1, 1,
            )
            row_index += 1
        self.vertical_spacer_3 = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding,
        )
        self.scroll_area_widget_layout.addItem(
            self.vertical_spacer_3, row_index, 0, 1, 1,
        )

    def handle_asset_frame_click(self, params: TransactionDetailPageModel):
        """Pass emit value to navigation page"""
        self._view_model.page_navigation.cfa_transaction_detail_page(params)

    def handle_show_hide(self, transaction_detail_frame):
        """It handled to hide and show transaction details frame"""
        if self.transfer_status == TransferStatusEnumModel.INTERNAL.value:
            if self.transaction_type == TransferType.ISSUANCE.value:
                transaction_detail_frame.transaction_type.setText(
                    'ISSUANCE',
                )
                transaction_detail_frame.transaction_amount.setStyleSheet(
                    'color:#01A781;font-weight: 600',
                )
                transaction_detail_frame.transaction_type.show()
                transaction_detail_frame.transfer_type.hide()
            else:
                transaction_detail_frame.transfer_type.show()
                transaction_detail_frame.transaction_type.hide()

    def show_loading_screen(self, loading: bool):
        """This method handled show loading screen on main asset page"""
        if loading:
            self.__loading_translucent_screen = LoadingTranslucentScreen(
                parent=self, description_text='Loading',
            )
            self.__loading_translucent_screen.start()
            self.__loading_translucent_screen.make_parent_disabled_during_loading(
                True,
            )
            self.asset_refresh_button.setDisabled(True)
            self.send_asset.setDisabled(True)
            self.receive_rgb_asset.setDisabled(True)
        else:
            if self.lightning_total_balance.text():
                self.render_timer.stop()
                self.__loading_translucent_screen.stop()
                self.__loading_translucent_screen.make_parent_disabled_during_loading(
                    False,
                )
                self.asset_refresh_button.setDisabled(False)
                self.send_asset.setDisabled(False)
                self.receive_rgb_asset.setDisabled(False)

    def handle_page_navigation(self):
        """Handle the page navigation according the NIA or CFA page"""
        if self.asset_type == AssetType.NIA.value:
            self._view_model.page_navigation.fungibles_asset_page()
        else:
            self._view_model.page_navigation.collectibles_asset_page()

    def is_channel_open_for_asset(self):
        """Check if there is an open channel for the current asset."""
        self.asset_id_detail.textChanged.connect(self.set_lightning_balance)
        for channel in self._view_model.channel_view_model.channels:
            if channel.is_usable and channel.ready:
                if channel.asset_id == self.asset_id_detail.toPlainText():
                    return True
        return False

    def set_lightning_balance(self):
        """This functions gets the total and spendable balances of the asset from all the open channels"""
        lightning_total_balance = 0
        lightning_spendable_balance = 0
        asset_id = self.asset_id_detail.toPlainText()
        if asset_id:
            for channel in self._view_model.channel_view_model.channels:
                if channel.asset_id == asset_id:
                    if channel.is_usable:
                        lightning_spendable_balance += channel.asset_local_amount
                    lightning_total_balance += channel.asset_local_amount

            self.lightning_total_balance.setText(str(lightning_total_balance))
            self.lightning_spendable_balance.setText(
                str(lightning_spendable_balance),
            )
            self.show_loading_screen(False)

    def handle_fail_transfer(self, idx, tx_id):
        """
        Handles the close button click for a transaction, with a custom confirmation dialog.
        """
        if tx_id:
            confirmation_dialog = ConfirmationDialog(
                parent=self, message=(f"{
                    QCoreApplication.translate(
                        IRIS_WALLET_TRANSLATIONS_CONTEXT, 'transaction_id', None,
                    )
                }: {tx_id}\n\n {
                    QCoreApplication.translate(
                        IRIS_WALLET_TRANSLATIONS_CONTEXT, 'cancel_transfer', None,
                    )
                }"),
            )
        else:
            confirmation_dialog = ConfirmationDialog(
                parent=self, message=QCoreApplication.translate(
                    IRIS_WALLET_TRANSLATIONS_CONTEXT, 'cancel_invoice', None,
                ),
            )
        confirmation_dialog.confirmation_dialog_continue_button.clicked.connect(
            lambda: self._confirm_fail_transfer(idx),
        )
        confirmation_dialog.confirmation_dialog_cancel_button.clicked.connect(
            confirmation_dialog.reject,
        )
        confirmation_dialog.exec()

    def _confirm_fail_transfer(self, idx):
        """Confirms the fail transfer action and closes the confirmation dialog."""
        self._view_model.cfa_view_model.on_fail_transfer(idx)

    def handle_img_path(self, image_path):
        """Configure the asset detail widget based on the provided image path."""
        if image_path:
            self.lightning_balance_frame.setMinimumSize(QSize(159, 120))
            self.label_asset_name = handle_img_path(
                self.rgb_asset_detail_widget,
                image_path,
                self.asset_image_layout,
                self.asset_id_frame,
                self.label_asset_name if hasattr(
                    self, 'label_asset_name',
                ) else None,
            )
            self.transactions_label.setMinimumWidth(305)

    def set_on_chain_transaction_frame(self, transaction, asset_name, asset_type, asset_id, image_path):
        """Handles and updates the UI for on-chain transaction details."""
        tx_id = str(transaction.txid)
        amount = str(transaction.amount_status)
        self.transaction_detail_frame = TransactionDetailFrame(
            self.scroll_area_widget_contents,
            TransactionDetailPageModel(
                tx_id=tx_id,
                asset_name=asset_name,
                amount=amount,
                asset_type=asset_type,
                asset_id=asset_id,
                image_path=image_path,
                confirmation_date=transaction.updated_at_date,
                confirmation_time=transaction.updated_at_time,
                consignment_endpoints=transaction.transport_endpoints,
                transfer_status=transaction.transfer_Status,
                transaction_status=transaction.status,
                recipient_id=transaction.recipient_id,
                change_utxo=transaction.change_utxo,
                receive_utxo=transaction.receive_utxo,
            ),
        )
        self.transaction_detail_frame.setAccessibleName(
            RGB_TRANSACTION_DETAIL_ON_CHAIN_FRAME,
        )
        self.transaction_detail_frame.close_button.setAccessibleName(
            TRANSACTION_DETAIL_CLOSE_BUTTON,
        )
        self.transaction_date = str(transaction.updated_at_date)
        self.transaction_time = str(transaction.created_at_time)
        self.transfer_status = str(
            transaction.transfer_Status.value,
        )
        self.transfer_amount = amount
        self.transaction_type = str(transaction.kind)
        self.transaction_status = str(
            transaction.status,
        )
        if self.transfer_status == TransferStatusEnumModel.SENT.value:
            self.transaction_detail_frame.transaction_amount.setStyleSheet(
                'color:#EB5A5A;font-weight: 600',
            )
        if self.transfer_status == TransferStatusEnumModel.RECEIVED.value:
            self.transaction_detail_frame.transaction_amount.setStyleSheet(
                'color:#01A781;font-weight: 600',
            )
        if self.transaction_date == TransactionStatusEnumModel.FAILED:
            self.transaction_detail_frame.transaction_amount.setStyleSheet(
                'color:#EB5A5A;font-weight: 600',
            )
        self.transaction_detail_frame.transaction_time.setText(
            self.transaction_time,
        )
        self.transaction_detail_frame.transaction_date.setText(
            self.transaction_date,
        )
        if self.transaction_status != TransactionStatusEnumModel.SETTLED:
            self.transaction_detail_frame.transaction_time.setStyleSheet(
                'color:#959BAE;font-weight: 400; font-size:14px',
            )
            self.transaction_detail_frame.transaction_time.setText(
                self.transaction_status,
            )
            self.transaction_detail_frame.transaction_date.setText(
                self.transaction_date,
            )
        self.on_chain_icon = QIcon()
        img_path = self.bitcoin_img_path.get(self.network.value)
        self.on_chain_icon.addFile(
            img_path,
            QSize(), QIcon.Normal, QIcon.Off,
        )
        self.transaction_detail_frame.transfer_type.setIcon(
            self.on_chain_icon,
        )
        self.transaction_detail_frame.transfer_type.setIconSize(
            QSize(18, 18),
        )
        self.transaction_detail_frame.transfer_type.setToolTip(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'on_chain', None,
            ),
        )
        self.transaction_detail_frame.transaction_amount.setText(
            self.transfer_amount,
        )
        if self.transaction_status == TransactionStatusEnumModel.WAITING_COUNTERPARTY:
            self.transaction_detail_frame.transaction_type.hide()
            self.transaction_detail_frame.transaction_amount.setStyleSheet(
                'color:#959BAE;font-weight: 600',
            )
            icon3 = QIcon()
            icon3.addFile(
                ':/assets/x_circle_red.png',
                QSize(), QIcon.Normal, QIcon.Off,
            )
            self.transaction_detail_frame.close_button.setIcon(icon3)
            self.transaction_detail_frame.close_button.setIconSize(
                QSize(18, 18),
            )
            self.transaction_detail_frame.close_button.clicked.connect(
                lambda _, idx=transaction.idx, tx_id=transaction.txid: self.handle_fail_transfer(
                    idx, tx_id,
                ),
            )
            self.transaction_detail_frame.close_button.setToolTip(
                QCoreApplication.translate(
                    IRIS_WALLET_TRANSLATIONS_CONTEXT, 'fail_transfer', None,
                ),
            )
        self.handle_show_hide(self.transaction_detail_frame)

    def set_lightning_transaction_frame(self, transaction, asset_name, asset_type):
        """Handles and updates the UI for off-chain (lightning) transaction details."""
        amount = str(transaction.asset_amount_status)
        self.transaction_detail_frame = TransactionDetailFrame(
            self.scroll_area_widget_contents,
            TransactionDetailPageModel(
                tx_id=str(transaction.payee_pubkey),
                asset_name=asset_name,
                asset_type=asset_type,
                amount=amount,
                asset_id=transaction.asset_id,
                transaction_status=transaction.status,
                is_off_chain=True,
                inbound=transaction.inbound,
                confirmation_date=transaction.created_at_date,
                confirmation_time=transaction.created_at_time,
                updated_date=transaction.updated_at_date,
                updated_time=transaction.updated_at_time,
            ),
        )
        self.transaction_detail_frame.setAccessibleName(
            RGB_TRANSACTION_DETAIL_LIGHTNING_FRAME,
        )
        self.transfer_amount = amount
        self.transaction_date = str(transaction.updated_at_date)
        self.transaction_time = str(transaction.created_at_time)
        self.transaction_status = str(transaction.status)
        if self.transaction_status == PaymentStatus.FAILED.value:
            self.transaction_detail_frame.transaction_amount.setStyleSheet(
                'color:#EB5A5A;font-weight: 600',
            )
        elif self.transaction_status == PaymentStatus.SUCCESS.value:
            if transaction.inbound:
                # Green color for successful received transactions
                self.transaction_detail_frame.transaction_amount.setStyleSheet(
                    'color:#01A781;font-weight: 600',
                )
            else:
                self.transaction_detail_frame.transaction_amount.setStyleSheet(
                    'color:#EB5A5A;font-weight: 600',
                )
        elif self.transaction_status == PaymentStatus.PENDING.value:
            # Grey color for pending transactions (both sent and received)
            self.transaction_detail_frame.transaction_amount.setStyleSheet(
                'color:#959BAE;font-weight: 600',
            )
        self.transaction_detail_frame.transaction_amount.setText(
            self.transfer_amount,
        )
        self.transaction_detail_frame.transaction_time.setText(
            self.transaction_time,
        )
        self.transaction_detail_frame.transaction_date.setText(
            self.transaction_date,
        )
        if self.transaction_status != PaymentStatus.SUCCESS:
            self.transaction_detail_frame.transaction_time.setStyleSheet(
                'color:#959BAE;font-weight: 400; font-size:14px',
            )
            self.transaction_detail_frame.transaction_time.setText(
                self.transaction_status,
            )
            self.transaction_detail_frame.transaction_date.setText(
                self.transaction_date,
            )
        self.lightning_icon = QIcon()
        self.lightning_icon.addFile(
            ':/assets/lightning_transaction.png',
            QSize(), QIcon.Normal, QIcon.Off,
        )
        self.transaction_detail_frame.transaction_type.hide()
        self.transaction_detail_frame.transfer_type.setIcon(
            self.lightning_icon,
        )
        self.transaction_detail_frame.transfer_type.setIconSize(
            QSize(18, 18),
        )
        self.transaction_detail_frame.transfer_type.setToolTip(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'lightning', None,
            ),
        )
