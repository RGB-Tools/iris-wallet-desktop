# pylint: disable=too-many-instance-attributes, too-many-statements,implicit-str-concat
"""This module contains the AboutWidget,
 which represents the UI for about page.
 """
from __future__ import annotations

from PySide6.QtCore import QCoreApplication
from PySide6.QtCore import QDir
from PySide6.QtCore import QSize
from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor
from PySide6.QtWidgets import QFileDialog
from PySide6.QtWidgets import QGridLayout
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtWidgets import QSpacerItem
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QWidget

from accessible_constant import ANNOUNCE_ADDRESS_ACCESSIBLE_DESCRIPTION
from accessible_constant import ANNOUNCE_ADDRESS_COPY_BUTTON
from accessible_constant import ANNOUNCE_ALIAS_ACCESSIBLE_DESCRIPTION
from accessible_constant import ANNOUNCE_ALIAS_COPY_BUTTON
from accessible_constant import BITCOIND_HOST_ACCESSIBLE_DESCRIPTION
from accessible_constant import BITCOIND_HOST_COPY_BUTTON
from accessible_constant import BITCOIND_PORT_ACCESSIBLE_DESCRIPTION
from accessible_constant import BITCOIND_PORT_COPY_BUTTON
from accessible_constant import DOWNLOAD_DEBUG_LOG
from accessible_constant import INDEXER_URL_ACCESSIBLE_DESCRIPTION
from accessible_constant import INDEXER_URL_COPY_BUTTON
from accessible_constant import LN_PEER_LISTENING_PORT_ACCESSIBLE_DESCRIPTION
from accessible_constant import LN_PEER_LISTENING_PORT_COPY_BUTTON
from accessible_constant import NODE_PUBKEY_ACCESSIBLE_DESCRIPTION
from accessible_constant import NODE_PUBKEY_COPY_BUTTON
from accessible_constant import RGB_PROXY_URL_ACCESSIBLE_DESCRIPTION
from accessible_constant import RGB_PROXY_URL_COPY_BUTTON
from src.data.repository.setting_repository import SettingRepository
from src.model.common_operation_model import NodeInfoResponseModel
from src.model.common_operation_model import UnlockRequestModel
from src.model.enums.enums_model import ToastPreset
from src.model.enums.enums_model import WalletType
from src.model.node_info_model import NodeInfoModel
from src.utils.common_utils import download_file
from src.utils.common_utils import network_info
from src.utils.common_utils import zip_logger_folder
from src.utils.constant import ANNOUNCE_ADDRESS
from src.utils.constant import ANNOUNCE_ALIAS
from src.utils.constant import IRIS_WALLET_TRANSLATIONS_CONTEXT
from src.utils.constant import LDK_PORT_KEY
from src.utils.constant import PRIVACY_POLICY_URL
from src.utils.constant import TERMS_OF_SERVICE_URL
from src.utils.helpers import get_bitcoin_config
from src.utils.helpers import load_stylesheet
from src.utils.info_message import INFO_DOWNLOAD_CANCELED
from src.utils.local_store import local_store
from src.version import __version__
from src.viewmodels.main_view_model import MainViewModel
from src.views.components.header_frame import HeaderFrame
from src.views.components.toast import ToastManager
from src.views.components.wallet_detail_frame import NodeInfoWidget


class AboutWidget(QWidget):
    """This class represents all the UI elements of the about page."""

    def __init__(self, view_model):
        super().__init__()
        self._view_model: MainViewModel = view_model
        self.network: str = ''
        network_info(self)
        get_node_info = NodeInfoModel()
        self.node_info: NodeInfoResponseModel = get_node_info.node_info
        wallet_type: WalletType = SettingRepository.get_wallet_type()
        self.ldk_port = local_store.get_value(LDK_PORT_KEY)
        self.setStyleSheet(load_stylesheet('views/qss/about_style.qss'))
        self.grid_layout = QGridLayout(self)
        self.grid_layout.setSpacing(0)
        self.grid_layout.setObjectName('grid_layout')
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.about_widget = QWidget(self)
        self.about_widget.setObjectName('about_widget')
        self.about_widget.setMinimumSize(QSize(492, 80))
        self.vertical_layout = QVBoxLayout(self.about_widget)
        self.vertical_layout.setSpacing(25)
        self.vertical_layout.setObjectName('vertical_layout')
        self.vertical_layout.setContentsMargins(25, 12, 25, -1)
        self.about_frame = HeaderFrame(
            title_logo_path=':/assets/about.png', title_name='about',
        )
        self.about_frame.refresh_page_button.hide()
        self.about_frame.action_button.hide()
        self.vertical_layout.addWidget(self.about_frame)

        self.about_vertical_layout = QVBoxLayout()
        self.about_vertical_layout.setSpacing(20)
        self.about_vertical_layout.setObjectName('about_vertical_layout')
        self.about_vertical_layout.setContentsMargins(10, -1, -1, -1)
        self.app_version_label = QLabel(self.about_widget)
        self.app_version_label.setObjectName('app_version_label')
        self.app_version_label.setAlignment(Qt.AlignCenter)

        self.about_vertical_layout.addWidget(
            self.app_version_label, 0, Qt.AlignLeft,
        )

        self.node_pub_key_frame = NodeInfoWidget(
            translation_key='node_pubkey', value=self.node_info.pubkey, v_layout=self.about_vertical_layout,
        )
        self.node_pub_key_frame.value_label.setAccessibleDescription(
            NODE_PUBKEY_ACCESSIBLE_DESCRIPTION,
        )
        self.node_pub_key_frame.node_pub_key_copy_button.setAccessibleName(
            NODE_PUBKEY_COPY_BUTTON,
        )
        self.get_bitcoin_config: UnlockRequestModel = get_bitcoin_config(
            self.network, password='',
        )
        if wallet_type.value == WalletType.EMBEDDED_TYPE_WALLET.value:
            self.ldk_port_frame = NodeInfoWidget(
                translation_key='ln_ldk_port', value=self.ldk_port, v_layout=self.about_vertical_layout,
            )
            self.ldk_port_frame.value_label.setAccessibleDescription(
                LN_PEER_LISTENING_PORT_ACCESSIBLE_DESCRIPTION,
            )
            self.ldk_port_frame.node_pub_key_copy_button.setAccessibleName(
                LN_PEER_LISTENING_PORT_COPY_BUTTON,
            )
        self.bitcoind_host_frame = NodeInfoWidget(
            translation_key='bitcoind_host', value=self.get_bitcoin_config.bitcoind_rpc_host, v_layout=self.about_vertical_layout,
        )
        self.bitcoind_host_frame.node_pub_key_copy_button.setAccessibleName(
            BITCOIND_HOST_COPY_BUTTON,
        )
        self.bitcoind_host_frame.value_label.setAccessibleDescription(
            BITCOIND_HOST_ACCESSIBLE_DESCRIPTION,
        )

        self.bitcoind_port_frame = NodeInfoWidget(
            translation_key='bitcoind_port', value=self.get_bitcoin_config.bitcoind_rpc_port, v_layout=self.about_vertical_layout,
        )
        self.bitcoind_port_frame.node_pub_key_copy_button.setAccessibleName(
            BITCOIND_PORT_COPY_BUTTON,
        )
        self.bitcoind_port_frame.value_label.setAccessibleDescription(
            BITCOIND_PORT_ACCESSIBLE_DESCRIPTION,
        )

        self.indexer_url_frame = NodeInfoWidget(
            translation_key='indexer_url', value=self.get_bitcoin_config.indexer_url, v_layout=self.about_vertical_layout,
        )
        self.indexer_url_frame.node_pub_key_copy_button.setAccessibleName(
            INDEXER_URL_COPY_BUTTON,
        )
        self.indexer_url_frame.value_label.setAccessibleDescription(
            INDEXER_URL_ACCESSIBLE_DESCRIPTION,
        )

        self.proxy_url_frame = NodeInfoWidget(
            translation_key='proxy_url', value=self.get_bitcoin_config.proxy_endpoint, v_layout=self.about_vertical_layout,
        )
        self.proxy_url_frame.node_pub_key_copy_button.setAccessibleName(
            RGB_PROXY_URL_COPY_BUTTON,
        )
        self.proxy_url_frame.value_label.setAccessibleDescription(
            RGB_PROXY_URL_ACCESSIBLE_DESCRIPTION,
        )

        if self.get_bitcoin_config.announce_addresses[0] != ANNOUNCE_ADDRESS:
            if isinstance(self.get_bitcoin_config.announce_addresses, list):
                value = ', '.join(
                    str(item) for item in self.get_bitcoin_config.announce_addresses
                )
            self.announce_address_frame = NodeInfoWidget(
                translation_key='announce_address', value=value, v_layout=self.about_vertical_layout,
            )
            self.announce_address_frame.node_pub_key_copy_button.setAccessibleName(
                ANNOUNCE_ADDRESS_COPY_BUTTON,
            )
            self.announce_address_frame.value_label.setAccessibleDescription(
                ANNOUNCE_ADDRESS_ACCESSIBLE_DESCRIPTION,
            )
        if self.get_bitcoin_config.announce_alias != ANNOUNCE_ALIAS:
            self.announce_alias_frame = NodeInfoWidget(
                translation_key='announce_alias', value=self.get_bitcoin_config.announce_alias, v_layout=self.about_vertical_layout,
            )
            self.announce_alias_frame.node_pub_key_copy_button.setAccessibleName(
                ANNOUNCE_ALIAS_COPY_BUTTON,
            )
            self.announce_alias_frame.value_label.setAccessibleDescription(
                ANNOUNCE_ALIAS_ACCESSIBLE_DESCRIPTION,
            )

        basepath = local_store.get_path()
        self.data_directory_path = NodeInfoWidget(
            translation_key='data_directory_path_label', value=basepath, v_layout=self.about_vertical_layout,
        )

        connection_type: WalletType = SettingRepository.get_wallet_type()

        self.rln_node_connection_type = NodeInfoWidget(
            translation_key='connection_type', value=connection_type.value.capitalize(), v_layout=self.about_vertical_layout,
        )

        basepath = local_store.get_path()
        self.data_directory_path = NodeInfoWidget(
            translation_key='data_directory_path_label', value=basepath, v_layout=self.about_vertical_layout,
        )

        connection_type: WalletType = SettingRepository.get_wallet_type()

        self.rln_node_connection_type = NodeInfoWidget(
            translation_key='connection_type', value=connection_type.value.capitalize(), v_layout=self.about_vertical_layout,
        )

        self.privacy_policy_label = QLabel(self.about_widget)
        self.privacy_policy_label.setObjectName('privacy_policy_label')
        self.privacy_policy_label.setTextInteractionFlags(
            Qt.TextBrowserInteraction,
        )
        self.privacy_policy_label.setOpenExternalLinks(True)
        self.about_vertical_layout.addWidget(self.privacy_policy_label)

        self.terms_service_label = QLabel(self.about_widget)
        self.terms_service_label.setObjectName('terms_service_label')
        self.terms_service_label.setTextInteractionFlags(
            Qt.TextBrowserInteraction,
        )
        self.terms_service_label.setOpenExternalLinks(True)
        self.about_vertical_layout.addWidget(self.terms_service_label)

        self.download_log = QPushButton()
        self.download_log.setCursor(
            QCursor(Qt.CursorShape.PointingHandCursor),
        )
        self.download_log.setAccessibleName(DOWNLOAD_DEBUG_LOG)
        self.download_log.setObjectName('download_log')
        self.download_log.setMinimumSize(QSize(280, 30))
        self.download_log.setMaximumSize(QSize(280, 30))

        self.about_vertical_layout.addWidget(self.download_log)

        self.vertical_layout.addLayout(self.about_vertical_layout)

        self.widget__vertical_spacer = QSpacerItem(
            20, 337, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding,
        )

        self.vertical_layout.addItem(self.widget__vertical_spacer)

        self.grid_layout.addWidget(self.about_widget, 0, 0, 1, 1)
        self.setup_ui_connection()

        self.retranslate_ui()

    def retranslate_ui(self):
        """Retranslate the UI elements."""
        self.privacy_policy_text = QCoreApplication.translate(
            IRIS_WALLET_TRANSLATIONS_CONTEXT, 'privacy_policy', None,
        )
        self.app_version_text = QCoreApplication.translate(
            IRIS_WALLET_TRANSLATIONS_CONTEXT, 'app_version', None,
        )
        self.terms_of_service_text = QCoreApplication.translate(
            IRIS_WALLET_TRANSLATIONS_CONTEXT, 'terms_of_service', None,
        )

        self.app_version_label.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, f'{self.app_version_text} {
                    __version__
                }-{self.network}', None,
            ),
        )
        self.privacy_policy_label.setText(
            f"< a style='color: #03CA9B;' href='{PRIVACY_POLICY_URL}'> {
                self.privacy_policy_text
            } < /a >",
        )
        self.terms_service_label.setText(
            f"< a style='color: #03CA9B;' href='{TERMS_OF_SERVICE_URL}' > {
                self.terms_of_service_text
            } < /a >",
        )
        self.download_log.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'download_debug_log', None,
            ),
        )
        self.rln_node_connection_type.key_label.setText(
            f"{
                QCoreApplication.translate(
                    IRIS_WALLET_TRANSLATIONS_CONTEXT, 'connection_type'
                )
            }:",
        )

    def setup_ui_connection(self):
        """Set up connections for UI elements."""
        self.download_log.clicked.connect(self.download_logs)

    def download_logs(self):
        """
        Handles the button click event to zip the logger folder and provide a save dialog.
        """
        # Base path where the logs folder is located
        base_path = local_store.get_path()

        # Zip the logger folder
        zip_filename, output_dir = zip_logger_folder(base_path)

        # Show a file dialog to save the zip file
        save_path, _ = QFileDialog.getSaveFileName(
            self, 'Save logs File', QDir.homePath() + '/' + zip_filename, 'Zip Files (*.zip)',
        )

        if save_path:
            download_file(save_path, output_dir)
        else:
            ToastManager.show_toast(
                self, ToastPreset.ERROR,
                description=INFO_DOWNLOAD_CANCELED,
            )
