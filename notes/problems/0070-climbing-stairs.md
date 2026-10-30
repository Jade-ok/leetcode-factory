My starting point is to make the two-step case explicit: one stair has one way, and two stairs have two ways, `[1, 1]` and `[2]`. These base cases make more sense to me than starting with zero stairs.

This is the recursive code I want to keep from my submission. The recurrence is correct, but the repeated work makes this version too slow for large inputs in the problem's range. It is my starting solution, not the optimized one.

```python
class Solution:
    def climbStairs(self, n: int) -> int:
        if n == 1:
            return 1
        if n == 2:
            return 2

        return self.climbStairs(n-1) + self.climbStairs(n-2)
```

## What the function actually returns

`climbStairs(k)` returns the **number of distinct ways to reach stair k**. It does not return the number of stairs, move a person up the staircase, or build a list of paths.

To reach stair `k`, the final move must be one of two things:

- A one-step move from stair `k - 1`.
- A two-step move from stair `k - 2`.

Every way of reaching `k - 1` can be extended with one final step. Every way of reaching `k - 2` can be extended with one final two-step move. These groups cover all possibilities and cannot overlap because their final moves differ.

That gives the recurrence:

```text
ways(k) = ways(k - 1) + ways(k - 2)
ways(1) = 1
ways(2) = 2
```

For three stairs, the split is concrete:

```text
Reach stair 2, then add 1:
[1, 1] -> [1, 1, 1]
[2]    -> [2, 1]

Reach stair 1, then add 2:
[1]    -> [1, 2]

2 ways + 1 way = 3 ways
```

`[2, 1]` and `[1, 2]` are different sequences. Order matters.

## How Python executes the recursion

Python evaluates the left operand of `+` before the right one. A caller waits for both returned values before it can add them and return its own answer. Each call has its own local `n`; calling the method with `n - 1` does not change the caller's `n`.

For `n = 4`, this is the complete call tree for my two-base-case version:

```text
climbStairs(4) = 5
|-- climbStairs(3) = 3
|   |-- climbStairs(2) = 2   [base case]
|   `-- climbStairs(1) = 1   [base case]
`-- climbStairs(2) = 2       [base case, called again]
```

The execution order is:

1. `climbStairs(4)` calls `climbStairs(3)` and waits.
2. `climbStairs(3)` calls `climbStairs(2)`. That call returns `2` immediately.
3. Back in `climbStairs(3)`, Python next calls `climbStairs(1)`, which returns `1`.
4. `climbStairs(3)` adds `2 + 1` and returns `3` to the call for `4`.
5. The call for `4` still needs its right-hand value. It calls `climbStairs(2)` again and gets `2`.
6. It adds `3 + 2` and returns `5`.

A base case stops **that call**, not the entire program. Execution resumes in the caller after the returned value is available. `self` is the same solution object throughout; the separate call frames hold the different values of `n`.

At `n = 5`, the repeated work is easier to see:

```text
ways(5)
|-- ways(4)
|   |-- ways(3)
|   |   |-- ways(2)
|   |   `-- ways(1)
|   `-- ways(2)
`-- ways(3)                 <- this whole subproblem is repeated
    |-- ways(2)
    `-- ways(1)
```

Returning a value does not automatically cache it. The second call to `ways(3)` repeats the same computation.

## Why the zero-stair version also works

The alternative base cases `ways(0) = 1` and `ways(1) = 1` use a counting convention: there is one empty sequence of moves that reaches the starting position. For two stairs, that empty prefix followed by a two-step move accounts for `[2]`.

```text
ways(2) = ways(1) + ways(0) = 1 + 1 = 2
```

Zero is a helper state here; the problem's actual input starts at `n = 1`. Both definitions produce the same answers on valid inputs. I prefer explicitly naming the two possibilities at `n = 2`.

## Time and space complexity of my recursive version

For the running time:

```text
T(n) = T(n - 1) + T(n - 2) + O(1)
```

- **Time: O(2^n)** is the usual interview upper bound. More tightly, the number of calls is **Theta(phi^n)**, where `phi = (1 + sqrt(5)) / 2`.
- **Auxiliary space: O(n)** for the deepest chain of active recursive calls.

The total number of calls and the maximum number of simultaneous calls are different. The execution explores the tree depth first; it does not keep every node in memory at once. The longest chain decreases `n` by one until it reaches a base case.

For these exact base cases, the call count is `2 * Fib(n) - 1`, with `Fib(1) = Fib(2) = 1`. At `n = 44`, that is 1,402,817,465 calls. This explains the time limit issue without running that enormous recursion.

## Keep the recursion, remove repeated work

Memoization preserves the recurrence and the base cases. All recursive calls must share the same memo dictionary. A helper makes that sharing explicit.

```python
class Solution:
    def climbStairs(self, n: int) -> int:
        memo = {1: 1, 2: 2}

        def ways(k: int) -> int:
            if k not in memo:
                memo[k] = ways(k - 1) + ways(k - 2)
            return memo[k]

        return ways(n)
```

Each distinct state is expanded at most once. Reaching a previously computed state becomes a dictionary lookup. The dictionary belongs to the outer method call, so it is not recreated on every helper call.

**Time: O(n). Auxiliary space: O(n)** for the memo and O(n) for the call stack, which is O(n) overall.

## Compute the same states from the bottom up

There is no need to wait for recursive calls if the smaller answers are already available. An array makes the computation order visible:

```python
class Solution:
    def climbStairs(self, n: int) -> int:
        if n == 1:
            return 1
        if n == 2:
            return 2

        dp = [0] * (n + 1)
        dp[1], dp[2] = 1, 2

        for stair in range(3, n + 1):
            dp[stair] = dp[stair - 1] + dp[stair - 2]

        return dp[n]
```

**Time: O(n). Auxiliary space: O(n)** for the array. This version has no recursive call stack.

Only the previous two values are needed, so the array can be reduced to two variables. This is the iterative version from our discussion:

```python
class Solution:
    def climbStairs(self, n: int) -> int:
        one, two = 1, 1

        for i in range(n-1):
            temp = one
            one = one + two
            two = temp

        return one
```

Initially, `one` represents `ways(1)` and `two` represents the helper state `ways(0)`. After each iteration, `one` advances to the next stair's answer and `two` keeps the previous answer.

```text
n = 5
                         one                 two
Before the loop          1 = ways(1)         1 = ways(0)
After iteration 1        2 = ways(2)         1 = ways(1)
After iteration 2        3 = ways(3)         2 = ways(2)
After iteration 3        5 = ways(4)         3 = ways(3)
After iteration 4        8 = ways(5)         5 = ways(4)
```

`temp` preserves the old `one` before it is overwritten. Without it, assigning `two = one` after updating `one` would make both variables hold the new value.

The loop performs `n - 1` iterations. At `n = 44`, it runs 43 times rather than making over a billion calls. **Time: O(n). Auxiliary space: O(1)** in the usual interview model where arithmetic on these bounded values is constant time.

I can also keep my preferred `1, 2` base cases in the constant-space version:

```python
class Solution:
    def climbStairs(self, n: int) -> int:
        if n <= 2:
            return n

        previous, current = 1, 2
        for stair in range(3, n + 1):
            previous, current = current, previous + current
        return current
```

Python evaluates the right-hand values before assigning either variable, so the simultaneous assignment keeps the old pair available.

Fast doubling or matrix exponentiation can compute `Fib(n + 1)` in O(log n) arithmetic steps. That is a further optimization for much larger `n`; for this problem's bound of 45, the O(n)-time, O(1)-auxiliary-space loop is the straightforward interview choice. A floating-point Fibonacci formula would introduce an avoidable rounding issue.

## How I would explain this in an interview

> I want to define what a smaller subproblem means first. Let ways(k) be the number of ways to reach stair k. The last move into stair k is either one step from k minus one, or two steps from k minus two. Those cases are exhaustive and disjoint, so I add their counts. My base cases are one way for one stair and two ways for two stairs. Direct recursion expresses this correctly, but it repeats the same states, giving exponential time and linear stack space. I can cache each state to get linear time. Since each state only needs the previous two answers, I would finish with an iterative solution using linear time and constant auxiliary space.

I should explain the state and why the cases can be added before walking through syntax. If asked how the recursion runs, I can trace `n = 4`, showing exactly where each caller waits and resumes. If asked to optimize, I can point to the repeated `ways(3)` subtree at `n = 5` rather than only naming dynamic programming.

Checks I would say out loud:

- `n = 1` returns `1`; `n = 2` returns `2`.
- `n = 3` returns `3`, covering both orders of a one-step and two-step move.
- `n = 4` returns `5`; `n = 5` returns `8`.
- The optimized version handles `n = 45` and returns `1836311903`.

References: [study conversation](https://chatgpt.com/share/6ae3ffab-4b10-83e8-bcda-53e1faf76729) and [LeetCode problem and constraints](https://leetcode.com/problems/climbing-stairs/). The first code block is the recursive version from my screenshot; the memoized and iterative variants are comparisons and improvements.
