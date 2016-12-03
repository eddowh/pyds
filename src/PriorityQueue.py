# -*- coding: utf-8 -*-

from .BinaryHeap import BinaryHeap


class PrioritizedElement(object):

    def __init__(self, el, priority):
        self._el = el
        self._priority = priority

    def get_element(self):
        return self._el

    def __cmp__(self, other):
        # greater priority means closer to the root
        if self._priority > other._priority:
            return -1
        elif self._priority == other._priority:
            return 0
        else:
            return 1


class PriorityQueue(object):

    def __init__(self):
        self._data = BinaryHeap()

    def clear(self):
        self._data = BinaryHeap()

    def insert(self, el, priority):
        prioritized_element = PrioritizedElement(el, priority)
        self._data.insert(prioritized_element)

    def batch_insert(self, prioritized_elements):
        pass

    def peek_lowest_priority(self):
        return self._data.peek_max()

    def remove_lowest_priority(self):
        self._data.remove_max()

    def pop_lowest_priority(self):
        lp = self.peek_lowest_priority()
        self.remove_lowest_priority()
        return lp

    def peek_highest_priority(self):
        return self._data.peek_min().get_element()

    def remove_highest_priority(self):
        self._data.remove_min()

    def pop_highest_priority(self):
        hp = self.peek_highest_priority()
        self.remove_highest_priority()
        return hp
