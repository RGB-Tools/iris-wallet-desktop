"""
Help page objects class for interacting with the application.
"""
from __future__ import annotations

from accessible_constant import HELP_CARD_TITLE_ACCESSIBLE_DESCRIPTION
from e2e_tests.test.utilities.base_operation import BaseOperations


class HelpPageObjects(BaseOperations):
    """Help page objects class."""

    def __init__(self, application):
        """
        Initializes the HelpPageObjects class with the application.

        Args:
            application: The application instance.
        """
        super().__init__(application)
        self.learn_about_rgb_frame_title = lambda: self.perform_action_on_element(
            role_name='label', description=HELP_CARD_TITLE_ACCESSIBLE_DESCRIPTION+'_1',
        )
        self.bitcoin_txn_frame_label = lambda: self.perform_action_on_element(
            role_name='label', description=HELP_CARD_TITLE_ACCESSIBLE_DESCRIPTION+'_2',
        )
        self.minimum_balance_frame_title = lambda: self.perform_action_on_element(
            role_name='label', description=HELP_CARD_TITLE_ACCESSIBLE_DESCRIPTION+'_3',
        )
        self.support_and_feedback = lambda: self.perform_action_on_element(
            role_name='label', description=HELP_CARD_TITLE_ACCESSIBLE_DESCRIPTION+'_4',
        )
        self.regtest_bitcoin_frame_title = lambda: self.perform_action_on_element(
            role_name='label', description=HELP_CARD_TITLE_ACCESSIBLE_DESCRIPTION+'_5',
        )

    def click_learn_about_rgb(self):
        """Clicks on learn about rgb frame"""
        return self.do_click(self.learn_about_rgb_frame_title()) if self.do_is_displayed(self.learn_about_rgb_frame_title()) else None

    def click_bitcoin_txn(self):
        """Clicks on bitcoin transaction frame"""
        return self.do_click(self.bitcoin_txn_frame_label()) if self.do_is_displayed(self.bitcoin_txn_frame_label()) else None

    def click_regtest_bitcoin(self):
        """Clicks on regtest bitcoin frame"""
        return self.do_click(self.regtest_bitcoin_frame_title()) if self.do_is_displayed(self.regtest_bitcoin_frame_title()) else None

    def click_minimum_balance(self):
        """Clicks on minimum balance frame"""
        return self.do_click(self.minimum_balance_frame_title()) if self.do_is_displayed(self.minimum_balance_frame_title()) else None

    def click_support_and_feedback(self):
        """Clicks on regtest bitcoin frame"""
        return self.do_click(self.support_and_feedback()) if self.do_is_displayed(self.support_and_feedback()) else None

    def get_learn_about_rgb_frame_title(self):
        """Returns the title of learn about rgb frame"""
        return self.do_get_text(self.learn_about_rgb_frame_title()) if self.do_is_displayed(self.learn_about_rgb_frame_title()) else None

    def get_bitcoin_txn_frame_label(self):
        """Returns the label of bitcoin transaction frame"""
        return self.do_get_text(self.bitcoin_txn_frame_label()) if self.do_is_displayed(self.bitcoin_txn_frame_label()) else None

    def get_regtest_bitcoin_frame_title(self):
        """Returns the title of regtest bitcoin frame"""
        return self.do_get_text(self.regtest_bitcoin_frame_title()) if self.do_is_displayed(self.regtest_bitcoin_frame_title()) else None

    def get_minimum_balance_frame_title(self):
        """Returns the title of minimum balance for issue and receive rgb asset frame"""
        return self.do_get_text(self.minimum_balance_frame_title()) if self.do_is_displayed(self.minimum_balance_frame_title()) else None

    def get_support_and_feedback_title(self):
        """Returns the title of support and feedback frame"""
        return self.do_get_text(self.support_and_feedback()) if self.do_is_displayed(self.support_and_feedback()) else None
