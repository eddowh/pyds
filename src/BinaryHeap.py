# -*- coding: utf-8 -*-

from cached_property import cached_property


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
        # invalidate the cache because internally updated
        del self['_find_max_leaf']

    def peek_min(self):
        if self._size < 1:
            raise IndexError("No elements in heap.")
        else:
            return self._heap[1]

    def delete_min(self):
        self._heap[1] = self._heap.pop()
        self._percolate_down(1)
        # invalidate the cache because internally updated
        del self['_find_max_leaf']

    def peek_max(self):
        if self._size < 1:
            raise IndexError("No elements in heap.")
        else:
            return self._heap[self._find_max_leaf()]

    def remove_max(self):
        # TODO: this can be very tricky
        # can we even do this without pointers...?
        pass

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
        if i * 2 + 1 > self.size:
            return i * 2
        else:
            return (
                i * 2
                if self._heap[i * 2] < self._heap[i * 2 + 1]
                else i * 2 + 1
            )

    def _find_max_child(self, i):
        if i * 2 + 1 > self.size:
            return i * 2
        else:
            return (
                i * 2
                if self._heap[i * 2] > self._heap[i * 2 + 1]
                else i * 2 + 1
            )

    @cached_property
    def _find_max_leaf(self):
        i = 1
        while i * 2 <= self.size:
            i = self._find_max_child(i)
        return i
