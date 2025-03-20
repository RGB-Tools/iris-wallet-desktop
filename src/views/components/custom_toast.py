# pylint: disable=too-many-instance-attributes, too-many-statements ,unused-import
"""This module has the UI and the logic for the custom toast notification"""
from __future__ import annotations

from PySide6.QtCore import QElapsedTimer
from PySide6.QtCore import QPoint
from PySide6.QtCore import QSize
from PySide6.QtCore import Qt
from PySide6.QtCore import QTimer
from PySide6.QtGui import QColor
from PySide6.QtGui import QCursor
from PySide6.QtGui import QGuiApplication
from PySide6.QtGui import QIcon
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QFrame
from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QProgressBar
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QWidget

from accessible_constant import TOASTER_CLOSE_BUTTON
from accessible_constant import TOASTER_DESCRIPTION
from accessible_constant import TOASTER_FRAME
from accessible_constant import TOASTER_TITLE
from src import resources_rc
from src.model.enums.enums_model import ToastPreset

SUCCESS_ACCENT_COLOR = QColor('#3E9141')
WARNING_ACCENT_COLOR = QColor('#FFC107')
ERROR_ACCENT_COLOR = QColor('#FF5722')
INFORMATION_ACCENT_COLOR = QColor('#2196F3')


class ToasterManager:
    """Manages the positioning and lifecycle of toasters."""
    active_toasters: list[ToasterUi] = []
    main_window = None  # Keep reference to the main window

    @classmethod
    def set_main_window(cls, main_window):
        """Set the main window for the toasters."""
        cls.main_window = main_window

    @classmethod
    def add_toaster(cls, toaster):
        """Add a new toaster to the manager and reposition all."""
        if cls.main_window:
            cls.active_toasters.append(toaster)
            cls.reposition_toasters()

    @classmethod
    def remove_toaster(cls, toaster):
        """Remove a toaster and reposition remaining ones."""
        if toaster in cls.active_toasters:
            cls.active_toasters.remove(toaster)
            cls.reposition_toasters()

    @classmethod
    def reposition_toasters(cls):
        """Reposition all toasters based on their order."""
        for index, toaster in enumerate(cls.active_toasters):
            parent = toaster.parent()
            if parent:
                # Use geometry() to get the position and size of the parent widget
                x = ToasterManager.main_window.size().width() - toaster.width() - 20
                y = ToasterManager.main_window.size().height() - (index + 1) * \
                    (toaster.height() + int(toaster.height() * 0.1)) - 15

                toaster.move(QPoint(x, y))


class ToasterUi(QWidget):
    """this class includes the ui for custom toaster"""

    def __init__(self, parent=None, description=None, duration=6000):
        super().__init__(ToasterManager.main_window)
        self.setObjectName('toaster')
        screen_width = QGuiApplication.primaryScreen().size().width()
        self.position = 'bottom-right'
        self.margin = 50
        self.duration = duration
        self.description_text = description
        self.setCursor(
            QCursor(Qt.CursorShape.PointingHandCursor),
        )

        # Initialize toasters with parent as the main window if not specified
        if ToasterManager.main_window is None and parent is None:
            raise ValueError('Main window not set for ToasterManager.')

        self.frame = QFrame(self)
        self.frame.setObjectName('toaster_frame')
        self.frame.setAccessibleName(TOASTER_FRAME)
        self.frame.setStyleSheet(
            'background-color: rgb(3,11,37);',
        )

        # Layout for frame
        self.vertical_layout_2 = QVBoxLayout(self.frame)
        self.vertical_layout_2.setSpacing(20)
        self.vertical_layout_2.setContentsMargins(0, 0, 0, 0)

        # Top content layout
        self.horizontal_layout_2 = QHBoxLayout()
        self.horizontal_layout_2.setContentsMargins(14, 14, 10, 0)

        # Icon and line separator
        self.horizontal_layout = QHBoxLayout()
        self.horizontal_layout.setSpacing(20)
        self.horizontal_layout.setContentsMargins(6, 6, 0, -1)

        self.icon = QLabel(self.frame)
        self.icon.setMinimumSize(QSize(18, 18))
        self.icon.setMaximumSize(QSize(18, 18))
        self.icon.setPixmap(QPixmap(':/assets/tick_circle.png'))
        self.icon.setScaledContents(True)
        self.horizontal_layout.addWidget(self.icon)

        self.line = QFrame(self.frame)
        self.line.setObjectName('line')
        self.line.setStyleSheet(
            '#line{background-color:#ffffff;border:1px #ffffff;}',
        )
        self.line.setFrameShape(QFrame.Shape.VLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)
        self.horizontal_layout.addWidget(self.line)

        self.horizontal_layout_2.addLayout(self.horizontal_layout)

        # Title and description layout
        self.vertical_layout = QVBoxLayout()
        self.vertical_layout.setSpacing(6)
        self.vertical_layout.setContentsMargins(0, 6, 0, 0)

        self.title = QLabel(self.frame)
        self.title.setObjectName('title')
        self.title.setAccessibleDescription(TOASTER_TITLE)
        self.title.setStyleSheet(
            """
            #title{
            color:#FFFFFF;font-weight:600;
            }
        """,
        )
        self.vertical_layout.addWidget(self.title, 0, Qt.AlignTop)

        self.description = QLabel(self.frame)
        self.description.setObjectName('description')
        self.description.setAccessibleDescription(TOASTER_DESCRIPTION)
        self.description.setStyleSheet(
            """
            #description{
            color:#D0D0D0;font-weight:500;
        }
        """,
        )
        self.description.setMaximumWidth(screen_width * 0.5)
        self.description.setWordWrap(True)
        self.description.adjustSize()
        self.vertical_layout.addWidget(self.description, 0, Qt.AlignBottom)

        self.horizontal_layout_2.addLayout(self.vertical_layout)

        # Close button
        self.close_button = QPushButton(self.frame)
        self.close_button.setAccessibleName(TOASTER_CLOSE_BUTTON)
        self.close_button.setMinimumSize(QSize(14, 14))
        self.close_button.setMaximumSize(QSize(14, 14))
        self.close_button.setStyleSheet('border: none;')
        icon1 = QIcon()
        icon1.addFile(':/assets/close_white.png')
        self.close_button.setIcon(icon1)
        self.close_button.setIconSize(QSize(12, 12))
        self.close_button.setFlat(True)
        self.horizontal_layout_2.addWidget(self.close_button, 0, Qt.AlignTop)

        self.vertical_layout_2.addLayout(self.horizontal_layout_2)

        # Smooth progress bar
        self.progress_bar = QProgressBar(self.frame)
        self.progress_bar.setObjectName('progressBar')
        self.progress_bar.setMaximumSize(QSize(16777215, 5))
        self.progress_bar.setValue(100)
        self.progress_bar.setStyleSheet(
            'QProgressBar {'
            '    border: none;'
            '    background-color: #444;'
            '    height: 4px;'
            '}'
            'QProgressBar::chunk {'
            '    background-color: #3E9141;'
            '    width: 1px;'
            '}',
        )
        self.vertical_layout_2.addWidget(self.progress_bar)

        # Timer for the progress bar
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(1)

        self.elapsed_timer = QElapsedTimer()
        self.elapsed_timer.start()

        self.retranslate_ui()
        self.setup_ui_connections()
        if parent:
            parent.resizeEvent = self._wrap_resize_event(parent.resizeEvent)
        self.adjust_toaster_size()

    def setup_ui_connections(self):
        """this method setups the ui connection for the toaster"""
        self.close_button.clicked.connect(self.close_toaster)
        ToasterManager.reposition_toasters()

    def retranslate_ui(self):
        """retranslate for toaster"""
        if self.description is not None:
            self.description.setText(self.description_text)
        self.progress_bar.setFormat('')

    def close_toaster(self):
        """this method closes the toaster when close button is clicked"""
        self.timer.stop()
        self.close()
        ToasterManager.remove_toaster(self)

    def show_toast(self):
        """displays the toaster"""
        self.show()
        ToasterManager.add_toaster(self)

    def update_progress(self):
        """this method updates the progress bar"""
        elapsed_time = self.elapsed_timer.elapsed()
        progress = max(0, 100 - (elapsed_time / self.duration) * 100)
        self.progress_bar.setValue(progress)

        if elapsed_time >= self.duration:
            self.close_toaster()

    def _wrap_resize_event(self, original_resize_event):
        """this is a wrapped resize event which moves the toaster along with parent"""
        def wrapped_resize_event(event):
            original_resize_event(event)
        return wrapped_resize_event

    def closeEvent(self, event):  # pylint:disable=invalid-name
        """this method handles the close event for toaster"""
        if self.timer.isActive():
            self.timer.stop()
        super().closeEvent(event)

    def enterEvent(self, event):  # pylint:disable=invalid-name
        """Stop the timer when the user hovers over the widget."""
        self.timer.stop()
        self.progress_bar.setValue(100)
        super().enterEvent(event)

    def leaveEvent(self, event):  # pylint:disable=invalid-name
        """Restart the timer when the user stops hovering."""
        self.elapsed_timer.restart()  # Restart the timer when leaving
        self.timer.start(1)  # Restart the progress update
        super().leaveEvent(event)

    def adjust_toaster_size(self):
        """Adjust the size of the toaster dynamically based on its content."""
        self.frame.adjustSize()
        self.adjustSize()

    def apply_preset(self, preset: ToastPreset):
        """
        Apply a preset to the toaster based on the given argument.

        Args:
            preset (str): One of 'INFORMATION', 'WARNING', 'ERROR', or 'SUCCESS'.
        """
        accent_color = None
        if preset == ToastPreset.SUCCESS:
            self.title.setText('Success')
            self.icon.setPixmap(QPixmap(':/assets/success_green.png'))
            accent_color = SUCCESS_ACCENT_COLOR
        elif preset == ToastPreset.WARNING:
            self.title.setText('Warning')
            self.icon.setPixmap(QPixmap(':/assets/warning_yellow.png'))
            accent_color = WARNING_ACCENT_COLOR
        elif preset == ToastPreset.ERROR:
            self.title.setText('Error')
            self.icon.setPixmap(QPixmap(':/assets/error_red.png'))
            accent_color = ERROR_ACCENT_COLOR
        elif preset == ToastPreset.INFORMATION:
            self.title.setText('Information')
            self.icon.setPixmap(QPixmap(':/assets/info_blue.png'))
            accent_color = INFORMATION_ACCENT_COLOR
        else:
            raise ValueError(
                "Invalid preset. Choose one of 'INFORMATION', 'WARNING', 'ERROR', or 'SUCCESS'.",
            )

        # Update progress bar color
        if accent_color:
            self.progress_bar.setStyleSheet(f"""
                QProgressBar {{
                    border: none;
                    background-color: #444;
                    height: 4px;
                }}
                QProgressBar::chunk {{
                    background-color: {accent_color.name()};
                    width: 1px;
                }}
            """)
