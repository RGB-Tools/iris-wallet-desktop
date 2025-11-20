# pylint: disable=too-many-instance-attributes, too-many-statements, unused-import,implicit-str-concat
"""
Custom dialog box for close channel
"""
from __future__ import annotations

from PySide6.QtCore import QCoreApplication
from PySide6.QtCore import QSize
from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor
from PySide6.QtWidgets import QDialog
from PySide6.QtWidgets import QFrame
from PySide6.QtWidgets import QGridLayout
from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtWidgets import QSpacerItem
from PySide6.QtWidgets import QVBoxLayout

from accessible_constant import CLOSE_CHANNEL_CONTINUE_BUTTON
from accessible_constant import CLOSE_CHANNEL_DIALOG
from src.utils.constant import IRIS_WALLET_TRANSLATIONS_CONTEXT
from src.utils.helpers import load_stylesheet
from src.viewmodels.main_view_model import MainViewModel


class CloseChannelDialog(QDialog):
    """Custom dialog box for close channel"""

    def __init__(self, page_navigate, pub_key, channel_id, parent=None):
        super().__init__(parent)
        self.setObjectName('custom_dialog')
        self.setAccessibleName(CLOSE_CHANNEL_DIALOG)
        self._page_navigate = page_navigate
        self._view_model = MainViewModel(page_navigate)
        self.pub_key = pub_key
        self.channel_id = channel_id
        # Hide the title bar and close button
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.resize(300, 160)
        self.setStyleSheet(
            load_stylesheet(
                'views/qss/close_channel_dialog_style.qss',
            ),
        )
        self.grid_layout_close_channel = QGridLayout(self)
        self.grid_layout_close_channel.setObjectName('gridLayout')
        self.grid_layout_close_channel.setContentsMargins(0, 0, 0, 0)
        self.close_channel_frame = QFrame(self)
        self.close_channel_frame.setObjectName('mnemonic_frame')
        self.close_channel_frame.setMinimumSize(QSize(400, 155))
        self.close_channel_frame.setMaximumSize(QSize(16777215, 155))

        self.close_channel_frame.setFrameShape(QFrame.StyledPanel)
        self.close_channel_frame.setFrameShadow(QFrame.Raised)
        self.vertical_layout_close_channel_frame = QVBoxLayout(
            self.close_channel_frame,
        )
        self.vertical_layout_close_channel_frame.setSpacing(40)
        self.vertical_layout_close_channel_frame.setObjectName(
            'vertical_layout_frame',
        )
        self.vertical_layout_close_channel_frame.setContentsMargins(
            21, -1, 25, -1,
        )
        self.close_channel_detail_text_label = QLabel(self.close_channel_frame)
        self.close_channel_detail_text_label.setObjectName(
            'mnemonic_detail_text_label',
        )
        self.close_channel_detail_text_label.setMinimumSize(QSize(370, 84))
        self.close_channel_detail_text_label.setMaximumSize(QSize(370, 84))

        self.close_channel_detail_text_label.setWordWrap(True)

        self.vertical_layout_close_channel_frame.addWidget(
            self.close_channel_detail_text_label,
        )

        self.close_channel_horizontal_button_layout = QHBoxLayout()
        self.close_channel_horizontal_button_layout.setSpacing(20)
        self.close_channel_horizontal_button_layout.setContentsMargins(
            1, 1, 1, 1,
        )
        self.close_channel_horizontal_button_layout.setObjectName(
            'horizontal_button_layout',
        )
        self.close_channel_cancel_button = QPushButton(
            self.close_channel_frame,
        )
        self.close_channel_cancel_button.setObjectName(
            'close_channel_cancel_button',
        )
        self.close_channel_cancel_button.setCursor(
            QCursor(Qt.CursorShape.PointingHandCursor),
        )
        self.close_channel_cancel_button.setMinimumSize(QSize(80, 35))
        self.close_channel_cancel_button.setMaximumSize(QSize(80, 35))

        self.close_channel_horizontal_button_layout.addWidget(
            self.close_channel_cancel_button,
        )

        self.close_channel_continue_button = QPushButton(
            self.close_channel_frame,
        )
        self.close_channel_continue_button.setObjectName(
            'close_channel_continue_button',
        )
        self.close_channel_continue_button.setAccessibleName(
            CLOSE_CHANNEL_CONTINUE_BUTTON,
        )
        self.close_channel_continue_button.setCursor(
            QCursor(Qt.CursorShape.PointingHandCursor),
        )
        self.close_channel_continue_button.setMinimumSize(QSize(80, 35))
        self.close_channel_continue_button.setMaximumSize(QSize(80, 35))

        self.close_channel_horizontal_button_layout.addWidget(
            self.close_channel_continue_button,
        )

        self.vertical_layout_close_channel_frame.addLayout(
            self.close_channel_horizontal_button_layout,
        )

        self.vertical_spacer_close_channel = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding,
        )

        self.vertical_layout_close_channel_frame.addItem(
            self.vertical_spacer_close_channel,
        )

        self.grid_layout_close_channel.addWidget(
            self.close_channel_frame, 0, 0, 1, 1,
        )
        self.setup_ui_connection()
        self.retranslate_ui()

    # setupUi
    def setup_ui_connection(self):
        """Set up connections for UI elements."""
        self.close_channel_continue_button.clicked.connect(self.close_channel)
        self.close_channel_cancel_button.clicked.connect(self.cancel)
        self._view_model.channel_view_model.loading_started.connect(
            self.disable_button_state,
        )
        self._view_model.channel_view_model.loading_finished.connect(
            self.enable_button_state,
        )

    def retranslate_ui(self):
        """Retranslate ui"""
        self.close_channel_text = f'{
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, "close_channel_prompt", None
            )
        } {self.pub_key}?'

        self.close_channel_detail_text_label.setText(self.close_channel_text)
        self.close_channel_cancel_button.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'cancel', None,
            ),
        )
        self.close_channel_continue_button.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'continue', None,
            ),
        )

    def close_channel(self):
        """Re-direct the channel management page after closing channel"""
        self._view_model.channel_view_model.close_channel(
            channel_id=self.channel_id, pub_key=self.pub_key,
        )
        self.close()

    def cancel(self):
        """Close when user click on cancel"""
        self.close()

    def disable_button_state(self):
        """Disable button state when channel closing operation starts"""
        self.close_channel_continue_button.setDisabled(True)

    def enable_button_state(self):
        """Enable button state when channel closing operation ends"""
        self.close_channel_continue_button.setDisabled(False)
