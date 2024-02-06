from __future__ import annotations
from typing import Optional, Any, List


def merge(l1: list, l2: list) -> list:
    lst = []
    i = 0
    j = 0
    while i < len(l1) and j < len(l2):
        if l1[i] < l2[j]:
            lst.append(l1[i])
            i += 1
        else:
            lst.append(l2[j])
            j += 1
    lst.extend(l1[i:])
    lst.extend(l2[j:])
    return lst


class Tree:
    _root: Optional[Any]
    _subtrees: List[Tree]

    def __init__(self, root: Optional[Any], subtrees: List[Tree]) -> None:
        self._root = root
        self._subtrees = subtrees

    def is_empty(self) -> bool:
        return self._root is None

    def __str__(self) -> str:
        # if self.is_empty():
        #     return ''
        # else:
        #     s = f'{self._root}\n'
        #     for subtree in self._subtrees:
        #         s += str(subtree)
        #     return s
        return self._str_indented(0)

    def indented_str(self) -> str:
        if self.is_empty():
            return ''
        elif not self._subtrees:
            return f'{self._root}\n'
        else:
            s = f'{self._root}\n'
            for subtree in self._subtrees:
                s += tab(subtree.indented_str())

    def _str_indented(self, depth: int) -> str:
        if self.is_empty():
            return ''
        else:
            s = ' ' * depth + f'{self._root}' + '\n'
            for subtree in self._subtrees:
                s += subtree._str_indented(depth + 1)
            return s


def tab(s: str) -> str:
    """
    >>> s = '4\\n\\t1\\n\\t2\\n\\t3\\n'
    >>> tab(s)
    '\\t4\\n\\t\\t1\\n\\t\\t2\\n\\t\\t3'
    """
    line_list = s.split('\n')

    for i in range(len(line_list)):
        line_list[i] = '\t' + line_list[i] + '\n'

    t = ''
    for line in line_list:
        t += line

    return t


if __name__ == '__main__':
    t1 = Tree(1, [])
    t2 = Tree(2, [])
    t3 = Tree(3, [])
    t4 = Tree(4, [t1, t2, t3])
    t5 = Tree(5, [])
    t6 = Tree(6, [t4, t5])
