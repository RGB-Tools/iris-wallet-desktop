# pylint: disable=too-many-instance-attributes, too-many-statements, unused-import
"""This module contains the FungibleAssetWidget class,
which represents the UI for fungible assets.
"""
from __future__ import annotations

from PySide6.QtCore import QByteArray
from PySide6.QtCore import QCoreApplication
from PySide6.QtCore import QRect
from PySide6.QtCore import QSize
from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor
from PySide6.QtGui import QImage
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QFrame
from PySide6.QtWidgets import QGridLayout
from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QScrollArea
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtWidgets import QSpacerItem
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QWidget

import src.resources_rc
from accessible_constant import FUNGIBLES_SCROLL_WIDGETS
from accessible_constant import ISSUE_NIA_ASSET
from src.data.repository.setting_repository import SettingRepository
from src.data.service.common_operation_service import CommonOperationService
from src.model.enums.enums_model import AssetType
from src.model.enums.enums_model import NetworkEnumModel
from src.model.enums.enums_model import ToastPreset
from src.model.enums.enums_model import TokenSymbol
from src.model.enums.enums_model import WalletType
from src.model.rgb_model import RgbAssetPageLoadModel
from src.utils.clickable_frame import ClickableFrame
from src.utils.common_utils import generate_identicon
from src.utils.constant import IRIS_WALLET_TRANSLATIONS_CONTEXT
from src.utils.helpers import load_stylesheet
from src.utils.info_message import INFO_FAUCET_NOT_AVAILABLE
from src.utils.info_message import INFO_TITLE
from src.utils.render_timer import RenderTimer
from src.utils.worker import ThreadManager
from src.viewmodels.main_view_model import MainViewModel
from src.views.components.header_frame import HeaderFrame
from src.views.components.loading_screen import LoadingTranslucentScreen
from src.views.components.toast import ToastManager


class FungibleAssetWidget(QWidget, ThreadManager):
    """This class represents all the UI elements of the fungible page."""
    _native_auth_finished: bool = False

    def __init__(self, view_model):
        self.render_timer = RenderTimer(
            task_name='FungibleAssetWidget Rendering',
        )
        self.render_timer.start()
        super().__init__()
        self._view_model: MainViewModel = view_model
        self._view_model.main_asset_view_model.asset_loaded.connect(
            self.show_assets,
        )
        self.network: NetworkEnumModel = SettingRepository.get_wallet_network()
        CommonOperationService.set_node_info()
        self.sidebar = None
        self.__loading_translucent_screen = None
        self.setStyleSheet(
            load_stylesheet(
                'views/qss/fungible_asset_style.qss',
            ),
        )
        self.setObjectName('my_assets_page')
        self.vertical_layout_fungible_1 = QVBoxLayout(self)
        self.vertical_layout_fungible_1.setObjectName(
            'vertical_layout_fungible_1',
        )
        self.vertical_layout_fungible_1.setContentsMargins(0, 0, 0, 0)
        self.fungibles_widget = QWidget(self)
        self.fungibles_widget.setObjectName('widget_2')
        self.vertical_layout_fungible_2 = QVBoxLayout(self.fungibles_widget)
        self.vertical_layout_fungible_2.setObjectName('vertical_layout_2')
        self.vertical_layout_fungible_2.setContentsMargins(25, 12, 25, 0)
        self.title_frame = HeaderFrame(
            title_logo_path=':/assets/my_asset.png', title_name='fungibles',
        )
        self.title_frame.action_button.setAccessibleName(ISSUE_NIA_ASSET)
        self.fungible_frame = None
        self.vertical_layout_fungible_frame = None
        self.grid_layout_fungible_frame = None
        self.asset_logo = None
        self.asset_name = None
        self.address = None
        self.amount = None
        self.token_symbol = None
        self.vertical_layout_4 = None
        self.image_label = None
        self.horizontal_spacer = None
        self.vertical_spacer_scroll_area = None
        self.header_frame = None
        self.header_layout = None
        self.logo_header = None
        self.name_header = None
        self.address_header = None
        self.amount_header = None
        self.outbound_amount_header = None
        self.symbol_header = None
        self.outbound_balance = None

        self.vertical_layout_fungible_2.addWidget(self.title_frame)

        self.fungibles_label = QLabel(self.fungibles_widget)
        self.fungibles_label.setObjectName('fungibles_label')
        self.fungibles_label.setMinimumSize(QSize(1016, 57))

        self.vertical_layout_fungible_2.addWidget(self.fungibles_label)

        self.scroll_area_fungible = QScrollArea(self.fungibles_widget)
        self.scroll_area_fungible.setObjectName('scroll_area_1')
        self.scroll_area_fungible.setWidgetResizable(True)
        self.scroll_area_fungible.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded,
        )
        self.scroll_area_fungible.setStyleSheet(
            load_stylesheet('views/qss/scrollbar.qss'),
        )
        self.scroll_area_fungible.setMinimumHeight(320)
        self.scroll_area_widget_fungible = QWidget()
        self.scroll_area_widget_fungible.setObjectName(
            'scrollAreaWidgetContents_2',
        )
        self.scroll_area_widget_fungible.setAccessibleName(
            FUNGIBLES_SCROLL_WIDGETS,
        )
        self.scroll_area_widget_fungible.setGeometry(QRect(0, 0, 1182, 2000))
        self.scroll_area_widget_fungible.setContentsMargins(0, -1, 10, -1)

        self.scroll_area_widget_fungible.setMaximumSize(
            QSize(16777215, 2000),
        )
        self.vertical_layout_scroll_content = QVBoxLayout(
            self.scroll_area_widget_fungible,
        )
        self.vertical_layout_scroll_content.setObjectName('verticalLayout_2')
        self.vertical_layout_scroll_content.setContentsMargins(0, -1, 0, -1)
        self.vertical_layout_3 = QVBoxLayout()
        self.vertical_layout_3.setSpacing(10)
        self.vertical_layout_3.setObjectName('verticalLayout_3')

        self.fungible_frame = QFrame(self.scroll_area_widget_fungible)

        self.vertical_layout_scroll_content.addLayout(self.vertical_layout_3)

        self.scroll_area_fungible.setWidget(self.scroll_area_widget_fungible)

        self.vertical_layout_fungible_2.addWidget(self.scroll_area_fungible)
        self.horizontal_layout_2 = QHBoxLayout()
        self.horizontal_layout_2.setSpacing(6)

        self.horizontal_layout_2.setObjectName('horizontalLayout_2')
        self.horizontal_layout_2.setContentsMargins(1, -1, 1, -1)

        self.vertical_layout_fungible_1.addWidget(self.fungibles_widget)
        self.fungibles_frame_card = QFrame(self.fungibles_widget)
        self.fungibles_frame_card.setObjectName('fungibles_frame_card')

        self.fungibles_frame_card.setFrameShape(QFrame.StyledPanel)
        self.fungibles_frame_card.setFrameShadow(QFrame.Raised)

        self.horizontal_layout_2.addWidget(self.fungibles_frame_card)

        self.vertical_layout_fungible_2.addLayout(self.horizontal_layout_2)
        self.retranslate_ui()
        self.setup_ui_connection()

    def show_assets(self):
        """This method creates all the fungible assets elements of the main asset page."""
        for i in reversed(range(self.vertical_layout_3.count())):
            widget = self.vertical_layout_3.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        self.header_frame = QFrame(self.scroll_area_widget_fungible)
        self.header_frame.setObjectName('header_frame')
        self.header_frame.setMinimumSize(QSize(900, 70))
        self.header_frame.setMaximumSize(QSize(16777215, 70))
        self.header_layout = QGridLayout(self.header_frame)
        self.header_layout.setContentsMargins(20, 6, 20, 6)

        self.logo_header = QLabel(self.header_frame)
        self.logo_header.setObjectName('logo_header')
        self.logo_header.setMinimumSize(QSize(40, 40))
        self.logo_header.setMaximumSize(QSize(40, 40))
        self.header_layout.addWidget(self.logo_header, 0, 1)

        self.name_header = QLabel(self.header_frame)
        self.name_header.setObjectName('name_header')
        self.name_header.setMinimumSize(QSize(130, 40))
        self.header_layout.addWidget(self.name_header, 0, 0, Qt.AlignLeft)

        self.address_header = QLabel(self.header_frame)
        self.address_header.setObjectName('address_header')
        self.address_header.setMinimumSize(QSize(600, 0))
        self.address_header.setMaximumSize(QSize(16777215, 16777215))
        self.header_layout.addWidget(self.address_header, 0, 2, Qt.AlignLeft)
        self.address_header.setStyleSheet(
            'padding-left: 10px;',
        )

        self.amount_header = QLabel(self.header_frame)
        self.amount_header.setObjectName('amount_header')
        self.amount_header.setWordWrap(True)
        self.amount_header.setMinimumSize(QSize(98, 40))
        self.header_layout.addWidget(self.amount_header, 0, 3, Qt.AlignLeft)

        self.outbound_amount_header = QLabel(self.header_frame)
        self.outbound_amount_header.setWordWrap(True)
        self.outbound_amount_header.setObjectName('outbound_amount_header')
        self.outbound_amount_header.setMinimumSize(QSize(70, 40))
        self.header_layout.addWidget(
            self.outbound_amount_header, 0, 4, Qt.AlignLeft,
        )

        self.symbol_header = QLabel(self.header_frame)
        self.symbol_header.setObjectName('symbol_header')
        self.header_layout.addWidget(self.symbol_header, 0, 5, Qt.AlignLeft)

        self.vertical_layout_3.addWidget(self.header_frame)
        bitcoin = self._view_model.main_asset_view_model.assets.vanilla

        bitcoin_img_path = {
            NetworkEnumModel.MAINNET.value: ':/assets/bitcoin.png',
            NetworkEnumModel.REGTEST.value: ':/assets/regtest_bitcoin.png',
            NetworkEnumModel.TESTNET4.value: ':/assets/testnet_bitcoin.png',
            NetworkEnumModel.TESTNET.value: ':/assets/testnet_bitcoin.png',
        }

        img_path = bitcoin_img_path.get(self.network.value)

        if img_path:
            self.create_fungible_card(bitcoin, img_path=img_path)

        for asset in self._view_model.main_asset_view_model.assets.nia:
            self.create_fungible_card(asset)
        self.vertical_spacer_scroll_area = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding,
        )
        self.vertical_layout_scroll_content.addItem(
            self.vertical_spacer_scroll_area,
        )
        self.name_header.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'asset_name', None,
            ),
        )
        self.address_header.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'asset_id', None,
            ),
        )
        self.amount_header.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'on_chain_balance', None,
            ),
        )
        self.outbound_amount_header.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'lightning_balance', None,
            ),
        )
        self.symbol_header.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'symbol_header', None,
            ),
        )

    def _get_asset_logo_pixmap(self, asset, img_path):
        """Generate and return the pixmap for the asset logo."""
        if img_path:
            return QPixmap(img_path)

        img_str = generate_identicon(asset.asset_id)
        image = QImage.fromData(QByteArray.fromBase64(img_str.encode()))
        return QPixmap.fromImage(image)

    def _get_address_text(self, asset, img_path):
        """Get the appropriate address text based on asset type and network."""
        if not img_path:
            return asset.asset_id

        network = SettingRepository.get_wallet_network()
        network_token_map = {
            NetworkEnumModel.REGTEST: TokenSymbol.REGTEST_BITCOIN,
            NetworkEnumModel.TESTNET: TokenSymbol.TESTNET_BITCOIN,
            NetworkEnumModel.TESTNET4: TokenSymbol.TESTNET4_BITCOIN,
        }
        return network_token_map.get(network, '')

    def _get_outbound_balance_text(self, asset, img_path):
        """Get the outbound balance text for the asset."""
        if img_path:
            return 'N/A'

        return str(asset.balance.offchain_outbound) if asset.balance.offchain_outbound else 'N/A'

    def _apply_bitcoin_naming(self, asset):
        """Apply Bitcoin-specific naming conventions based on ticker."""
        if 'BTC' not in asset.ticker:
            return

        self.token_symbol.setText(TokenSymbol.SAT.value)
        bitcoin_asset = AssetType.BITCOIN.value.lower()

        # For mainnet Bitcoin
        if asset.ticker == TokenSymbol.BITCOIN.value:
            self.asset_name.setText(bitcoin_asset)
            return

        # For testnet variants and regtest, use network to distinguish
        # since TESTNET_BITCOIN and TESTNET4_BITCOIN have the same ticker 'tBTC'
        network = SettingRepository.get_wallet_network()
        network_naming_map = {
            NetworkEnumModel.TESTNET: f'{NetworkEnumModel.TESTNET.value} {bitcoin_asset}',
            NetworkEnumModel.TESTNET4: f'{NetworkEnumModel.TESTNET4.value} {bitcoin_asset}',
            NetworkEnumModel.REGTEST: f'{NetworkEnumModel.REGTEST.value} {bitcoin_asset}',
        }

        if network in network_naming_map:
            self.asset_name.setText(network_naming_map[network])

    def create_fungible_card(self, asset, img_path=None):
        """This method creates all the fungible assets elements of the main asset page."""
        self.fungible_frame = ClickableFrame(
            asset.asset_id, asset.name, self.fungibles_widget, asset_type=AssetType.BITCOIN if img_path else AssetType.NIA,
        )
        self.fungible_frame.setStyleSheet(
            load_stylesheet('views/qss/fungible_asset_style.qss'),
        )

        self.fungible_frame.setCursor(
            QCursor(Qt.CursorShape.PointingHandCursor),
        )
        self.fungible_frame.setObjectName('frame_4')
        self.fungible_frame.setMinimumSize(QSize(900, 70))
        self.fungible_frame.setMaximumSize(QSize(16777215, 70))

        self.fungible_frame.setFrameShape(QFrame.StyledPanel)
        self.fungible_frame.setFrameShadow(QFrame.Raised)
        self.vertical_layout_fungible_frame = QVBoxLayout(self.fungible_frame)
        self.vertical_layout_fungible_frame.setObjectName('vertical_layout_16')
        self.grid_layout_fungible_frame = QGridLayout()
        self.grid_layout_fungible_frame.setObjectName(
            'horizontal_layout_7',
        )
        self.grid_layout_fungible_frame.setContentsMargins(6, 0, 6, 0)

        # Asset Logo
        self.asset_logo = QLabel(self.fungible_frame)
        self.asset_logo.setObjectName('asset_logo')
        self.asset_logo.setMinimumSize(QSize(40, 40))
        self.asset_logo.setMaximumSize(QSize(40, 40))
        self.asset_logo.setPixmap(self._get_asset_logo_pixmap(asset, img_path))
        self.grid_layout_fungible_frame.addWidget(self.asset_logo, 0, 0)

        # Asset Name
        self.asset_name = QLabel(self.fungible_frame)
        self.asset_name.setObjectName('asset_name')
        self.asset_name.setMinimumSize(QSize(135, 40))
        self.asset_name.setStyleSheet(
            load_stylesheet(
                'views/qss/fungible_asset_style.qss',
            ),
        )
        self.asset_name.setText(asset.name)
        self.grid_layout_fungible_frame.addWidget(self.asset_name, 0, 1)

        # Address
        self.address = QLabel(self.fungible_frame)
        self.address.setObjectName('address')
        self.address.setMinimumSize(QSize(600, 0))
        self.address.setMaximumSize(QSize(16777215, 16777215))
        self.address.setStyleSheet('padding-left:10px;')
        self.address.setText(self._get_address_text(asset, img_path))
        self.grid_layout_fungible_frame.addWidget(
            self.address, 0, 2, Qt.AlignLeft,
        )

        # Amount
        self.amount = QLabel(self.fungible_frame)
        self.amount.setObjectName('amount')
        self.amount.setMinimumSize(QSize(100, 40))
        self.amount.setText(str(asset.balance.future))
        self.grid_layout_fungible_frame.addWidget(
            self.amount, 0, 3, Qt.AlignLeft,
        )

        # Off-Chain Outbound Balance
        self.outbound_balance = QLabel(self.fungible_frame)
        self.outbound_balance.setObjectName('outbound_balance')
        self.outbound_balance.setMinimumSize(QSize(80, 40))
        self.outbound_balance.setText(
            self._get_outbound_balance_text(asset, img_path),
        )
        self.grid_layout_fungible_frame.addWidget(
            self.outbound_balance, 0, 4, Qt.AlignLeft,
        )

        # Token Symbol
        self.token_symbol = QLabel(self.fungible_frame)
        self.token_symbol.setObjectName('token_symbol')
        self.token_symbol.setText(asset.ticker)
        self.grid_layout_fungible_frame.addWidget(
            self.token_symbol, 0, 5, Qt.AlignLeft,
        )

        self.vertical_layout_fungible_frame.addLayout(
            self.grid_layout_fungible_frame,
        )

        # Apply Bitcoin-specific naming
        self._apply_bitcoin_naming(asset)

        self.vertical_layout_3.addWidget(self.fungible_frame)
        self.fungible_frame.clicked.connect(self.handle_asset_frame_click)

    def setup_ui_connection(self):
        """Set up connections for UI elements."""
        self.handle_backup_visibility()
        self.check_faucet_availability()
        self._view_model.main_asset_view_model.get_assets()
        self.title_frame.refresh_page_button.clicked.connect(
            self.refresh_asset,
        )
        self.title_frame.action_button.clicked.connect(
            lambda: self._view_model.main_asset_view_model.navigate_issue_asset(
                self._view_model.page_navigation.issue_nia_asset_page,
            ),
        )
        self._view_model.main_asset_view_model.loading_started.connect(
            self.show_fungible_loading_screen,
        )
        self._view_model.main_asset_view_model.loading_finished.connect(
            self.stop_fungible_loading_screen,
        )
        self._view_model.main_asset_view_model.message.connect(
            self.show_message,
        )

    def retranslate_ui(self):
        """Retranslate the UI elements."""
        self.show_fungible_loading_screen()
        self.fungibles_label.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'fungibles', None,
            ),
        )

    def refresh_asset(self):
        """This method start the render timer and perform the fungible asset list refresh"""
        self.render_timer.start()
        self._view_model.main_asset_view_model.get_assets(
            rgb_asset_hard_refresh=True,
        )

    def handle_asset_frame_click(self, asset_id, asset_name, image_path, asset_type):
        """This method handles fungibles asset click of the main asset page."""
        if asset_type == AssetType.BITCOIN.value:
            self._view_model.page_navigation.bitcoin_page()
        else:
            self._view_model.cfa_view_model.asset_info.emit(
                asset_id, asset_name, image_path, asset_type,
            )
            self._view_model.page_navigation.cfa_detail_page(
                RgbAssetPageLoadModel(asset_type=asset_type),
            )

    def show_fungible_loading_screen(self):
        """This method handled show loading screen on main asset page"""
        self.__loading_translucent_screen = LoadingTranslucentScreen(
            parent=self, description_text='Loading', dot_animation=True,
        )
        self.__loading_translucent_screen.start()
        self.title_frame.refresh_page_button.setDisabled(True)

    def stop_fungible_loading_screen(self):
        """This method handled stop loading screen on main asset page"""
        self.render_timer.stop()
        self.__loading_translucent_screen.stop()
        self.title_frame.refresh_page_button.setDisabled(False)

    def show_message(self, fungible_asset_toast_preset, message):
        """This method handled showing message main asset page"""
        if fungible_asset_toast_preset == ToastPreset.SUCCESS:
            ToastManager.success(description=message)
        if fungible_asset_toast_preset == ToastPreset.ERROR:
            ToastManager.error(description=message)
        if fungible_asset_toast_preset == ToastPreset.INFORMATION:
            ToastManager.info(description=message)
        if fungible_asset_toast_preset == ToastPreset.WARNING:
            ToastManager.warning(description=message)

    def handle_backup_visibility(self):
        """This method handle the backup visibility on embedded or connect wallet type."""
        wallet_type: WalletType = SettingRepository.get_wallet_type()
        self.sidebar = self._view_model.page_navigation.sidebar()
        if WalletType.REMOTE_TYPE_WALLET.value == wallet_type.value:
            self.sidebar.backup.hide()
        if WalletType.EMBEDDED_TYPE_WALLET.value == wallet_type.value:
            self.sidebar.backup.show()

    def check_faucet_availability(self):
        """Check the availability of faucets and connect the signal to handle updates."""
        self._view_model.faucets_view_model.get_faucet_list()
        self._view_model.faucets_view_model.faucet_available.connect(
            self.update_faucet_availability,
        )

    def update_faucet_availability(self, available: bool):
        """Update the sidebar faucet status based on availability.

        Args:
            available (bool): Indicates whether the faucet is available.
        """
        self.sidebar = self._view_model.page_navigation.sidebar()
        if available:
            self.sidebar.faucet.setCheckable(True)
        else:
            self.sidebar.faucet.setCheckable(False)
            self.sidebar.faucet.setStyleSheet(
                'Text-align:left;'
                'font: 15px "Inter";'
                'color: rgb(120, 120, 120);'
                'padding: 17.5px 16px;'
                'background-image: url(:/assets/right_small.png);'
                'background-repeat: no-repeat;'
                'background-position: right center;'
                'background-origin: content;',
            )
            # Disconnecting all previous click events
            self.sidebar.faucet.clicked.disconnect()
            self.sidebar.faucet.clicked.connect(
                self.show_faucet_unavailability_message,
            )

    def show_faucet_unavailability_message(self):
        """Display a message indicating that the faucet is not available."""
        ToastManager.info(
            description=INFO_FAUCET_NOT_AVAILABLE,
        )
