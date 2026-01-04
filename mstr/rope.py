from __future__ import annotations
from typing import Optional, Tuple
import random

class Node:
    __slots__ = ['value', 'priority', 'size', 'left', 'right', 'rev', 'hash1', 'hash2']
    def __init__(self, value: str):
        self.value = value
        self.priority = random.random()
        self.size = 1
        self.left: Optional[Node] = None
        self.right: Optional[Node] = None
        self.rev = False
        self.hash1 = ord(value)
        self.hash2 = ord(value)

def get_size(node: Optional[Node]) -> int:
    return node.size if node else 0

def update(node: Optional[Node]) -> None:
    if node:
        node.size = get_size(node.left) + 1 + get_size(node.right)
        h1 = h2 = ord(node.value)
        if node.left:
            h1 = (node.left.hash1 * 131 + h1) & 0xFFFFFFFFFFFFFFFF
            h2 = (node.left.hash2 * 137 + h2) & 0xFFFFFFFFFFFFFFFF
        if node.right:
            h1 = (h1 * 131 + node.right.hash1) & 0xFFFFFFFFFFFFFFFF
            h2 = (h2 * 137 + node.right.hash2) & 0xFFFFFFFFFFFFFFFF
        node.hash1, node.hash2 = h1, h2

def push(node: Optional[Node]) -> None:
    if node and node.rev:
        node.left, node.right = node.right, node.left
        if node.left: node.left.rev ^= True
        if node.right: node.right.rev ^= True
        node.rev = False

def split(node: Optional[Node], k: int) -> Tuple[Optional[Node], Optional[Node]]:
    if not node: return None, None
    push(node)
    ls = get_size(node.left)
    if ls >= k:
        l, r = split(node.left, k)
        node.left = r
        update(node)
        return l, node
    elif ls + 1 > k:
        l, r = split(node.left, k)
        node.left = r
        update(node)
        return l, node
    else:
        l, r = split(node.right, k - ls - 1)
        node.right = l
        update(node)
        return node, r

def merge(l: Optional[Node], r: Optional[Node]) -> Optional[Node]:
    if not l: return r
    if not r: return l
    push(l); push(r)
    if l.priority > r.priority:
        l.right = merge(l.right, r)
        update(l)
        return l
    else:
        r.left = merge(l, r.left)
        update(r)
        return r