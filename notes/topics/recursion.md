A recursive function solves one state by calling itself on smaller states. Before writing the calls, I need a precise sentence describing what one call returns or changes.

For `ways(k)`, the result is a count. For a subtree function, the result might be the root of a transformed subtree or a node found inside that subtree. Returning from a call resumes its caller; it does not stop the entire traversal.

## State, base case, progress, combination

- Define the input state and the meaning of the return value.
- State what happens when the input is small enough to answer directly.
- Make every recursive dependency move toward a base case.
- Explain how returned values produce the answer for the current state.

This is the shape, not a requirement to use the same code for every problem:

```python
def solve(state):
    if is_base_case(state):
        return base_result(state)

    smaller_result = solve(smaller_state(state))
    return combine(state, smaller_result)
```

`is_base_case`, `smaller_state`, and `combine` are placeholders. Their meanings must come from the problem. Some functions make several calls; some recurse for side effects and return nothing.

## Calls and returned values are separate ideas

Each call has its own frame and local variables. The caller keeps waiting while a child call runs. After that child returns, the caller continues from where it stopped.

In Python, for `solve(a) + solve(b)`, the left call finishes before the right call starts. The addition happens only after both values are available.

The objects referenced by frames can still be shared. A shared tree, dictionary, list, or visited set can be changed by several calls even though their local variables belong to different frames.

## A call tree is not the call stack

A call tree shows all calls made throughout execution. The stack contains only the currently active chain of calls.

Count the total work across calls for time complexity. Measure the maximum number of simultaneous frames for stack space. These can grow at very different rates.

- A recurrence such as `ways(n - 1) + ways(n - 2)` repeats overlapping states. Without caching, time is exponential but stack depth is O(n).
- A tree traversal that visits each node once takes O(N) time, even if each node makes two recursive calls. Stack space is O(h), where h is the tree height; a skewed tree can have h = N.
- Graph traversal needs cycle prevention. Marking each vertex before exploring its neighbors lets an adjacency-list DFS run in O(V + E) time.

Two recursive calls do not, by themselves, prove O(2^n) time. I need to identify the states, how much they overlap, and how many times they are processed.

## Memoization and iteration

Memoization helps when different paths ask for the answer to the same state. Define a key that captures the entire state and share the cache between calls.

For Climbing Stairs, the state is just the remaining stair count. There are O(n) distinct states. Caching gives O(n) time and O(n) auxiliary space including the stack.

If dependencies have a simple evaluation order, bottom-up iteration can remove the recursion. If only a few earlier answers remain necessary, I can then reduce the stored state. Climbing Stairs only needs two previous answers.

## Interview phrasing

> For this call, the state is ___. The function returns ___. The base case is ___ because ___. Each recursive call makes progress by ___. Once those calls return, I combine their results by ___. To analyze the cost, I count ___ distinct states or nodes and ___ work per state. The deepest active chain is ___, so the auxiliary stack space is ___.

I should fill these blanks with the current problem, not recite them without explaining the reasoning.
