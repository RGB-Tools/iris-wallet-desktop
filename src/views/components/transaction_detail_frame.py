"""This module contains the TransactionDetailFrame class,
which represents the UI for transaction detail.
"""
# pylint: disable=invalid-name
from __future__ import annotations

from PySide6.QtCore import QCoreApplication
from PySide6.QtCore import QSize
from PySide6.QtCore import Qt
from PySide6.QtCore import Signal
from PySide6.QtGui import QCursor
from PySide6.QtWidgets import QFrame
from PySide6.QtWidgets import QGridLayout
from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QWidget

from accessible_constant import TRANSFER_STATUS
from src.model.transaction_detail_page_model import TransactionDetailPageModel
from src.utils.constant import IRIS_WALLET_TRANSLATIONS_CONTEXT


class TransactionDetailFrame(QFrame):
    """This class represents transaction detail frame of the application."""
    click_frame = Signal(TransactionDetailPageModel)

    def __init__(self, parent=None, params: TransactionDetailPageModel | None = None, **kwargs):
        super().__init__(parent, **kwargs)
        self.params: TransactionDetailPageModel | None = params
        self.set_frame()

    def mousePressEvent(self, event):
        """Handles the mouse press event to emit the clicked signal."""
        self.click_frame.emit(self.params)
        super().mousePressEvent(event)

    def set_frame(self):
        """This method represents set the transaction details frame"""
        self.setObjectName('transaction_detail_frame')
        self.setMinimumSize(QSize(335, 70))
        self.setMaximumSize(QSize(335, 70))
        self.setStyleSheet(
            'QFrame{\n'
            'background: transparent;\n'
            'background-color:#1B233B;\n'
            'border-radius: 8px;\n'
            '}'
            'QFrame:hover{\n'
            'border-radius: 8px;\n'
            'border: 1px solid rgb(102, 108, 129);\n'
            '}',
        )
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        self.setLineWidth(-1)
        self.frame_grid_layout = QGridLayout(self)
        self.frame_grid_layout.setObjectName('frame_grid_layout')
        self.frame_grid_layout.setContentsMargins(15, -1, 15, 9)
        self.transaction_date = QLabel(self)
        self.transaction_date.setObjectName('label_13')
        self.transaction_date.setMinimumSize(QSize(83, 20))
        self.transaction_date.setStyleSheet(
            'font: 14px "Inter";\n'
            'color: #D0D3DD;\n'
            'background: transparent;\n'
            'border: none;\n'
            'font-weight: 600;\n'
            '',
        )

        self.frame_grid_layout.addWidget(
            self.transaction_date,
            0,
            0,
            1,
            1,
            Qt.AlignLeft,
        )

        self.close_button = QPushButton(self)
        self.close_button.setObjectName('close_btn')
        self.close_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.close_button.setMinimumSize(QSize(24, 24))
        self.close_button.setMaximumSize(QSize(24, 24))

        self.frame_grid_layout.addWidget(
            self.close_button,
            0,
            1,
            1,
            1,
            Qt.AlignRight,
        )

        self.transaction_amount = QLabel(self)
        self.transaction_amount.setFixedHeight(18)
        self.transaction_amount.setObjectName('label_15')
        self.transaction_amount.setStyleSheet(
            'font: 15px "Inter";\n'
            'color: #EB5A5A;\n'
            'background: transparent;\n'
            'border: none;\n'
            'font-weight: 600;\n'
            '',
        )

        self.transaction_time = QLabel(self)
        self.transaction_time.setObjectName('label_14')
        self.transaction_time.setAccessibleDescription(TRANSFER_STATUS)
        self.transaction_time.setMinimumSize(QSize(60, 18))
        self.transaction_time.setStyleSheet(
            'font: 15px "Inter";\n'
            'color: #959BAE;\n'
            'background: transparent;\n'
            'border: none;\n'
            'font-weight: 400;\n'
            '',
        )

        self.frame_grid_layout.addWidget(
            self.transaction_time,
            1,
            0,
            1,
            1,
            Qt.AlignLeft,
        )

        self.transfer_type = QPushButton(self)
        self.transfer_type.setObjectName('transaction_button')
        self.transfer_type.setMinimumSize(QSize(24, 24))
        self.transfer_type.setMaximumSize(QSize(24, 24))

        self.transaction_type = QLabel(self)
        self.transaction_type.setObjectName('transaction_type')
        self.transaction_type.setMinimumSize(QSize(60, 18))
        self.transaction_type.setStyleSheet(
            'font: 15px "Inter";\n'
            'color: #959BAE;\n'
            'background: transparent;\n'
            'border: none;\n'
            'font-weight: 400;\n'
            '',
        )
        self.frame_grid_layout.addWidget(
            self.transaction_type,
            0,
            1,
            1,
            1,
            Qt.AlignRight,
        )

        self.transaction_detail_frame_horizontal_layout = QHBoxLayout()
        self.transaction_detail_frame_horizontal_layout.setSpacing(6)
        self.transaction_detail_frame_horizontal_layout.addWidget(
            self.transaction_amount,
        )
        self.transaction_detail_frame_horizontal_layout.addWidget(
            self.transfer_type,
        )

        self.frame_grid_layout.addLayout(
            self.transaction_detail_frame_horizontal_layout,
            1,
            1,
            1,
            1,
            Qt.AlignRight,
        )

        return (
            self.transaction_date,
            self.transaction_time,
            self.transaction_amount,
            self.transfer_type,
        )

    def no_transaction_frame(self):
        """This method creates a frame if there are no transactions"""
        no_transaction_widget = QWidget(self)
        no_transaction_layout = QVBoxLayout(no_transaction_widget)
        self.setStyleSheet('background:transparent')
        self.transfer_type.hide()
        no_transaction_label = QLabel(no_transaction_widget)
        no_transaction_label.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'no_transfer_history', None,
            ),
        )
        no_transaction_label.setAlignment(Qt.AlignCenter)
        no_transaction_label.setStyleSheet(
            'font: 16px "Inter";\n'
            'color: #959BAE;\n'  # Suitable color for text
            'background: transparent;\n'
            'border: none;\n'
            'font-weight: 500;\n',
        )

        no_transaction_layout.addStretch()
        no_transaction_layout.addWidget(no_transaction_label)
        no_transaction_layout.addStretch()

        return no_transaction_widget
