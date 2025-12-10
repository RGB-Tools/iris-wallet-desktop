# pylint: disable=too-many-instance-attributes, too-many-statements, unused-import
"""This module contains the CollectiblesAssetWidget class,
which represents the UI for collectibles assets.
"""
from __future__ import annotations

from PySide6.QtCore import QCoreApplication
from PySide6.QtCore import QSize
from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor
from PySide6.QtWidgets import QFormLayout
from PySide6.QtWidgets import QFrame
from PySide6.QtWidgets import QGridLayout
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QScrollArea
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtWidgets import QSpacerItem
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QWidget

import src.resources_rc
from accessible_constant import ISSUE_CFA_ASSET
from src.model.enums.enums_model import AssetType
from src.model.enums.enums_model import ToastPreset
from src.model.rgb_model import RgbAssetPageLoadModel
from src.utils.clickable_frame import ClickableFrame
from src.utils.common_utils import convert_hex_to_image
from src.utils.common_utils import resize_image
from src.utils.constant import IRIS_WALLET_TRANSLATIONS_CONTEXT
from src.utils.helpers import load_stylesheet
from src.utils.logging import logger
from src.utils.render_timer import RenderTimer
from src.viewmodels.main_view_model import MainViewModel
from src.views.components.header_frame import HeaderFrame
from src.views.components.loading_screen import LoadingTranslucentScreen
from src.views.components.toast import ToastManager


class CollectiblesAssetWidget(QWidget):
    """This class represents all the UI elements of the collectibles asset page."""

    def __init__(self, view_model):
        self.render_timer = RenderTimer(
            task_name='CollectiblesAssetWidget Rendering',
        )
        self.render_timer.start()
        super().__init__()
        self._view_model: MainViewModel = view_model
        self.setStyleSheet(
            load_stylesheet(
                'views/qss/collectible_asset_style.qss',
            ),
        )
        self.num_columns = None
        self._view_model.main_asset_view_model.asset_loaded.connect(
            self.create_collectibles_frames,
        )

        self.setObjectName('collectibles_page')
        self.loading_screen = None
        self.grid_layout_widget = None
        self.vertical_layout_collectibles = QVBoxLayout(self)
        self.vertical_layout_collectibles.setObjectName(
            'vertical_layout_collectibles',
        )
        self.vertical_layout_collectibles.setContentsMargins(0, 0, 0, 0)
        self.widget = QWidget(self)
        self.widget.setObjectName('collectibles_widget')

        self.vertical_layout_2 = QVBoxLayout(self.widget)
        self.vertical_layout_2.setObjectName('vertical_layout_2')
        self.vertical_layout_2.setContentsMargins(25, 12, 25, 0)
        self.asset_name = None
        self.collectibles_frame = None
        self.collectible_frame_grid_layout = None
        self.collectible_asset_name = None
        self.image_label = None
        self.horizontal_spacer = None
        self.vertical_spacer_scroll_area = None

        self.collectible_header_frame = HeaderFrame(
            title_name='collectibles', title_logo_path=':/assets/my_asset.png',
        )
        self.collectible_header_frame.action_button.setAccessibleName(
            ISSUE_CFA_ASSET,
        )
        self.vertical_layout_2.addWidget(self.collectible_header_frame)

        self.collectibles_label = QLabel(self.widget)
        self.collectibles_label.setObjectName('collectibles_label')
        self.collectibles_label.setMinimumSize(QSize(1016, 50))
        self.collectibles_label.setMaximumSize(QSize(1016, 50))

        self.vertical_layout_2.addWidget(self.collectibles_label)

        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(6)

        self.grid_layout.setObjectName('grid_layout')
        self.grid_layout.setContentsMargins(1, -1, 1, -1)

        self.vertical_layout_collectibles.addWidget(self.widget)
        self.collectibles_frame_card = QFrame(self.widget)
        self.collectibles_frame_card.setObjectName('collectibles_frame_card')

        self.collectibles_frame_card.setFrameShape(QFrame.StyledPanel)
        self.collectibles_frame_card.setFrameShadow(QFrame.Raised)
        self.collectible_frame_grid_layout = QFormLayout(
            self.collectibles_frame_card,
        )
        self.collectible_frame_grid_layout.setObjectName(
            'collectible_frame_grid_layout',
        )
        self.collectible_frame_grid_layout.setHorizontalSpacing(0)
        self.collectible_frame_grid_layout.setVerticalSpacing(0)
        self.collectible_frame_grid_layout.setContentsMargins(3, -1, 3, -1)

        self.grid_layout.addWidget(self.collectibles_frame_card)

        self.vertical_layout_2.addLayout(self.grid_layout)

        self.retranslate_ui()
        self.setup_ui_connection()
        self.resizeEvent = self.resize_event_called  # pylint: disable=invalid-name

    def calculate_columns(self):
        """Calculate the number of columns based on the available width"""
        available_width = self.width()
        item_width = 290
        num_columns = max(1, available_width // item_width)
        return num_columns

    def resize_event_called(self, event):
        """It updates the layout of collectibles when window is resized"""
        super().resizeEvent(event)
        self._view_model.main_asset_view_model.asset_loaded.connect(
            self.update_grid_layout,
        )

    def update_grid_layout(self):
        """Update the grid layout with new number of columns"""
        num_columns = self.calculate_columns()
        collectibles_list = self._view_model.main_asset_view_model.assets.cfa
        total_items = len(collectibles_list)

        if hasattr(self, 'scroll_area'):
            grid_widget = self.scroll_area.widget()
            grid_layout = grid_widget.layout()
            grid_layout.setSpacing(40)

            # Clear the existing layout
            for i in reversed(range(grid_layout.count())):
                item = grid_layout.itemAt(i)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    grid_layout.removeItem(item)

            # Add widgets to the grid layout
            for index, coll_asset in enumerate(collectibles_list):
                collectibles_frame = self.create_collectible_frame(coll_asset)
                row = index // num_columns
                col = index % num_columns
                grid_layout.addWidget(collectibles_frame, row, col)
            # Add spacers if the last row is not full
            if total_items < 5:
                remaining_columns = num_columns - (total_items % num_columns)
                row = total_items // num_columns
                for col in range(num_columns - remaining_columns, num_columns):
                    horizontal_spacer = QSpacerItem(
                        242, 242, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum,
                    )
                    grid_layout.addItem(horizontal_spacer, row, col)

            self.grid_layout = grid_layout
            self.resizeEvent = self.resize_event_called

    def create_collectibles_frames(self):
        """Initial setup for the grid layout and scroll area"""
        if not hasattr(self, 'scroll_area'):
            grid_widget = QWidget()
            self.grid_layout_widget = QGridLayout(grid_widget)
            grid_widget.setStyleSheet("""
                border:none;
                background: transparent;
            """)

            self.scroll_area = QScrollArea()  # pylint: disable=W0201
            self.scroll_area.setWidgetResizable(True)
            self.scroll_area.setWidget(grid_widget)
            self.scroll_area.setVerticalScrollBarPolicy(
                Qt.ScrollBarPolicy.ScrollBarAsNeeded,
            )
            self.scroll_area.setStyleSheet(
                load_stylesheet('views/qss/scrollbar.qss'),
            )

            self.grid_layout.addWidget(self.scroll_area)

        self.grid_layout.setSpacing(10)
        self.grid_layout.setVerticalSpacing(20)
        self.update_grid_layout()
        self.resizeEvent = self.resize_event_called

    def create_collectible_frame(self, coll_asset):
        """Create a single collectible frame"""
        if coll_asset.media.hex is None:
            image_path = coll_asset.media.file_path
        else:
            image_path = coll_asset.media.hex
        collectibles_frame = ClickableFrame(
            coll_asset.asset_id,
            coll_asset.name,
            image_path=image_path,
            asset_type=AssetType.CFA,
        )
        collectibles_frame.setObjectName('collectibles_frame')
        collectibles_frame.setCursor(
            QCursor(Qt.CursorShape.PointingHandCursor),
        )
        collectibles_frame.setStyleSheet(
            'background: transparent;\n'
            'border: none;\n'
            'border-top-left-radius: 8px;\n'
            'border-top-right-radius: 8px;\n',
        )
        collectibles_frame.setFrameShape(QFrame.StyledPanel)
        collectibles_frame.setFrameShadow(QFrame.Raised)

        form_layout = QFormLayout(collectibles_frame)
        form_layout.setObjectName('formLayout')
        form_layout.setHorizontalSpacing(0)
        form_layout.setVerticalSpacing(0)
        form_layout.setContentsMargins(0, 0, 0, 0)

        collectible_asset_name = QLabel(collectibles_frame)
        collectible_asset_name.setObjectName('collectible_asset_name')
        collectible_asset_name.setMinimumSize(242, 42)
        collectible_asset_name.setMaximumSize(242, 42)

        image_label = QLabel()
        image_label.setObjectName('collectible_image')
        image_label.setMinimumSize(242, 242)
        image_label.setMaximumSize(242, 242)
        image_label.setStyleSheet(
            'border-radius: 8px; border: none; background: transparent;',
        )
        image_label.setStyleSheet(
            'QLabel{\n'
            'border-top-left-radius: 8px;\n'
            'border-top-right-radius: 8px;\n'
            'border-bottom-left-radius: 0px;\n'
            'border-bottom-right-radius: 0px;\n'
            'background: transparent;\n'
            'background-color: rgb(27, 35, 59);\n'
            '}\n',
        )

        if coll_asset.media.hex is None:
            resized_image = resize_image(coll_asset.media.file_path, 242, 242)
            image_label.setPixmap(resized_image)
        else:
            pixmap = convert_hex_to_image(coll_asset.media.hex)
            resized_image = resize_image(pixmap, 242, 242)
            if not pixmap.isNull():
                image_label.setPixmap(resized_image)
            else:
                logger.error(
                    'Failed to load image: %s',
                    coll_asset.media.file_path,
                )

        form_layout.addRow(image_label)

        collectible_asset_name.setStyleSheet(
            'QLabel{\n'
            'font: 15px "Inter";\n'
            'color: #FFFFFF;\n'
            'font-weight:600;\n'
            'border-top-left-radius: 0px;\n'
            'border-top-right-radius: 0px;\n'
            'border-bottom-left-radius: 8px;\n'
            'border-bottom-right-radius: 8px;\n'
            'background: transparent;\n'
            'background-color: rgb(27, 35, 59);\n'
            'padding: 10.5px, 10px, 10.5px, 10px;\n'
            'padding-left: 11px\n'
            '}\n'
            '',
        )
        collectible_asset_name.setText(coll_asset.name)

        form_layout.addRow(collectible_asset_name)

        collectibles_frame.clicked.connect(self.handle_collectible_frame_click)
        self.resizeEvent = self.resize_event_called
        return collectibles_frame

    def setup_ui_connection(self):
        """Set up connections for UI elements."""
        self._view_model.main_asset_view_model.get_assets()
        self.collectible_header_frame.refresh_page_button.clicked.connect(
            self.trigger_render_and_refresh,
        )
        self.collectible_header_frame.action_button.clicked.connect(
            lambda: self._view_model.main_asset_view_model.navigate_issue_asset(
                self._view_model.page_navigation.issue_cfa_asset_page,
            ),
        )
        self._view_model.main_asset_view_model.loading_started.connect(
            self.show_collectible_asset_loading,
        )
        self._view_model.main_asset_view_model.loading_finished.connect(
            self.stop_loading_screen,
        )
        self._view_model.main_asset_view_model.message.connect(
            self.show_message,
        )

    def trigger_render_and_refresh(self):
        """This method start the render timer and perform the collectible asset list refresh"""
        self.render_timer.start()
        self._view_model.main_asset_view_model.get_assets(
            rgb_asset_hard_refresh=True,
        )

    def retranslate_ui(self):
        """Retranslate the UI elements."""
        self.show_collectible_asset_loading()
        self.collectible_header_frame.action_button.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'issue_new_collectibles', None,
            ),
        )
        self.collectibles_label.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'collectibles', None,
            ),
        )

    def handle_collectible_frame_click(self, asset_id, asset_name, image_path, asset_type):
        """This method handles collectibles asset click of the main asset page."""
        if asset_id is None or asset_name is None or image_path is None or asset_type is None:
            return
        self._view_model.cfa_view_model.asset_info.emit(
            asset_id, asset_name, image_path, asset_type,
        )
        self._view_model.page_navigation.cfa_detail_page(
            RgbAssetPageLoadModel(asset_type=asset_type),
        )

    def show_collectible_asset_loading(self):
        """This method handled show loading screen on main asset page"""
        self.loading_screen = LoadingTranslucentScreen(
            parent=self, description_text='Loading', dot_animation=True,
        )
        self.loading_screen.start()
        self.collectible_header_frame.refresh_page_button.setDisabled(True)

    def stop_loading_screen(self):
        """This method handled stop loading screen on main asset page"""
        self.loading_screen.stop()
        self.collectible_header_frame.refresh_page_button.setDisabled(False)
        self.render_timer.stop()

    def show_message(self, collectibles_asset_toast_preset, message):
        """This method handled showing message main asset page"""
        if collectibles_asset_toast_preset == ToastPreset.SUCCESS:
            ToastManager.success(description=message)
        if collectibles_asset_toast_preset == ToastPreset.ERROR:
            ToastManager.error(description=message)
        if collectibles_asset_toast_preset == ToastPreset.INFORMATION:
            ToastManager.info(description=message)
        if collectibles_asset_toast_preset == ToastPreset.WARNING:
            ToastManager.warning(description=message)
