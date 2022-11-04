from datetime import datetime
from typing import Dict, List, TypedDict

class PayerRecord(TypedDict):
    payer: str
    points: int

class TransactionRecord(PayerRecord):
    ts: datetime

class UserAccount:
    """
    Abstract DataStructure to add transactions, spend points, and get balance points on a user
    """
    def __init__(self) -> None:
        pass

    def add(self, transactions: List[TransactionRecord]) -> List[PayerRecord]:
        return []

    def balance(self) -> Dict[str, int]:
        return {}

    def spend(self, points: int) -> List[PayerRecord]:
        return []
