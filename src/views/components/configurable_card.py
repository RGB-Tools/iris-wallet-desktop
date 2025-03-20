# pylint: disable=too-many-instance-attributes, too-many-statements, unused-import
"""
This module defines the `ConfigurableCardFrame` class, which represents a customizable card interface
for displaying and editing configuration settings.
"""
from __future__ import annotations

from PySide6.QtCore import QCoreApplication
from PySide6.QtCore import QSize
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QComboBox
from PySide6.QtWidgets import QFrame
from PySide6.QtWidgets import QGridLayout
from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QLineEdit
from PySide6.QtWidgets import QVBoxLayout

from accessible_constant import EXPIRY_TIME_COMBO_BOX
from accessible_constant import INPUT_BOX_NAME
from src.model.common_operation_model import ConfigurableCardModel
from src.utils.clickable_frame import ClickableFrame
from src.utils.constant import IRIS_WALLET_TRANSLATIONS_CONTEXT
from src.utils.helpers import load_stylesheet
from src.views.components.buttons import PrimaryButton


class ConfigurableCardFrame(ClickableFrame):
    """
    A custom confirmation dialog with a message and two buttons: Continue and Cancel.

    This dialog is designed to display a message to the user and allow them to confirm
    or cancel an action. It uses a frameless window design with a blur effect and is modal.
    """
    _expanded_frame = None  # Tracks the currently expanded frame

    def __init__(self, parent, params: ConfigurableCardModel):
        super().__init__(parent)
        self.suggestion_desc = None
        self.inner_horizontal_layout = None
        self.input_value = None
        self.time_unit_combobox = None
        self.params: ConfigurableCardModel | None = params
        self.is_expanded = False
        self.setObjectName('card_frame')
        self.setMinimumSize(QSize(492, 79))
        self.setMaximumSize(QSize(492, 91))
        self.setStyleSheet(
            load_stylesheet(
                'views/qss/configurable_card.qss',
            ),
        )

        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        self.configurable_card_grid_layout = QGridLayout(self)
        self.configurable_card_grid_layout.setObjectName('grid_layout_8')
        self.configurable_card_grid_layout.setVerticalSpacing(9)
        self.configurable_card_grid_layout.setContentsMargins(10, 15, 9, 19)
        self.configurable_card_vertical_layout = QVBoxLayout()
        self.configurable_card_vertical_layout.setObjectName(
            'configurable_card_vertical_layout',
        )
        self.title_label = QLabel(self)
        self.title_label.setObjectName('title_label')
        self.title_label.setStyleSheet('border:none')
        self.title_label.setAlignment(Qt.AlignCenter)

        self.configurable_card_vertical_layout.addWidget(
            self.title_label, 0, Qt.AlignLeft,
        )

        self.title_desc = QLabel(self)
        self.title_desc.setObjectName('title_desc')
        self.title_desc.setMinimumSize(QSize(450, 45))
        self.title_desc.setWordWrap(True)

        self.configurable_card_vertical_layout.addWidget(self.title_desc)

        self.configurable_card_grid_layout.addLayout(
            self.configurable_card_vertical_layout, 0, 0, 1, 1,
        )

        self.title_label.setText(self.params.title_label)
        self.title_desc.setText(
            self.params.title_desc,
        )
        self.save_button = PrimaryButton()

        self.clicked.connect(self.toggle_expand)

    def toggle_expand(self):
        """Expand this frame and collapse any other expanded frames."""
        if self.is_expanded:
            self.collapse_frame()
        else:
            # Collapse the currently expanded frame if it's not this one
            if ConfigurableCardFrame._expanded_frame and ConfigurableCardFrame._expanded_frame != self:
                ConfigurableCardFrame._expanded_frame.collapse_frame()

            # Expand this frame and set it as the currently expanded frame
            ConfigurableCardFrame._expanded_frame = self
            self.expand_frame()

    def expand_frame(self):
        """Expands the frame and updates its state."""
        self.setMaximumSize(QSize(492, 220))
        self.is_expanded = True
        self.show_change_content()

    def collapse_frame(self):
        """Collapses the frame and updates its state."""
        self.setMaximumSize(QSize(492, 91))
        self.is_expanded = False
        self.suggestion_desc.hide()
        self.input_value.hide()
        self.time_unit_combobox.hide()
        self.save_button.hide()
        self.title_desc.setMinimumSize(QSize(492, 45))

    def show_change_content(self):
        """Show input box of default value"""
        self.suggestion_desc = QLabel(self)
        self.suggestion_desc.setStyleSheet('border:none')
        self.suggestion_desc.setObjectName('value_label')

        self.configurable_card_grid_layout.addWidget(
            self.suggestion_desc, 1, 0, 1, 1,
        )

        self.configurable_card_vertical_layout = QVBoxLayout()
        self.configurable_card_vertical_layout.setObjectName(
            'configurable_card_vertical_layout',
        )

        self.configurable_card_vertical_layout.addWidget(
            self.title_label, 0, Qt.AlignLeft,
        )

        self.title_desc.setMinimumSize(QSize(492, 26))

        self.configurable_card_vertical_layout.addWidget(self.title_desc)

        self.configurable_card_grid_layout.addLayout(
            self.configurable_card_vertical_layout, 0, 0, 1, 1,
        )
        self.inner_horizontal_layout = QHBoxLayout()
        self.inner_horizontal_layout.setContentsMargins(
            0, 0, 40, 0,
        )
        self.inner_horizontal_layout.setSpacing(20)
        self.input_value = QLineEdit(self)
        self.input_value.setFrame(False)
        self.input_value.setObjectName('input_value')
        self.input_value.setAccessibleName(INPUT_BOX_NAME)
        self.input_value.setMinimumSize(QSize(300, 35))
        self.input_value.setMaximumSize(QSize(492, 16777215))
        self.time_unit_combobox = QComboBox()
        self.time_unit_combobox.setMinimumSize(QSize(90, 35))
        self.time_unit_combobox.setAccessibleDescription(EXPIRY_TIME_COMBO_BOX)

        self.inner_horizontal_layout.addWidget(
            self.input_value, alignment=Qt.AlignLeft,
        )
        self.inner_horizontal_layout.addWidget(
            self.time_unit_combobox,
        )
        self.configurable_card_grid_layout.addLayout(
            self.inner_horizontal_layout, 2, 0, 1, 1,
        )

        self.save_button.setObjectName('save_button')
        self.save_button.setMinimumSize(QSize(100, 30))
        self.save_button.setMaximumSize(QSize(100, 40))
        self.save_button.show()
        self.configurable_card_grid_layout.addWidget(
            self.save_button, 3, 0, 1, 1,
        )

        self.save_button.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'save', None,
            ),
        )
        self.suggestion_desc.setText(
            self.params.suggestion_desc,
        )
        self.add_translated_item('minutes')
        self.add_translated_item('hours')
        self.add_translated_item('days')
        self.input_value.textChanged.connect(
            self.check_input_and_toggle_save_button,
        )

    def add_translated_item(self, text: str):
        """Adds a translated item to the time unit combo box."""
        if self.time_unit_combobox:
            translated_text = QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, text, None,
            )
            self.time_unit_combobox.addItem(translated_text)

    def check_input_and_toggle_save_button(self):
        """Check if input_value is empty and enable/disable save button."""
        if not self.input_value.text().strip():
            self.save_button.setDisabled(True)
        else:
            self.save_button.setDisabled(False)
