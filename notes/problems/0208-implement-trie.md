## How I recognized it

- "Does any word **start with** this prefix?" (autocomplete) → **Trie**.
- Many words share the same beginning → store the shared letters only once, as a tree.

## Key idea

Every node is a dictionary. Its keys are the next letters, and each value is the child node (another dictionary). A special key `"*"` marks "a word ends here". All three methods walk down the tree one letter at a time.

Let `N` be the number of inserted words and `L` the length of the word or prefix we are working with.

## 1. Brute force: a set of words, O(N · L) for startsWith

```python
class Trie:
    def __init__(self):
        self.words = set()

    def insert(self, word: str) -> None:
        self.words.add(word)

    def search(self, word: str) -> bool:
        return word in self.words

    def startsWith(self, prefix: str) -> bool:
        return any(w.startswith(prefix) for w in self.words)
```

`search` is fast, but `startsWith` has to check **every word**. That is the bottleneck.

**Time: insert and search O(L), startsWith O(N · L). Space: O(total letters).**

## 2. Better: Trie with nested dictionaries, O(L) for everything

What changes: words with the same prefix share one path, so `startsWith` only walks `L` steps and never looks at other words.

```text
insert("app")
"a"   not here → add {} → move down
"p"   not here → add {} → move down
"p"   not here → add {} → move down
done  → node["*"] = True

insert("apple")
"a" "p" "p"   already here → just move down
"l"   not here → add {} → move down
"e"   not here → add {} → move down
done  → node["*"] = True
```

```text
a
└── p
    └── p
        ├── *        "app" ends here
        └── l
            └── e
                └── *    "apple" ends here
```

`"*"` is a flag on a node, not a path to walk. A node can have `"*"` and children at the same time.

My solution:

```python
class Trie:

    def __init__(self):
        self.root = {}
        
    def insert(self, word: str) -> None:
        node = self.root
        for i in word:
            if i not in node:
                node[i] = {}
            
            node = node[i]
        node["*"] = True
        
    def search(self, word: str) -> bool:
        node = self.root
        for i in word:
            if i not in node:
                return False
            node = node[i]
        
        return "*" in node

    def startsWith(self, prefix: str) -> bool:
        node = self.root
        for i in prefix:
            if i not in node:
                return False
            node = node[i]  
        return True
```

`search` and `startsWith` are the same walk. Only the last line is different:

```text
trie has only "apple"

               walk a → p → p    last line
search("app")      found          "*" in node?  → False
startsWith("app")  found          return True   → True
```

**Time: O(L) for each call. Space: O(total letters inserted)**, and less when words share prefixes.

## Complexity at a glance

```text
Approach        insert   search   startsWith   Space
Set of words    O(L)     O(L)     O(N · L)     O(total letters)
Trie            O(L)     O(L)     O(L)         O(total letters)
```

## In the interview

```text
words: "app", "apple"

root
 └ a
   └ p
     └ p *
       └ l
         └ e *
```

> Say: "Each node is a dictionary from a letter to the next node. Words that start the same way share one path. A star marks where a word ends. Search and startsWith both walk down letter by letter, but only search needs the star at the end."

## Remember

- Move down every time: `node = node[i]` goes **outside** the `if`.
- End check is `"*" in node`, not `node == {"*": True}`. A node can have `"*"` and more letters.
- `node[i]` has no quotes (a variable). `node["*"]` has quotes (fixed text).
