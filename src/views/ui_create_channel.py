# pylint: disable=too-many-instance-attributes, too-many-statements, unused-import
"""This module contains the CreateChannelWidget class,
which represents the UI for open channel page.
"""
from __future__ import annotations

from PySide6.QtCore import QCoreApplication
from PySide6.QtCore import QRect
from PySide6.QtCore import QRegularExpression
from PySide6.QtCore import QSize
from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor
from PySide6.QtGui import QIcon
from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtGui import QValidator
from PySide6.QtWidgets import QCheckBox
from PySide6.QtWidgets import QComboBox
from PySide6.QtWidgets import QFrame
from PySide6.QtWidgets import QGridLayout
from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QLineEdit
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QScrollArea
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtWidgets import QSpacerItem
from PySide6.QtWidgets import QStackedWidget
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QWidget

import src.resources_rc
from accessible_constant import CHANNEL_ASSET_AMOUNT
from accessible_constant import CHANNEL_CAPACITY_SAT
from accessible_constant import CHANNEL_COMBOBOX
from accessible_constant import CHANNEL_NEXT_BUTTON
from accessible_constant import CHANNEL_PREV_BUTTON
from accessible_constant import CREATE_CHANNEL_CLOSE_BUTTON
from accessible_constant import CREATE_CHANNEL_ERROR_LABEL
from accessible_constant import NODE_URI_INPUT
from accessible_constant import PUSH_MSAT_VALUE
from src.model.common_operation_model import NodeInfoResponseModel
from src.model.node_info_model import NodeInfoModel
from src.model.success_model import SuccessPageModel
from src.utils.common_utils import sat_to_msat
from src.utils.common_utils import set_placeholder_value
from src.utils.constant import IRIS_WALLET_TRANSLATIONS_CONTEXT
from src.utils.helpers import handle_asset_address
from src.utils.helpers import load_stylesheet
from src.utils.node_url_validator import NodeValidator
from src.utils.render_timer import RenderTimer
from src.viewmodels.main_view_model import MainViewModel
from src.views.components.buttons import PrimaryButton
from src.views.components.buttons import SecondaryButton
from src.views.components.loading_screen import LoadingTranslucentScreen
from src.views.components.wallet_logo_frame import WalletLogoFrame


class CreateChannelWidget(QWidget):
    """This class represents all the UI elements of the create channel page."""

    def __init__(self, view_model):
        super().__init__()
        self.render_timer = RenderTimer(task_name='ChannelCreation Rendering')
        self._view_model: MainViewModel = view_model
        self.setStyleSheet(
            load_stylesheet(
                'views/qss/create_channel_style.qss',
            ),
        )
        self.grid_layout = QGridLayout(self)
        self.amount = None
        self.asset_id = None
        self.__loading_translucent_screen = None
        self.valid_url = False
        self.pub_key = None
        get_node_info = NodeInfoModel()
        self.node_validation_info: NodeInfoResponseModel = get_node_info.node_info
        self.grid_layout.setObjectName('gridLayout')
        self.wallet_logo = QFrame(self)
        self.wallet_logo = WalletLogoFrame()
        self.grid_layout.addWidget(self.wallet_logo, 0, 0, 1, 1)

        self.vertical_spacer_top = QSpacerItem(
            20,
            78,
            QSizePolicy.Policy.Minimum,
            QSizePolicy.Policy.Expanding,
        )

        self.grid_layout.addItem(self.vertical_spacer_top, 0, 1, 1, 1)

        self.horizontal_spacer_left = QSpacerItem(
            337,
            20,
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Minimum,
        )

        self.grid_layout.addItem(self.horizontal_spacer_left, 1, 0, 1, 1)

        self.open_channel_page = QWidget()
        self.open_channel_page.setObjectName('open_channel_page')
        self.open_channel_page.setMaximumSize(QSize(530, 750))

        self.create_channel_vertical_layout = QVBoxLayout(
            self.open_channel_page,
        )
        self.create_channel_vertical_layout.setObjectName('verticalLayout_2')
        self.create_channel_vertical_layout.setContentsMargins(1, -1, 1, 35)
        self.header_horizontal_layout = QHBoxLayout()
        self.header_horizontal_layout.setSpacing(8)
        self.header_horizontal_layout.setObjectName('header_horizontal_layout')
        self.header_horizontal_layout.setContentsMargins(35, 5, 40, 0)
        self.open_channel_title = QLabel(self.open_channel_page)
        self.open_channel_title.setObjectName('open_channel_title')
        self.open_channel_title.setMinimumSize(QSize(415, 63))

        self.header_horizontal_layout.addWidget(self.open_channel_title)

        self.open_close_button = QPushButton(self.open_channel_page)
        self.open_close_button.setObjectName('open_close_button')
        self.open_close_button.setAccessibleName(CREATE_CHANNEL_CLOSE_BUTTON)
        self.open_close_button.setMinimumSize(QSize(24, 24))
        self.open_close_button.setMaximumSize(QSize(24, 24))
        self.open_close_button.setAutoFillBackground(False)
        self.open_close_button.setCursor(
            QCursor(Qt.CursorShape.PointingHandCursor),
        )

        icon = QIcon()
        icon.addFile(':/assets/x_circle.png', QSize(), QIcon.Normal, QIcon.Off)
        self.open_close_button.setIcon(icon)
        self.open_close_button.setIconSize(QSize(24, 24))
        self.open_close_button.setCheckable(False)
        self.open_close_button.setChecked(False)

        self.header_horizontal_layout.addWidget(
            self.open_close_button, 0, Qt.AlignHCenter,
        )

        self.create_channel_vertical_layout.addLayout(
            self.header_horizontal_layout,
        )

        self.channel_bottom_line = QFrame(self.open_channel_page)
        self.channel_bottom_line.setObjectName('channel_bottom_line')

        self.channel_bottom_line.setFrameShape(QFrame.Shape.HLine)
        self.channel_bottom_line.setFrameShadow(QFrame.Shadow.Sunken)

        self.create_channel_vertical_layout.addWidget(self.channel_bottom_line)

        self.inner_vertical_layout = QVBoxLayout()
        self.inner_vertical_layout.setSpacing(15)
        self.inner_vertical_layout.setObjectName('inner_vertical_layout')
        self.inner_vertical_layout.setContentsMargins(80, 10, 80, -1)
        self.node_info = QLabel(self.open_channel_page)
        self.node_info.setWordWrap(True)
        self.node_info.setObjectName('node_info')
        self.node_info.setMinimumSize(QSize(0, 41))
        self.node_info.setMaximumSize(QSize(16777215, 50))
        self.node_info.setAutoFillBackground(False)
        self.inner_vertical_layout.addWidget(self.node_info)

        self.pub_key_label = QLabel(self.open_channel_page)
        self.pub_key_label.setObjectName('pub_key_label')
        self.pub_key_label.setMinimumSize(QSize(335, 0))
        self.pub_key_label.setMaximumSize(QSize(335, 16777215))

        self.inner_vertical_layout.addWidget(self.pub_key_label)

        self.public_key_input = QLineEdit(self.open_channel_page)
        self.public_key_input.setObjectName('public_key_input')
        self.public_key_input.setAccessibleName(NODE_URI_INPUT)
        self.public_key_input.setMinimumSize(QSize(335, 40))

        self.public_key_input.setClearButtonEnabled(True)

        self.inner_vertical_layout.addWidget(self.public_key_input)

        self.error_label = QLabel()
        self.error_label.setObjectName('error_label')
        self.error_label.setAccessibleDescription(CREATE_CHANNEL_ERROR_LABEL)
        self.error_label.hide()
        self.inner_vertical_layout.addWidget(self.error_label)

        self.create_channel_vertical_layout.addLayout(
            self.inner_vertical_layout,
        )

        self.stacked_widget = QStackedWidget(self.open_channel_page)
        self.stacked_widget.setObjectName('stackedWidget')

        # Step 1 for create channel start here
        self.create_channel_step_1 = QWidget()
        self.create_channel_step_1.setObjectName('create_channel_step_1')
        self.grid_layout_1 = QGridLayout(self.create_channel_step_1)
        self.grid_layout_1.setObjectName('gridLayout_4')

        self.create_channel_scroll_area = QScrollArea(
            self.create_channel_step_1,
        )
        self.create_channel_scroll_area.setObjectName(
            'create_channel_scroll_area',
        )
        self.create_channel_scroll_area.setMinimumSize(QSize(0, 200))
        self.create_channel_scroll_area.setMaximumSize(QSize(360, 200))
        self.create_channel_scroll_area.setLayoutDirection(Qt.LeftToRight)
        self.create_channel_scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff,
        )
        self.create_channel_scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff,
        )
        self.create_channel_scroll_area.setWidgetResizable(True)
        self.create_channel_scroll_area_contents = QWidget()
        self.create_channel_scroll_area_contents.setObjectName(
            'create_channel_scroll_area_contents',
        )
        self.create_channel_scroll_area.setStyleSheet(
            'border:none;background-color:transparent',
        )
        self.create_channel_scroll_area_contents.setGeometry(
            QRect(0, 0, 360, 200),
        )
        self.grid_layout_2 = QGridLayout(
            self.create_channel_scroll_area_contents,
        )
        self.grid_layout_2.setObjectName('gridLayout_5')

        self.create_channel_scroll_area.setWidget(
            self.create_channel_scroll_area_contents,
        )

        self.grid_layout_1.addWidget(
            self.create_channel_scroll_area, 2, 0, 1, 1,
        )

        self.stacked_widget.addWidget(self.create_channel_step_1)

        # Step 2 start from here
        self.create_channel_step_2 = QWidget()
        self.create_channel_step_2.setObjectName('create_channel_step_2')
        self.grid_layout_3 = QGridLayout(self.create_channel_step_2)
        self.grid_layout_3.setObjectName('gridLayout_2')
        self.grid_layout_3.setContentsMargins(80, -1, 80, -1)
        self.details_frame = QFrame(self.create_channel_step_2)
        self.details_frame.setObjectName('details_frame')
        self.details_frame.setFrameShape(QFrame.StyledPanel)
        self.details_frame.setFrameShadow(QFrame.Raised)
        self.grid_layout_4 = QGridLayout(self.details_frame)
        self.grid_layout_4.setObjectName('gridLayout_3')
        self.grid_layout_4.setContentsMargins(20, 20, 20, 20)
        self.horizontal_layout = QHBoxLayout()
        self.horizontal_layout.setObjectName('horizontalLayout')
        self.horizontal_layout.setContentsMargins(6, 15, 6, 15)
        self.amount_line_edit = QLineEdit(self.details_frame)
        self.amount_line_edit.setObjectName('lineEdit')
        self.amount_line_edit.setAccessibleName(CHANNEL_ASSET_AMOUNT)
        self.number_validation = QRegularExpression(r'^\d+$')
        self.validator = QRegularExpressionValidator(self.number_validation)
        self.amount_line_edit.setValidator(self.validator)
        self.amount_line_edit.setMinimumSize(QSize(0, 40))
        self.grid_layout_4.addWidget(self.amount_line_edit, 2, 0, 1, 1)
        self.amount_validation_label = QLabel(self.details_frame)
        self.amount_validation_label.setWordWrap(True)
        self.amount_validation_label.setObjectName('amount_validation_label')
        self.amount_validation_label.hide()
        self.grid_layout_4.addWidget(self.amount_validation_label, 3, 0, 1, 1)

        self.combo_box = QComboBox(self.details_frame)
        self.combo_box.setObjectName('comboBox')
        self.combo_box.setAccessibleDescription(CHANNEL_COMBOBOX)
        self.combo_box.setMinimumSize(QSize(126, 40))

        self.grid_layout_4.addWidget(self.combo_box, 0, 0, 1, 1)

        self.amount_label = QLabel(self.details_frame)
        self.amount_label.setObjectName('amount_label')
        self.amount_label.setMaximumSize(QSize(16777215, 30))

        self.grid_layout_4.addWidget(self.amount_label, 1, 0, 1, 1)

        self.capacity_sat_label = QLabel(self.details_frame)
        self.capacity_sat_label.setObjectName('capacity_sat_label')
        self.capacity_sat_label.setMaximumSize(QSize(16777215, 30))

        self.grid_layout_4.addWidget(self.capacity_sat_label, 4, 0, 1, 1)

        self.capacity_sat_value = QLineEdit(self.details_frame)
        self.capacity_sat_value.setValidator(self.validator)

        self.capacity_sat_value.setObjectName('capacity_sat_value')
        self.capacity_sat_value.setAccessibleName(CHANNEL_CAPACITY_SAT)
        self.capacity_sat_value.setMinimumSize(QSize(0, 40))
        self.grid_layout_4.addWidget(self.capacity_sat_value, 5, 0, 1, 1)
        self.channel_capacity_validation_label = QLabel(self.details_frame)
        self.channel_capacity_validation_label.setWordWrap(True)
        self.channel_capacity_validation_label.setObjectName(
            'channel_capacity_validation_label',
        )
        self.channel_capacity_validation_label.hide()
        self.grid_layout_4.addWidget(
            self.channel_capacity_validation_label, 6, 0, 1, 1,
        )

        self.push_msat_label = QLabel(self.details_frame)
        self.push_msat_label.setObjectName('push_msat_label')
        self.push_msat_label.setMaximumSize(QSize(16777215, 30))

        self.grid_layout_4.addWidget(self.push_msat_label, 7, 0, 1, 1)

        self.push_msat_value = QLineEdit(self.details_frame)
        self.push_msat_value.setObjectName('push_msat_value')
        self.push_msat_value.setAccessibleName(PUSH_MSAT_VALUE)
        self.push_msat_value.setMinimumSize(QSize(0, 40))
        self.push_msat_value.setValidator(self.validator)
        self.push_msat_value.setText('0')

        self.grid_layout_4.addWidget(self.push_msat_value, 8, 0, 1, 1)

        self.push_msat_validation_label = QLabel(self.details_frame)
        self.push_msat_validation_label.setWordWrap(True)
        self.push_msat_validation_label.setObjectName(
            'push_msat_validation_label',
        )
        self.push_msat_validation_label.setStyleSheet('padding-top:5px;')
        self.push_msat_validation_label.hide()
        self.grid_layout_4.addWidget(
            self.push_msat_validation_label, 9, 0, 1, 1,
        )

        self.horizontal_layout_1 = QHBoxLayout()
        self.horizontal_layout_1.setObjectName('horizontalLayout_2')
        self.horizontal_layout_1.setContentsMargins(1, -1, 95, 1)
        self.slow_checkbox = QCheckBox(self.details_frame)
        self.slow_checkbox.setObjectName('checkBox')
        self.slow_checkbox.setAutoExclusive(True)

        self.horizontal_layout_1.addWidget(self.slow_checkbox)
        self.medium_checkbox = QCheckBox(self.details_frame)
        self.medium_checkbox.setObjectName('medium_checkbox')
        self.medium_checkbox.setAutoExclusive(True)

        self.horizontal_layout_1.addWidget(self.medium_checkbox)

        self.fast_checkbox = QCheckBox(self.details_frame)
        self.fast_checkbox.setObjectName('checkBox_2')
        self.fast_checkbox.setAutoExclusive(True)

        self.horizontal_layout_1.addWidget(self.fast_checkbox)

        self.grid_layout_4.addLayout(self.horizontal_layout_1, 10, 0, 1, 1)

        self.txn_label = QLabel(self.details_frame)
        self.txn_label.setObjectName('txn_label')
        self.txn_label.setMaximumSize(QSize(16777215, 20))

        self.grid_layout_4.addWidget(self.txn_label, 9, 0, 1, 1)

        self.grid_layout_3.addWidget(self.details_frame, 0, 1, 1, 1)

        self.stacked_widget.addWidget(self.create_channel_step_2)

        self.create_channel_vertical_layout.addWidget(self.stacked_widget)

        self.inner_vertical_spacer = QSpacerItem(
            20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding,
        )

        self.create_channel_vertical_layout.addItem(self.inner_vertical_spacer)

        self.channel_top_line = QFrame(self.open_channel_page)
        self.channel_top_line.setObjectName('channel_top_line')

        self.channel_top_line.setFrameShape(QFrame.Shape.HLine)
        self.channel_top_line.setFrameShadow(QFrame.Shadow.Sunken)

        self.create_channel_vertical_layout.addWidget(self.channel_top_line)

        self.button_top_vertical_spacer = QSpacerItem(
            20, 24, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred,
        )

        self.create_channel_vertical_layout.addItem(
            self.button_top_vertical_spacer,
        )

        self.horizontal_layout_2 = QHBoxLayout()
        self.horizontal_layout_2.setObjectName('horizontalLayout_5')
        self.channel_prev_button = SecondaryButton()
        self.channel_prev_button.setAccessibleName(CHANNEL_PREV_BUTTON)
        self.channel_prev_button.setMinimumSize(QSize(201, 40))
        self.channel_prev_button.setMaximumSize(QSize(201, 16777215))
        self.channel_prev_button.setAutoRepeat(False)
        self.channel_prev_button.setAutoExclusive(False)
        self.channel_prev_button.setFlat(False)

        self.horizontal_layout_2.addWidget(self.channel_prev_button)

        self.channel_next_button = PrimaryButton()
        self.channel_next_button.setAccessibleName(CHANNEL_NEXT_BUTTON)
        self.channel_next_button.setMinimumSize(QSize(201, 40))
        self.channel_next_button.setMaximumSize(QSize(201, 16777215))

        self.channel_next_button.setAutoRepeat(False)
        self.channel_next_button.setAutoExclusive(False)
        self.channel_next_button.setFlat(False)

        self.horizontal_layout_2.addWidget(self.channel_next_button)

        self.create_channel_vertical_layout.addLayout(self.horizontal_layout_2)

        self.grid_layout.addWidget(self.open_channel_page, 1, 1, 1, 1)

        self.main_horizontal_spacer_right = QSpacerItem(
            336, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum,
        )

        self.grid_layout.addItem(self.main_horizontal_spacer_right, 1, 2, 1, 1)

        self.widget_vertical_spacer_bottom = QSpacerItem(
            20,
            77,
            QSizePolicy.Policy.Minimum,
            QSizePolicy.Policy.Expanding,
        )

        self.grid_layout.addItem(
            self.widget_vertical_spacer_bottom, 2, 1, 1, 1,
        )

        self.retranslate_ui()
        self.on_page_load()
        self.stacked_widget.setCurrentIndex(0)
        self.setup_ui_connection()

        self.slow_checkbox.hide()
        self.medium_checkbox.hide()
        self.fast_checkbox.hide()
        self.txn_label.hide()

    def show_asset_in_combo_box(self):
        """This method populates the combo box with available assets."""
        self.combo_box.clear()
        bitcoin = self._view_model.main_asset_view_model.assets.vanilla
        self.combo_box.addItem(bitcoin.ticker)

        all_assets = [
            (asset.ticker, asset.asset_id) for asset in self._view_model.channel_view_model.nia_asset
        ] + [
            (asset.name, asset.asset_id) for asset in self._view_model.channel_view_model.cfa_asset
        ]

        for name, asset_id in all_assets:
            self.combo_box.addItem(
                f"{name} | {handle_asset_address(asset_id, short_len=14)}",
            )

    def setup_ui_connection(self):
        """This method handled connection to the slots"""
        self.channel_next_button.clicked.connect(self.handle_next)
        self.channel_prev_button.clicked.connect(self.handle_prev)
        self.show_asset_in_combo_box()
        self.combo_box.currentIndexChanged.connect(self.on_combo_box_changed)
        self.amount_line_edit.textChanged.connect(self.on_amount_changed)
        self.public_key_input.textChanged.connect(self.on_public_url_changed)
        self.capacity_sat_value.textChanged.connect(self.handle_button_enable)
        self.push_msat_value.textChanged.connect(self.handle_button_enable)
        self.public_key_input.textChanged.connect(self.handle_button_enable)
        self.amount_line_edit.textChanged.connect(self.handle_button_enable)
        self.combo_box.currentTextChanged.connect(self.handle_button_enable)
        self.open_close_button.clicked.connect(
            self._view_model.page_navigation.channel_management_page,
        )
        self._view_model.channel_view_model.loading_started.connect(
            self.show_create_channel_loading,
        )
        self._view_model.channel_view_model.loading_finished.connect(
            self.stop_loading_screen,
        )
        self._view_model.channel_view_model.is_loading.connect(
            self.update_loading_state,
        )
        self._view_model.channel_view_model.channel_created.connect(
            self.channel_created,
        )
        self.amount_line_edit.textChanged.connect(
            self.handle_amount_validation,
        )
        self.push_msat_value.textChanged.connect(
            lambda: self.set_push_amount_placeholder(self.push_msat_value),
        )
        self.amount_line_edit.textChanged.connect(
            lambda: set_placeholder_value(self.amount_line_edit),
        )
        self.capacity_sat_value.textChanged.connect(
            lambda: set_placeholder_value(self.capacity_sat_value),
        )

    def retranslate_ui(self):
        """This method handled to retranslate the ui initially"""
        self.open_channel_title.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'open_channel', None,
            ),
        )
        self.node_info.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT,
                'open_channel_desc',
                None,
            ),
        )
        self.pub_key_label.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'node_uri', None,
            ),
        )
        self.public_key_input.setPlaceholderText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT,
                'node_uri',
                None,
            ),
        )
        self.slow_checkbox.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT,
                'slow',
                None,
            ),
        )
        self.medium_checkbox.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT,
                'medium',
                None,
            ),
        )
        self.fast_checkbox.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'fast', None,
            ),
        )
        self.amount_line_edit.setPlaceholderText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'enter_amount', None,
            ),
        )

        self.txn_label.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'Transaction fees', None,
            ),
        )
        self.amount_label.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'amount', None,
            ),
        )
        self.channel_prev_button.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'go_back', None,
            ),
        )
        self.channel_next_button.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'next', None,
            ),
        )
        self.push_msat_label.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'initial_push_amount', None,
            ),
        )
        self.capacity_sat_value.setPlaceholderText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'amount_in_sat', None,
            ),
        )
        self.push_msat_value.setPlaceholderText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'amount_in_sat', None,
            ),
        )
        self.capacity_sat_label.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'capacity_of_channel', None,
            ),
        )
        channel_capacity_validation_text = QCoreApplication.translate(
            IRIS_WALLET_TRANSLATIONS_CONTEXT, 'channel_capacity_validation', None,
        ).format(self.node_validation_info.channel_capacity_min_sat, self.node_validation_info.channel_capacity_max_sat)

        self.channel_capacity_validation_label.setText(
            channel_capacity_validation_text,
        )
        self.push_msat_validation_label.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'push_amount_validation', None,
            ),
        )

    def on_page_load(self):
        """Sets up the UI elements when the page loads."""
        if self.stacked_widget.currentIndex() == 0:
            self.channel_prev_button.hide()
            self.amount_label.hide()
            self.amount_line_edit.hide()
            self.channel_next_button.setMaximumSize(QSize(402, 40))
            self.stacked_widget.hide()
            self.open_channel_page.setMaximumSize(QSize(530, 450))
        self.channel_next_button.setEnabled(False)

    def handle_next(self):
        """This method handled next button click"""
        index = self.stacked_widget.currentIndex()
        if index == 0:
            self.stacked_widget.setCurrentIndex(1)
            self.public_key_input.setDisabled(True)
            self.channel_next_button.setEnabled(False)
            self.channel_prev_button.show()
            self.channel_next_button.setMaximumSize(QSize(201, 40))
            self.open_channel_page.setMaximumSize(QSize(530, 750))
            self.stacked_widget.show()
            self.handle_button_enable()
        if index == 1:
            push_msat = sat_to_msat(self.push_msat_value.text())
            if self.asset_id is not None:
                self._view_model.channel_view_model.create_rgb_channel(
                    self.pub_key, self.asset_id, self.amount, self.capacity_sat_value.text(
                    ), push_msat,
                )
            if self.asset_id is None:
                self._view_model.channel_view_model.create_channel_with_btc(
                    self.pub_key, self.capacity_sat_value.text(), self.push_msat_value.text(),
                )

        if index == 2:
            self._view_model.page_navigation.channel_management_page()

    def channel_created(self):
        """This method handled after channel created"""
        header = 'Open Channel'
        title = QCoreApplication.translate(
            IRIS_WALLET_TRANSLATIONS_CONTEXT, 'channel_open_request_title', None,
        )
        button_name = QCoreApplication.translate(
            IRIS_WALLET_TRANSLATIONS_CONTEXT, 'finish', None,
        )
        description = QCoreApplication.translate(
            IRIS_WALLET_TRANSLATIONS_CONTEXT, 'channel_open_request_desc', None,
        )
        params = SuccessPageModel(
            header=header,
            title=title,
            description=description,
            button_text=button_name,
            callback=self._view_model.page_navigation.channel_management_page,
        )
        self._view_model.page_navigation.show_success_page(params)

    def handle_prev(self):
        """This method handled on previous button click"""
        index = self.stacked_widget.currentIndex()
        if index == 1:
            self.stacked_widget.setCurrentIndex(0)
            self.channel_prev_button.hide()
            self.channel_next_button.setMaximumSize(QSize(402, 40))
            self.public_key_input.setDisabled(False)
            self.channel_next_button.setEnabled(True)
            self.open_channel_page.setMaximumSize(QSize(530, 450))
            self.stacked_widget.hide()

    def on_combo_box_changed(self, index):
        """This method handled combo box means get to selected asset"""
        if index > 0:
            all_assets = self._view_model.channel_view_model.nia_asset + \
                self._view_model.channel_view_model.cfa_asset
            selected_asset = all_assets[index - 1]
            self.asset_id = selected_asset.asset_id
            self.amount_label.show()
            self.amount_line_edit.show()
            self.handle_button_enable()
        if index == 0:
            self.asset_id = None
            self.amount_label.hide()
            self.amount_line_edit.hide()
            self.amount_validation_label.hide()
            self.handle_button_enable()

    def on_amount_changed(self, amount):
        """This method handled entered amount"""
        self.amount = amount

    def on_public_url_changed(self, pub_key):
        """This method handled public url is valid or not """
        validator = NodeValidator()
        state = validator.validate(self.public_key_input.text(), 0)[0]
        self.valid_url = state == QValidator.Acceptable
        if self.valid_url:
            self.error_label.hide()
            self.channel_next_button.setEnabled(True)
        else:
            self.error_label.setText(
                QCoreApplication.translate(
                    IRIS_WALLET_TRANSLATIONS_CONTEXT, 'valid_node_prompt', None,
                ),
            )
            self.error_label.show()
            self.channel_next_button.setEnabled(False)

        self.pub_key = pub_key

        if self.public_key_input.text() == '':
            self.error_label.hide()

    def handle_button_enable(self):
        """This method handles button states."""
        # Initially, disable the button
        self.channel_next_button.setEnabled(False)

        # Get the current index of the stacked widget
        index = self.combo_box.currentIndex()
        page_index = self.stacked_widget.currentIndex()
        # Common checks for required fields
        pub_key_filled = bool(self.pub_key)
        amount_filled = bool(self.amount)
        push_msat_filled = bool(self.push_msat_value.text())
        capacity_filled = bool(self.capacity_sat_value.text())
        if page_index == 0 and self.pub_key and self.valid_url:
            self.channel_next_button.setEnabled(True)

        if page_index == 1:
            capacity_value = self.capacity_sat_value.text()
            if capacity_value.strip() == '':
                capacity_value = 0  # or set a default value like 0
            else:
                capacity_value = int(capacity_value)

            if index == 0:
                self.validate_and_enable_button(
                    capacity_filled, push_msat_filled, index,
                )

            # For index > 0 (subsequent pages)
            elif index > 0:
                self.validate_and_enable_button(
                    capacity_filled, push_msat_filled, pub_key_filled, amount_filled, index,
                )

    def show_create_channel_loading(self):
        """This method handled show loading screen on create channel"""
        self.__loading_translucent_screen = LoadingTranslucentScreen(
            parent=self, description_text='Loading', dot_animation=True,
        )
        self.__loading_translucent_screen.start()

    def stop_loading_screen(self):
        """This method handled stop loading screen on create channel"""
        if self.__loading_translucent_screen:
            self.__loading_translucent_screen.stop()

    def update_loading_state(self, is_loading: bool):
        """
        Updates the loading state of the proceed_wallet_password object.

        This method prints the loading state and starts or stops the loading animation
        of the proceed_wallet_password object based on the value of is_loading.
        """
        if is_loading is True:
            self.render_timer.start()
            self.channel_prev_button.setDisabled(True)
            self.open_close_button.setDisabled(True)
            self.channel_next_button.start_loading()
        if is_loading is False:
            self.render_timer.stop()
            self.open_close_button.setDisabled(False)
            self.channel_prev_button.setDisabled(False)
            self.channel_next_button.stop_loading()

    def validate_and_enable_button(
        self, capacity_filled, push_msat_filled,
        pub_key_filled=None, amount_filled=None, index=0,
    ):
        """
        Validates the input fields and enables or disables the "Next" button based on the provided conditions.

        Behavior:
        - If capacity_filled and push_msat_filled are True, and for index > 0, pub_key_filled and amount_filled are also True:
            - Validates the capacity against CHANNEL_MIN_CAPACITY and CHANNEL_MAX_CAPACITY.
            - If the capacity is within range, the "Next" button is enabled, and the validation label is hidden.
            - If the capacity is out of range, the appropriate validation label (for index 0 or index > 0) is shown, and the button is disabled.
        - If any required fields are not filled, the "Next" button is disabled.
        """
        try:
            push_amount = self.push_msat_value.text().strip()
            push_amount = int(push_amount)
        except ValueError:
            push_amount = 0
        capacity_value = int(self.capacity_sat_value.text() or 0)

        if push_amount > capacity_value:
            self.push_msat_validation_label.show()
            push_msat_filled = False
            self.channel_next_button.setEnabled(False)
        else:
            self.push_msat_validation_label.hide()
            self.channel_next_button.setEnabled(True)

        if capacity_filled and push_msat_filled:
            # Capacity validation with different labels for index 0 and index > 0
            if index == 0:
                if capacity_value < self.node_validation_info.channel_capacity_min_sat or \
                        capacity_value > self.node_validation_info.channel_capacity_max_sat:
                    channel_capacity_validation_text = QCoreApplication.translate(
                        IRIS_WALLET_TRANSLATIONS_CONTEXT, 'channel_capacity_validation', None,
                    ).format(self.node_validation_info.channel_capacity_min_sat, self.node_validation_info.channel_capacity_max_sat)

                    self.channel_capacity_validation_label.setText(
                        channel_capacity_validation_text,
                    )
                    self.channel_capacity_validation_label.show()
                    self.channel_next_button.setEnabled(False)
                    return
            else:
                self.channel_capacity_validation_label.hide()
                self.channel_next_button.setEnabled(True)
            if index >= 1:
                if capacity_value < self.node_validation_info.rgb_channel_capacity_min_sat or \
                        capacity_value > self.node_validation_info.channel_capacity_max_sat:
                    channel_capacity_validation_text = QCoreApplication.translate(
                        IRIS_WALLET_TRANSLATIONS_CONTEXT, 'channel_capacity_validation', None,
                    ).format(self.node_validation_info.rgb_channel_capacity_min_sat, self.node_validation_info.channel_capacity_max_sat)
                    self.channel_capacity_validation_label.setText(
                        channel_capacity_validation_text,
                    )
                    self.channel_capacity_validation_label.show()
                    self.channel_next_button.setEnabled(False)
                    return
            else:
                self.channel_capacity_validation_label.hide()
                self.channel_next_button.setEnabled(True)
            # For index > 0, additional fields must be filled
            if index > 0 and (pub_key_filled is None or amount_filled is None or not (pub_key_filled and amount_filled) or self.amount_line_edit.text() == '0'):
                self.channel_next_button.setEnabled(False)
                return
        else:
            self.channel_next_button.setEnabled(False)

    def handle_amount_validation(self):
        """This method handled asset amount validation"""
        asset_amount = 0
        selected_asset = 0
        channel_asset_max_amount = self.node_validation_info.channel_asset_max_amount
        channel_asset_min_amount = self.node_validation_info.channel_asset_min_amount
        if self.combo_box.currentIndex() > 0:
            selected_asset = self.combo_box.currentText()
        for asset in self._view_model.channel_view_model.nia_asset:
            if selected_asset == asset.ticker:
                asset_amount = asset.balance.future
        entered_amount = self.amount_line_edit.text()
        if entered_amount.strip() == '':
            entered_amount = 0  # or set a default value like 0
        else:
            entered_amount = int(entered_amount)
        if entered_amount > 0:
            if asset_amount is not None and (channel_asset_max_amount < entered_amount or channel_asset_min_amount > entered_amount):
                channel_amount_validation_text = QCoreApplication.translate(
                    IRIS_WALLET_TRANSLATIONS_CONTEXT, 'channel_amount_validation', None,
                ).format(channel_asset_min_amount, channel_asset_max_amount)
                self.amount_validation_label.setText(
                    channel_amount_validation_text,
                )
                self.amount_validation_label.show()
                self.channel_next_button.setEnabled(False)
            else:
                self.amount_validation_label.hide()
        else:
            self.amount_validation_label.setText(
                QCoreApplication.translate(
                    IRIS_WALLET_TRANSLATIONS_CONTEXT, 'channel_with_zero_amount_validation', None,
                ),
            )

            self.amount_validation_label.show()
            self.channel_next_button.setEnabled(False)

    def set_push_amount_placeholder(self, parent: QLineEdit, value='0'):
        """this modules defaults the initial push amount value to 0 and make sure it is not empty"""
        text = parent.text()
        if text == '':
            # If the field is cleared, set it to '0'
            parent.setText(value)
        elif text.startswith(value) and len(text) > 1:
            # If the text starts with "0" but has more than one character, remove the leading "0"
            parent.setText(text[1:])
