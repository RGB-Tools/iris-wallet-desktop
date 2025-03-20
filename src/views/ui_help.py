# pylint: disable=too-many-instance-attributes, too-many-statements, unused-import,implicit-str-concat
"""This module contains the HelpWidget,
 which represents the UI for help page.
 """
from __future__ import annotations

from PySide6.QtCore import QCoreApplication
from PySide6.QtCore import QRect
from PySide6.QtCore import QSize
from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor
from PySide6.QtWidgets import QFrame
from PySide6.QtWidgets import QGridLayout
from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QScrollArea
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtWidgets import QSpacerItem
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QWidget

from accessible_constant import HELP_CARD_TITLE_ACCESSIBLE_DESCRIPTION
from src.model.help_card_content_model import HelpCardContentModel
from src.utils.constant import IRIS_WALLET_TRANSLATIONS_CONTEXT
from src.utils.helpers import load_stylesheet
from src.viewmodels.main_view_model import MainViewModel
from src.views.components.header_frame import HeaderFrame


class HelpWidget(QWidget):
    """This class represents all the UI elements of the help page."""

    def __init__(self, view_model):
        super().__init__()
        self._model = HelpCardContentModel.create_default()
        self.setStyleSheet(load_stylesheet('views/qss/help_style.qss'))
        self._view_model: MainViewModel = view_model
        self.help_card_frame = None
        self.vertical_layout_3 = None
        self.help_card_title_labe = None
        self.help_card_detail_label = None
        self.url_vertical_layout = None
        self.url = None
        self.help_card_title_label = None
        self.grid_layout = QGridLayout(self)
        self.grid_layout.setSpacing(0)
        self.grid_layout.setObjectName('gridLayout')
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.help_widget = QWidget(self)
        self.help_widget.setObjectName('help_widget')
        self.help_widget.setMinimumSize(QSize(492, 80))

        self.vertical_layout_2 = QVBoxLayout(self.help_widget)
        self.vertical_layout_2.setSpacing(12)
        self.vertical_layout_2.setObjectName('verticalLayout_2')
        self.vertical_layout_2.setContentsMargins(25, 12, 25, 1)
        self.help_title_frame = HeaderFrame(
            title_logo_path=':/assets/question_circle.png', title_name='help',
        )
        self.help_title_frame.refresh_page_button.hide()
        self.help_title_frame.action_button.hide()
        self.vertical_layout_2.addWidget(self.help_title_frame)

        self.help_title_label = QLabel(self.help_widget)
        self.help_title_label.setObjectName('help_title_label')
        self.help_title_label.setMinimumSize(QSize(0, 54))
        self.help_title_label.setMaximumSize(QSize(16777215, 54))

        self.help_title_label.setAlignment(Qt.AlignCenter)

        self.vertical_layout_2.addWidget(
            self.help_title_label, 0, Qt.AlignLeft,
        )

        self.help_card_vertical_layout = QVBoxLayout()
        self.help_card_vertical_layout.setSpacing(8)
        self.help_card_vertical_layout.setObjectName(
            'help_card_vertical_layout',
        )
        self.help_card_scroll_area = QScrollArea(self.help_widget)
        self.help_card_scroll_area.setObjectName('help_card_scroll_area')
        self.help_card_scroll_area.setWidgetResizable(True)

        self.help_card_scroll_area_widget_contents = QWidget()
        self.help_card_scroll_area_widget_contents.setObjectName(
            'help_card_scroll_area_widget_contents',
        )
        self.help_card_scroll_area_widget_contents.setGeometry(
            QRect(0, 0, 1082, 681),
        )
        self.vertical_layout_4 = QVBoxLayout(
            self.help_card_scroll_area_widget_contents,
        )
        self.vertical_layout_4.setObjectName('verticalLayout_4')

        self.help_card_scroll_area.setWidget(
            self.help_card_scroll_area_widget_contents,
        )

        self.help_card_vertical_layout.addWidget(self.help_card_scroll_area)

        self.vertical_layout_2.addLayout(self.help_card_vertical_layout)

        self.grid_layout.addWidget(self.help_widget, 0, 0, 1, 1)

        self.retranslate_ui()

        self.create_help_frames()

    def retranslate_ui(self):
        """Retranslate the UI elements."""
        self.help_title_label.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'help', None,
            ),
        )

    def create_help_frames(self):
        """Creates the help frames and distributes them into two columns."""
        count = 1
        help_card_horizontal_layout = QHBoxLayout()

        help_card_left_vertical_layout = QVBoxLayout()
        help_card_right_vertical_layout = QVBoxLayout()

        card_list = self._model.card_content
        for i, card in enumerate(card_list):
            help_card = self.create_help_card(
                card.title, card.detail, card.links, count,
            )
            count += 1
            if i % 2 == 0:
                help_card_left_vertical_layout.addWidget(help_card)
            else:
                help_card_right_vertical_layout.addWidget(help_card)

        help_card_left_vertical_layout.addStretch()
        help_card_right_vertical_layout.addStretch()
        self.main_horizontal_spacer = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum,
        )
        help_card_horizontal_layout.addLayout(help_card_left_vertical_layout)
        help_card_horizontal_layout.addLayout(help_card_right_vertical_layout)
        help_card_horizontal_layout.addItem(self.main_horizontal_spacer)

        self.vertical_layout_4.addLayout(help_card_horizontal_layout)

        self.main_vertical_spacer = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding,
        )

        self.vertical_layout_4.addItem(self.main_vertical_spacer)

    def create_help_card(self, title, detail, links, count):
        """This method creates the single help card"""
        self.help_card_frame = QFrame(
            self.help_card_scroll_area_widget_contents,
        )
        self.help_card_frame.setObjectName('help_card_frame')
        self.help_card_frame.setMinimumSize(QSize(492, 70))
        self.help_card_frame.setMaximumSize(QSize(335, 16777215))

        self.help_card_frame.setFrameShape(QFrame.StyledPanel)
        self.help_card_frame.setFrameShadow(QFrame.Raised)
        self.vertical_layout_3 = QVBoxLayout(self.help_card_frame)
        self.vertical_layout_3.setSpacing(15)
        self.vertical_layout_3.setObjectName('verticalLayout_3')
        self.vertical_layout_3.setContentsMargins(15, 20, 15, 20)
        self.help_card_title_label = QLabel(self.help_card_frame)
        self.help_card_title_label.setObjectName('help_card_title_label')
        self.help_card_title_label.setAccessibleDescription(
            HELP_CARD_TITLE_ACCESSIBLE_DESCRIPTION+'_'+str(count),
        )
        self.help_card_title_label.setWordWrap(True)

        self.vertical_layout_3.addWidget(self.help_card_title_label)

        self.help_card_detail_label = QLabel(self.help_card_frame)
        self.help_card_detail_label.setObjectName('help_card_detail_label')
        self.help_card_detail_label.setWordWrap(True)

        self.vertical_layout_3.addWidget(self.help_card_detail_label)

        self.url_vertical_layout = QVBoxLayout()
        self.url_vertical_layout.setObjectName('url_vertical_layout')
        if links:
            for link in links:
                self.url = QLabel(self.help_card_frame)
                self.url.setObjectName(str(link))
                self.url.setText(
                    f"<a style='color: #03CA9B;' href='{link}'>{link}</a>",
                )
                self.url.setMinimumSize(QSize(0, 15))
                self.url.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
                self.url.setTextInteractionFlags(Qt.TextBrowserInteraction)
                self.url.setOpenExternalLinks(True)
                self.url_vertical_layout.addWidget(self.url)
        if links:
            for link in links:
                self.url = QLabel(self.help_card_frame)
                self.url.setObjectName(str(link))
                self.url.setText(
                    f"<a style='color: #03CA9B;' href='{link}'>{link}</a>",
                )
                self.url.setMinimumSize(QSize(0, 15))
                self.url.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
                self.url.setTextInteractionFlags(Qt.TextBrowserInteraction)
                self.url.setOpenExternalLinks(True)
                self.url_vertical_layout.addWidget(self.url)

        self.vertical_layout_3.addLayout(self.url_vertical_layout)

        self.help_card_title_label.setText(
            QCoreApplication.translate('iris_wallet_desktop', title),
        )
        translated_detail = QCoreApplication.translate(
            'iris_wallet_desktop', detail, None,
        )

        rgb_info_link = '<a href="https://rgb.info" style="color: #03CA9B; text-decoration: none;">rgb.info</a>'

        formatted_detail = translated_detail.replace(
            'rgb.info', rgb_info_link,
        ) if 'rgb.info' in translated_detail else translated_detail

        self.help_card_detail_label.setText(formatted_detail)

        return self.help_card_frame
