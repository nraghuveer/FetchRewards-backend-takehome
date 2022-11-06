# How the transactions are stored?
So the use-case here is to add/store the list transactions, and spend them as per the given rules.

Rules are following
* oldest should be spent first and we cannnot spend beyond the available
* there should be no overspending

Since we want to first spend the oldest its better to use a datastructure which it is easy for us get the oldest record to spend in constant time.
The most typical one for this kind of use-case is min-heap, which gives us min element in constant time
The other approach is to use a sorted list.

Below are pros and cons for min heap and sorted list

## MinHeap
1. Constant pop of min-heap, so if the heap key is timestamp, we can get oldest transaction in constant time.
2. For the balance, we need to aggregate all the records in the min-heap. which is O(n)
3. For spend, each pop from heap takes O(log n) and in worst case, we do it for n times. So O(n.log n)
3. So add takes O(log n) for each transaction, balance take O(n) and spend takes takes O(n.log n)

## Sorted List
1. For spend, selecting the oldest record takes constant time each time
2. For balance, we need to aggregate all the records, which is O(n)
3. Addition of new transactions takes O(n.log n) => append to end and sort again
4. We can speed up addition using binary search insertion technique, which bring each addition to O(log n) time (same as min-heap)
5. Python, internally uses a list to implement a min-heap (uses list to repesent binary search tree)

Both the approaches have a bottle-neck, the spend takes linear time.
To overcome this, we need some kind of abstract datastructure.
One such abstract datastructure is "MinHeap + Dictionary"
