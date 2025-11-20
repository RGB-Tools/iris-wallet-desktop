# pylint: disable=too-many-instance-attributes
"""
This file contains the AssetDetailPageObjects class, which provides methods for interacting with the asset detail page.
"""
from __future__ import annotations

from dogtail.tree import root

from accessible_constant import ASSET_CLOSE_BUTTON
from accessible_constant import ASSET_ID_COPY_BUTTON
from accessible_constant import ASSET_LIGHTNING_SPENDABLE_BALANCE
from accessible_constant import ASSET_LIGHTNING_TOTAL_BALANCE
from accessible_constant import ASSET_ON_CHAIN_SPENDABLE_BALANCE
from accessible_constant import ASSET_ON_CHAIN_TOTAL_BALANCE
from accessible_constant import ASSET_RECEIVE_BUTTON
from accessible_constant import ASSET_REFRESH_BUTTON
from accessible_constant import ASSET_SEND_BUTTON
from accessible_constant import CONFIRMAION_DIALOG
from accessible_constant import CONFIRMATION_DIALOG_CONTINUE_BUTTON
from accessible_constant import RGB_TRANSACTION_DETAIL_LIGHTNING_FRAME
from accessible_constant import RGB_TRANSACTION_DETAIL_ON_CHAIN_FRAME
from accessible_constant import TRANSACTION_DETAIL_CLOSE_BUTTON
from accessible_constant import TRANSFER_STATUS
from e2e_tests.test.utilities.base_operation import BaseOperations


class AssetDetailPageObjects(BaseOperations):
    """
    This class provides methods for interacting with the asset detail page.
    """

    def __init__(self, application):
        """
        Initializes the AssetDetailPageObjects class.
        Parameters:
            application (object): The application object.
        """
        super().__init__(application)

        self.close_button = lambda: self.perform_action_on_element(
            role_name='push button', name=ASSET_CLOSE_BUTTON,
        )
        self.send_button = lambda: self.perform_action_on_element(
            role_name='push button', name=ASSET_SEND_BUTTON,
        )
        self.refresh_button = lambda: self.perform_action_on_element(
            role_name='push button', name=ASSET_REFRESH_BUTTON,
        )
        self.on_chain_total_balance = lambda: self.perform_action_on_element(
            role_name='label', description=ASSET_ON_CHAIN_TOTAL_BALANCE,
        )
        self.on_chain_spendable_balance = lambda: self.perform_action_on_element(
            role_name='label', description=ASSET_ON_CHAIN_SPENDABLE_BALANCE,
        )
        self.lightning_total_balance = lambda: self.perform_action_on_element(
            role_name='label', description=ASSET_LIGHTNING_TOTAL_BALANCE,
        )
        self.lightning_spendable_balance = lambda: self.perform_action_on_element(
            role_name='label', description=ASSET_LIGHTNING_SPENDABLE_BALANCE,
        )
        self.rgb_transaction_on_chain_frame = lambda: self.get_first_element(
            role_name='panel', name=RGB_TRANSACTION_DETAIL_ON_CHAIN_FRAME,
        )
        self.rgb_transaction_lightning_frame = lambda: self.get_first_element(
            role_name='panel', name=RGB_TRANSACTION_DETAIL_LIGHTNING_FRAME,
        )
        self.transfer_status = lambda: self.get_first_element(
            role_name='label', description=TRANSFER_STATUS,
        )
        self.receive_button = lambda: self.perform_action_on_element(
            role_name='push button', name=ASSET_RECEIVE_BUTTON,
        )
        self.copy_button = lambda: self.perform_action_on_element(
            role_name='push button', name=ASSET_ID_COPY_BUTTON,
        )
        self.fail_transfer_button = lambda: self.get_first_element(
            role_name='push button', name=TRANSACTION_DETAIL_CLOSE_BUTTON,
        )
        self.confirmation_dialog = lambda: root.child(
            roleName='dialog', name=CONFIRMAION_DIALOG,
        )
        self.confirmation_continue_button = lambda: self.confirmation_dialog().child(
            roleName='push button', name=CONFIRMATION_DIALOG_CONTINUE_BUTTON,
        )

    def click_close_button(self):
        """
        Clicks the close button on the asset detail page.

        Returns:
            bool: True if the button is clicked successfully, None otherwise.
        """
        return self.do_click(self.close_button()) if self.do_is_displayed(self.close_button()) else None

    def click_send_button(self):
        """
        Clicks the send button on the asset detail page.

        Returns:
            bool: True if the button is clicked successfully, None otherwise.
        """
        return self.do_click(self.send_button()) if self.do_is_displayed(self.send_button()) else None

    def click_receive_button(self):
        """
        Clicks the receive button on the asset detail page.

        Returns:
            bool: True if the button is clicked successfully, None otherwise.
        """
        return self.do_click(self.receive_button()) if self.do_is_displayed(self.receive_button()) else None

    def click_refresh_button(self):
        """
        Clicks the refresh button on the asset detail page.

        Returns:
            bool: True if the button is clicked successfully, None otherwise.
        """
        return self.do_click(self.refresh_button()) if self.do_is_displayed(self.refresh_button()) else None

    def get_on_chain_total_balance(self):
        """
        Retrieves the on-chain total balance from the asset detail page.

        Returns:
            str: The on-chain total balance if it is displayed, None otherwise.
        """
        return self.do_get_text(self.on_chain_total_balance()) if self.do_is_displayed(self.on_chain_total_balance()) else None

    def get_on_chain_spendable_balance(self):
        """
        Retrieves the on-chain spendable balance from the asset detail page.

        Returns:
            str: The on-chain spendable balance if it is displayed, None otherwise.
        """
        return self.do_get_text(self.on_chain_spendable_balance()) if self.do_is_displayed(self.on_chain_spendable_balance()) else None

    def get_lightning_total_balance(self):
        """
        Retrieves the lightning total balance from the asset detail page.

        Returns:
            str: The lightning total balance if it is displayed, None otherwise.
        """
        return self.do_get_text(self.lightning_total_balance()) if self.do_is_displayed(self.lightning_total_balance()) else None

    def get_lightning_spendable_balance(self):
        """
        Retrieves the lightning spendable balance from the asset detail page.

        Returns:
            str: The lightning spendable balance if it is displayed, None otherwise.
        """
        return self.do_get_text(self.lightning_spendable_balance()) if self.do_is_displayed(self.lightning_spendable_balance()) else None

    def click_rgb_transaction_on_chain_frame(self):
        """
        Clicks the bitcoin transaction frame on the asset detail page.
        """
        return self.do_click(self.rgb_transaction_on_chain_frame()) if self.do_is_displayed(self.rgb_transaction_on_chain_frame()) else None

    def click_rgb_transaction_lightning_frame(self):
        """
        Clicks the bitcoin transaction frame on the asset detail page.
        """
        return self.do_click(self.rgb_transaction_lightning_frame()) if self.do_is_displayed(self.rgb_transaction_lightning_frame()) else None

    def get_transfer_status(self):
        """
        Retrieves the transfer status from the asset detail page.
        """
        return self.do_get_text(self.transfer_status()) if self.do_is_displayed(self.transfer_status()) else None

    def click_copy_button(self):
        """
        Clicks the copy button on the asset detail page.
        """
        if self.do_is_displayed(self.copy_button()):
            return self.copy_button().click()
        return None

    def click_confirmation_continue_button(self):
        """
        Clicks the transaction detail frame on the asset detail page.
        """
        return self.do_click(self.confirmation_continue_button()) if self.do_is_displayed(self.confirmation_continue_button()) else None

    def click_fail_transfer_button(self):
        """
        Clicks the fail transfer button on the asset detail page.
        """
        return self.do_click(self.fail_transfer_button()) if self.do_is_displayed(self.fail_transfer_button()) else None
