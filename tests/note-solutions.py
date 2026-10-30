import re
from pathlib import Path

root = Path(__file__).resolve().parents[1]
body = (root / 'notes/problems/0070-climbing-stairs.md').read_text()
blocks = re.findall(r'^```python\n([\s\S]*?)^```', body, re.M)
assert len(blocks) == 5
expected = {1: 1, 2: 2, 3: 3, 4: 5, 5: 8, 10: 89, 45: 1836311903}
a, b = 1, 2
answers = {1: a, 2: b}
for n in range(3, 46):
    a, b = b, a + b
    answers[n] = b

for index, code in enumerate(blocks):
    namespace = {}
    exec(compile(code, f'climbing-stairs-variant-{index + 1}', 'exec'), namespace)
    cls = namespace['Solution']
    limit = 20 if index == 0 else 45
    for n in range(1, limit + 1):
        assert cls().climbStairs(n) == answers[n], (index, n)
    for n, answer in expected.items():
        if n <= limit:
            assert cls().climbStairs(n) == answer
    if index == 0:
        original = cls.climbStairs
        calls = depth = max_depth = 0
        def counted(self, n):
            global calls, depth, max_depth
            calls += 1
            depth += 1
            max_depth = max(max_depth, depth)
            try:
                return original(self, n)
            finally:
                depth -= 1
        cls.climbStairs = counted
        assert cls().climbStairs(5) == 8
        assert calls == 9 and max_depth == 4, (calls, max_depth)

# Call counts are calculated, not produced by executing the expensive input.
fib_a, fib_b = 0, 1
for _ in range(44):
    fib_a, fib_b = fib_b, fib_a + fib_b
assert 2 * fib_a - 1 == 1402817465
print('PASS: all five Climbing Stairs implementations; valid-domain boundaries; exact recursion call count and stack depth.')

from collections import deque
from random import Random

class Node:
    def __init__(self, val, left=None, right=None):
        self.val, self.left, self.right = val, left, right

def make_tree(values):
    if not values or values[0] is None:
        return None, {}
    root = Node(values[0])
    nodes, queue = {root.val: root}, deque([root])
    index = 1
    while queue and index < len(values):
        node = queue.popleft()
        for attribute in ['left', 'right']:
            if index == len(values):
                break
            value = values[index]
            index += 1
            if value is not None:
                child = Node(value)
                setattr(node, attribute, child)
                nodes[value] = child
                queue.append(child)
    return root, nodes

def serialize(root):
    queue, result = deque([root]), []
    while queue:
        node = queue.popleft()
        result.append(None if node is None else node.val)
        if node is not None:
            queue.extend([node.left, node.right])
    while result and result[-1] is None:
        result.pop()
    return result

def implementations(filename):
    text = (root / 'notes/problems' / filename).read_text()
    for code in re.findall(r'^```python\n([\s\S]*?)^```', text, re.M):
        namespace = {}
        exec(compile(code, filename, 'exec'), namespace)
        yield namespace['Solution']

for cls in implementations('0226-invert-binary-tree.md'):
    assert cls().invertTree(None) is None
    for values, expected in [([1], [1]), ([1, 2], [1, None, 2]), ([4, 2, 7, 1, 3, 6, 9], [4, 7, 2, 9, 6, 3, 1])]:
        tree, original_nodes = make_tree(values)
        answer = cls().invertTree(tree)
        assert answer is tree
        assert serialize(answer) == expected
        assert serialize(cls().invertTree(answer)) == values
        _, roundtrip_nodes = make_tree(serialize(answer))
        assert len(original_nodes) == len(roundtrip_nodes)
        # Traverse the actual result and check that every original object is retained.
        queue, actual = [answer], set()
        while queue:
            node = queue.pop()
            if node is not None:
                actual.add(id(node))
                queue.extend([node.left, node.right])
        assert actual == {id(node) for node in original_nodes.values()}

lca_classes = list(implementations('0236-lowest-common-ancestor.md'))
for cls in lca_classes:
    tree, nodes = make_tree([3, 5, 1, 6, 2, 0, 8, None, None, 7, 4])
    for p, q, expected in [(5, 1, 3), (5, 4, 5), (7, 4, 2), (3, 4, 3)]:
        assert cls().lowestCommonAncestor(tree, nodes[p], nodes[q]) is nodes[expected]

    rng = Random(70)
    random_nodes = [Node(i) for i in range(50)]
    open_slots = [(random_nodes[0], 'left'), (random_nodes[0], 'right')]
    for child in random_nodes[1:]:
        slot = rng.randrange(len(open_slots))
        parent, side = open_slots.pop(slot)
        setattr(parent, side, child)
        open_slots.extend([(child, 'left'), (child, 'right')])
    paths = {}
    queue = deque([(random_nodes[0], [])])
    while queue:
        node, path = queue.popleft()
        current = path + [node]
        paths[node] = current
        for child in [node.left, node.right]:
            if child is not None:
                queue.append((child, current))
    for _ in range(100):
        p, q = rng.sample(random_nodes, 2)
        common = [a for a, b in zip(paths[p], paths[q]) if a is b]
        assert cls().lowestCommonAncestor(random_nodes[0], p, q) is common[-1]

chain = [Node(i) for i in range(2000)]
for parent, child in zip(chain, chain[1:]):
    parent.right = child
assert lca_classes[1]().lowestCommonAncestor(chain[0], chain[1500], chain[1999]) is chain[1500]
print('PASS: both tree variants; empty and asymmetric trees; in-place identity; LCA ancestor/split cases; 100 random target pairs; iterative depth-2000 case.')
