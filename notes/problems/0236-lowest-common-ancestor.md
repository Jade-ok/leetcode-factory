The lowest common ancestor is the deepest node whose subtree contains both targets. A target can be its own ancestor, so if `p` is above `q`, the answer can be `p` itself.

This is a general binary tree, not a binary search tree. I cannot choose a child by comparing node values.

The shared discussion mentions this problem but does not include my submitted code. This is a reference implementation for explaining the return values and comparing approaches.

```python
class Solution:
    def lowestCommonAncestor(self, root, p, q):
        if root is None or root is p or root is q:
            return root

        left = self.lowestCommonAncestor(root.left, p, q)
        right = self.lowestCommonAncestor(root.right, p, q)

        if left is not None and right is not None:
            return root
        return left if left is not None else right
```

## What a returned node means

The return value is a signal about the subtree, not always the final answer for the entire tree.

- `None`: neither target is in this subtree.
- A target node: that target was found; it may also be the answer if the other target is below it.
- Another node: both targets have been found, and this node is their lowest common ancestor within the subtree.

Each caller uses the signals from its two children. If both are nonempty, the targets lie on opposite sides of the current node, so the current node is the answer. If only one is nonempty, the caller passes that node upward unchanged.

The comparisons use `is` because the inputs are node objects. Returning `root.val` would return the wrong kind of result.

## Trace the split

Use this tree:

```text
          3
        /   \
       5     1
      / \   / \
     6   2 0   8
        / \
       7   4
```

For `p = node 7` and `q = node 4`:

1. The call at `7` returns the target node `7`; the call at `4` returns `4`.
2. The call at `2` receives a nonempty result from each side. It returns node `2`.
3. The call at `5` gets `None` from the subtree at `6` and node `2` from its right subtree. It passes node `2` upward.
4. The call at `3` gets node `2` from the left and `None` from the right subtree. It returns node `2`.

The ancestors do not replace an already found answer just because they are also common ancestors. Passing the nonempty child result upward preserves the lowest one.

Python evaluates the left recursive call before the right one. Each parent waits for the two results before choosing what to return.

## Why returning a target immediately is valid

For `p = node 5` and `q = node 4`, the call at `5` returns `5` immediately. It does not need to recurse below `5` to find `4` in this implementation.

If the other target is below this target, the target itself is already the lowest possible common ancestor. If the other target is elsewhere, the returned target becomes a signal for a higher caller to combine with the other side.

This reasoning relies on the problem's guarantee that **both distinct target nodes exist in the tree**. If one target could be absent, the same implementation could return the other target even though no valid two-target answer exists. That version of the problem needs additional presence tracking.

## Time and space complexity

Let `N` be the number of nodes and `h` the tree height measured in nodes along the deepest path.

- **Worst-case time: O(N)**. A node is visited at most once. Early target returns may skip some subtrees, but the worst case still examines the tree.
- **Auxiliary space: O(h)** for recursion. A balanced tree gives O(log N) stack depth; a skewed tree can require O(N).

Caching does not improve this single-query traversal: it is not recomputing the same subtree through multiple paths.

Python's recursion limit matters for a sufficiently deep tree. The problem permits up to 100,000 nodes, so the recursive version can fail with a recursion-depth error on a long chain even though its recurrence is correct. An iterative implementation handles that case without relying on a deeper Python call stack.

## Iteration with parent references

Build parent references until both targets have been discovered. Then collect the ancestors of `p` and climb upward from `q`. The first node on `q`'s upward path that belongs to that set is the lowest shared ancestor.

```python
class Solution:
    def lowestCommonAncestor(self, root, p, q):
        if root is None:
            return None

        parent = {root: None}
        stack = [root]
        while p not in parent or q not in parent:
            node = stack.pop()
            if node.left is not None:
                parent[node.left] = node
                stack.append(node.left)
            if node.right is not None:
                parent[node.right] = node
                stack.append(node.right)

        ancestors = set()
        node = p
        while node is not None:
            ancestors.add(node)
            node = parent[node]

        node = q
        while node not in ancestors:
            node = parent[node]
        return node
```

This uses the same guarantee that both targets exist. **Time is O(N), auxiliary space is O(N)** for the parent references, traversal stack, and ancestor set. It removes the recursion-depth issue, at the cost of storing parent information even when the tree is balanced. It is not a faster asymptotic algorithm for a single query.

For many LCA queries on the same fixed tree, preprocessing depths and binary-lifting ancestors is a different tradeoff: O(N log N) preprocessing time and storage, then O(log N) per query. That extra structure is unnecessary for one query.

## How I would explain it in an interview

> First I would confirm that both targets exist and that this is a general binary tree. Each recursive call returns a useful node from its subtree, or None if it finds neither target. If a node is one of the targets, I return it. Otherwise I collect the two child results. Two nonempty results mean the targets split across this node, so it is their lowest common ancestor. With only one result, I pass it upward. This visits each node at most once, giving linear worst-case time and O(h) stack space. For a deeply skewed tree in Python, I would use an iterative parent-reference approach to avoid the recursion limit, with O(N) extra storage.

Checks I would explain:

- Targets in opposite root subtrees: `5` and `1` return root `3`.
- One target is the ancestor of the other: `5` and `4` return `5`.
- Targets split deeper down: `7` and `4` return `2`, not `3`.
- Targets in a long chain: use the iterative version when recursion depth is too large.
- Return the actual node object, not its value.

References: [problem definition, examples, and target-presence guarantee](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/) and [the study conversation that mentions this problem](https://chatgpt.com/share/6ae3ffab-4b10-83e8-bcda-53e1faf76729).
