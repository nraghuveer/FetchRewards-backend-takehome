import unittest
from datetime import datetime, timedelta
from useraccount import UserAccount, TransactionRecord, InSufficientPoints

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

    def test_overspending(self):
        useracc = UserAccount()
        now = datetime.now()
        records = [
            TransactionRecord("DANNON", 200, now - timedelta(0, 5*60)),
            TransactionRecord("UNILEVER", 200, now - timedelta(0, 4*60)),
            TransactionRecord("DANNON", -200, now - timedelta(0)),
            TransactionRecord("MILLER", 100, now + timedelta(1)),
        ]
        useracc.add(records)
        assert useracc.total_points() == 300
        balance = useracc.balance()
        self.assertEqual(balance["MILLER"], 100)
        self.assertEqual(balance["DANNON"], 0)
        self.assertEqual(balance["UNILEVER"], 200)
        self.assertRaises(InSufficientPoints, useracc.spend, 301)
        # if the spend fails, the balanances should remain the same
        balance = useracc.balance()
        self.assertEqual(balance["MILLER"], 100)
        self.assertEqual(balance["DANNON"], 0)
        self.assertEqual(balance["UNILEVER"], 200)

    def test_deficient_before_first_spend(self):
        useracc = UserAccount()
        now = datetime.now()
        records = [
            TransactionRecord("DANNON", 200, now - timedelta(0, 5*60)),
            TransactionRecord("UNILEVER", 200, now - timedelta(0, 4*60)),
            TransactionRecord("DANNON", -200, now - timedelta(0)),
            TransactionRecord("MILLER", -300, now + timedelta(1)),
        ]
        useracc.add(records)
        self.assertEqual(useracc.total_points(), -100)
        self.assertRaises(InSufficientPoints, useracc.spend, 3)
        # add 102 points to account
        useracc.add([TransactionRecord("DANNON", 102, now + timedelta(1))])
        # now total points should be 2, since we had -100 previous
        self.assertEqual(useracc.total_points(), 2)
        # we should not be able to spend 3 now
        self.assertRaises(InSufficientPoints, useracc.spend, 3)
        # add a transaction with 10 points, but this is less than DANNON-102 by a day
        useracc.add([TransactionRecord("MILLER", 10, now + timedelta(2))])
        spend_summary = useracc.spend(3)
        balance = useracc.balance()
        self.assertEqual(balance, {"MILLER", 9})
        self.assertEqual(useracc.total_points(), 9)
        self.assertEqual(spend_summary, {"DANNON": 2, "MILLER": 1})







if __name__ == "__main__":
    unittest.main()




