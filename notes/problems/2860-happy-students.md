## Key idea

Try every group size `s` from `0` to `n`. Student `i` is happy only if:

- selected and `s > nums[i]`, or
- not selected and `s < nums[i]`.

If `nums[i] == s`, that student can't be happy, so the size `s` fails. Otherwise each student's choice is forced: `nums[i] < s` must be selected. So `s` works when exactly `s` students have `nums[i] < s`.

```text
[1, 2, 3], s = 2
i = 0   2 > 1    -> must be selected
i = 1   2 == 2   -> invalid either way, s = 2 fails
i = 2   2 < 3    -> must not be selected
```

## Brute force: O(n^2)

```python
class Solution:
    def countWays(self, nums: List[int]) -> int:
        ans = 0
        for s in range(len(nums) + 1):
            valid = True
            cnt = 0
            for i in range(len(nums)):
                if nums[i] == s:
                    valid = False
                elif nums[i] < s:
                    cnt += 1
            if valid and cnt == s:
                ans += 1
        return ans
```

## Optimized: sort, O(n log n)

After sorting, the selected group of size `s` has to be the `s` smallest values. So size `s` works when:

```text
nums[s-1] < s < nums[s]
```

- `s = 0`: nobody is selected, so the smallest value must be `> 0`.
- `s = n`: everyone is selected. This always works because `nums[i] < n`.

```python
class Solution:
    def countWays(self, nums: List[int]) -> int:
        nums.sort()
        ans = 0
        n = len(nums)

        for s in range(n + 1):
            if s == 0:
                if nums[0] > 0:
                    ans += 1
            elif s == n:
                ans += 1
            elif nums[s-1] < s and nums[s] > s:
                ans += 1

        return ans
```

**Time: O(n log n)** for the sort. **Space: O(1)** extra, not counting the sort.

## Remember

- Fix the group size first, and each student's choice is forced.
- Sorting means "selected" = a prefix of the sorted array.
