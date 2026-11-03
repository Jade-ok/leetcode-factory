## Key idea

First count each number with a dictionary. Then the problem becomes "pick the `k` keys with the largest counts". The only difference between solutions is how you pick them.

## Brute force: sort by count, O(n log n)

```python
class Solution:
    def topKFrequent(self, nums: list[int], k: int) -> list[int]:
        dic = {}
        for n in nums:
            dic[n] = dic.get(n, 0) + 1

        sorted_list = sorted(dic, key=dic.get, reverse=True)
        return sorted_list[:k]
```

`sorted(dic, key=dic.get)` sorts the keys by their counts.

**Time: O(n log n)**, from sorting up to `n` unique keys. **Space: O(n).**

## Heap of size k: O(n log k)

Keep a **min-heap** of `(frequency, num)` holding at most `k` items. When it grows past `k`, pop the smallest count. What's left is the `k` most frequent.

```python
import heapq

class Solution:
    def topKFrequent(self, nums: list[int], k: int) -> list[int]:
        dic = {}
        heap = []

        for n in nums:
            dic[n] = dic.get(n, 0) + 1

        for num, frequency in dic.items():
            heapq.heappush(heap, (frequency, num))
            if len(heap) > k:
                heapq.heappop(heap)

        return [i[1] for i in heap]
```

- Put `frequency` first in the tuple, because the heap compares the first item.
- It's a min-heap, so the top is always the weakest candidate. That makes it the one to throw out.

**Time: O(n log k).** Each push and pop costs `log k`. **Space: O(n)** for the dictionary, O(k) for the heap.

## Next: bucket sort

To try: get it down to O(n) without sorting.

## Remember

- Count with a dictionary first, then choose the top `k`.
- Use a min-heap of size `k` when you want the top `k` items.
