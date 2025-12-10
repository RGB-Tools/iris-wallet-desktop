"""
This module provides the services for the asset detail page.
"""
# pylint: disable=broad-except
from __future__ import annotations

from datetime import datetime

from src.data.repository.payments_repository import PaymentRepository
from src.data.repository.rgb_repository import RgbRepository
from src.model.enums.enums_model import AssetTransferStatusEnumModel
from src.model.enums.enums_model import TransactionStatusEnumModel
from src.model.enums.enums_model import TransferStatusEnumModel
from src.model.payments_model import ListPaymentResponseModel
from src.model.rgb_model import AssetBalanceResponseModel
from src.model.rgb_model import AssetIdModel
from src.model.rgb_model import ListOnAndOffChainTransfersWithBalance
from src.model.rgb_model import ListTransferAssetResponseModel
from src.model.rgb_model import ListTransfersRequestModel
from src.model.rgb_model import TransactionTxModel
from src.model.rgb_model import TransferAsset
from src.utils.custom_exception import CommonException
from src.utils.custom_exception import ServiceOperationException
from src.utils.handle_exception import handle_exceptions


class AssetDetailPageService:
    'This class contain services for asset detail page'
    @staticmethod
    def get_asset_transactions(list_transfers_request_model: ListTransfersRequestModel) -> ListOnAndOffChainTransfersWithBalance | None:
        """
        Retrieves and processes asset transactions for a given asset ID. This function fetches the list of transactions
        associated with the asset, formats date and time fields, and sets appropriate transfer statuses based on the
        transaction type. The results are sorted by transaction idx in descending order.

        Args:
        list_transfers_request_model (ListTransfersRequestModel): The model containing the asset ID for which transactions are to be retrieved.

        Returns:
        ListTransferAssetWithBalanceResponseModel | CommonException: The processed list of transactions with formatted date and
        time and updated statuses, or an exception if an error occurs during processing.

        Raises:
        ServiceOperationException: If an unknown transaction type is encountered.
        """
        try:
            transactions: ListTransferAssetResponseModel = RgbRepository.list_transfers(
                list_transfers_request_model,
            )
            balance: AssetBalanceResponseModel = RgbRepository.get_asset_balance(
                AssetIdModel(asset_id=list_transfers_request_model.asset_id),
            )
            lightning: ListPaymentResponseModel = PaymentRepository.list_payment()

            if (not transactions or not transactions.transfers) and (not lightning or not lightning.payments):
                return ListOnAndOffChainTransfersWithBalance(transfers=[], lightning=[], asset_balance=balance)
            if lightning and lightning.payments:
                for transaction in lightning.payments:
                    if transaction is None:
                        continue
                    # Convert the timestamp to a datetime object and format it
                    update_at = datetime.fromtimestamp(
                        transaction.updated_at,
                    )
                    transaction.updated_at_date = update_at.strftime(
                        '%Y-%m-%d',
                    )
                    transaction.updated_at_time = update_at.strftime(
                        '%H:%M:%S',
                    )
                    # Convert the timestamp to a datetime object and format it
                    create_at = datetime.fromtimestamp(transaction.created_at)
                    transaction.created_at_date = create_at.strftime(
                        '%Y-%m-%d',
                    )
                    transaction.created_at_time = create_at.strftime(
                        '%H:%M:%S',
                    )
                    transaction.asset_amount_status = f'-{str(transaction.asset_amount)}' if not transaction.inbound else f'+{
                        str(transaction.asset_amount)
                    }'

            if transactions and transactions.transfers:
                for transaction in transactions.transfers:
                    if transaction is None:
                        continue

                    status_to_check = [
                        TransactionStatusEnumModel.SETTLED,
                        TransactionStatusEnumModel.FAILED,
                        TransactionStatusEnumModel.CONFIRMED,
                        TransactionStatusEnumModel.WAITING_CONFIRMATIONS,
                        TransactionStatusEnumModel.WAITING_COUNTERPARTY,
                    ]

                    if transaction.status in [status.value for status in status_to_check]:
                        # Convert the timestamp to a datetime object and format it
                        update_at = datetime.fromtimestamp(
                            transaction.updated_at,
                        )
                        transaction.updated_at_date = update_at.strftime(
                            '%Y-%m-%d',
                        )
                        transaction.updated_at_time = update_at.strftime(
                            '%H:%M:%S',
                        )

                    # Convert the timestamp to a datetime object and format it
                    create_at = datetime.fromtimestamp(transaction.created_at)
                    transaction.created_at_date = create_at.strftime(
                        '%Y-%m-%d',
                    )
                    transaction.created_at_time = create_at.strftime(
                        '%H:%M:%S',
                    )
                    AssetDetailPageService.assign_transfer_status(transaction)

            transactions.transfers = sorted(
                transactions.transfers or [],
                # Using an else clause just for safety in type checking
                key=lambda x: x.idx if x is not None else -1,
                reverse=True,
            )

            return ListOnAndOffChainTransfersWithBalance(onchain_transfers=transactions.transfers, off_chain_transfers=lightning.payments, asset_balance=balance)
        except Exception as exc:
            return handle_exceptions(exc)

    @staticmethod
    def get_single_asset_transaction(asset_id: ListTransfersRequestModel, transaction_tx: TransactionTxModel) -> TransferAsset | None:
        """
        Retrieves a single asset transaction based on a transaction ID or index.

        This method searches through a list of asset transactions to find one that matches either the transaction ID or the idx

        Parameters:
        - asset_id (ListTransfersRequestModel): The model containing the ID of the asset whose transactions are to be retrieved.
        - transaction_tx (TrasactionTxModel): The model containing the transaction ID (`tx_id`) and/or the transaction index (`idx`)

        Returns:
        - TransferAsset | None: Returns the matching transaction if found; otherwise, returns None if no match is found or if there are no transactions.
        - CommonException | Exception: Raises or returns an exception if an error occurs during the process.

        Raises:
        - CommonException: If a specific known error related to the business logic occurs.
        - Exception: For general exceptions, the error is handled by the `handle_exceptions` method which transform it into a CommonException exception type.
        """
        try:
            transactions = AssetDetailPageService.get_asset_transactions(
                asset_id,
            )

            if not transactions or not transactions.transfers:
                return None

            for transaction in transactions.transfers:
                if transaction is None:
                    continue

                if transaction_tx.tx_id and transaction.txid == transaction_tx.tx_id:
                    return transaction
                if transaction_tx.idx and transaction.idx == transaction_tx.idx:
                    return transaction

            return None
        except CommonException as exc:
            raise exc
        except Exception as exc:
            return handle_exceptions(exc)

    @staticmethod
    def assign_transfer_status(transaction):
        """
        Assign transfer statuses and amount status based on transaction kind.
        """
        # Assign transfer statuses based on the transaction kind
        if transaction.kind == AssetTransferStatusEnumModel.ISSUANCE.value:
            transaction.transfer_Status = TransferStatusEnumModel.INTERNAL
            transaction.amount_status = f"""+{
                str(transaction.assignments[0].value)
            }"""
        elif transaction.kind in (
            AssetTransferStatusEnumModel.RECEIVE_BLIND.value,
            AssetTransferStatusEnumModel.RECEIVE_WITNESS.value,
        ):
            transaction.transfer_Status = TransferStatusEnumModel.RECEIVED
            amount_val = None
            if (
                transaction.assignments
                and len(transaction.assignments) > 0
                and transaction.assignments[0].value is not None
            ):
                amount_val = transaction.assignments[0].value
            elif (
                transaction.requested_assignment
                and transaction.requested_assignment.value is not None
            ):
                amount_val = transaction.requested_assignment.value

            transaction.amount_status = f"+{
                str(amount_val)
                if amount_val is not None else '0'
            }"
        elif transaction.kind == AssetTransferStatusEnumModel.SEND.value:
            transaction.amount_status = f"""-{
                str(transaction.requested_assignment.value)
            }"""
            transaction.transfer_Status = TransferStatusEnumModel.SENT
        else:
            raise ServiceOperationException(
                'Unknown transaction type',
            )
