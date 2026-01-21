# pylint: disable=too-many-instance-attributes, too-many-statements, unused-import
"""This module contains the ChannelManagement class,
which represents the UI for main assets.
"""
from __future__ import annotations

from PySide6.QtCore import QCoreApplication
from PySide6.QtCore import QRect
from PySide6.QtCore import QSize
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QFrame
from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QScrollArea
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtWidgets import QSpacerItem
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QWidget

import src.resources_rc
from accessible_constant import UNSPENT_CLICKABLE_FRAME
from accessible_constant import UNSPENT_UTXO_ASSET_ID
from accessible_constant import UNSPENT_UTXO_OUTPOINT
from accessible_constant import UNSPENT_WIDGET
from src.data.repository.setting_repository import SettingRepository
from src.model.enums.enums_model import NetworkEnumModel
from src.utils.clickable_frame import ClickableFrame
from src.utils.common_utils import copy_text
from src.utils.constant import IRIS_WALLET_TRANSLATIONS_CONTEXT
from src.utils.helpers import load_stylesheet
from src.utils.render_timer import RenderTimer
from src.viewmodels.main_view_model import MainViewModel
from src.views.components.header_frame import HeaderFrame
from src.views.components.loading_screen import LoadingTranslucentScreen


class ViewUnspentList(QWidget):
    """This class represents all the UI elements of the main asset page."""

    def __init__(self, view_model):
        self.render_timer = RenderTimer(task_name='ViewUnspentList Rendering')
        self.render_timer.start()
        super().__init__()
        self.event_val = None
        self.image_path = None
        self.resizeEvent = self.change_layout  # pylint: disable=invalid-name
        self._view_model: MainViewModel = view_model
        self._view_model.unspent_view_model.list_loaded.connect(
            lambda: self.show_unspent_list(update_layout=self.event_val),
        )
        self.network: NetworkEnumModel = SettingRepository.get_wallet_network()
        self.setStyleSheet(load_stylesheet('views/qss/unspent_list_style.qss'))
        self.unspent_clickable_frame = None
        self.view_unspent_vertical_layout = None
        self.clickable_frame_horizontal_layout = None
        self.unspent_logo = None
        self.asset_name = None
        self.address = None
        self.utxo_size = None
        self.scroll_v_spacer = None
        self.__loading_translucent_screen = None
        self.window_size = None
        self.setObjectName('view_unspent_list_page')
        self.vertical_layout_unspent_list = QVBoxLayout(self)
        self.vertical_layout_unspent_list.setObjectName(
            'vertical_layout_unspent_list',
        )
        self.vertical_layout_unspent_list.setContentsMargins(0, 0, 0, 10)
        self.widget_unspent_list = QWidget(self)
        self.widget_unspent_list.setObjectName('widget_channel')

        self.vertical_layout_2_unspent = QVBoxLayout(self.widget_unspent_list)
        self.vertical_layout_2_unspent.setObjectName(
            'vertical_layout_2_channel',
        )
        self.vertical_layout_2_unspent.setContentsMargins(25, 12, 25, 0)

        self.header_unspent_frame = HeaderFrame(
            title_logo_path=':/assets/view_unspent_list.png', title_name='view_unspent_list',
        )
        self.header_unspent_frame.action_button.hide()
        self.vertical_layout_2_unspent.addWidget(self.header_unspent_frame)

        # Sorting drop down
        self.sub_title = QLabel()
        self.sub_title.setFixedSize(QSize(150, 50))

        self.sub_title.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'unspent_list', None,
            ),
        )
        self.vertical_layout_2_unspent.addWidget(self.sub_title)

        self.unspent_list_widget = QWidget()
        self.unspent_list_widget.setObjectName('channel_list_widget')
        self.unspent_list_widget.setGeometry(QRect(21, 160, 1051, 399))
        self.main_list_v_layout = QVBoxLayout(self.unspent_list_widget)
        self.main_list_v_layout.setObjectName('main_list_v_layout')
        self.main_list_v_layout.setContentsMargins(0, 0, 0, 0)

        self.unspent_scroll_area = QScrollArea(self)
        self.unspent_scroll_area.setObjectName('scroll_area')
        self.unspent_scroll_area.setAutoFillBackground(False)
        self.unspent_scroll_area.setStyleSheet('border:none')
        self.unspent_scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded,
        )
        self.unspent_scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAsNeeded,
        )
        self.unspent_scroll_area.setStyleSheet(
            load_stylesheet('views/qss/scrollbar.qss'),
        )
        self.unspent_scroll_area.setWidgetResizable(True)

        self.unspent_scroll_area_widget_contents = QWidget()
        self.unspent_scroll_area_widget_contents.setObjectName(
            'scroll_area_widget_contents',
        )
        self.unspent_scroll_area_widget_contents.setAccessibleName(
            UNSPENT_WIDGET,
        )
        self.unspent_scroll_area_widget_contents.setGeometry(
            QRect(0, 0, 1049, 321),
        )

        self.unspent_list_v_box_layout = QVBoxLayout(
            self.unspent_scroll_area_widget_contents,
        )
        self.unspent_list_v_box_layout.setSpacing(6)
        self.unspent_list_v_box_layout.setObjectName('list_v_box_layout')
        self.unspent_list_v_box_layout.setContentsMargins(0, 0, 0, 0)

        self.vertical_layout = QVBoxLayout()
        self.vertical_layout.setSpacing(10)
        self.vertical_layout.setObjectName('vertical_layout_3')
        self.vertical_layout_2_unspent.addLayout(self.vertical_layout)

        self.horizontal_layout = QHBoxLayout()
        self.horizontal_layout.setSpacing(16)
        self.horizontal_layout.setObjectName('horizontal_layout_2')
        self.vertical_layout_unspent_list.addWidget(self.widget_unspent_list)
        self.vertical_layout_2_unspent.addLayout(self.horizontal_layout)

        self.unspent_scroll_area.setWidget(
            self.unspent_scroll_area_widget_contents,
        )
        self.main_list_v_layout.addWidget(self.unspent_scroll_area)
        self.vertical_layout_2_unspent.addWidget(self.unspent_list_widget)

        self.setup_ui_connection()
        self.resizeEvent = self.change_layout  # pylint: disable=invalid-name

    def show_unspent_list(self, update_layout: bool = False):
        """This method shows the unspent list"""
        self.clear_unspent_list_layout()

        for _list in self._view_model.unspent_view_model.unspent_list:
            unspent_clickable_frame = self.create_unspent_clickable_frame(
                _list, update_layout,
            )
            self.unspent_list_v_box_layout.addWidget(unspent_clickable_frame)

        # Add spacer at the end
        self.scroll_v_spacer = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding,
        )
        self.unspent_list_v_box_layout.addItem(self.scroll_v_spacer)
        self.resizeEvent = self.change_layout  # pylint: disable=invalid-name

    def setup_ui_connection(self):
        """Set up connections for UI elements."""
        self._view_model.unspent_view_model.get_unspent_list()
        self.header_unspent_frame.refresh_page_button.clicked.connect(
            self.trigger_render_and_refresh,
        )
        self._view_model.unspent_view_model.loading_started.connect(
            self.show_view_unspent_loading,
        )
        self._view_model.unspent_view_model.loading_finished.connect(
            self.hide_loading_screen,
        )
        self.show_view_unspent_loading()

    def trigger_render_and_refresh(self):
        """This method start the render timer and perform the unspent list refresh"""
        self.render_timer.start()
        self._view_model.unspent_view_model.get_unspent_list(
            is_hard_refresh=True,
        )

    def handle_asset_frame_click(self, asset_id):
        """This method handles channel click of the channel management asset page."""
        copy_text(asset_id)

    def show_view_unspent_loading(self):
        """This method handled show loading screen on main asset page"""
        self.__loading_translucent_screen = LoadingTranslucentScreen(
            parent=self, description_text='Loading', dot_animation=True,
        )
        self.__loading_translucent_screen.set_description_label_direction(
            'Bottom',
        )
        self.__loading_translucent_screen.start()
        self.header_unspent_frame.refresh_page_button.setDisabled(True)

    def hide_loading_screen(self):
        """This method handled stop loading screen on main asset page"""
        self.render_timer.stop()
        self.__loading_translucent_screen.stop()
        self.header_unspent_frame.refresh_page_button.setDisabled(False)

    def change_layout(self, event):
        """This method is called whenever the window is resized."""
        # Emit the custom signal with new width and height
        super().resizeEvent(event)
        self.window_size = event.size().width()
        if self.window_size > 1389:
            self.show_unspent_list(True)
            self.event_val = True
        else:
            self.show_unspent_list(False)
            self.event_val = False

    def create_unspent_clickable_frame(self, _list, update_layout):
        """Create a clickable frame for each unspent item."""
        unspent_clickable_frame = ClickableFrame(
            _list.utxo.outpoint, self.unspent_scroll_area_widget_contents,
        )
        unspent_clickable_frame.setObjectName('frame_4')
        unspent_clickable_frame.setAccessibleName(UNSPENT_CLICKABLE_FRAME)
        unspent_clickable_frame.setMinimumSize(QSize(900, 75))
        unspent_clickable_frame.setMaximumSize(QSize(16777215, 75))
        unspent_clickable_frame.setFrameShape(QFrame.StyledPanel)
        unspent_clickable_frame.setFrameShadow(QFrame.Raised)

        # Set up layouts and labels
        view_unspent_vertical_layout = QVBoxLayout(unspent_clickable_frame)
        clickable_frame_horizontal_layout = QHBoxLayout()
        clickable_frame_horizontal_layout.setSpacing(9)
        clickable_frame_horizontal_layout.setContentsMargins(6, 3, 12, 3)

        # Unspent Logo
        unspent_logo = QLabel(unspent_clickable_frame)
        unspent_logo.setMaximumSize(QSize(40, 40))
        image_path = self.get_image_path(_list)
        unspent_logo.setPixmap(QPixmap(image_path))

        clickable_frame_horizontal_layout.addWidget(unspent_logo)

        # Asset Name
        asset_name = QLabel(unspent_clickable_frame)
        asset_name.setToolTip(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'click_to_copy', None,
            ),
        )
        asset_name.setAccessibleDescription(UNSPENT_UTXO_OUTPOINT)
        asset_name.setText(_list.utxo.outpoint)

        asset_detail_vertical_layout = QVBoxLayout()
        asset_detail_vertical_layout.setObjectName(
            'asset_detail_vertical_layout',
        )
        asset_detail_vertical_layout.setContentsMargins(6, 0, 0, 0)

        asset_detail_vertical_layout.addWidget(asset_name)

        # Add more widgets to the layout
        address = QLabel(unspent_clickable_frame)
        address.setAccessibleDescription(UNSPENT_UTXO_ASSET_ID)
        self.set_address_label(address, _list, update_layout)
        if not _list.utxo.colorable:
            address.deleteLater()
        asset_detail_vertical_layout.addWidget(address)
        clickable_frame_horizontal_layout.addLayout(
            asset_detail_vertical_layout,
        )
        utxo_size = QLabel(unspent_clickable_frame)
        utxo_size.setText(f"{_list.utxo.btc_amount} sat")
        utxo_size.setAlignment(
            Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter,
        )
        clickable_frame_horizontal_layout.addWidget(utxo_size)

        view_unspent_vertical_layout.addLayout(
            clickable_frame_horizontal_layout,
        )

        # Connect the frame click event
        unspent_clickable_frame.clicked.connect(self.handle_asset_frame_click)
        return unspent_clickable_frame

    def clear_unspent_list_layout(self):
        """Clear all the widgets and spacers from the layout."""
        for i in reversed(range(self.unspent_list_v_box_layout.count())):
            item = self.unspent_list_v_box_layout.itemAt(i)
            widget = item.widget()

            if widget is not None and widget.objectName() == 'frame_4':
                widget.deleteLater()
                self.unspent_list_v_box_layout.removeWidget(widget)
            elif item.spacerItem() is not None:
                self.unspent_list_v_box_layout.removeItem(item.spacerItem())

    def set_address_label(self, label, _list, update_layout):
        """Set the text and size for the address label."""
        if _list.utxo.colorable:
            asset_id = ' '.join(
                token.asset_id if not update_layout else token.asset_id
                for token in _list.rgb_allocations if token.asset_id
            )
            label.setText(asset_id if asset_id else 'NA')
        else:
            label.setText('')

    def get_image_path(self, _list):
        """Return the appropriate image path based on the network and colorable status."""
        if _list.utxo.colorable:
            return ':/assets/images/rgb_logo_round.png'
        return {
            NetworkEnumModel.MAINNET.value: ':/assets/bitcoin.png',
            NetworkEnumModel.REGTEST.value: ':/assets/regtest_bitcoin.png',
            NetworkEnumModel.TESTNET.value: ':/assets/testnet_bitcoin.png',
            NetworkEnumModel.TESTNET4.value: ':/assets/testnet_bitcoin.png',
        }.get(self.network.value)
