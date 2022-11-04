from collections import defaultdict
from heapq import heappush, heappop
from datetime import datetime
from typing import Dict, List
from dataclasses import dataclass

class InSufficientPoints(Exception):
    """ raised when there are no enough points to spend """
    pass

@dataclass
class PayerRecord:
    payer: str
    points: int

@dataclass
class TransactionRecord(PayerRecord):
    ts: datetime
    # heapq uses this method compare records
    def __lt__(self, other: 'TransactionRecord') -> bool:
        return self.ts < other.ts


class UserAccount:
    """
    Abstract DataStructure to add transactions, spend points, and get balance points on a user
    """
    def __init__(self) -> None:
        # list of all positive transactions
        self._transactions: List[TransactionRecord] = []
        # points for each payer based that were given as "spent" already (i.e. given as part of add transactions)
        self._pending_spends: Dict[str, int] = defaultdict(int)

    def __add_transaction(self, transac: TransactionRecord):
        """
        Adds the given transaction into UserAccount.

        :param transac: transaction to add
        :type transac: TransactionRecord
        """
        if transac.points == 0:
            return
        if transac.points > 0:
            heappush(self._transactions, transac)
        else: # this is a spend, add this pending spend
            # if this is more than the balance, throw error
            if -1 * transac.points > self.balance()[transac.payer]:
                raise InSufficientPoints(f"Cannot add -{transac.points} for payer {transac.payer}")
            self._pending_spends[transac.payer] += -1 * transac.points

    def _get_next_transaction_to_spend(self) -> TransactionRecord:
        """Returns the next transaction that we can use to spend.
        A transaction with zero points is also considered valid transaction, so it is returned too

        :raises ValueError: If called when there are no transcations
        :return: TransactionRecord that we can use to spend
        :rtype: TransactionRecord
        """
        if not self._transactions:
            raise ValueError("No Transactions!")

        oldest = heappop(self._transactions)
        # there are some points that are pending, first remove them and allocate the remaining
        if oldest.payer in self._pending_spends and self._pending_spends[oldest.payer] > 0:
            removed = min(self._pending_spends[oldest.payer], oldest.points)
            oldest.points -= removed
            # update the pending for this payer
            self._pending_spends[oldest.payer] -= removed
        return oldest

    def add(self, new_transactions: List[TransactionRecord]) -> None:
        """
        Adds the given transactions into the user account

        :param new_transactions: list of new transactions, can include both normal and earned point transactions
        :type new_transactions: List[TransactionRecord]
        :return: None
        :rtype: None
        """
        for transac in sorted(new_transactions, key=lambda x: -x.points):
            self.__add_transaction(transac)

    def balance(self) -> Dict[str, int]:
        """Returns balance of the useraccount

        :return: balance dictionary where payer is key and avaialble points as value
        :rtype: Dict[str, int]
        """
        d: Dict[str, int] = defaultdict(int)
        for transac in self._transactions:
            d[transac.payer] += transac.points
        for payer, points in self._pending_spends.items():
            d[payer] -= points
            # if the payer has zero balance, remove it
            if d[payer] == 0:
                d.pop(payer)
        return d

    def total_points(self) -> int:
        return sum(self.balance().values())

    def _spend_summary(self, records: List[PayerRecord]) -> Dict[str, int]:
        spend_summary: Dict[str, int] = defaultdict(int)
        for record in records:
            spend_summary[record.payer] += record.points
        return spend_summary

    def spend(self, points: int) -> Dict[str, int]:
        """
        Spends given points from the useraccount

        :param points: points to spend
        :type points: int
        :raises InSufficientPoints: raised when the given total points avaiable are less than the given points
        :return: dictionary of spending summary, where key is payer and value is points spent (in negative, because its spending)
        :rtype: Dict[str, int]
        """
        if self.total_points() < points:
            raise InSufficientPoints(f"There are no enough points to spend {points} points")

        history = []
        while points and self._transactions:
            oldest = self._get_next_transaction_to_spend()
            if oldest.points == 0:
                continue
            spent = min(points, oldest.points)
            points -= spent
            history.append(PayerRecord(oldest.payer, -spent))
            oldest.points -= spent
            # if there are any remaining points in the oldest transaction, add them back
            if oldest.points > 0:
                self.__add_transaction(oldest)
        return self._spend_summary(history)


