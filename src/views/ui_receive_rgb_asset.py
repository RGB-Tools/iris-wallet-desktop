# pylint: disable=too-many-instance-attributes, too-many-statements, unused-import
"""This module contains the ReceiveRGBAssetWidget class,
 which represents the UI for receive cfa.
 """
from __future__ import annotations

from PySide6.QtCore import QCoreApplication
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QWidget

import src.resources_rc
from src.data.repository.setting_card_repository import SettingCardRepository
from src.model.enums.enums_model import AssetType
from src.model.enums.enums_model import ToastPreset
from src.model.selection_page_model import AssetDataModel
from src.utils.common_utils import copy_text
from src.utils.constant import IRIS_WALLET_TRANSLATIONS_CONTEXT
from src.utils.render_timer import RenderTimer
from src.viewmodels.main_view_model import MainViewModel
from src.views.components.loading_screen import LoadingTranslucentScreen
from src.views.components.receive_asset import ReceiveAssetWidget
from src.views.components.toast import ToastManager


class ReceiveRGBAssetWidget(QWidget):
    """This class represents all the UI elements of the Receive rgb asset page."""

    def __init__(self, view_model, params: AssetDataModel):
        super().__init__()
        self.render_timer = RenderTimer(task_name='ReceiveRGBAsset Rendering')
        self.render_timer.start()
        self._view_model: MainViewModel = view_model
        self.originating_page = params.asset_type
        self.asset_id = params.asset_id
        self.close_page_navigation = params.close_page_navigation
        self.expiry_time = params.expiry_time
        self.expiry_unit = params.expiry_unit
        self.default_min_confirmation = SettingCardRepository.get_default_min_confirmation()
        self.receive_rgb_asset_page = ReceiveAssetWidget(
            self._view_model,
            'CFA page',
            'cfa_address_info',
        )
        self.__loading_translucent_screen = LoadingTranslucentScreen(
            parent=self, description_text='Loading', dot_animation=True,
        )
        # Adding the receive asset widget to the layout of this widget
        layout = QVBoxLayout()
        layout.addWidget(self.receive_rgb_asset_page)
        self.setLayout(layout)
        self.generate_invoice()
        self.setup_ui_connection()

    def generate_invoice(self):
        """Call get rgb invoice to get invoice"""
        if self.originating_page in [
            'NIA',
            'fungibles',
            'CFA',
            'collectibles',
            'channel_management',
            'view_unspent_list',
            'faucets',
            'settings',
            'help',
            'about',
            'backup',
        ]:
            self._view_model.receive_cfa_view_model.get_rgb_invoice(
                self.default_min_confirmation.min_confirmation, self.asset_id,
            )

    def setup_ui_connection(self):
        """Set up connections for UI elements."""
        self.show_receive_rgb_loading()
        self.receive_rgb_asset_page.copy_button.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'copy_rgb_invoice', None,
            ),
        )
        self.receive_rgb_asset_page.address_label.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'rgb_invoice_label', None,
            ),
        )
        self.receive_rgb_asset_page.copy_button.clicked.connect(
            lambda: copy_text(self.receive_rgb_asset_page.receiver_address),
        )
        self.receive_rgb_asset_page.copy_button.clicked.connect(
            lambda: self.receive_rgb_asset_page.copy_button.setText('Copied!'),
        )
        self.receive_rgb_asset_page.receive_asset_close_button.clicked.connect(
            self.close_button_navigation,
        )
        self._view_model.receive_cfa_view_model.address.connect(
            self.update_address,
        )
        self._view_model.ln_offchain_view_model.invoice_get_event.connect(
            lambda address: self.update_address(address, ln_invoice=True),
        )
        self._view_model.receive_cfa_view_model.message.connect(
            self.handle_message,
        )
        self._view_model.ln_offchain_view_model.invoice_get_event.connect(
            self.hide_loading_screen,
        )
        self._view_model.receive_cfa_view_model.hide_loading.connect(
            self.hide_loading_screen,
        )

    def close_button_navigation(self):
        """
        Navigate to the specified page when the close button is clicked.
        """

        if self.close_page_navigation == AssetType.CFA.value:
            self._view_model.page_navigation.collectibles_asset_page()
        elif self.close_page_navigation == AssetType.NIA.value:
            self._view_model.page_navigation.fungibles_asset_page()
        else:
            navigation_map = {
                'NIA': self._view_model.page_navigation.fungibles_asset_page,
                'fungibles': self._view_model.page_navigation.fungibles_asset_page,
                'create_invoice': self._view_model.page_navigation.fungibles_asset_page,
                'CFA': self._view_model.page_navigation.collectibles_asset_page,
                'collectibles': self._view_model.page_navigation.collectibles_asset_page,
                'channel_management': self._view_model.page_navigation.channel_management_page,
                'view_unspent_list': self._view_model.page_navigation.view_unspent_list_page,
                'faucets': self._view_model.page_navigation.faucets_page,
                'settings': self._view_model.page_navigation.settings_page,
                'help': self._view_model.page_navigation.help_page,
                'about': self._view_model.page_navigation.about_page,
                'backup': self._view_model.page_navigation.backup_page,
            }
            receive_asset_navigation = navigation_map.get(
                self.originating_page,
            )
            if receive_asset_navigation:
                receive_asset_navigation()
            else:
                ToastManager.error(
                    description=f'No navigation defined for {
                        self.originating_page
                    }',
                )

    def update_address(self, address: str, ln_invoice: bool = False):
        """This method used to update new address"""
        self.receive_rgb_asset_page.update_qr_and_address(address)
        if ln_invoice:
            self.receive_rgb_asset_page.copy_button.setText(
                QCoreApplication.translate(
                    IRIS_WALLET_TRANSLATIONS_CONTEXT, 'copy_ln_invoice', None,
                ),
            )
            self.receive_rgb_asset_page.address_label.setText(
                QCoreApplication.translate(
                    IRIS_WALLET_TRANSLATIONS_CONTEXT, 'ln_invoice_label', None,
                ),
            )
            self.receive_rgb_asset_page.wallet_address_description_text.setText(
                QCoreApplication.translate(IRIS_WALLET_TRANSLATIONS_CONTEXT, 'ln_invoice_info', None).format(
                    self.expiry_time, self.expiry_unit,
                ),
            )

    def handle_message(self, msg_type: int, message: str):
        """This method handled to show message."""
        if msg_type == ToastPreset.ERROR:
            ToastManager.error(message)
        else:
            ToastManager.success(message)

    def show_receive_rgb_loading(self):
        """This method handled show loading screen on receive assets page"""
        self.receive_rgb_asset_page.label.hide()
        self.receive_rgb_asset_page.receiver_address.hide()
        self.__loading_translucent_screen.set_description_label_direction(
            'Bottom',
        )
        self.__loading_translucent_screen.start()
        self.receive_rgb_asset_page.copy_button.hide()

    def hide_loading_screen(self):
        """This method handled stop loading screen on receive assets page"""
        self.render_timer.stop()
        self.receive_rgb_asset_page.label.show()
        self.receive_rgb_asset_page.receiver_address.show()
        self.__loading_translucent_screen.stop()
        self.receive_rgb_asset_page.copy_button.show()
