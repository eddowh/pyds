# -*- coding: utf-8 -*-


class BinaryHeap(object):

    def __init__(self):
        # initialize with one element in the front
        # for one-based inded array
        # so integer division is easier when determining
        # children and parent "nodes"
        self._heap = [None]

    @property
    def size(self):
        return len(self._heap) - 1

    def insert(self, el):
        self._heap.append(el)
        self._percolate_up(self.size)

    def peek_min(self):
        if self._size < 1:
            raise IndexError("No elements in heap.")
        else:
            return self._heap[1]

    def delete_min(self):
        self._heap[1] = self._heap.pop()
        self._percolate_down(1)

    def _percolate_up(self, i):
        while i // 2 > 0:  # cannot go further than root node
            if self._heap[i] < self._heap[i // 2]:
                # swap them
                self._heap[i], self._heap[i // 2] = \
                    self._heap[i // 2], self._heap[i]
            i //= 2

    def _percolate_down(self, i):
        while i * 2 <= self.size:
            mc = self._find_min_child(i)
            if self._heap[i] > self._heap[mc]:
                # swap elements
                self._heap[i], self._heap[mc] = \
                    self._heap[mc], self._heap[i]
            i = mc

    def _find_min_child(self, i):
        # when there is only one leaf child
        if i * 2 + 1 > self._size:
            return i * 2
        else:
            return (
                i * 2
                if self._heap[i * 2] < self._heap[i * 2 + 1]
                else i * 2 + 1
            )
