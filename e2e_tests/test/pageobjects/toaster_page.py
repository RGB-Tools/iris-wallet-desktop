# pylint: disable=too-many-return-statements,too-many-branches
"""
This module contains the ToasterPageObjects class, which provides methods for interacting with toaster page elements.
"""
from __future__ import annotations

import time

from accessible_constant import TOASTER_CLOSE_BUTTON
from accessible_constant import TOASTER_DESCRIPTION
from accessible_constant import TOASTER_FRAME
from accessible_constant import TOASTER_TITLE
from e2e_tests.test.utilities.base_operation import BaseOperations
from e2e_tests.test.utilities.dogtail_config import is_ci_environment


class ToasterPageObjects(BaseOperations):
    """
    A class representing toaster page objects.

    Attributes:
        application (object): The application instance.
        toaster_frame (lambda): A lambda function to get the toaster frame element.
        toaster_title (lambda): A lambda function to get the toaster title element.
        toaster_description (lambda): A lambda function to get the toaster description element.
        toaster_close_button (lambda): A lambda function to get the toaster close button element.
    """

    def __init__(self, application):
        """
        Initializes the ToasterPageObjects instance.

        Args:
            application (object): The application instance.
        """
        super().__init__(application)

        self.toaster_frame = lambda: self.perform_action_on_element(
            role_name='panel', name=TOASTER_FRAME,
        )
        self.toaster_title = lambda: self.perform_action_on_element(
            role_name='label', description=TOASTER_TITLE,
        )
        self.toaster_description = lambda: self.perform_action_on_element(
            role_name='label', description=TOASTER_DESCRIPTION,
        )
        self.toaster_close_button = lambda: self.perform_action_on_element(
            role_name='push button', name=TOASTER_CLOSE_BUTTON,
        )

    def wait_for_toaster(self, timeout=15, poll_interval=0.2):
        """
        Wait for toaster to appear in AT-SPI tree with aggressive polling.
        Captures the description IMMEDIATELY to avoid disappearance issues.

        Args:
            timeout (int): Maximum seconds to wait. Default 15s for CI.
            poll_interval (float): Seconds between polls. Default 0.2s for aggressive detection.

        Returns:
            tuple: (toaster_element, description_text) if found, (None, None) otherwise.
                   Description is captured immediately to prevent race conditions.
        """

        if is_ci_environment():
            timeout = 20

        start_time = time.time()
        attempt = 0

        print(
            f"[TOASTER] Waiting for toaster (timeout={timeout}s, poll_interval={
                poll_interval
            }s)...",
        )

        while time.time() - start_time < timeout:
            attempt += 1
            try:
                # Search AT-SPI tree directly for toaster panel
                toasters = self.application.findChildren(
                    lambda node: node.roleName == 'panel'
                    and node.name == TOASTER_FRAME,
                )

                if toasters:
                    # Check if any toaster is actually showing
                    for toaster in toasters:
                        if toaster.showing:
                            # IMMEDIATELY capture description before toaster can disappear
                            description = self._extract_description_immediately(
                                toaster,
                            )
                            elapsed = time.time() - start_time
                            print(
                                f"[TOASTER] Found toaster after {attempt} attempts ({elapsed:.2f}s), description: {
                                    description
                                }",
                            )
                            # Return both element and description
                            return (toaster, description)
            except Exception as e:
                if attempt % 10 == 0:  # Log every 10th attempt to avoid spam
                    print(f"[TOASTER] Attempt {attempt}: {e}")

            time.sleep(poll_interval)

        print(f"[TOASTER] Timeout after {attempt} attempts ({timeout}s)")
        return (None, None)  # Return tuple for consistency

    def _extract_description_immediately(self, toaster_element):
        """
        Extract description from toaster IMMEDIATELY to prevent race conditions.
        This is called as soon as the toaster is found, before it can disappear.

        Args:
            toaster_element: The toaster panel element.

        Returns:
            str: Description text if found, None otherwise.
        """
        try:
            # Find description labels within this specific toaster
            descriptions = toaster_element.findChildren(
                lambda node: node.roleName == 'label' and node.description == TOASTER_DESCRIPTION,
            )

            if descriptions:
                # Get the last one(most recent)
                last_desc = descriptions[-1]
                text = last_desc.name if hasattr(last_desc, 'name') else None
                if text:
                    return text

            # Fallback: try to get any label text from the toaster
            labels = toaster_element.findChildren(
                lambda node: node.roleName == 'label' and node.name,
            )
            if labels and len(labels) > 1:  # Skip title, get description
                return labels[-1].name

        except Exception as e:
            print(f"[TOASTER] Failed to extract description immediately: {e}")

        return None

    def click_toaster_frame(self):
        """
        Waits for toaster, captures description immediately, then clicks it.

        Returns:
            tuple: (toaster_element, description) if successful, (False, None) otherwise.
        """
        toaster_element, description = self.wait_for_toaster()
        if not toaster_element:
            return (False, None)

        try:
            self.do_click(toaster_element)
            return (toaster_element, description)
        except Exception as e:
            print(f'[TOASTER] Failed to click toaster: {e}')
            return (False, None)

    def click_and_get_description(self, filter_pattern=None):
        """
        Convenience method that waits for toaster, captures description, and clicks it.

        Args:
            filter_pattern (str, optional): A substring to filter the toaster text.

        Returns:
            str: The toaster description if successful, None otherwise.
        """
        toaster_element, description = self.click_toaster_frame()
        if not toaster_element:
            return None

        # Apply filter if needed
        if filter_pattern and description:
            if filter_pattern not in description:
                return None

        return description

    def get_toaster_title(self):
        """
        Gets the text of the toaster title element if it is displayed.

        Returns:
            str: The text of the element if it is displayed, None otherwise.
        """
        return self.do_get_text(self.toaster_title()) if self.do_is_displayed(self.toaster_title()) else None

    def get_toaster_description(self, filter_pattern=None, max_retries=4, toaster_element=None):
        """
        Gets the text of the toaster description element.
        DEPRECATED: Prefer using click_toaster_frame() which returns description immediately.
        This method is kept for backward compatibility but may fail if toaster disappears.

        Args:
            filter_pattern (str, optional): A substring to filter the toaster text.
            max_retries (int): Number of retries if description is not immediately available.
            toaster_element (Node, optional): Pre-found toaster element to use. If None, will search for one.

        Returns:
            str: The text of the element if found, None otherwise.
        """
        # If no element provided, try to wait for toaster
        if toaster_element is None:
            toaster_element, description = self.wait_for_toaster()
            if description:  # If we got description from wait_for_toaster, use it
                if filter_pattern and filter_pattern not in description:
                    return None
                return description
            if not toaster_element:
                print('[TOASTER] No toaster found for description')
                return None

        # If element is a tuple (from new click_toaster_frame), extract
        if isinstance(toaster_element, tuple):
            element, desc = toaster_element
            if desc:  # Use captured description if available
                if filter_pattern and filter_pattern not in desc:
                    return None
                return desc
            toaster_element = element

        # Legacy path: try to get description from the specific toaster we have
        for attempt in range(max_retries):
            try:
                # Try to get description from this specific toaster
                text = self._get_description_from_toaster(
                    toaster_element, filter_pattern,
                )
                if text:
                    return text

                # On last attempt, try fallback search
                if attempt == max_retries - 1:
                    text = self._fallback_description_search(filter_pattern)
                    if text:
                        return text

            except Exception:
                pass

            # Small delay before retry
            if attempt < max_retries - 1:
                time.sleep(0.2)

        return None

    def _get_description_from_toaster(self, toaster_element, filter_pattern=None):
        """
        Extract description text from a specific toaster element.

        Args:
            toaster_element: The toaster element to search within.
            filter_pattern (str, optional): Filter pattern to match.

        Returns:
            str: Description text if found and matches filter, None otherwise.
        """
        descriptions = toaster_element.findChildren(
            lambda node: node.roleName == 'label' and node.description == TOASTER_DESCRIPTION,
        )

        if not descriptions:
            return None

        # Get the last description (most recent)
        last_desc = descriptions[-1]
        text = last_desc.name if hasattr(last_desc, 'name') else None

        if not text:
            return None

        # Apply filter if provided
        if filter_pattern and filter_pattern not in text:
            return None

        return text

    def _fallback_description_search(self, filter_pattern=None):
        """
        Fallback search for toaster description in entire application tree.

        Args:
            filter_pattern (str, optional): Filter pattern to match.

        Returns:
            str: Description text if found, None otherwise.
        """
        matches = self.application.findChildren(
            lambda node: node.roleName == 'label' and node.description == TOASTER_DESCRIPTION,
        )

        if not matches:
            return None

        # Filter matches if pattern is provided
        if filter_pattern:
            matches = [
                m for m in matches if m.name and filter_pattern in m.name
            ]

        if not matches:
            return None

        # Pick the LAST matched node (most recent toaster)
        last_node = matches[-1]
        if last_node.name:
            return last_node.name

        return None

    def click_toaster_close_button(self):
        """
        Clicks the toaster close button element if it is displayed.

        Returns:
            bool: True if the element is clicked, False otherwise.
        """
        return self.do_click(self.toaster_close_button()) if self.do_is_displayed(self.toaster_close_button()) else None
