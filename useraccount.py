from collections import defaultdict
from heapq import heappush, heappop
from datetime import datetime
from typing import Dict, List, TypedDict
from dataclasses import dataclass

class InSufficientPoints(Exception):
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
        self._transactions: List[TransactionRecord] = []
        self._earning_points: Dict[str, int] = defaultdict(int)

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
        else:
            self._earning_points[transac.payer] += -1 * transac.points

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
        # if there are any earning points to consider for this payer
        if oldest.payer in self._earning_points and self._earning_points[oldest.payer] > 0:
            # e = 100, oldest.points = 10 => get next, change e
            # e = 10, oldest.points = 100 => set e =0 and return modified oldest
            removed = min(self._earning_points[oldest.payer], oldest.points)
            oldest.points -= removed
            self._earning_points[oldest.payer] -= removed
        return oldest

    def add(self, new_transactions: List[TransactionRecord]) -> None:
        """
        Adds the given transactions into the user account

        :param new_transactions: list of new transactions, can include both normal and earned point transactions
        :type new_transactions: List[TransactionRecord]
        :return: None
        :rtype: None
        """
        for transac in new_transactions:
            self.__add_transaction(transac)

    def balance(self) -> Dict[str, int]:
        """Returns balance of the useraccount

        :return: balance dictionary where payer is key and avaialble points as value
        :rtype: Dict[str, int]
        """
        d: Dict[str, int] = defaultdict(int)
        for transac in self._transactions:
            d[transac.payer] += transac.points
        for payer, points in self._earning_points.items():
            d[payer] -= points
        return d

    def total_points(self) -> int:
        return sum(self.balance().values())

    def spend(self, points: int) -> List[PayerRecord]:
        """
        Spends given points from the useraccount

        :param points: points to spend
        :type points: int
        :raises InSufficientPoints: raised when the given total points avaiable are less than the given points
        :return: list of records which were used to spend the given points
        :rtype: List[PayerRecord]
        """

        if self.total_points() < points:
            raise InSufficientPoints(f"There are no enough points to spend {points} points")

        history = []
        while points and self._transactions:
            oldest = self._get_next_transaction_to_spend()
            if oldest.points == 0:
                continue
            # points = 100, oldest.points=80
            # points=80, odlest.points=100
            spent = min(points, oldest.points)
            points -= spent
            history.append(PayerRecord(oldest.payer, -spent))
            oldest.points -= spent
            if oldest.points > 0:
                self.__add_transaction(oldest)
        return history


