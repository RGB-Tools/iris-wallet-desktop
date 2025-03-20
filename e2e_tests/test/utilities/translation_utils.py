"""
Translation manager for iris wallet desktop application.
"""
from __future__ import annotations

import sys

from PySide6.QtCore import QCoreApplication
from PySide6.QtCore import QTranslator
from PySide6.QtWidgets import QApplication


class TranslationManager:
    """
    Translation manager for iris wallet desktop application.
    """
    _translator = None
    _app = None  # Ensure QApplication exists

    @classmethod
    def load_translation(cls, qm_file='src/translations/en_IN.qm'):
        """
        Load translation globally and ensure QApplication exists.

        Args:
            qm_file (str): Path to the translation file (default: 'src/translations/en_IN.qm')
        """
        if not cls._app:
            cls._app = QApplication.instance() or QApplication(sys.argv)

        if cls._translator is None:
            cls._translator = QTranslator()
            if cls._translator.load(qm_file):
                QCoreApplication.installTranslator(cls._translator)
            else:
                raise ValueError(f"Failed to load translation file: {qm_file}")

    @staticmethod
    def translate(key):
        """
        Translate a given key.

        Args:
            key (str): Key to be translated

        Returns:
            str: Translated key
        """
        return QCoreApplication.translate('iris_wallet_desktop', key)
