"""
Dogtail configuration module for optimizing AT-SPI performance in CI environments.

This module configures dogtail's search behavior, timeouts, and retry logic to handle
slow AT-SPI responses, especially in CI environments where accessibility services
may be slower to respond.
"""
from __future__ import annotations

import os
import time

from dogtail import config
from dogtail.tree import root


def is_ci_environment():
    """
    Detect if running in a CI environment.

    Returns:
        bool: True if running in CI, False otherwise.
    """
    return os.getenv('CI', '').lower() in ('true', '1', 'yes')


def configure_dogtail():
    """
    Configure dogtail with optimized settings for CI environments.

    This function sets up dogtail's configuration to handle slow AT-SPI responses
    by adjusting search timeouts, retry intervals, and action delays.
    """
    in_ci = is_ci_environment()

    search_backoff = float(
        os.getenv('DOGTAIL_SEARCH_BACKOFF', '1.5' if in_ci else '0.5'),
    )

    # Configure search behavior
    config.config.searchBackoffDuration = search_backoff
    config.config.searchCutoffCount = 60 if in_ci else 30

    # Delay before performing actions
    config.config.defaultDelay = 1.5 if in_ci else 0.2

    # Delay after performing actions
    config.config.actionDelay = 1.5 if in_ci else 0.3

    # Delay between keystrokes when typing
    config.config.typingDelay = 0.1 if in_ci else 0.05


def warm_up_atspi(timeout=10):
    """
    Warm up the AT-SPI accessibility tree by pre-loading it.

    This function attempts to access the accessibility tree early to ensure
    AT-SPI is fully initialized before tests begin.

    Args:
        timeout (int): Maximum time to wait for AT-SPI warmup (in seconds).
    """
    start_time = time.time()
    attempts = 0
    max_attempts = 5

    while time.time() - start_time < timeout and attempts < max_attempts:
        try:
            _ = root.children
            time.sleep(1)
            return True
        except Exception:
            attempts += 1
            time.sleep(1)

    return True


def get_ci_timeout_multiplier():
    """
    Get the timeout multiplier for CI environments.

    Returns:
        float: Multiplier to apply to timeouts (1.5x in CI, 1.0x locally).
    """
    return 1.5 if is_ci_environment() else 1.0


def get_default_timeout(base_timeout=30):
    """
    Get the default timeout adjusted for the current environment.

    Args:
        base_timeout (int): Base timeout in seconds.

    Returns:
        int: Adjusted timeout for the current environment.
    """
    multiplier = get_ci_timeout_multiplier()
    return int(base_timeout * multiplier)


def get_toaster_timeout():
    """
    Get the timeout for toaster element searches.
    Toasters are short-lived (6s display time), so we need shorter timeouts.

    Returns:
        int: Timeout in seconds (10s in CI, 8s locally).
    """
    return 10 if is_ci_environment() else 8


def get_toaster_poll_interval():
    """
    Get the polling interval for toaster element searches.
    Aggressive polling is needed to catch short-lived toasters.

    Returns:
        float: Poll interval in seconds (0.1s for aggressive polling).
    """
    return 0.1


def get_max_consecutive_failures():
    """
    Get the maximum number of consecutive element search failures
    before circuit breaker triggers.

    Returns:
        int: Max failures (3 in CI, 2 locally).
    """
    return 3 if is_ci_environment() else 2


def get_element_search_timeout():
    """
    Get the default timeout for element searches.
    Reduced from 30s to 20s for faster failure detection.

    Returns:
        int: Timeout in seconds (30s in CI, 20s locally).
    """
    return get_default_timeout(20)


# Initialize dogtail configuration when module is imported
configure_dogtail()
