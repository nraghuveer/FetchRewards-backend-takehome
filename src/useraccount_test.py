import unittest
from datetime import datetime, timedelta
from useraccount import UserAccount, TransactionRecord, InSufficientPoints

class TestUserAccount(unittest.TestCase):
    def test_standard_example(self):
        useracc = UserAccount()
        now = datetime.now()
        records = [
            TransactionRecord(payer="DANNON", points=300, timestamp=now - timedelta(0, 5*60)),
            TransactionRecord(payer="UNILEVER", points=200, timestamp=now - timedelta(0, 4*60)),
            TransactionRecord(payer="DANNON", points=-200, timestamp=now - timedelta(0)),
            TransactionRecord(payer="MILLER COORS", points=10000, timestamp=now + timedelta(1)),
            TransactionRecord(payer="DANNON", points=1000, timestamp=now + timedelta(2)),
        ]
        useracc.add(records)
        balance = useracc.balance()
        self.assertEquals(balance, {"DANNON": 1100, "UNILEVER": 200, "MILLER COORS": 10000})
        assert useracc.total_points() == 11300
        spend_summary = useracc.spend(5000)
        self.assertEquals(spend_summary, {"DANNON": -100, "UNILEVER": -200, "MILLER COORS": -4700})
        assert useracc.total_points() == 11300 - 5000
        balance = useracc.balance()
        self.assertEquals(balance, {"DANNON": 1000, "MILLER COORS": 5300})

    def test_overspending(self):
        useracc = UserAccount()
        now = datetime.now()
        records = [
            TransactionRecord(payer="DANNON", points=200, timestamp=now - timedelta(0, 5*60)),
            TransactionRecord(payer="UNILEVER", points=200, timestamp=now - timedelta(0, 4*60)),
            TransactionRecord(payer="DANNON", points=-200, timestamp=now - timedelta(0)),
            TransactionRecord(payer="MILLER", points=100, timestamp=now + timedelta(1)),
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

    def test_more_negative_in_add(self):
        useracc = UserAccount()
        now = datetime.now()
        records = [
            TransactionRecord(payer="DANNON", points=200, timestamp=now - timedelta(0, 5*60)),
            TransactionRecord(payer="UNILEVER", points=200, timestamp=now - timedelta(0, 4*60)),
            TransactionRecord(payer="DANNON", points=-200, timestamp=now - timedelta(0)),
            TransactionRecord(payer="DANNON", points=-100, timestamp=now - timedelta(0)),
        ]
        self.assertRaises(InSufficientPoints, useracc.add, records)

    def test_spend_oldest(self):
        useracc = UserAccount()
        now = datetime.now()
        records = [
            TransactionRecord(payer="X", points=200, timestamp=now - timedelta(0, 5*60)), # now - 5 minutes
            TransactionRecord(payer="Y", points=200, timestamp=now - timedelta(0, 4*60)), # now - 4 minutes
            TransactionRecord(payer="X", points=-200, timestamp=now), # now
            TransactionRecord(payer="Z", points=300, timestamp=now - timedelta(1)), # yesterday same time
        ]
        useracc.add(records)
        spend_summary = useracc.spend(301)
        self.assertEqual(spend_summary, {"Z": -300, "Y": -1})
        balance = useracc.balance()
        self.assertEqual(balance, {"Y": 199})

if __name__ == "__main__":
    unittest.main()




