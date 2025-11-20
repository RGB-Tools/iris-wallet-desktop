# pylint: disable=too-many-instance-attributes, too-many-statements, unused-import,too-few-public-methods
# This is a UI model class that only defines UI components and holds structured data.
# It does not require additional public method
"""This module contains the SwapWidget class,
which represents the UI for Swap page.
"""
from __future__ import annotations

from PySide6.QtCore import QCoreApplication
from PySide6.QtCore import QRect
from PySide6.QtCore import QSize
from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor
from PySide6.QtGui import QIcon
from PySide6.QtGui import QPixmap
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
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QWidget

import src.resources_rc
from src.utils.helpers import load_stylesheet
from src.viewmodels.main_view_model import MainViewModel
from src.views.components.wallet_logo_frame import WalletLogoFrame


class SwapWidget(QWidget):
    """This class represents all the UI elements of the swap page."""

    def __init__(self, view_model):
        super().__init__()
        self._view_model: MainViewModel = view_model
        self.setStyleSheet(load_stylesheet('views/qss/swap_style.qss'))
        self.setObjectName('swap')
        self.swap_grid_layout_main = QGridLayout(self)
        self.swap_grid_layout_main.setObjectName('gridLayout_22')
        self.vertical_spacer_grid_layout_1 = QSpacerItem(
            20, 190, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding,
        )

        self.swap_grid_layout_main.addItem(
            self.vertical_spacer_grid_layout_1, 0, 2, 1, 1,
        )

        self.horizontal_spacer_grid_layout_1 = QSpacerItem(
            266, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum,
        )

        self.swap_grid_layout_main.addItem(
            self.horizontal_spacer_grid_layout_1, 2, 0, 1, 1,
        )

        self.wallet_frame = WalletLogoFrame()

        self.swap_grid_layout_main.addWidget(self.wallet_frame, 0, 0, 1, 2)

        self.horizontal_spacer_grid_layout_2 = QSpacerItem(
            265, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum,
        )

        self.swap_grid_layout_main.addItem(
            self.horizontal_spacer_grid_layout_2, 1, 3, 1, 1,
        )

        self.vertical_spacer_grid_layout_2 = QSpacerItem(
            20, 190, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding,
        )

        self.swap_grid_layout_main.addItem(
            self.vertical_spacer_grid_layout_2, 3, 1, 1, 1,
        )

        self.swap_widget = QWidget(self)
        self.swap_widget.setObjectName('swap_widget')
        self.swap_widget.setMinimumSize(QSize(499, 831))
        self.swap_widget.setMaximumSize(QSize(499, 831))

        self.grid_layout_1 = QGridLayout(self.swap_widget)
        self.grid_layout_1.setSpacing(6)
        self.grid_layout_1.setObjectName('grid_layout_1')
        self.grid_layout_1.setContentsMargins(1, 4, 1, 30)
        self.vertical_layout_swap_widget = QVBoxLayout()
        self.vertical_layout_swap_widget.setSpacing(11)
        self.vertical_layout_swap_widget.setObjectName(
            'vertical_layout_swap_widget',
        )
        self.horizontal_layout_swap_title = QHBoxLayout()
        self.horizontal_layout_swap_title.setObjectName(
            'horizontal_layout_swap_title',
        )
        self.horizontal_layout_swap_title.setContentsMargins(35, 9, 40, 0)
        self.swap_title_label = QLabel(self.swap_widget)
        self.swap_title_label.setObjectName('swap_title_label')
        self.swap_title_label.setMinimumSize(QSize(415, 63))

        self.horizontal_layout_swap_title.addWidget(self.swap_title_label)

        self.swap_close_button = QPushButton(self.swap_widget)
        self.swap_close_button.setObjectName('swap_close_button')
        self.swap_close_button.setMinimumSize(QSize(24, 24))
        self.swap_close_button.setMaximumSize(QSize(50, 65))
        self.swap_close_button.setAutoFillBackground(False)

        close_icon = QIcon()
        close_icon.addFile(
            ':/assets/x_circle.png',
            QSize(),
            QIcon.Normal,
            QIcon.Off,
        )
        self.swap_close_button.setIcon(close_icon)
        self.swap_close_button.setIconSize(QSize(24, 24))
        self.swap_close_button.setCheckable(False)
        self.swap_close_button.setChecked(False)

        self.horizontal_layout_swap_title.addWidget(
            self.swap_close_button, 0, Qt.AlignHCenter,
        )

        self.vertical_layout_swap_widget.addLayout(
            self.horizontal_layout_swap_title,
        )

        self.line_3 = QFrame(self.swap_widget)
        self.line_3.setObjectName('line_3')

        self.line_3.setFrameShape(QFrame.Shape.HLine)
        self.line_3.setFrameShadow(QFrame.Shadow.Sunken)

        self.vertical_layout_swap_widget.addWidget(self.line_3)

        self.from_frame = QFrame(self.swap_widget)
        self.from_frame.setObjectName('from_frame')
        self.from_frame.setMinimumSize(QSize(335, 182))
        self.from_frame.setMaximumSize(QSize(16777215, 16777215))

        self.from_frame.setFrameShape(QFrame.StyledPanel)
        self.from_frame.setFrameShadow(QFrame.Raised)
        self.grid_layout_2 = QGridLayout(self.from_frame)
        self.grid_layout_2.setObjectName('grid_layout_2')
        self.grid_layout_2.setVerticalSpacing(10)
        self.grid_layout_2.setContentsMargins(10, 17, -1, 0)
        self.horizontal_layout_from_input_combobox = QHBoxLayout()
        self.horizontal_layout_from_input_combobox.setObjectName(
            'horizontal_layout_from_input_combobox',
        )
        self.from_amount_input = QLineEdit(self.from_frame)
        self.from_amount_input.setObjectName('from_amount_input')
        self.from_amount_input.setMinimumSize(QSize(170, 40))
        self.from_amount_input.setMaximumSize(QSize(170, 40))

        self.horizontal_layout_from_input_combobox.addWidget(
            self.from_amount_input,
        )

        self.from_asset_combobox = QComboBox(self.from_frame)
        self.from_asset_combobox.addItem('')
        self.from_asset_combobox.setObjectName('from_asset_combobox')
        self.from_asset_combobox.setMinimumSize(QSize(125, 40))
        self.from_asset_combobox.setMaximumSize(QSize(125, 40))

        self.horizontal_layout_from_input_combobox.addWidget(
            self.from_asset_combobox,
        )

        self.grid_layout_2.addLayout(
            self.horizontal_layout_from_input_combobox, 2, 0, 1, 1,
        )

        self.horizontal_layout_button_p = QHBoxLayout()
        self.horizontal_layout_button_p.setObjectName(
            'horizontal_layout_button_p',
        )
        self.horizontal_layout_button_p.setContentsMargins(-1, -1, 0, -1)
        self.button_25p = QPushButton(self.from_frame)
        self.button_25p.setObjectName('button_25p')
        self.button_25p.setMinimumSize(QSize(67, 34))
        self.button_25p.setMaximumSize(QSize(67, 34))

        self.horizontal_layout_button_p.addWidget(self.button_25p)

        self.button_50p = QPushButton(self.from_frame)
        self.button_50p.setObjectName('button_50p')
        self.button_50p.setMinimumSize(QSize(67, 34))
        self.button_50p.setMaximumSize(QSize(67, 34))

        self.horizontal_layout_button_p.addWidget(self.button_50p)

        self.button_75p = QPushButton(self.from_frame)
        self.button_75p.setObjectName('button_75p')
        self.button_75p.setMinimumSize(QSize(67, 34))
        self.button_75p.setMaximumSize(QSize(67, 34))

        self.horizontal_layout_button_p.addWidget(self.button_75p)

        self.button_100p = QPushButton(self.from_frame)
        self.button_100p.setObjectName('button_100p')
        self.button_100p.setMinimumSize(QSize(67, 34))
        self.button_100p.setMaximumSize(QSize(67, 34))

        self.horizontal_layout_button_p.addWidget(self.button_100p)

        self.grid_layout_2.addLayout(
            self.horizontal_layout_button_p, 3, 0, 1, 1,
        )

        self.horizontal_layout_from_trading_balance = QHBoxLayout()
        self.horizontal_layout_from_trading_balance.setSpacing(1)
        self.horizontal_layout_from_trading_balance.setObjectName(
            'horizontal_layout_from_trading_balance',
        )
        self.horizontal_layout_from_trading_balance.setContentsMargins(
            7, -1, -1, -1,
        )
        self.trading_balance_label = QLabel(self.from_frame)
        self.trading_balance_label.setObjectName('trading_balance_label')
        self.trading_balance_label.setMinimumSize(QSize(100, 18))
        self.trading_balance_label.setMaximumSize(QSize(16777215, 18))

        self.horizontal_layout_from_trading_balance.addWidget(
            self.trading_balance_label,
        )

        self.trading_balance_value = QLabel(self.from_frame)
        self.trading_balance_value.setObjectName('trading_balance_value')
        self.trading_balance_value.setMinimumSize(QSize(30, 0))
        self.trading_balance_value.setMaximumSize(QSize(16777215, 18))

        self.horizontal_layout_from_trading_balance.addWidget(
            self.trading_balance_value,
        )

        self.info_label = QLabel(self.from_frame)
        self.info_label.setObjectName('info_label')
        self.info_label.setMinimumSize(QSize(15, 0))
        self.info_label.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.info_label.setPixmap(QPixmap(':/assets/info_circle.png'))

        self.horizontal_layout_from_trading_balance.addWidget(
            self.info_label, 0, Qt.AlignRight,
        )

        self.horizontal_spacer_13 = QSpacerItem(
            40, 15, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum,
        )

        self.horizontal_layout_from_trading_balance.addItem(
            self.horizontal_spacer_13,
        )

        self.grid_layout_2.addLayout(
            self.horizontal_layout_from_trading_balance, 0, 0, 1, 1,
        )

        self.from_label = QLabel(self.from_frame)
        self.from_label.setObjectName('from_label')
        self.from_label.setMinimumSize(QSize(0, 20))
        self.from_label.setMaximumSize(QSize(16777215, 20))

        self.grid_layout_2.addWidget(self.from_label, 1, 0, 1, 1)

        self.vertical_spacer_from = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding,
        )

        self.grid_layout_2.addItem(self.vertical_spacer_from, 4, 0, 1, 1)

        self.vertical_layout_swap_widget.addWidget(
            self.from_frame, 0, Qt.AlignHCenter,
        )

        self.vertical_spacer_swap_widget_2 = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding,
        )

        self.vertical_layout_swap_widget.addItem(
            self.vertical_spacer_swap_widget_2,
        )

        self.swap_icon = QLabel(self.swap_widget)
        self.swap_icon.setObjectName('swap_icon')
        self.swap_icon.setMinimumSize(QSize(0, 25))
        self.swap_icon.setMaximumSize(QSize(16777215, 25))

        self.swap_icon.setPixmap(QPixmap(':/assets/swap.png'))

        self.vertical_layout_swap_widget.addWidget(
            self.swap_icon, 0, Qt.AlignHCenter,
        )

        self.to_frame = QFrame(self.swap_widget)
        self.to_frame.setObjectName('to_frame')
        self.to_frame.setMinimumSize(QSize(335, 132))
        self.to_frame.setMaximumSize(QSize(335, 16777215))

        self.to_frame.setFrameShape(QFrame.StyledPanel)
        self.to_frame.setFrameShadow(QFrame.Raised)
        self.vertical_layout_7 = QVBoxLayout(self.to_frame)
        self.vertical_layout_7.setObjectName('verticalLayout_7')
        self.vertical_layout_7.setContentsMargins(9, 12, -1, 15)
        self.horizontal_layout_to_trading_balance = QHBoxLayout()
        self.horizontal_layout_to_trading_balance.setSpacing(1)
        self.horizontal_layout_to_trading_balance.setObjectName(
            'horizontal_layout_to_trading_balance',
        )
        self.horizontal_layout_to_trading_balance.setContentsMargins(
            7, -1, -1, -1,
        )
        self.trading_balance_to = QLabel(self.to_frame)
        self.trading_balance_to.setObjectName('trading_balance_to')
        self.trading_balance_to.setMinimumSize(QSize(100, 18))
        self.trading_balance_to.setMaximumSize(QSize(16777215, 18))

        self.horizontal_layout_to_trading_balance.addWidget(
            self.trading_balance_to,
        )

        self.trading_balance_amount_to = QLabel(self.to_frame)
        self.trading_balance_amount_to.setObjectName(
            'trading_balance_amount_to',
        )
        self.trading_balance_amount_to.setMinimumSize(QSize(30, 0))
        self.trading_balance_amount_to.setMaximumSize(QSize(16777215, 18))

        self.horizontal_layout_to_trading_balance.addWidget(
            self.trading_balance_amount_to,
        )

        self.info_to = QLabel(self.to_frame)
        self.info_to.setObjectName('info_to')
        self.info_to.setMinimumSize(QSize(15, 0))
        self.info_to.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.info_to.setPixmap(QPixmap(':/assets/info_circle.png'))

        self.horizontal_layout_to_trading_balance.addWidget(self.info_to)

        self.horizontal_spacer_to = QSpacerItem(
            40, 15, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum,
        )

        self.horizontal_layout_to_trading_balance.addItem(
            self.horizontal_spacer_to,
        )

        self.vertical_layout_7.addLayout(
            self.horizontal_layout_to_trading_balance,
        )

        self.to_label = QLabel(self.to_frame)
        self.to_label.setObjectName('to_label')

        self.vertical_layout_7.addWidget(self.to_label)

        self.horizontal_layout_to_input_combobox = QHBoxLayout()
        self.horizontal_layout_to_input_combobox.setObjectName(
            'horizontal_layout_to_input_combobox',
        )
        self.to_amount_input = QLineEdit(self.to_frame)
        self.to_amount_input.setObjectName('to_amount_input')
        self.to_amount_input.setMinimumSize(QSize(170, 40))
        self.to_amount_input.setMaximumSize(QSize(170, 40))

        self.horizontal_layout_to_input_combobox.addWidget(
            self.to_amount_input,
        )

        self.to_asset_combobox = QComboBox(self.to_frame)
        self.to_asset_combobox.addItem('')
        self.to_asset_combobox.setObjectName('to_asset_combobox')
        self.to_asset_combobox.setMinimumSize(QSize(125, 40))
        self.to_asset_combobox.setMaximumSize(QSize(125, 40))

        self.horizontal_layout_to_input_combobox.addWidget(
            self.to_asset_combobox,
        )

        self.vertical_layout_7.addLayout(
            self.horizontal_layout_to_input_combobox,
        )

        self.vertical_layout_swap_widget.addWidget(
            self.to_frame, 0, Qt.AlignHCenter,
        )

        self.label_9 = QLabel(self.swap_widget)
        self.label_9.setObjectName('label_9')
        self.label_9.setMinimumSize(QSize(0, 25))

        self.vertical_layout_swap_widget.addWidget(
            self.label_9, 0, Qt.AlignHCenter,
        )

        self.market_maker_frame = QFrame(self.swap_widget)
        self.market_maker_frame.setObjectName('market_maker_frame')
        self.market_maker_frame.setMinimumSize(QSize(345, 178))
        self.market_maker_frame.setMaximumSize(QSize(345, 16777215))

        self.market_maker_frame.setFrameShape(QFrame.StyledPanel)
        self.market_maker_frame.setFrameShadow(QFrame.Raised)
        self.vertical_layout_9 = QVBoxLayout(self.market_maker_frame)
        self.vertical_layout_9.setObjectName('verticalLayout_9')
        self.vertical_layout_9.setContentsMargins(-1, 12, -1, 12)
        self.vertical_layout_market_maker_frame = QVBoxLayout()
        self.vertical_layout_market_maker_frame.setObjectName(
            'vertical_layout_market_maker_frame',
        )
        self.scroll_area_maker = QScrollArea(self.market_maker_frame)
        self.scroll_area_maker.setObjectName('scroll_area_maker')
        self.scroll_area_maker.setWidgetResizable(True)
        self.scroll_area_widget_contents_maker = QWidget()
        self.scroll_area_widget_contents_maker.setObjectName(
            'scroll_area_widget_contents_maker',
        )
        self.scroll_area_widget_contents_maker.setGeometry(
            QRect(0, 0, 320, 112),
        )
        self.vertical_layout_15 = QVBoxLayout(
            self.scroll_area_widget_contents_maker,
        )
        self.vertical_layout_15.setSpacing(10)
        self.vertical_layout_15.setObjectName('verticalLayout_15')
        self.vertical_layout_15.setContentsMargins(5, 1, 5, 1)
        self.maker_vertical_layout = QVBoxLayout()
        self.maker_vertical_layout.setObjectName('maker_vertical_layout')
        self.maker_horizontal_layout = QHBoxLayout()
        self.maker_horizontal_layout.setObjectName('maker_horizontal_layout')
        self.market_maker_label = QLabel(
            self.scroll_area_widget_contents_maker,
        )
        self.market_maker_label.setObjectName('market_maker_label')
        self.market_maker_label.setMinimumSize(QSize(0, 40))
        self.market_maker_label.setMaximumSize(QSize(16777215, 40))

        self.maker_horizontal_layout.addWidget(self.market_maker_label)

        self.market_maker_input = QLineEdit(
            self.scroll_area_widget_contents_maker,
        )
        self.market_maker_input.setObjectName('market_maker_input')
        self.market_maker_input.setMinimumSize(QSize(147, 40))
        self.market_maker_input.setMaximumSize(QSize(16777215, 40))

        self.maker_horizontal_layout.addWidget(self.market_maker_input)

        self.market_maker_icon = QLabel(self.scroll_area_widget_contents_maker)
        self.market_maker_icon.setObjectName('market_maker_icon')
        self.market_maker_icon.setMaximumSize(QSize(16777215, 40))
        self.market_maker_icon.setPixmap(QPixmap(':/assets/btc_lightning.png'))

        self.maker_horizontal_layout.addWidget(self.market_maker_icon)

        self.maker_vertical_layout.addLayout(self.maker_horizontal_layout)

        self.vertical_layout_15.addLayout(self.maker_vertical_layout)

        self.maker_horizontal_layout1 = QHBoxLayout()
        self.maker_horizontal_layout1.setObjectName('maker_horizontal_layout1')
        self.market_maker_label1 = QLabel(
            self.scroll_area_widget_contents_maker,
        )
        self.market_maker_label1.setObjectName('market_maker_label1')
        self.market_maker_label1.setMinimumSize(QSize(0, 40))
        self.market_maker_label1.setMaximumSize(QSize(16777215, 40))

        self.maker_horizontal_layout1.addWidget(self.market_maker_label1)

        self.market_maker_input1 = QLineEdit(
            self.scroll_area_widget_contents_maker,
        )
        self.market_maker_input1.setObjectName('market_maker_input1')
        self.market_maker_input1.setMinimumSize(QSize(147, 40))
        self.market_maker_input1.setMaximumSize(QSize(16777215, 40))

        self.maker_horizontal_layout1.addWidget(self.market_maker_input1)

        self.market_maker_icon1 = QLabel(
            self.scroll_area_widget_contents_maker,
        )
        self.market_maker_icon1.setObjectName('market_maker_icon1')
        self.market_maker_icon1.setMaximumSize(QSize(16777215, 40))
        self.market_maker_icon1.setPixmap(
            QPixmap(':/assets/btc_lightning.png'),
        )

        self.maker_horizontal_layout1.addWidget(self.market_maker_icon1)

        self.vertical_layout_15.addLayout(self.maker_horizontal_layout1)

        self.scroll_area_spacer = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding,
        )

        self.vertical_layout_15.addItem(self.scroll_area_spacer)

        self.scroll_area_maker.setWidget(
            self.scroll_area_widget_contents_maker,
        )

        self.vertical_layout_market_maker_frame.addWidget(
            self.scroll_area_maker,
        )

        self.vertical_layout_9.addLayout(
            self.vertical_layout_market_maker_frame,
        )

        self.add_market_maker_button = QPushButton(self.market_maker_frame)
        self.add_market_maker_button.setObjectName('add_market_maker_button')
        self.add_market_maker_button.setMinimumSize(QSize(300, 34))
        self.add_market_maker_button.setMaximumSize(QSize(300, 34))

        self.vertical_layout_9.addWidget(
            self.add_market_maker_button, 0, Qt.AlignHCenter,
        )

        self.vertical_layout_swap_widget.addWidget(
            self.market_maker_frame, 0, Qt.AlignHCenter,
        )

        self.vertical_spacer_swap_widget_3 = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding,
        )

        self.vertical_layout_swap_widget.addItem(
            self.vertical_spacer_swap_widget_3,
        )

        self.line_4 = QFrame(self.swap_widget)
        self.line_4.setObjectName('line_4')

        self.line_4.setFrameShape(QFrame.Shape.HLine)
        self.line_4.setFrameShadow(QFrame.Shadow.Sunken)

        self.vertical_layout_swap_widget.addWidget(self.line_4)

        self.swap_button_layout = QHBoxLayout()
        self.swap_button_layout.setObjectName('swap_button_layout')
        self.swap_button_layout.setContentsMargins(-1, 22, -1, -1)
        self.swap_button = QPushButton(self.swap_widget)
        self.swap_button.setObjectName('swap_button')
        size_policy_swap_button = QSizePolicy(
            QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed,
        )
        size_policy_swap_button.setHorizontalStretch(1)
        size_policy_swap_button.setVerticalStretch(0)
        size_policy_swap_button.setHeightForWidth(
            self.swap_button.sizePolicy().hasHeightForWidth(),
        )
        self.swap_button.setSizePolicy(size_policy_swap_button)
        self.swap_button.setMinimumSize(QSize(402, 40))
        self.swap_button.setMaximumSize(QSize(402, 16777215))

        self.swap_button_layout.addWidget(self.swap_button, 0, Qt.AlignHCenter)

        self.vertical_layout_swap_widget.addLayout(self.swap_button_layout)

        self.grid_layout_1.addLayout(
            self.vertical_layout_swap_widget, 0, 0, 1, 1,
        )

        self.swap_grid_layout_main.addWidget(self.swap_widget, 1, 1, 2, 2)

        self.retranslate_ui()

    def retranslate_ui(self):
        """Retranslate the UI elements."""
        self.wallet_frame.logo_text.setText(
            QCoreApplication.translate('MainWindow', 'Iris Wallet', None),
        )
        self.from_amount_input.setText(
            QCoreApplication.translate('MainWindow', '0', None),
        )
        self.from_asset_combobox.setItemText(
            0, QCoreApplication.translate('MainWindow', 'rBTC', None),
        )
        self.swap_title_label.setText(
            QCoreApplication.translate('MainWindow', 'Swap', None),
        )
        self.button_25p.setText(
            QCoreApplication.translate('MainWindow', '25%', None),
        )
        self.button_50p.setText(
            QCoreApplication.translate('MainWindow', '50%', None),
        )
        self.button_75p.setText(
            QCoreApplication.translate('MainWindow', '75%', None),
        )
        self.button_100p.setText(
            QCoreApplication.translate('MainWindow', '100%', None),
        )
        self.trading_balance_label.setText(
            QCoreApplication.translate('MainWindow', 'Trading balance:', None),
        )
        self.trading_balance_value.setText(
            QCoreApplication.translate('MainWindow', '40,500', None),
        )
# if QT_CONFIG(tooltip)
        self.info_label.setToolTip(
            QCoreApplication.translate(
                'MainWindow', 'Hello i m status', None,
            ),
        )
# endif // QT_CONFIG(tooltip)
        self.from_label.setText(
            QCoreApplication.translate('MainWindow', 'From', None),
        )
        self.swap_icon.setText('')
        self.trading_balance_to.setText(
            QCoreApplication.translate(
                'MainWindow', 'Trading balance:', None,
            ),
        )
        self.trading_balance_amount_to.setText(
            QCoreApplication.translate('MainWindow', '40,500', None),
        )
# if QT_CONFIG(tooltip)
        self.info_to.setToolTip(
            QCoreApplication.translate(
                'MainWindow', 'Hello i m status', None,
            ),
        )
# endif // QT_CONFIG(tooltip)
        self.to_label.setText(
            QCoreApplication.translate('MainWindow', 'To', None),
        )
        self.to_amount_input.setText(
            QCoreApplication.translate('MainWindow', '0', None),
        )
        self.to_asset_combobox.setItemText(
            0, QCoreApplication.translate('MainWindow', 'rBTC', None),
        )

        self.label_9.setText(
            QCoreApplication.translate(
                'MainWindow', '2 routes found', None,
            ),
        )
        self.market_maker_label.setText(
            QCoreApplication.translate('MainWindow', 'Market maker 1', None),
        )
        self.market_maker_input.setText(
            QCoreApplication.translate('MainWindow', '1', None),
        )
        self.market_maker_icon.setText('')
        self.market_maker_label1.setText(
            QCoreApplication.translate('MainWindow', 'Market maker 2', None),
        )
        self.market_maker_input1.setText(
            QCoreApplication.translate('MainWindow', '0.99', None),
        )
        self.market_maker_icon1.setText('')
        self.add_market_maker_button.setText(
            QCoreApplication.translate(
                'MainWindow', 'Add new market maker', None,
            ),
        )
        self.swap_button.setText(
            QCoreApplication.translate('MainWindow', 'Swap', None),
        )
