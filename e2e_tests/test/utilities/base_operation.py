# pylint: disable=unused-import
"""
This module provides a class for performing base operations on a graphical user interface (GUI) application.
"""
from __future__ import annotations

import os
import re
import time

import pyperclip
from dogtail.rawinput import keyCombo
from dogtail.rawinput import pressKey
from dogtail.rawinput import typeText
from dotenv import load_dotenv
from Xlib import display
from Xlib import X

from accessible_constant import TOASTER_DESCRIPTION

load_dotenv()
NATIVE_AUTHENTICATION_PASSWORD = os.getenv('NATIVE_AUTHENTICATION_PASSWORD')


class BaseOperations:
    """
    A class for performing base operations on a GUI application.

    Attributes:
        application (Node): The root node of the GUI application.
    """

    def __init__(self, application):
        """
        Initializes the BaseOperations class.

        Args:
            application (Node): The root node of the GUI application.
        """
        self.application = application

        # Define the elements like buttons and text fields as lambdas
        self.refresh_button = lambda: self.perform_action_on_element(
            role_name='push button', name='refresh_button',
        )
        self.close_button = lambda: self.perform_action_on_element(
            role_name='push button', name='close_button',
        )
        self.copy_button = lambda: self.perform_action_on_element(
            role_name='push button', name='Copy address',
        )

    def click_close_button(self):
        """
        Clicks on the cancel button.

        Returns:
            None
        """
        button = self.close_button()
        if self.do_is_displayed(button):
            self.do_click(button)

    def click_refresh_button(self):
        """
        Clicks on the refresh button.

        Returns:
            None
        """
        button = self.refresh_button()
        if self.do_is_displayed(button):
            self.do_click(button)

    def do_click(self, element):
        """
        Clicks on the specified element.

        Args:
            element (Node): The element to click on.

        Returns:
            None
        """
        if self.do_is_displayed(element):
            element.click()

    def do_set_value(self, element, value):
        """
        Sets the value of the specified element.

        Args:
            element (Node): The element to set the value for.
            value (str): The value to set.

        Returns:
            None
        """
        if self.do_is_displayed(element):
            element.typeText(value)

    def do_set_text(self, element, value):
        """
        Sets the value of the specified element.

        Args:
            element (Node): The element to set the value for.
            value (str): The value to set.

        Returns:
            None
        """
        if self.do_is_displayed(element):
            element.text = value

    def do_get_text(self, element):
        """
        Gets the text of the specified element.

        Args:
            element (Node): The element to get the text from.

        Returns:
            str: The text of the element.
        """
        if self.do_is_displayed(element):
            return element.name

        return None

    def do_is_displayed(self, element):
        """
        Checks if the specified element is displayed.

        Args:
            element (Node): The element to check.

        Returns:
            bool: True if the element is displayed, False otherwise.
        """
        element.grabFocus()
        return element and element.showing

    def do_is_enabled(self, element):
        """
        Checks if the specified element is enabled.

        Args:
            element (Node): The element to check.

        Returns:
            bool: True if the element is enabled, False otherwise.
        """
        return element.enabled

    def click_copy_button(self):
        """
        Clicks on the copy address button.

        Returns:
            None
        """
        button = self.copy_button()
        if self.do_is_displayed(button):
            self.do_click(button)

    def do_get_copied_address(self):
        """
        Gets the copied address.

        Returns:
            str: The copied address.
        """
        return pyperclip.paste()

    def activate_window_by_name(self, window_name):
        """
        Activates the window with the given name.

        Args:
            window_name (str): The name of the window to activate.

        Returns:
            None
        """
        d = display.Display()
        root = d.screen().root
        root.change_attributes(event_mask=X.SubstructureNotifyMask)

        # Get window list
        raw_data = root.get_full_property(
            d.intern_atom(
                '_NET_CLIENT_LIST',
            ), X.AnyPropertyType,
        ).value
        for window_id in raw_data:
            window = d.create_resource_object('window', window_id)
            window_name_property = window.get_wm_name()

            if window_name_property and re.search(window_name, window_name_property):
                window.set_input_focus(X.RevertToParent, X.CurrentTime)
                window.raise_window()
                d.sync()
                print(f"Activated window: {window_name}")
                return

        print(f"Window '{window_name}' not found")

    def do_focus_on_application(self, application):
        """
        Focuses on the given application.

        Args:
            application (str): The name of the application to focus on.

        Returns:
            None
        """
        return self.activate_window_by_name(application)

    def perform_action_on_element(self, role_name, name=None, description=None, timeout=30, retry_interval=0.5):
        """
        Retrieves the specified element with the given role and name or description, with retries.

        Args:
            role_name (str): The role of the element.
            name (str, optional): The name of the element. Defaults to None.
            description (str, optional): The description of the element. Defaults to None.
            timeout (int): The maximum time to wait for the element in seconds. Defaults to 30.
            retry_interval (float): The time to wait between retries in seconds. Defaults to 0.5.

        Returns:
            Node: The retrieved element, or False if no matching element is found within the timeout.
        """
        start_time = time.time()
        elements = []

        while time.time() - start_time < timeout:
            try:
                # Try to find elements by name or description
                if name:
                    elements = list(
                        self.application.findChildren(
                            lambda n: n.roleName == role_name and n.name == name,
                        ),
                    )
                elif description:
                    elements = list(
                        self.application.findChildren(
                            lambda n: n.roleName == role_name and n.description == description,
                        ),
                    )

                if elements:
                    element = elements[-1]
                    if element.showing:
                        element.grabFocus()
                        return element

            except Exception as e:
                # Log the exception and retry
                print(f"Exception while finding element: {e}")

            # Wait before the next retry
            time.sleep(retry_interval)

        return False

    def get_first_element(self, role_name, name=None, description=None, timeout=30, retry_interval=0.5):
        """
        Retrieves the first element with the given role and name or description, with retries.

        Args:
            role_name (str): The role of the element.
            name (str, optional): The name of the element. Defaults to None.
            description (str, optional): The description of the element. Defaults to None.
            timeout (int): The maximum time to wait for the element in seconds. Defaults to 30.
            retry_interval (float): The time to wait between retries in seconds. Defaults to 0.5.

        Returns:
            Node: The retrieved element, or False if no matching element is found within the timeout.
        """
        start_time = time.time()
        elements = []

        while time.time() - start_time < timeout:
            try:
                # Try to find elements by name or description
                if name:
                    elements = list(
                        self.application.findChildren(
                            lambda n: n.roleName == role_name and n.name == name,
                        ),
                    )
                elif description:
                    elements = list(
                        self.application.findChildren(
                            lambda n: n.roleName == role_name and n.description == description,
                        ),
                    )

                if elements:
                    for element in elements:
                        if element.showing and element.sensitive:
                            element.grabFocus()
                            return element

            except Exception as e:
                # Log the exception and retry
                print(f"Exception while finding element: {e}")

            # Wait before the next retry
            time.sleep(retry_interval)

        return False

    def do_clear_text(self, element):
        """
        Clears the text of the specified element
        """

        if self.do_is_displayed(element):

            for _ in range(len(element.text)):
                pressKey('backspace')

    def get_text(self, element):
        """gets the text of the specified element from its description"""
        if self.do_is_displayed(element):
            return element.text
        return None

    def wait_for_toaster_message(self, toaster_name=TOASTER_DESCRIPTION, timeout=120, interval=0.5):
        """
        Waits until a toaster message appears on the screen.

        Args:
            toaster_name (str): The accessible name of the toaster message.
            timeout (int): Maximum time to wait (in seconds). Default is 120 seconds.
            interval (float): Time interval between checks. Default is 0.5 seconds.

        Raises:
            TimeoutError: If the toaster message does not appear within the timeout.
        """
        start_time = time.time()

        while time.time() - start_time < timeout:
            try:
                toaster = self.perform_action_on_element(
                    role_name='label', description=toaster_name,
                )
                if toaster:
                    return  # Exit function when toaster appears
            except Exception:
                pass  # Ignore errors if the element is not found yet

            time.sleep(interval)  # Wait and retry

        raise TimeoutError(
            f"""Toaster message '{
                toaster_name
            }' did not appear within {timeout} seconds.""",
        )

    def do_get_child_count(self, element):
        """gets the number of children of the specified element"""
        if self.do_is_displayed(element):

            return element.children

        return None

    def enter_native_password(self):
        """Enter the password when the native auth dialog is show"""
        typeText(NATIVE_AUTHENTICATION_PASSWORD)
        keyCombo('enter')
