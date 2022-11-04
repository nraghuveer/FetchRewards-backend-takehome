# Background

* Users have points in their accounts
* Users only see a single balance in their accounts.
* But for reporting purposes, we actually track their points per payer/partner
* Transaction Record scheme
    1. payer: string
    2. points: integer
    3. timestamp: date

* For earning points ( points earned?) -> actions through which points are earned determines the payer
* when a user spends points, they doesn't know or care which payer the cpoints come from
    * but this information (where payer from which the points came from) is needed by accounting team

There are two rules for determining what points to "spend" first
1. Oldest points (based on transaction timestamp)
2. no payers points to go negative

# Routes
1. Add transactions for a specific payer and date
2. Spend points using the rules above and return a list of {payer: string, points: integer}
* return all payer point balances