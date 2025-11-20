# pylint : disable = possibly-used-before-assignment
"""
SendOperation class provides methods for sending assets using bitcoin or lightning transfer.
"""
from __future__ import annotations

from e2e_tests.test.pageobjects.main_page_objects import MainPageObjects
from e2e_tests.test.utilities.base_operation import BaseOperations
from src.utils.info_message import INFO_BITCOIN_SENT


class SendOperation(MainPageObjects, BaseOperations):
    """
    Initializes the SendOperation class with the application.
    """

    def __init__(self, application):
        """
        Sends assets using bitcoin or lightning transfer.
        """
        super().__init__(application)

    def send(self, application, receiver_invoice, amount=None, transfer_type=None, is_native_auth_enabled: bool = False):
        """
        Send assets using bitcoin or lightning transfer.

        :param receiver_invoice: The recipient's invoice.
        :param amount: The amount to send.
        :param transfer_type: The type of transfer ('bitcoin' or 'lightning').
        """
        self.do_focus_on_application(application)
        if transfer_type == 'bitcoin' and self.do_is_displayed(self.wallet_transfer_page_objects.on_chain_button()):
            self.wallet_transfer_page_objects.click_on_chain_button()

        if transfer_type == 'lightning' and self.do_is_displayed(self.wallet_transfer_page_objects.lightning_button()):
            self.wallet_transfer_page_objects.click_lightning_button()

        send_objects = self.send_asset_page_objects if transfer_type != 'lightning' else self.send_ln_invoice_page_objects

        if self.do_is_displayed(send_objects.invoice_input()):
            send_objects.enter_asset_invoice(receiver_invoice)

        if amount and hasattr(send_objects, 'asset_amount_input') and self.do_is_displayed(send_objects.asset_amount_input()):
            send_objects.enter_asset_amount(amount)

        if self.do_is_displayed(send_objects.send_button()):
            send_objects.click_send_button()

        if is_native_auth_enabled is True:
            self.enter_native_password()

    def send_with_no_fund(self, application, receiver_invoice, amount, transfer_type=None):
        """
        Send assets without sufficient funds.
        """
        validation = None
        self.do_focus_on_application(application)
        if transfer_type == 'bitcoin' and self.do_is_displayed(self.wallet_transfer_page_objects.on_chain_button()):
            self.wallet_transfer_page_objects.click_on_chain_button()

        if self.do_is_displayed(self.send_asset_page_objects.invoice_input()):
            self.send_asset_page_objects.enter_asset_invoice(receiver_invoice)

        if self.do_is_displayed(self.send_asset_page_objects.asset_amount_input()):
            self.send_asset_page_objects.enter_asset_amount(amount)

        if self.do_is_displayed(self.send_asset_page_objects.amount_validation()):
            validation = self.send_asset_page_objects.get_amount_validation()

        if self.do_is_displayed(self.send_asset_page_objects.send_asset_close_button()):
            self.send_asset_page_objects.click_send_asset_close_button()

        return validation

    def send_with_wrong_invoice(self, application, receiver_invoice, amount, transfer_type=None):
        """
        Send assets with a wrong invoice.
        """
        description = None
        self.do_focus_on_application(application)
        if transfer_type == 'bitcoin' and self.do_is_displayed(self.wallet_transfer_page_objects.on_chain_button()):
            self.wallet_transfer_page_objects.click_on_chain_button()

        if self.do_is_displayed(self.send_asset_page_objects.invoice_input()):
            self.send_asset_page_objects.enter_asset_invoice(receiver_invoice)

        if self.do_is_displayed(self.send_asset_page_objects.asset_amount_input()):
            self.send_asset_page_objects.enter_asset_amount(amount)

        if self.do_is_displayed(self.send_asset_page_objects.send_button()):
            self.send_asset_page_objects.click_send_button()

        if self.do_is_displayed(self.toaster_page_objects.toaster_frame()):
            description = self.toaster_page_objects.click_and_get_description()

        if self.do_is_displayed(self.send_asset_page_objects.send_asset_close_button()):
            self.send_asset_page_objects.click_send_asset_close_button()

        return description

    def send_with_custom_fee_rate(self, application, receiver_invoice, amount, fee_rate, transfer_type=None):
        """
        Sends assets using bitcoin or lightning transfer with a custom fee rate.
        """

        description = None

        self.do_focus_on_application(application)
        if transfer_type == 'bitcoin' and self.do_is_displayed(self.wallet_transfer_page_objects.on_chain_button()):
            self.wallet_transfer_page_objects.click_on_chain_button()

        if self.do_is_displayed(self.send_asset_page_objects.invoice_input()):
            self.send_asset_page_objects.enter_asset_invoice(receiver_invoice)

        if self.do_is_displayed(self.send_asset_page_objects.asset_amount_input()):
            self.send_asset_page_objects.enter_asset_amount(amount)

        if self.do_is_displayed(self.send_asset_page_objects.fee_rate_input()):
            self.send_asset_page_objects.enter_fee_rate(fee_rate)

        if self.do_is_displayed(self.send_asset_page_objects.send_button()):
            self.send_asset_page_objects.click_send_button()

        toaster_element = None
        if self.do_is_displayed(self.toaster_page_objects.toaster_frame()):
            toaster_element, description = self.toaster_page_objects.click_toaster_frame()

        # Filter description if we got one
        if toaster_element and description:
            filter_text = INFO_BITCOIN_SENT.split('{}', maxsplit=1)[0]
            if filter_text not in description:
                description = None

        return description
