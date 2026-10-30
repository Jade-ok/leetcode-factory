For every node, its left and right subtrees need to exchange places. Swapping only the root's children is not enough: each subtree must also be inverted.

The shared discussion mentions this problem but does not include my submitted code. The implementation below is a reference for reviewing the recursion, not a copy of my submission.

```python
class Solution:
    def invertTree(self, root):
        if root is None:
            return None

        inverted_left = self.invertTree(root.left)
        inverted_right = self.invertTree(root.right)
        root.left, root.right = inverted_right, inverted_left
        return root
```

## What one call promises

`invertTree(root)` returns the root of the inverted subtree that originally started at `root`.

The base case is an empty subtree. It is already inverted, so the function returns `None`. For a nonempty subtree, I can first obtain the inverted children, connect them on opposite sides, and return the current root.

This implementation changes the existing nodes. `return root` returns a reference to the same root object, whose children may now be different. It does not create a new root or return the root's value.

## Follow the returned subtree roots

Consider this tree:

```text
        4
      /   \
     2     7
    / \   / \
   1   3 6   9
```

The call for `4` waits while the call for `2` runs. The call for `2` first processes `1` and `3`. Each leaf calls the function on its two empty children, receives `None` twice, and returns itself.

Once the two child calls for `2` have returned, it reconnects `3` on the left and `1` on the right. It returns the root object `2` to the waiting call for `4`.

The same process turns the subtree at `7` into a subtree with children `9` and `6`. Finally, `4` receives both inverted subtree roots and connects them on opposite sides:

```text
        4
      /   \
     7     2
    / \   / \
   9   6 3   1
```

The two local names `inverted_left` and `inverted_right` make the return values explicit. They also prevent confusion about which child a later call is using while links are being changed.

## Why this is correct

An empty subtree is unchanged. Assume both child calls return correctly inverted subtrees. Placing the inverted right subtree on the left and the inverted left subtree on the right then makes the entire current subtree its mirror. This argument applies from the leaves back up to the root.

The function must return the current root after the reconnection. Returning only one child would discard part of the tree from the result.

## Time and space complexity

Let `N` be the number of nodes and `h` the maximum number of nodes along a root-to-leaf path.

- **Time: O(N)**. Every nonempty node is processed once and performs constant work beyond its child calls. The empty-child calls are also linear in number.
- **Auxiliary space: O(h)** for the active recursion stack. This is O(log N) for a balanced tree and O(N) for a chain.
- The nodes are reused, but that does not make the auxiliary space O(1). The stack still uses memory.

There are two recursive calls at each nonempty node, but their subtrees are disjoint. This is different from Climbing Stairs, where the same smaller state is recomputed through different branches. Memoization would add storage without removing repeated subtree work here.

## An iterative alternative

An explicit stack avoids recursive calls. Swap a node's children, then arrange to process both children as well.

```python
class Solution:
    def invertTree(self, root):
        if root is None:
            return None

        stack = [root]
        while stack:
            node = stack.pop()
            node.left, node.right = node.right, node.left
            if node.left is not None:
                stack.append(node.left)
            if node.right is not None:
                stack.append(node.right)
        return root
```

This still takes O(N) time. The explicit DFS stack uses O(h) space as an upper bound, which can be O(N) over all tree shapes. Its size does not have to equal the recursive stack size for every particular tree.

A BFS implementation instead stores a queue and uses O(w) space, where `w` is the maximum tree width. A wide tree can make that queue much larger than a balanced tree's recursive stack. Changing traversal order is not automatically a memory optimization.

## How I would explain it in an interview

> I define the recursive function to return the root of an inverted subtree. An empty subtree returns None. For a real node, I invert both child subtrees, attach them on opposite sides, and return the current node. If the two recursive results are correct, this reconnection makes the current subtree correct too. Every node is processed once, so the time is linear. The extra space is the recursion depth: logarithmic for a balanced tree and linear for a skewed one. I can use an explicit stack if I want to avoid recursive calls, while keeping the same traversal work.

I would check an empty tree, a single node, a node with only one child, and an asymmetric tree. Inverting twice should restore the original structure and keep the same node objects.

References: [problem definition and examples](https://leetcode.com/problems/invert-binary-tree/) and [the study conversation that mentions this problem](https://chatgpt.com/share/6ae3ffab-4b10-83e8-bcda-53e1faf76729).
