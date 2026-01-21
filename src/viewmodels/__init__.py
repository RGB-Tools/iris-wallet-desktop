"""
viewmodels
==========

Description:
------------
The `viewmodels` package contains various viewmodels that
connect view and model functionality.

Submodules:
-----------
- IssueNIAViewModel: Connects NIA models to IssueNIAWidget
                       to enable communication between them.
- MainAssetViewModel: Connects main assets models to MainAssetWidget
                      to enable communication between them.
- SetWalletPasswordViewModel: Connects setWallet models to SetWalletWidget
                              to enable communication between them.
- TermsViewModel: Connects term models to TerAndConditionWidget
                  to enable communication between them.
- WelcomeViewModel: Connects welcome models to WelcomeWidget
                    to enable communication between them.

Usage:
------
Examples of how to use the utilities in this package:

    >>> from viewmodels import IssueNIAViewModel
    >>> model = IssueNIAViewModel()
    >>> print(model)
"""
from __future__ import annotations
