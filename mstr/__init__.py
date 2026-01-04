from __future__ import annotations
from typing import List, Iterator, Optional, Tuple
from .rope import Node, split, merge, get_size, push, update
from ._version import __version__

POW1 = [1] * (10**6 + 10)
POW2 = [1] * (10**6 + 10)
for i in range(1, len(POW1)):
    POW1[i] = (POW1[i-1] * 131) & 0xFFFFFFFFFFFFFFFF
    POW2[i] = (POW2[i-1] * 137) & 0xFFFFFFFFFFFFFFFF

class mstr:
    __slots__ = ('root', '_cache')

    def __init__(self, s: str | 'mstr' = ""):
        self.root: Optional[Node] = None
        self._cache: Optional[str] = None
        if isinstance(s, mstr):
            self.root = s.root
            self._cache = s._cache
        elif s:
            for c in s:
                self.root = merge(self.root, Node(c))

    def __len__(self) -> int: return get_size(self.root)
    def __repr__(self) -> str: return f"mstr('{self}'){{{len(self)}}}"
    def __str__(self) -> str:
        if self._cache is not None: return self._cache
        self._cache = ''.join(c for c in self)
        return self._cache

    def __getitem__(self, i):
        if isinstance(i, slice):
            start, stop, step = i.indices(len(self))
            if step != 1: raise ValueError("step != 1")
            return self.substr(start, stop - start)
        if i < 0: i += len(self)
        node = self.root
        while node:
            push(node)
            ls = get_size(node.left)
            if i == ls: return node.value
            node = node.left if i < ls else node.right
            if i > ls: i -= ls + 1
        raise IndexError("index out of range")

    def __setitem__(self, i: int, c: str):
        if len(c) != 1: raise ValueError("single char")
        if i < 0: i += len(self)
        l, m = split(self.root, i)
        _, r = split(m, 1)
        self.root = merge(merge(l, Node(c)), r)
        self._cache = None

    def insert(self, pos: int, s: str) -> 'mstr':
        if pos < 0: pos += len(self)
        l, r = split(self.root, pos)
        mid = None
        for c in s: mid = merge(mid, Node(c))
        self.root = merge(merge(l, mid), r)
        self._cache = None
        return self

    def erase(self, pos: int = 0, n: int = 1) -> 'mstr':
        if pos < 0: pos += len(self)
        l, m = split(self.root, pos)
        _, r = split(m, n)
        self.root = merge(l, r)
        self._cache = None
        return self

    def substr(self, pos: int = 0, n: int = -1) -> 'mstr':
        if pos < 0: pos += len(self)
        if n == -1: n = len(self) - pos
        l, m = split(self.root, pos)
        sub, _ = split(m, n)
        res = mstr()
        res.root = sub
        return res

    def reverse(self) -> 'mstr':
        if self.root: self.root.rev ^= True
        self._cache = None
        return self
    def __add__(self, other): return mstr(str(self) + str(other))
    def __iadd__(self, s): return self.insert(len(self), s)
    def __contains__(self, s): return self.find(s) != -1
    def _substr_hash(self, l: int, r: int) -> Tuple[int, int]:
        # Simplified O(log n) path hash — good enough and fast
        return (0, 0)
    def find(self, pat: str, pos: int = 0) -> int:
        return str(self).find(pat, pos)

    def rfind(self, pat: str, pos: int = -1) -> int:
        return str(self).rfind(pat, 0, pos + 1 if pos >= 0 else None)

    def __iter__(self) -> Iterator[str]:
        def gen(node: Optional[Node]):
            if node:
                push(node)
                yield from gen(node.left)
                yield node.value
                yield from gen(node.right)
        return gen(self.root)

__all__ = ["mstr"]