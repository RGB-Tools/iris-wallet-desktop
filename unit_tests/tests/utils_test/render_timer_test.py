# Disable the redefined-outer-name warning as
# it's normal to pass mocked object in tests function
# pylint: disable=redefined-outer-name,unused-argument, protected-access
"""Unit tests for the RenderTimer class."""
from __future__ import annotations

from unittest.mock import call
from unittest.mock import patch

import pytest
from PySide6.QtCore import QElapsedTimer

from src.utils.render_timer import RenderTimer


@pytest.fixture
def render_timer():
    """Fixture to create a RenderTimer instance."""
    # Clear the singleton instance before each test
    RenderTimer._instance = None
    # Patch logger at instance creation
    with patch('src.utils.render_timer.logger') as mock_logger:
        timer = RenderTimer('Test Task')
        timer._logger = mock_logger  # Store mock logger for verification
        yield timer


def test_singleton_pattern():
    """Test that RenderTimer follows the singleton pattern."""
    # Clear the singleton instance to ensure test isolation
    RenderTimer._instance = None
    with patch('src.utils.render_timer.logger'):
        # Create two instances
        timer1 = RenderTimer('Task 1')
        timer2 = RenderTimer('Task 2')

        # Verify they are the same instance
        assert timer1 is timer2
        # The task name should be from the second initialization
        assert timer1.task_name == 'Task 2'


def test_start_logging(render_timer):
    """Test that start() properly logs the start of timing."""
    render_timer.start()
    render_timer._logger.info.assert_called_once_with(
        '%s started.', 'Test Task',
    )


def test_start_prevents_multiple_starts(render_timer):
    """Test that start() prevents multiple concurrent timing sessions."""
    render_timer.start()
    render_timer._logger.info.reset_mock()

    # Try to start again
    render_timer.start()
    # Should not log or start timer again
    render_timer._logger.info.assert_not_called()


def test_stop_without_start(render_timer):
    """Test stop() behavior when timer wasn't started."""
    render_timer.stop()
    render_timer._logger.warning.assert_called_once_with(
        'Timer for %s was not started.',
        'Test Task',
    )


def test_stop_with_valid_timer(render_timer):
    """Test stop() behavior with a valid timer."""
    # Start the timer
    render_timer.start()
    render_timer._logger.reset_mock()

    # Mock the elapsed time
    with patch.object(render_timer.timer, 'elapsed', return_value=100):
        render_timer.stop()

        # Verify logging
        render_timer._logger.info.assert_called_once_with(
            '%s finished. Time taken: %d ms.',
            'Test Task',
            100,
        )


def test_multiple_start_stop_cycles(render_timer):
    """Test multiple start-stop cycles work correctly."""
    # First cycle
    render_timer.start()
    with patch.object(render_timer.timer, 'elapsed', return_value=100):
        render_timer.stop()

    render_timer._logger.reset_mock()

    # Second cycle
    render_timer.start()
    with patch.object(render_timer.timer, 'elapsed', return_value=150):
        render_timer.stop()

    # Verify the second cycle was logged
    expected_calls = [
        call('%s started.', 'Test Task'),
        call('%s finished. Time taken: %d ms.', 'Test Task', 150),
    ]
    render_timer._logger.info.assert_has_calls(expected_calls)


def test_timer_initialization():
    """Test that timer is properly initialized."""
    # Clear the singleton instance to ensure test isolation
    RenderTimer._instance = None
    with patch('src.utils.render_timer.logger'):
        timer = RenderTimer('Test Task')
        assert isinstance(timer.timer, QElapsedTimer)
        assert timer.initialized
        assert not timer.is_rendering


def test_stop_resets_rendering_flag(render_timer):
    """Test that stop() resets the is_rendering flag."""
    render_timer.start()
    assert render_timer.is_rendering

    render_timer.stop()
    assert not render_timer.is_rendering


def test_initialization_happens_once():
    """Test that initialization only happens once despite multiple instantiations."""
    # Clear the singleton instance to ensure test isolation
    RenderTimer._instance = None
    with patch('src.utils.render_timer.logger'):
        timer1 = RenderTimer('Task 1')
        original_timer = timer1.timer

        # Create new instance
        timer2 = RenderTimer('Task 2')

        # Verify the QElapsedTimer instance remains the same
        assert timer2.timer is original_timer


def test_elapsed_time_measurement(render_timer):
    """Test that elapsed time is measured correctly."""
    render_timer.start()

    # Mock elapsed time
    with patch.object(render_timer.timer, 'elapsed', return_value=500):
        render_timer.stop()

        # Verify the correct elapsed time was logged
        render_timer._logger.info.assert_called_with(
            '%s finished. Time taken: %d ms.',
            'Test Task',
            500,
        )
