# pylint: disable=too-many-instance-attributes, too-many-statements, unused-import
"""This module contains the ChannelManagement class,
which represents the UI for main assets.
"""
from __future__ import annotations

from PySide6.QtCore import QByteArray
from PySide6.QtCore import QCoreApplication
from PySide6.QtCore import QRect
from PySide6.QtCore import QSize
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtGui import QImage
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QComboBox
from PySide6.QtWidgets import QFrame
from PySide6.QtWidgets import QGraphicsBlurEffect
from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QScrollArea
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtWidgets import QSpacerItem
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QWidget

import src.resources_rc
from accessible_constant import CHANNEL_STATUS
from accessible_constant import CREATE_CHANNEL_BUTTON
from src.model.channels_model import ChannelDetailDialogModel
from src.utils.clickable_frame import ClickableFrame
from src.utils.common_utils import generate_identicon
from src.utils.common_utils import get_bitcoin_info_by_network
from src.utils.constant import IRIS_WALLET_TRANSLATIONS_CONTEXT
from src.utils.helpers import create_circular_pixmap
from src.utils.helpers import load_stylesheet
from src.utils.render_timer import RenderTimer
from src.viewmodels.main_view_model import MainViewModel
from src.views.components.header_frame import HeaderFrame
from src.views.components.loading_screen import LoadingTranslucentScreen
from src.views.ui_channel_detail_dialog import ChannelDetailDialogBox


class ChannelManagement(QWidget):
    """This class represents all the UI elements of the Channel management page."""

    def __init__(self, view_model):
        self.channel_ui_render_timer = RenderTimer(
            task_name='ChannelManagement Rendering',
        )
        self.channel_ui_render_timer.start()
        super().__init__()
        self._view_model: MainViewModel = view_model
        self.setStyleSheet(
            load_stylesheet(
                'views/qss/channel_management_style.qss',
            ),
        )
        self.header_col = [
            'Asset',
            'Asset ID',
            'Local Balance',
            'Remote Balance',
            'Status',
        ]
        self.list_frame = None
        self.close_channel_dialog_box = None
        self.list_h_box_layout = None
        self.counter_party = None
        self.pub_key = None
        self.scroll_v_spacer = None
        self.asset_local_balance = None
        self.channel_management_loading_screen = None
        self.bitcoin_local_balance = None
        self.bitcoin_remote_balance = None
        self.asset_logo = None
        self.asset_name = None
        self.local_balance = None
        self.remote_balance = None
        self.nia_asset_lookup = {}
        self.status_pixmap = None
        self.local_balance_value = None
        self.remote_balance_value = None
        self.channel_frame_horizontal_layout = None
        self.asset_id_value = None

        self.setObjectName('channel_management_page')
        self.vertical_layout_channel = QVBoxLayout(self)
        self.vertical_layout_channel.setObjectName('vertical_layout_channel')
        self.vertical_layout_channel.setContentsMargins(0, 0, 0, 10)
        self.widget_channel = QWidget(self)
        self.widget_channel.setObjectName('widget_channel')

        self.vertical_layout_2_channel = QVBoxLayout(self.widget_channel)
        self.vertical_layout_2_channel.setObjectName(
            'vertical_layout_2_channel',
        )
        self.vertical_layout_2_channel.setContentsMargins(25, 12, 25, 0)

        self.header_frame = HeaderFrame(
            title_name='channel_management', title_logo_path=':/assets/channel_management.png',
        )
        self.header_frame.action_button.setAccessibleName(
            CREATE_CHANNEL_BUTTON,
        )
        self.vertical_layout_2_channel.addWidget(self.header_frame)

        # Sorting drop down
        self.sort_combobox = QComboBox()
        self.sort_combobox.setFixedSize(QSize(150, 50))

        self.sort_combobox.addItems(
            [
                'Counter party',
                'PubKey',
                'Opened on Date',
                'Local balance',
                'Remote balance',
                'Asset',
                'Channel status',
                'Status',
            ],
        )
        self.sort_combobox.hide()
        self.vertical_layout_2_channel.addWidget(self.sort_combobox)

        # Channel list ui
        self.channel_list_widget = QWidget()
        self.channel_list_widget.setObjectName('channel_list_widget')
        self.channel_list_widget.setGeometry(QRect(21, 160, 1051, 399))
        self.main_list_v_layout = QVBoxLayout(self.channel_list_widget)
        self.main_list_v_layout.setObjectName('main_list_v_layout')
        self.main_list_v_layout.setContentsMargins(0, 0, 0, 0)

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setObjectName('scroll_area')
        self.scroll_area.setAutoFillBackground(False)
        self.scroll_area.setStyleSheet('border:none')
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setWidgetResizable(True)

        self.scroll_area_widget_contents = QWidget()
        self.scroll_area_widget_contents.setObjectName(
            'scroll_area_widget_contents',
        )
        self.scroll_area_widget_contents.setGeometry(QRect(0, 0, 1049, 321))

        self.list_v_box_layout = QVBoxLayout(self.scroll_area_widget_contents)
        self.list_v_box_layout.setSpacing(6)
        self.list_v_box_layout.setObjectName('list_v_box_layout')
        self.list_v_box_layout.setContentsMargins(0, 0, 0, 0)

        self.vertical_layout_3 = QVBoxLayout()
        self.vertical_layout_3.setSpacing(10)
        self.vertical_layout_3.setObjectName('vertical_layout_3')
        self.vertical_layout_2_channel.addLayout(self.vertical_layout_3)

        self.horizontal_layout_2 = QHBoxLayout()
        self.horizontal_layout_2.setSpacing(16)
        self.horizontal_layout_2.setObjectName('horizontal_layout_2')
        self.vertical_layout_channel.addWidget(self.widget_channel)
        self.vertical_layout_2_channel.addLayout(self.horizontal_layout_2)

        self.channel_header = QFrame(self)
        self.channel_header.setObjectName('channel_header')
        self.channel_header.setMinimumSize(QSize(900, 70))
        self.channel_header.setMaximumSize(QSize(16777215, 70))
        self.channel_header.setFrameShape(QFrame.Shape.StyledPanel)
        self.channel_header.setFrameShadow(QFrame.Shadow.Raised)

        self.channel_header_layout = QHBoxLayout(self.channel_header)
        self.channel_header_layout.setSpacing(6)
        self.channel_header_layout.setObjectName('channel_header_layout')

        self.asset_logo_label = QLabel(self.channel_header)
        self.asset_logo_label.setObjectName('asset_logo_label')
        self.asset_logo_label.setMinimumSize(QSize(40, 40))
        self.asset_logo_label.setMaximumSize(QSize(40, 40))

        self.channel_header_layout.addWidget(self.asset_logo_label)

        self.asset_name_label = QLabel(self.channel_header)
        self.asset_name_label.setObjectName('asset_name_label')
        self.asset_name_label.setMinimumSize(QSize(136, 40))
        self.channel_header_layout.addWidget(self.asset_name_label)

        self.asset_id_label = QLabel(self.channel_header)
        self.asset_id_label.setObjectName('asset_id_label')
        self.asset_id_label.setMinimumSize(QSize(450, 0))
        self.asset_id_label.setMaximumSize(QSize(16777215, 16777215))
        self.asset_id_label.setAlignment(
            Qt.AlignmentFlag.AlignLeading | Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
        )

        self.channel_header_layout.addWidget(self.asset_id_label)

        self.local_balance_label = QLabel(self.channel_header)
        self.local_balance_label.setObjectName('local_balance_label')
        self.local_balance_label.setMinimumSize(QSize(136, 0))
        self.local_balance_label.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignLeading | Qt.AlignmentFlag.AlignVCenter,
        )

        self.channel_header_layout.addWidget(self.local_balance_label)

        self.remote_balance_label = QLabel(self.channel_header)
        self.remote_balance_label.setObjectName('remote_balance_label')
        self.remote_balance_label.setMinimumSize(QSize(136, 0))
        self.remote_balance_label.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignLeading | Qt.AlignmentFlag.AlignVCenter,
        )

        self.channel_header_layout.addWidget(self.remote_balance_label)

        self.status_label = QLabel(self.channel_header)
        self.status_label.setObjectName('status_label')
        self.status_label.setMinimumSize(QSize(60, 0))
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.channel_header_layout.addWidget(self.status_label)

        self.vertical_spacer = QSpacerItem(
            20, 78, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding,
        )

        self.vertical_layout_2_channel.addWidget(self.channel_header)

        self.scroll_area.setWidget(self.scroll_area_widget_contents)
        self.main_list_v_layout.addWidget(self.scroll_area)
        self.vertical_layout_2_channel.addWidget(self.channel_list_widget)
        self.retranslate_ui()
        self.setup_ui_connection()
        self._view_model.channel_view_model.available_channels()
        self._view_model.channel_view_model.get_asset_list()

    def show_available_channels(self):
        """This method shows the available channels."""
        for i in reversed(range(self.list_v_box_layout.count())):
            item = self.list_v_box_layout.itemAt(i)
            widget = item.widget()

            # If it's a widget and it's named 'frame_4', remove it
            if widget is not None and widget.objectName() == 'list_frame':
                widget.deleteLater()
                self.list_v_box_layout.removeWidget(widget)

            # If it's a spacer item, remove it
            elif item.spacerItem() is not None:
                self.list_v_box_layout.removeItem(item.spacerItem())
        for channel in self._view_model.channel_view_model.channels:
            if not channel.peer_pubkey:
                continue
            self.list_frame = ClickableFrame(self.scroll_area_widget_contents)
            self.list_frame.setObjectName('list_frame')
            self.list_frame.setMinimumSize(QSize(0, 70))
            self.list_frame.setMaximumSize(QSize(16777215, 70))
            self.list_frame.setFrameShape(QFrame.Shape.StyledPanel)
            self.list_frame.setFrameShadow(QFrame.Shadow.Raised)

            self.channel_frame_horizontal_layout = QHBoxLayout(self.list_frame)
            self.channel_frame_horizontal_layout.setSpacing(6)
            self.channel_frame_horizontal_layout.setContentsMargins(
                20, 0, 20, 0,
            )

            self.asset_logo = QLabel(self.list_frame)
            self.asset_logo.setObjectName('asset_logo')
            self.asset_logo.setMinimumSize(QSize(40, 0))
            self.asset_logo.setMaximumSize(QSize(40, 16777215))

            self.channel_frame_horizontal_layout.addWidget(
                self.asset_logo, Qt.AlignmentFlag.AlignLeading | Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
            )

            self.asset_name = QLabel(self.list_frame)
            self.asset_name.setObjectName('asset_name')
            self.asset_name.setMinimumSize(QSize(136, 40))

            if channel.asset_id:
                for key, value in self._view_model.channel_view_model.total_asset_lookup_list.items():
                    if channel.asset_id == key:
                        self.asset_name.setText(value)

                img_str = generate_identicon(channel.asset_id)
                image = QImage.fromData(
                    QByteArray.fromBase64(img_str.encode()),
                )
                pixmap = QPixmap.fromImage(image)
                self.asset_logo.setPixmap(pixmap)

            self.channel_frame_horizontal_layout.addWidget(self.asset_name)

            self.asset_id_value = QLabel(self.list_frame)
            self.asset_id_value.setObjectName('asset_id')
            self.asset_id_value.setMinimumSize(QSize(450, 0))
            self.asset_id_value.setText(channel.asset_id)

            self.channel_frame_horizontal_layout.addWidget(self.asset_id_value)

            self.local_balance_value = QLabel(self.list_frame)
            self.local_balance_value.setObjectName('local_balance_value')
            self.local_balance_value.setMinimumSize(QSize(136, 0))
            self.local_balance_value.setText(
                str(
                    channel.asset_local_amount if channel.asset_id else int(
                        channel.outbound_balance_msat/1000,
                    ),
                ),
            )
            self.local_balance_value.setAlignment(
                Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTrailing | Qt.AlignmentFlag.AlignVCenter,
            )

            self.channel_frame_horizontal_layout.addWidget(
                self.local_balance_value,
            )

            self.remote_balance_value = QLabel(self.list_frame)
            self.remote_balance_value.setObjectName('remote_balance_value')
            self.remote_balance_value.setMinimumSize(QSize(136, 0))
            self.remote_balance_value.setText(
                str(
                    channel.asset_remote_amount if channel.asset_id else int(
                        channel.inbound_balance_msat/1000,
                    ),
                ),
            )
            self.remote_balance_value.setAlignment(
                Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTrailing | Qt.AlignmentFlag.AlignVCenter,
            )

            self.channel_frame_horizontal_layout.addWidget(
                self.remote_balance_value,
            )

            self.status_pixmap = QLabel(self.list_frame)
            self.status_pixmap.setObjectName('status_pixmap')
            self.status_pixmap.setAccessibleName(CHANNEL_STATUS)
            self.status_pixmap.setMinimumSize(QSize(60, 0))
            self.status_pixmap.setStyleSheet(
                'padding-left:25px;',
            )

            color = (
                QColor(235, 90, 90) if channel.status == 'Closing' else
                QColor(0, 201, 145) if channel.is_usable else
                QColor(169, 169, 169) if channel.ready and not channel.is_usable else
                QColor(255, 255, 0)
            )

            self.status_pixmap.setToolTip(
                QCoreApplication.translate(IRIS_WALLET_TRANSLATIONS_CONTEXT, 'closing', None) if color == QColor(235, 90, 90) else
                QCoreApplication.translate(IRIS_WALLET_TRANSLATIONS_CONTEXT, 'opening', None) if color == QColor(0, 201, 145) else
                QCoreApplication.translate(IRIS_WALLET_TRANSLATIONS_CONTEXT, 'offline', None) if color == QColor(169, 169, 169) else
                QCoreApplication.translate(
                    IRIS_WALLET_TRANSLATIONS_CONTEXT, 'pending', None,
                ),
            )
            self.status_pixmap.setAlignment(Qt.AlignmentFlag.AlignCenter)
            pixmap = create_circular_pixmap(16, color)
            self.status_pixmap.setPixmap(pixmap)

            self.channel_frame_horizontal_layout.addWidget(self.status_pixmap)

            self.list_v_box_layout.addWidget(self.list_frame)
            if channel.asset_id is None:
                bitcoin_asset = get_bitcoin_info_by_network()
                self.asset_id_value.setText(bitcoin_asset[0])
                self.asset_name.setText(bitcoin_asset[1])
                self.asset_logo.setPixmap(QPixmap(bitcoin_asset[2]))

            def create_click_handler(channel):
                return lambda: self.channel_detail_event(
                    channel_id=channel.channel_id,
                    pub_key=channel.peer_pubkey,
                    bitcoin_local_balance=channel.outbound_balance_msat,
                    bitcoin_remote_balance=channel.inbound_balance_msat,
                )
            self.list_frame.clicked.connect(
                create_click_handler(channel),
            )
        self.scroll_v_spacer = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding,
        )
        self.list_v_box_layout.addItem(self.scroll_v_spacer)

    def channel_detail_event(self, channel_id, pub_key, bitcoin_local_balance, bitcoin_remote_balance):
        """This method shows the channel detail dialog box when a channel frame is clicked"""

        params = ChannelDetailDialogModel(
            pub_key=pub_key,
            channel_id=channel_id,
            bitcoin_local_balance=bitcoin_local_balance,
            bitcoin_remote_balance=bitcoin_remote_balance,
        )
        channel_detail_dialog_box = ChannelDetailDialogBox(
            page_navigate=self._view_model.page_navigation,
            param=params,
            parent=self,
        )
        blur_effect = QGraphicsBlurEffect()
        blur_effect.setBlurRadius(10)
        self.setGraphicsEffect(blur_effect)
        channel_detail_dialog_box.exec()

    def setup_ui_connection(self):
        """Set up connections for UI elements."""
        self._view_model.channel_view_model.loading_started.connect(
            self.show_channel_management_loading,
        )
        self._view_model.channel_view_model.list_loaded.connect(
            self.show_available_channels,
        )
        self._view_model.channel_view_model.loading_finished.connect(
            self.hide_loading_screen,
        )
        self.header_frame.action_button.clicked.connect(
            self._view_model.channel_view_model.navigate_to_create_channel_page,
        )
        self.header_frame.refresh_page_button.clicked.connect(
            self.trigger_render_and_refresh,
        )
        self._view_model.channel_view_model.channel_deleted.connect(
            self._view_model.page_navigation.channel_management_page,
        )

    def retranslate_ui(self):
        """Retranslate the UI elements."""
        self.header_frame.action_button.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'create_channel', None,
            ),
        )
        self.status_label.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'status', None,
            ),
        )

        self.asset_id_label.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'asset_id', None,
            ),
        )
        self.asset_name_label.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'asset', None,
            ),
        )
        self.local_balance_label.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'local_balance', None,
            ),
        )
        self.remote_balance_label.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'remote_balance', None,
            ),
        )

    def trigger_render_and_refresh(self):
        """This method start the render timer and perform the channel list refresh"""
        self.channel_ui_render_timer.start()
        self._view_model.channel_view_model.available_channels()
        self._view_model.channel_view_model.get_asset_list()

    def show_channel_management_loading(self):
        """This method handled show loading screen on main asset page"""
        self.channel_management_loading_screen = LoadingTranslucentScreen(
            parent=self, description_text='Loading', dot_animation=True,
        )
        self.channel_management_loading_screen.set_description_label_direction(
            'Bottom',
        )
        self.channel_management_loading_screen.start()
        self.channel_management_loading_screen.make_parent_disabled_during_loading(
            True,
        )
        self.header_frame.setDisabled(True)

    def hide_loading_screen(self):
        """This method handled stop loading screen on main asset page"""
        self.channel_management_loading_screen.stop()
        self.channel_ui_render_timer.stop()
        self.channel_management_loading_screen.make_parent_disabled_during_loading(
            False,
        )
        self.header_frame.setDisabled(False)
