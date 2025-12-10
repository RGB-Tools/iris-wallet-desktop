# pylint: disable=too-many-instance-attributes, too-many-statements, unused-import
"""This module contains the SettingsWidget class,
which represents the UI for settings page.
"""
from __future__ import annotations

from PySide6.QtCore import QCoreApplication
from PySide6.QtCore import QSize
from PySide6.QtCore import Qt
from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import QDialog
from PySide6.QtWidgets import QFrame
from PySide6.QtWidgets import QGridLayout
from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtWidgets import QSpacerItem
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QWidget

from accessible_constant import ASK_AUTH_FOR_APP_LOGIN
from accessible_constant import ASK_AUTH_FOR_APP_LOGIN_TOGGLE
from accessible_constant import ASK_AUTH_FOR_IMPORTANT_QUESTION
from accessible_constant import ASK_AUTH_FOR_IMPORTANT_QUESTION_TOGGLE
from accessible_constant import HIDE_EXHAUSTED_ASSETS
from accessible_constant import HIDE_EXHAUSTED_ASSETS_TOGGLE
from accessible_constant import KEYRING_STORAGE
from accessible_constant import KEYRING_TOGGLE_BUTTON
from accessible_constant import SET_DEFAULT_EXP_TIME
from accessible_constant import SET_DEFAULT_FEE_RATE
from accessible_constant import SET_DEFAULT_MIN_EXPIRATION
from accessible_constant import SPECIFY_ANNOUNCE_ADD
from accessible_constant import SPECIFY_ANNOUNCE_ALIAS
from accessible_constant import SPECIFY_BITCOIND_HOST
from accessible_constant import SPECIFY_BITCOIND_PORT
from accessible_constant import SPECIFY_INDEXER_URL
from accessible_constant import SPECIFY_RGB_PROXY_URL
from src.data.repository.setting_repository import SettingRepository
from src.model.common_operation_model import ConfigurableCardModel
from src.model.enums.enums_model import NetworkEnumModel
from src.model.setting_model import SettingPageLoadModel
from src.utils.constant import ANNOUNCE_ADDRESS
from src.utils.constant import ANNOUNCE_ALIAS
from src.utils.constant import BITCOIND_RPC_HOST_MAINNET
from src.utils.constant import BITCOIND_RPC_HOST_REGTEST
from src.utils.constant import BITCOIND_RPC_HOST_TESTNET
from src.utils.constant import BITCOIND_RPC_HOST_TESTNET4
from src.utils.constant import BITCOIND_RPC_PORT_MAINNET
from src.utils.constant import BITCOIND_RPC_PORT_REGTEST
from src.utils.constant import BITCOIND_RPC_PORT_TESTNET
from src.utils.constant import BITCOIND_RPC_PORT_TESTNET4
from src.utils.constant import FEE_RATE
from src.utils.constant import INDEXER_URL_MAINNET
from src.utils.constant import INDEXER_URL_REGTEST
from src.utils.constant import INDEXER_URL_TESTNET
from src.utils.constant import INDEXER_URL_TESTNET4
from src.utils.constant import IRIS_WALLET_TRANSLATIONS_CONTEXT
from src.utils.constant import LN_INVOICE_EXPIRY_TIME
from src.utils.constant import LN_INVOICE_EXPIRY_TIME_UNIT
from src.utils.constant import MIN_CONFIRMATION
from src.utils.constant import MNEMONIC_KEY
from src.utils.constant import PROXY_ENDPOINT_MAINNET
from src.utils.constant import PROXY_ENDPOINT_REGTEST
from src.utils.constant import PROXY_ENDPOINT_TESTNET
from src.utils.constant import PROXY_ENDPOINT_TESTNET4
from src.utils.constant import WALLET_PASSWORD_KEY
from src.utils.helpers import load_stylesheet
from src.utils.info_message import INFO_VALIDATION_OF_NODE_PASSWORD_AND_KEYRING_ACCESS
from src.utils.keyring_storage import get_value
from src.viewmodels.main_view_model import MainViewModel
from src.views.components.configurable_card import ConfigurableCardFrame
from src.views.components.header_frame import HeaderFrame
from src.views.components.keyring_error_dialog import KeyringErrorDialog
from src.views.components.loading_screen import LoadingTranslucentScreen
from src.views.components.settings_helpers import check_keyring_state_for_password
from src.views.components.settings_helpers import set_endpoint_based_on_network
from src.views.components.settings_helpers import set_frame_content
from src.views.components.toast import ToastManager
from src.views.components.toggle_switch import ToggleSwitch
from src.views.ui_restore_mnemonic import RestoreMnemonicWidget


class SettingsWidget(QWidget):
    """This class represents all the UI elements of the settings page."""

    def __init__(self, view_model):
        super().__init__()
        self._view_model: MainViewModel = view_model
        self.setStyleSheet(load_stylesheet('views/qss/settings_style.qss'))
        self.__loading_translucent_screen = None
        self.fee_rate = FEE_RATE
        self.expiry_time = LN_INVOICE_EXPIRY_TIME
        self.expiry_time_unit = LN_INVOICE_EXPIRY_TIME_UNIT
        self.indexer_url = None
        self.proxy_endpoint = None
        self.bitcoind_host = None
        self.bitcoind_port = None
        self.announce_address = ANNOUNCE_ADDRESS
        self.announce_alias = ANNOUNCE_ALIAS
        self.min_confirmation = MIN_CONFIRMATION
        self.indexer_url, self.proxy_endpoint, self.bitcoind_host, self.bitcoind_port = set_endpoint_based_on_network()
        self.current_network = None
        self.grid_layout = QGridLayout(self)
        self.grid_layout.setSpacing(0)
        self.grid_layout.setObjectName('gridLayout')
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.settings_widget = QWidget(self)
        self.settings_widget.setObjectName('settings_widget')
        self.settings_widget.setMinimumSize(QSize(492, 80))
        self.vertical_layout_6 = QVBoxLayout(self.settings_widget)
        self.vertical_layout_6.setObjectName('verticalLayout_6')
        self.vertical_layout_6.setContentsMargins(25, 12, 25, 0)
        self.settings_frame = HeaderFrame(
            title_logo_path=':/assets/settings.png', title_name='settings',
        )
        self.settings_frame.refresh_page_button.hide()
        self.settings_frame.action_button.hide()
        self.vertical_layout_6.addWidget(self.settings_frame)
        self.settings_label = QLabel(self.settings_widget)
        self.settings_label.setObjectName('settings_label')
        self.settings_label.setMinimumSize(QSize(1016, 45))
        self.vertical_layout_6.addWidget(self.settings_label)
        self.card_horizontal_layout_settings = QHBoxLayout()
        self.card_horizontal_layout_settings.setSpacing(25)
        self.card_horizontal_layout_settings.setObjectName(
            'card_horizontal_layout_settings',
        )
        self.stack_1_vertical_layout = QVBoxLayout()
        self.stack_1_vertical_layout.setSpacing(4)
        self.stack_1_vertical_layout.setObjectName('stack_1_vertical_layout')

        self.imp_operation_frame = QFrame(self.settings_widget)
        self.imp_operation_frame.setObjectName('imp_operation_frame')
        self.imp_operation_frame.setAccessibleName(
            ASK_AUTH_FOR_IMPORTANT_QUESTION,
        )
        self.imp_operation_frame.setMinimumSize(QSize(492, 92))
        self.imp_operation_frame.setMaximumWidth(492)
        self.imp_operation_frame.setFrameShape(QFrame.StyledPanel)
        self.imp_operation_frame.setFrameShadow(QFrame.Raised)
        self.grid_layout_6 = QGridLayout(self.imp_operation_frame)
        self.grid_layout_6.setObjectName('gridLayout_6')
        self.ask_auth_content_vertical_layout = QVBoxLayout()
        self.ask_auth_content_vertical_layout.setObjectName(
            'ask_auth_content_vertical_layout',
        )
        self.imp_operation_label = QLabel(self.imp_operation_frame)
        self.imp_operation_label.setObjectName('imp_operation_label')
        self.imp_operation_label.setStyleSheet('')
        self.imp_operation_label.setAlignment(Qt.AlignCenter)
        self.ask_auth_content_vertical_layout.addWidget(
            self.imp_operation_label, 0, Qt.AlignLeft,
        )
        self.auth_imp_desc = QLabel(self.imp_operation_frame)
        self.auth_imp_desc.setObjectName('auth_imp_desc')
        self.auth_imp_desc.setWordWrap(True)
        self.auth_imp_desc.setMinimumSize(QSize(385, 46))

        self.ask_auth_content_vertical_layout.addWidget(
            self.auth_imp_desc, 0,
        )

        self.grid_layout_6.addLayout(
            self.ask_auth_content_vertical_layout, 0, 0, 1, 1,
        )

        self.imp_operation_auth_toggle_button = ToggleSwitch(
            self.imp_operation_frame,
        )
        self.imp_operation_auth_toggle_button.setObjectName(
            'imp_operation_auth_toggle_button',
        )
        self.imp_operation_auth_toggle_button.setAccessibleName(
            ASK_AUTH_FOR_IMPORTANT_QUESTION_TOGGLE,
        )
        self.imp_operation_auth_toggle_button.setMinimumSize(QSize(50, 35))
        self.imp_operation_auth_toggle_button.setMaximumSize(QSize(50, 35))
        self.imp_operation_auth_toggle_button.setStyleSheet(
            'border: 1px solid white',
        )
        self.grid_layout_6.addWidget(
            self.imp_operation_auth_toggle_button, 0, 1, 1, 1,
        )
        self.ask_auth_login_frame = QFrame(self.settings_widget)
        self.ask_auth_login_frame.setObjectName('ask_auth_login_frame')
        self.ask_auth_login_frame.setAccessibleName(ASK_AUTH_FOR_APP_LOGIN)
        self.ask_auth_login_frame.setMinimumSize(QSize(492, 92))
        self.ask_auth_login_frame.setMaximumWidth(492)
        self.ask_auth_login_frame.setStyleSheet('')
        self.ask_auth_login_frame.setFrameShape(QFrame.StyledPanel)
        self.ask_auth_login_frame.setFrameShadow(QFrame.Raised)
        self.grid_layout_5 = QGridLayout(self.ask_auth_login_frame)
        self.grid_layout_5.setObjectName('gridLayout_5')
        self.ask_auth_login_content_vertical_layout = QVBoxLayout()
        self.ask_auth_login_content_vertical_layout.setObjectName(
            'ask_auth_login_content_vertical_layout',
        )
        self.login_auth_label = QLabel(self.ask_auth_login_frame)
        self.login_auth_label.setObjectName('login_auth_label')
        self.login_auth_label.setStyleSheet('')
        self.login_auth_label.setAlignment(Qt.AlignCenter)
        self.ask_auth_login_content_vertical_layout.addWidget(
            self.login_auth_label, 0, Qt.AlignLeft,
        )
        self.auth_login_desc = QLabel(self.ask_auth_login_frame)
        self.auth_login_desc.setObjectName('auth_login_desc')
        self.auth_login_desc.setWordWrap(True)
        self.auth_login_desc.setMinimumSize(QSize(385, 46))
        self.ask_auth_login_content_vertical_layout.addWidget(
            self.auth_login_desc, 0,
        )
        self.grid_layout_5.addLayout(
            self.ask_auth_login_content_vertical_layout, 0, 0, 1, 1,
        )
        self.login_auth_toggle_button = ToggleSwitch(self.ask_auth_login_frame)
        self.login_auth_toggle_button.setObjectName('login_auth_toggle_button')
        self.login_auth_toggle_button.setAccessibleName(
            ASK_AUTH_FOR_APP_LOGIN_TOGGLE,
        )
        self.login_auth_toggle_button.setMinimumSize(QSize(50, 35))
        self.login_auth_toggle_button.setMaximumSize(QSize(50, 35))
        self.login_auth_toggle_button.setStyleSheet('border: 1px solid white')

        self.grid_layout_5.addWidget(self.login_auth_toggle_button, 0, 1, 1, 1)

        self.hide_exhausted_asset_frame = QFrame(self.settings_widget)
        self.hide_exhausted_asset_frame.setObjectName(
            'hide_exhausted_asset_frame',
        )
        self.hide_exhausted_asset_frame.setAccessibleName(
            HIDE_EXHAUSTED_ASSETS,
        )
        self.hide_exhausted_asset_frame.setMinimumSize(QSize(492, 92))
        self.hide_exhausted_asset_frame.setMaximumWidth(492)
        self.hide_exhausted_asset_frame.setStyleSheet('')
        self.hide_exhausted_asset_frame.setFrameShape(QFrame.StyledPanel)
        self.hide_exhausted_asset_frame.setFrameShadow(QFrame.Raised)
        self.grid_layout_2 = QGridLayout(self.hide_exhausted_asset_frame)
        self.grid_layout_2.setObjectName('gridLayout_2')
        self.hide_exhausted_asset_toggle_button = ToggleSwitch(
            self.hide_exhausted_asset_frame,
        )
        self.hide_exhausted_asset_toggle_button.setObjectName(
            'hide_exhausted_asset_toggle_button',
        )
        self.hide_exhausted_asset_toggle_button.setAccessibleName(
            HIDE_EXHAUSTED_ASSETS_TOGGLE,
        )
        self.hide_exhausted_asset_toggle_button.setMinimumSize(QSize(50, 35))
        self.hide_exhausted_asset_toggle_button.setMaximumSize(QSize(50, 35))
        self.hide_exhausted_asset_toggle_button.setStyleSheet(
            'border: 1px solid white',
        )

        self.grid_layout_2.addWidget(
            self.hide_exhausted_asset_toggle_button, 0, 1, 1, 1,
        )

        self.hide_exhausted_asset_layout = QVBoxLayout()
        self.hide_exhausted_asset_layout.setObjectName(
            'hide_exhausted_asset_layout',
        )
        self.hide_exhausted_label = QLabel(self.hide_exhausted_asset_frame)
        self.hide_exhausted_label.setObjectName('hide_exhausted_label')
        self.hide_exhausted_label.setStyleSheet('')
        self.hide_exhausted_label.setAlignment(Qt.AlignCenter)

        self.hide_exhausted_asset_layout.addWidget(
            self.hide_exhausted_label, 0, Qt.AlignLeft,
        )
        self.hide_asset_desc = QLabel(self.hide_exhausted_asset_frame)
        self.hide_asset_desc.setWordWrap(True)
        self.hide_asset_desc.setObjectName('hide_asset_desc')
        self.hide_asset_desc.setMinimumSize(QSize(385, 46))

        self.hide_exhausted_asset_layout.addWidget(self.hide_asset_desc)

        self.grid_layout_2.addLayout(
            self.hide_exhausted_asset_layout, 0, 0, 1, 1,
        )
        self.keyring_storage_frame = QFrame(self.settings_widget)
        self.keyring_storage_frame.setObjectName(
            'keyring_storage_frame',
        )
        self.keyring_storage_frame.setAccessibleName(KEYRING_STORAGE)
        self.keyring_storage_frame.setMinimumSize(QSize(492, 79))
        self.keyring_storage_frame.setMaximumWidth(492)
        self.keyring_storage_frame.setFrameShape(QFrame.StyledPanel)
        self.keyring_storage_frame.setFrameShadow(QFrame.Raised)
        self.grid_layout_keyring = QGridLayout(self.keyring_storage_frame)
        self.grid_layout_keyring.setObjectName('grid_layout_keyring')
        self.keyring_toggle_button = ToggleSwitch(
            self.keyring_storage_frame,
        )
        self.keyring_toggle_button.setObjectName(
            'keyring_toggle_button',
        )
        self.keyring_toggle_button.setAccessibleName(KEYRING_TOGGLE_BUTTON)
        self.keyring_toggle_button.setMinimumSize(QSize(50, 35))
        self.keyring_toggle_button.setMaximumSize(QSize(50, 35))
        self.keyring_toggle_button.setStyleSheet(
            'border: 1px solid white',
        )

        self.grid_layout_keyring.addWidget(
            self.keyring_toggle_button, 0, 1, 1, 1,
        )

        self.keyring_frame_layout = QVBoxLayout()
        self.keyring_frame_layout.setObjectName(
            'keyring_frame_layout',
        )
        self.keyring_label = QLabel(self.keyring_storage_frame)
        self.keyring_label.setObjectName('keyring_label')
        self.keyring_label.setAlignment(Qt.AlignCenter)

        self.keyring_frame_layout.addWidget(
            self.keyring_label, 0, Qt.AlignLeft,
        )
        self.keyring_desc = QLabel(self.keyring_storage_frame)
        self.keyring_desc.setWordWrap(True)
        self.keyring_desc.setObjectName('keyring_desc')
        self.keyring_desc.setMinimumSize(QSize(385, 46))
        self.keyring_frame_layout.addWidget(
            self.keyring_desc, 0, Qt.AlignLeft,
        )
        self.grid_layout_keyring.addLayout(
            self.keyring_frame_layout, 0, 0, 1, 1,
        )
        self.stack_1_spacer = QSpacerItem(
            20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding,
        )
        self.stack_2_vertical_layout = QVBoxLayout()
        self.stack_2_vertical_layout.setSpacing(10)
        self.stack_2_vertical_layout.setObjectName('stack_2_vertical_layout')
        self.set_fee_rate_frame = ConfigurableCardFrame(
            self,
            ConfigurableCardModel(
                title_label=QCoreApplication.translate(
                    IRIS_WALLET_TRANSLATIONS_CONTEXT, 'set_default_fee', None,
                ),
                title_desc=QCoreApplication.translate(
                    IRIS_WALLET_TRANSLATIONS_CONTEXT,
                    'set_default_fee_send',
                    None,
                ),
                suggestion_desc=QCoreApplication.translate(
                    IRIS_WALLET_TRANSLATIONS_CONTEXT,
                    'set_fee_rate_value_label',
                    None,
                ),
                placeholder_value=str(self.fee_rate),
            ),
        )
        self.set_fee_rate_frame.setAccessibleName(SET_DEFAULT_FEE_RATE)
        self.set_expiry_time_frame = ConfigurableCardFrame(
            self,
            ConfigurableCardModel(
                title_label=QCoreApplication.translate(
                    IRIS_WALLET_TRANSLATIONS_CONTEXT, 'set_default_expiry_time', None,
                ),
                title_desc=QCoreApplication.translate(
                    IRIS_WALLET_TRANSLATIONS_CONTEXT,
                    'set_default_expiry_time_desc',
                    None,
                ),
                suggestion_desc=QCoreApplication.translate(
                    IRIS_WALLET_TRANSLATIONS_CONTEXT,
                    'input_expiry_time_desc',
                    None,
                ),
                placeholder_value=self.expiry_time,
            ),

        )
        self.set_expiry_time_frame.setAccessibleName(SET_DEFAULT_EXP_TIME)
        self.set_indexer_url_frame = ConfigurableCardFrame(
            self,
            ConfigurableCardModel(
                title_label=QCoreApplication.translate(
                    IRIS_WALLET_TRANSLATIONS_CONTEXT, 'set_indexer_url', None,
                ),
                title_desc=QCoreApplication.translate(
                    IRIS_WALLET_TRANSLATIONS_CONTEXT,
                    'set_indexer_url_desc',
                    None,
                ),
                placeholder_value=self.indexer_url,
            ),
        )
        self.set_indexer_url_frame.setAccessibleName(SPECIFY_INDEXER_URL)
        self.set_proxy_endpoint_frame = ConfigurableCardFrame(
            self,
            ConfigurableCardModel(
                title_label=QCoreApplication.translate(
                    IRIS_WALLET_TRANSLATIONS_CONTEXT, 'set_proxy_endpoint', None,
                ),
                title_desc=QCoreApplication.translate(
                    IRIS_WALLET_TRANSLATIONS_CONTEXT,
                    'set_proxy_endpoint_desc',
                    None,
                ),
                placeholder_value=self.proxy_endpoint,
            ),
        )
        self.set_proxy_endpoint_frame.setAccessibleName(SPECIFY_RGB_PROXY_URL)
        self.set_bitcoind_rpc_host_frame = ConfigurableCardFrame(
            self,
            ConfigurableCardModel(
                title_label=QCoreApplication.translate(
                    IRIS_WALLET_TRANSLATIONS_CONTEXT, 'set_bitcoind_host', None,
                ),
                title_desc=QCoreApplication.translate(
                    IRIS_WALLET_TRANSLATIONS_CONTEXT,
                    'set_bitcoind_host_desc',
                    None,
                ),
                placeholder_value=self.bitcoind_host,
            ),
        )
        self.set_bitcoind_rpc_host_frame.setAccessibleName(
            SPECIFY_BITCOIND_HOST,
        )
        self.set_bitcoind_rpc_port_frame = ConfigurableCardFrame(
            self,
            ConfigurableCardModel(
                title_label=QCoreApplication.translate(
                    IRIS_WALLET_TRANSLATIONS_CONTEXT, 'set_bitcoind_port', None,
                ),
                title_desc=QCoreApplication.translate(
                    IRIS_WALLET_TRANSLATIONS_CONTEXT,
                    'set_bitcoind_port_desc',
                    None,
                ),
                placeholder_value=self.bitcoind_port,
            ),
        )
        self.set_bitcoind_rpc_port_frame.setAccessibleName(
            SPECIFY_BITCOIND_PORT,
        )
        self.set_announce_address_frame = ConfigurableCardFrame(
            self,
            ConfigurableCardModel(
                title_label=QCoreApplication.translate(
                    IRIS_WALLET_TRANSLATIONS_CONTEXT, 'set_announce_address', None,
                ),
                title_desc=QCoreApplication.translate(
                    IRIS_WALLET_TRANSLATIONS_CONTEXT,
                    'set_announce_address_desc',
                    None,
                ),
                placeholder_value=self.announce_address,
            ),
        )
        self.set_announce_address_frame.setAccessibleName(SPECIFY_ANNOUNCE_ADD)
        self.set_announce_alias_frame = ConfigurableCardFrame(
            self,
            ConfigurableCardModel(
                title_label=QCoreApplication.translate(
                    IRIS_WALLET_TRANSLATIONS_CONTEXT, 'set_announce_alias', None,
                ),
                title_desc=QCoreApplication.translate(
                    IRIS_WALLET_TRANSLATIONS_CONTEXT,
                    'set_announce_alias_desc',
                    None,
                ),
                placeholder_value=self.announce_alias,
            ),
        )
        self.set_announce_alias_frame.setAccessibleName(SPECIFY_ANNOUNCE_ALIAS)
        self.set_minimum_confirmation_frame = ConfigurableCardFrame(
            self,
            ConfigurableCardModel(
                title_label=QCoreApplication.translate(
                    IRIS_WALLET_TRANSLATIONS_CONTEXT, 'set_minimum_confirmation', None,
                ),
                title_desc=QCoreApplication.translate(
                    IRIS_WALLET_TRANSLATIONS_CONTEXT,
                    'set_minimum_confirmation_desc',
                    None,
                ),
                placeholder_value=self.min_confirmation,
            ),
        )
        self.set_minimum_confirmation_frame.setAccessibleName(
            SET_DEFAULT_MIN_EXPIRATION,
        )

        stack_1_widgets = [
            self.imp_operation_frame,
            self.ask_auth_login_frame,
            self.hide_exhausted_asset_frame,
            self.keyring_storage_frame,
            self.set_fee_rate_frame,
            self.set_expiry_time_frame,
            self.set_minimum_confirmation_frame,
        ]
        for widget in stack_1_widgets:
            self.stack_1_vertical_layout.addWidget(widget, 0, Qt.AlignLeft)

        self.stack_1_vertical_layout.addItem(self.stack_1_spacer)

        self.card_horizontal_layout_settings.addLayout(
            self.stack_1_vertical_layout,
        )

        stack_2_widgets = [
            self.set_indexer_url_frame,
            self.set_proxy_endpoint_frame,
            self.set_bitcoind_rpc_host_frame,
            self.set_bitcoind_rpc_port_frame,
            self.set_announce_address_frame,
            self.set_announce_alias_frame,
        ]
        for widget in stack_2_widgets:
            self.stack_2_vertical_layout.addWidget(widget, 0, Qt.AlignLeft)
        self.stack_2_spacer = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding,
        )
        self.stack_2_vertical_layout.addItem(self.stack_2_spacer)

        self.card_horizontal_layout_settings.addLayout(
            self.stack_2_vertical_layout,
        )

        self.horizontal_spacer = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum,
        )
        self.card_horizontal_layout_settings.addItem(self.horizontal_spacer)
        self.vertical_layout_6.addLayout(self.card_horizontal_layout_settings)
        self.widget__vertical_spacer = QSpacerItem(
            20, 1000, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding,
        )
        self.vertical_layout_6.addItem(self.widget__vertical_spacer)
        self.grid_layout.addWidget(self.settings_widget, 0, 0, 1, 1)
        self.__loading_translucent_screen = LoadingTranslucentScreen(
            parent=self, description_text=INFO_VALIDATION_OF_NODE_PASSWORD_AND_KEYRING_ACCESS, dot_animation=True,
        )
        self.setup_ui_connection()
        self.retranslate_ui()
        self.on_page_load()

    def retranslate_ui(self):
        """Retranslate the UI elements."""
        self.settings_label.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'settings', None,
            ),
        )
        self.imp_operation_label.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'auth_important_ops', None,
            ),
        )
        self.auth_imp_desc.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'auth_spending_ops', None,
            ),
        )
        self.login_auth_label.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'auth_login', None,
            ),
        )
        self.auth_login_desc.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'enable_auth_login', None,
            ),
        )
        self.hide_exhausted_label.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'hide_exhausted_assets', None,
            ),
        )
        self.hide_asset_desc.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT,
                'hide_zero_balance_assets',
                None,
            ),
        )
        self.keyring_label.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'keyring_label', 'Keyring storage',
            ),
        )
        self.keyring_desc.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'keyring_desc', 'Store sensitive data, such as passwords and mnemonics, in the keyring.',
            ),
        )
        self.handle_keyring_toggle_status()

    def setup_ui_connection(self):
        """Set up connections for UI elements."""
        self.login_auth_toggle_button.clicked.connect(
            self.handle_login_auth_toggle_button,
        )
        self.imp_operation_auth_toggle_button.clicked.connect(
            self.handle_imp_operation_auth_toggle_button,
        )
        self.hide_exhausted_asset_toggle_button.clicked.connect(
            self.handle_hide_exhausted_asset_toggle_button,
        )
        self.keyring_toggle_button.clicked.connect(
            self.handle_keyring_storage,
        )
        self._view_model.setting_view_model.native_auth_enable_event.connect(
            self.imp_operation_auth_toggle_button.setChecked,
        )
        self._view_model.setting_view_model.native_auth_logging_event.connect(
            self.login_auth_toggle_button.setChecked,
        )
        self._view_model.setting_view_model.on_page_load_event.connect(
            self.handle_on_page_load,
        )
        self._view_model.setting_view_model.on_success_validation_keyring_event.connect(
            self.handle_keyring_toggle_status,
        )
        self._view_model.setting_view_model.on_error_validation_keyring_event.connect(
            self.handle_keyring_toggle_status,
        )
        self._view_model.setting_view_model.loading_status.connect(
            self.show_loading_screen,
        )
        self._view_model.setting_view_model.is_loading.connect(
            self._update_loading_state,
        )
        click_handlers = {
            self.set_fee_rate_frame: self.handle_fee_rate_frame,
            self.set_expiry_time_frame: self.handle_expiry_time_frame,
            self.set_indexer_url_frame: self.handle_indexer_url_frame,
            self.set_proxy_endpoint_frame: self.handle_proxy_endpoint_frame,
            self.set_bitcoind_rpc_host_frame: self.handle_bitcoind_host_frame,
            self.set_bitcoind_rpc_port_frame: self.handle_bitcoind_port_frame,
            self.set_announce_address_frame: self.handle_announce_address_frame,
            self.set_announce_alias_frame: self.handle_announce_alias_frame,
            self.set_minimum_confirmation_frame: self.handle_minimum_confirmation_frame,
        }
        for widget, handler in click_handlers.items():
            widget.clicked.connect(handler)
        save_handlers = {
            self.set_fee_rate_frame.save_button: self._set_fee_rate_value,
            self.set_expiry_time_frame.save_button: self._set_expiry_time,
            self.set_indexer_url_frame.save_button: self._set_indexer_url,
            self.set_proxy_endpoint_frame.save_button: self._set_proxy_endpoint,
            self.set_bitcoind_rpc_host_frame.save_button: self._set_bitcoind_host,
            self.set_bitcoind_rpc_port_frame.save_button: self._set_bitcoind_port,
            self.set_announce_address_frame.save_button: self._set_announce_address,
            self.set_announce_alias_frame.save_button: self._set_announce_alias,
            self.set_minimum_confirmation_frame.save_button: self._set_min_confirmation,
        }
        for save_button, handler in save_handlers.items():
            save_button.clicked.connect(handler)

    def _set_fee_rate_value(self):
        """Set the default fee rate value based on user input."""
        self._view_model.setting_view_model.set_default_fee_rate(
            self.set_fee_rate_frame.input_value.text(),
        )

    def _set_expiry_time(self):
        """Set the default expiry time based on user input."""
        self._view_model.setting_view_model.set_default_expiry_time(
            self.set_expiry_time_frame.input_value.text(
            ), self.set_expiry_time_frame.time_unit_combobox.currentText(),
        )

    def _set_indexer_url(self):
        """Set the default indexer url based on user input. """
        password = check_keyring_state_for_password(self, self._view_model)
        if password:
            self._view_model.setting_view_model.check_indexer_url_endpoint(
                self.set_indexer_url_frame.input_value.text(), password,
            )

    def _set_proxy_endpoint(self):
        """Set the default proxy endpoint based on user input."""
        password = check_keyring_state_for_password(self, self._view_model)
        if password:
            self._view_model.setting_view_model.check_proxy_endpoint(
                self.set_proxy_endpoint_frame.input_value.text(), password,
            )

    def _set_bitcoind_host(self):
        """ Set the default bitcoind host based on user input."""
        password = check_keyring_state_for_password(self, self._view_model)
        if password:
            self._view_model.setting_view_model.set_bitcoind_host(
                self.set_bitcoind_rpc_host_frame.input_value.text(), password,
            )

    def _set_bitcoind_port(self):
        """Set the default bitcoind port based on user input."""
        password = check_keyring_state_for_password(self, self._view_model)
        if password:
            self._view_model.setting_view_model.set_bitcoind_port(
                int(self.set_bitcoind_rpc_port_frame.input_value.text()), password,
            )

    def _set_announce_address(self):
        """Set the default announce address based on user input."""
        password = check_keyring_state_for_password(self, self._view_model)
        if password:
            self._view_model.setting_view_model.set_announce_address(
                self.set_announce_address_frame.input_value.text(), password,
            )

    def _set_announce_alias(self):
        """Set the default announce alias based on user input."""
        password = check_keyring_state_for_password(self, self._view_model)
        if password:
            self._view_model.setting_view_model.set_announce_alias(
                self.set_announce_alias_frame.input_value.text(), password,
            )

    def _set_min_confirmation(self):
        """Set the default minimum confirmation based on user input."""
        self._view_model.setting_view_model.set_min_confirmation(
            int(self.set_minimum_confirmation_frame.input_value.text()),
        )

    def handle_imp_operation_auth_toggle_button(self):
        """Handle the toggle button for important operation authentication."""
        self._view_model.setting_view_model.enable_native_authentication(
            self.imp_operation_auth_toggle_button.isChecked(),
        )

    def handle_login_auth_toggle_button(self):
        """Handle the toggle button for login authentication."""
        self._view_model.setting_view_model.enable_native_logging(
            self.login_auth_toggle_button.isChecked(),
        )

    def handle_hide_exhausted_asset_toggle_button(self):
        """Handle the toggle button for hiding exhausted assets."""
        self._view_model.setting_view_model.enable_exhausted_asset(
            self.hide_exhausted_asset_toggle_button.isChecked(),
        )

    def on_page_load(self):
        """Handle the page load event."""
        self._view_model.setting_view_model.on_page_load()

    def handle_on_page_load(self, response: SettingPageLoadModel):
        """Handle on page load event callback"""
        self.imp_operation_auth_toggle_button.setChecked(
            response.status_of_native_auth.is_enabled,
        )
        self.login_auth_toggle_button.setChecked(
            response.status_of_native_logging_auth.is_enabled,
        )
        self.hide_exhausted_asset_toggle_button.setChecked(
            response.status_of_exhausted_asset.is_enabled,
        )
        self.fee_rate = response.value_of_default_fee.fee_rate
        self.expiry_time = response.value_of_default_expiry_time.time
        self.expiry_time_unit = response.value_of_default_expiry_time.unit
        self.indexer_url = response.value_of_default_indexer_url.url
        self.proxy_endpoint = response.value_of_default_proxy_endpoint.endpoint
        self.bitcoind_host = response.value_of_default_bitcoind_rpc_host.host
        self.bitcoind_port = response.value_of_default_bitcoind_rpc_port.port
        self.announce_address = response.value_of_default_announce_address.address
        self.announce_alias = response.value_of_default_announce_alias.alias
        self.min_confirmation = response.value_of_default_min_confirmation.min_confirmation

    def handle_keyring_toggle_status(self):
        """Updates the keyring toggle button status based on the stored keyring state."""
        stored_keyring_status = SettingRepository.get_keyring_status()
        self.keyring_toggle_button.setChecked(not stored_keyring_status)
        self.ask_auth_login_frame.setDisabled(stored_keyring_status)
        self.imp_operation_frame.setDisabled(stored_keyring_status)
        if stored_keyring_status is True:
            message = QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'auth_keyring_message', None,
            )
            self.auth_login_desc.setText(message)
            self.auth_imp_desc.setText(message)

            self.imp_operation_auth_toggle_button.hide()
            self.login_auth_toggle_button.hide()

    def handle_on_error(self, message: str):
        """Handle error message"""
        self.handle_keyring_toggle_status()
        ToastManager.error(message)

    def handle_keyring_storage(self):
        """Handles keyring storage operations by applying a blur effect to the UI and
        determining the appropriate dialog to display based on the stored keyring status."""
        stored_keyring_status = SettingRepository.get_keyring_status()
        if stored_keyring_status is False:
            network: NetworkEnumModel = SettingRepository.get_wallet_network()
            mnemonic: str = get_value(MNEMONIC_KEY, network.value)
            password: str = get_value(WALLET_PASSWORD_KEY, network.value)
            keyring_dialog = KeyringErrorDialog(
                mnemonic=mnemonic,
                password=password,
                parent=self,
                originating_page='settings_page',
                navigate_to=self._view_model.page_navigation.settings_page,
            )
            keyring_dialog.error.connect(self.handle_on_error)
            keyring_dialog.finished.connect(
                self.handle_keyring_toggle_status(),
            )
            keyring_dialog.exec()
        if stored_keyring_status is True:
            mnemonic_dialog = RestoreMnemonicWidget(
                parent=self, view_model=self._view_model, origin_page='setting_page',
            )
            mnemonic_dialog.finished.connect(
                self.handle_keyring_toggle_status(),
            )
            mnemonic_dialog.exec()

    def show_loading_screen(self, status):
        """This method handled show loading screen on wallet selection page"""
        sidebar = self._view_model.page_navigation.sidebar()
        if status is True:
            sidebar.setDisabled(True)
            self.__loading_translucent_screen.start()
        if not status:
            sidebar.setDisabled(False)
            self.__loading_translucent_screen.stop()
            self._view_model.page_navigation.settings_page()

    def _update_loading_state(self, is_loading: bool):
        """Updates the loading state for all relevant frames save buttons."""
        frames = [
            self.set_indexer_url_frame,
            self.set_proxy_endpoint_frame,
            self.set_bitcoind_rpc_host_frame,
            self.set_bitcoind_rpc_port_frame,
            self.set_announce_address_frame,
            self.set_announce_alias_frame,
        ]
        for frame in frames:
            if is_loading:
                frame.save_button.start_loading()
            else:
                frame.save_button.stop_loading()

    def handle_fee_rate_frame(self):
        """Handle the frame for setting the fee rate."""
        set_frame_content(
            self.set_fee_rate_frame,
            self.fee_rate,
            validator=QIntValidator(),
            suggestion_desc=self.set_fee_rate_frame.suggestion_desc,
        )

    def handle_expiry_time_frame(self):
        """Handle the frame for setting the expiry time and unit."""
        set_frame_content(
            self.set_expiry_time_frame,
            self.expiry_time,
            validator=QIntValidator(),
            suggestion_desc=self.set_expiry_time_frame.suggestion_desc,
            time_unit_combobox=self.set_expiry_time_frame.time_unit_combobox,

        )
        self.set_expiry_time_frame.time_unit_combobox.setCurrentText(
            str(self.expiry_time_unit),
        )

    def handle_indexer_url_frame(self):
        """Handle the frame for setting the indexer url."""
        set_frame_content(
            self.set_indexer_url_frame,
            self.indexer_url,
        )

    def handle_proxy_endpoint_frame(self):
        """Handle the frame for setting the proxy endpoint."""
        set_frame_content(
            self.set_proxy_endpoint_frame,
            self.proxy_endpoint,
        )

    def handle_bitcoind_host_frame(self):
        """Handle the frame for setting the bitcoind host."""
        set_frame_content(
            self.set_bitcoind_rpc_host_frame,
            self.bitcoind_host,
        )

    def handle_bitcoind_port_frame(self):
        """Handle the frame for setting the bitcoind port."""
        set_frame_content(
            self.set_bitcoind_rpc_port_frame,
            self.bitcoind_port,
            validator=QIntValidator(),
        )

    def handle_announce_address_frame(self):
        """Handle the frame for setting the announce address."""
        set_frame_content(
            self.set_announce_address_frame,
            self.announce_address,
        )

    def handle_announce_alias_frame(self):
        """Handle the frame for setting the announce alias."""
        set_frame_content(
            self.set_announce_alias_frame,
            self.announce_alias,
        )

    def handle_minimum_confirmation_frame(self):
        """Handle the frame for setting the minimum confirmation."""
        set_frame_content(
            self.set_minimum_confirmation_frame,
            self.min_confirmation,
            QIntValidator(),
        )
