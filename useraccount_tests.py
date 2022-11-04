import unittest
from datetime import datetime, timedelta
from useraccount import UserAccount, TransactionRecord

class TestUserAccount(unittest.TestCase):
    def test_standard_example(self):
        useracc = UserAccount()
        now = datetime.now()
        records = [
            TransactionRecord("DANNON", 300, now - timedelta(0, 5*60)),
            TransactionRecord("UNILEVER", 200, now - timedelta(0, 4*60)),
            TransactionRecord("DANNON", -200, now - timedelta(0)),
            TransactionRecord("MILLER COORS", 10000, now + timedelta(1)),
            TransactionRecord("DANNON", 1000, now + timedelta(2)),
        ]
        useracc.add(records)
        balance = useracc.balance()
        assert balance["DANNON"] == 1100
        assert balance["UNILEVER"] == 200
        assert balance["MILLER COORS"] == 10000
        assert useracc.total_points() == 11300
        spend_summary = useracc.spend(5000)
        spend_summary = {r.payer: r.points for r in spend_summary}
        assert spend_summary["DANNON"] == -100
        assert spend_summary["UNILEVER"] == -200
        assert spend_summary["MILLER COORS"] == -4700
        assert useracc.total_points() == 11300 - 5000
        balance = useracc.balance()
        assert balance["DANNON"] == 1000
        assert balance["UNILEVER"] == 0
        assert balance["MILLER COORS"] == 5300

if __name__ == "__main__":
    unittest.main()






