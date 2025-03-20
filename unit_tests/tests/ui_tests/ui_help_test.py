"""Unit test for Enter Help UI."""
# Disable the redefined-outer-name warning as
# it's normal to pass mocked objects in test functions
# pylint: disable=redefined-outer-name,unused-argument,protected-access
from __future__ import annotations

from unittest.mock import MagicMock

import pytest
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QVBoxLayout

from src.viewmodels.main_view_model import MainViewModel
from src.views.ui_help import HelpWidget


@pytest.fixture
def help_page_navigation():
    """Fixture to create a mocked page navigation object."""
    mock_navigation = MagicMock()
    return mock_navigation


@pytest.fixture
def mock_help_view_model(help_page_navigation):
    """Fixture to create a MainViewModel instance with mocked page navigation."""
    return MainViewModel(help_page_navigation)


@pytest.fixture
def help_widget(mock_help_view_model):
    """Fixture to create a HelpWidget instance."""
    return HelpWidget(mock_help_view_model)


def test_retranslate_ui(help_widget: HelpWidget):
    """Test that the UI strings are correctly translated."""
    help_widget.retranslate_ui()

    assert help_widget.help_title_frame.title_name.text() == 'help'
    assert help_widget.help_title_label.text() == 'help'


def test_create_help_card(help_widget):
    """Test that a help card is created correctly with the given title, detail, and links."""
    title = 'Test Title'
    detail = 'Test Detail'
    links = ['http://example.com', 'http://example.org']
    count = 1
    help_card_frame = help_widget.create_help_card(title, detail, links, count)

    assert isinstance(help_card_frame, QFrame)
    assert help_card_frame.objectName() == 'help_card_frame'
    assert help_card_frame.minimumSize().width() == 492
    assert help_card_frame.minimumSize().height() == 70
    assert help_card_frame.maximumSize().width() == 335
    assert help_card_frame.maximumSize().height() == 16777215
    assert help_card_frame.frameShape() == QFrame.StyledPanel
    assert help_card_frame.frameShadow() == QFrame.Raised

    # Check that the title and detail are set correctly
    title_label = help_card_frame.findChild(QLabel, 'help_card_title_label')
    assert title_label.text() == title
    assert title_label.wordWrap() is True

    detail_label = help_card_frame.findChild(QLabel, 'help_card_detail_label')
    assert detail_label.text() == detail
    assert detail_label.wordWrap() is True

    # Check that the links are set correctly
    for link in links:
        link_label = help_card_frame.findChild(QLabel, link)
        assert link_label.text() == f"<a style='color: #03CA9B;' href='{
            link
        }'>{link}</a>"
        assert link_label.minimumSize().height() == 15
        assert link_label.cursor().shape() == Qt.CursorShape.PointingHandCursor
        assert link_label.textInteractionFlags() == Qt.TextBrowserInteraction
        assert link_label.openExternalLinks() is True

    # Test with no links
    help_card_frame = help_widget.create_help_card(title, detail, None, count)
    assert help_card_frame.findChild(QLabel, 'http://example.com') is None

    # Test vertical layout properties
    vertical_layout = help_card_frame.findChild(
        QVBoxLayout, 'verticalLayout_3',
    )
    assert vertical_layout.spacing() == 15
    margins = vertical_layout.contentsMargins()
    assert (
        margins.left(), margins.top(), margins.right(),
        margins.bottom(),
    ) == (15, 20, 15, 20)


def test_create_help_frames(help_widget, qtbot):
    """Test that help frames are created and distributed correctly into two columns."""
    # Call the method
    help_widget.create_help_frames()

    # Get the card list from the model
    card_list = help_widget._model.card_content

    # Verify horizontal layout exists and has correct spacer
    assert help_widget.main_horizontal_spacer is not None
    assert help_widget.main_horizontal_spacer.sizeHint().width() == 40
    assert help_widget.main_horizontal_spacer.sizeHint().height() == 20

    # Verify vertical spacer exists and has correct properties
    assert help_widget.main_vertical_spacer is not None
    assert help_widget.main_vertical_spacer.sizeHint().width() == 20
    assert help_widget.main_vertical_spacer.sizeHint().height() == 40

    # Find all help card frames
    help_cards = help_widget.findChildren(QFrame, 'help_card_frame')

    # Clear any existing cards before checking
    for card in help_cards[len(card_list):]:
        card.deleteLater()
    help_cards = help_cards[:len(card_list)]

    # Verify number of cards matches model content
    assert len(help_cards) == len(card_list)

    # Verify each card's content
    for i, card in enumerate(card_list):
        help_card = help_cards[i]

        title_label = help_card.findChild(QLabel, 'help_card_title_label')
        detail_label = help_card.findChild(QLabel, 'help_card_detail_label')

        assert title_label.text() == card.title
        assert detail_label.text() == card.detail

        if card.links:
            for link in card.links:
                link_label = help_card.findChild(QLabel, str(link))
                assert link_label is not None
                assert link_label.text() == f"<a style='color: #03CA9B;' href='{
                    link
                }'>{link}</a>"
