# -*- coding: utf-8 -*-


class Node(object):

    def __init__(self, val, prev=None, next=None):
        self.val = val
        self.prev = prev
        self.next = next

    def __eq__(self, other):
        if self is other:
            return True
        elif other is None:
            return False
        else:
            return (
                self.prev == other.prev and
                self.next == other.next and
                self.val == other.val
            )


class DoublyLinkedList(object):
    _head = None
    _tail = None
    _size = 0

    def __init__(self, lst=None):
        if lst is None:
            pass
        elif (type(lst) is DoublyLinkedList or
              type(lst) is list):
            for item in lst:
                self.push(item)

    def __str__(self):
        res = ""
        for item in self:
            res += "{}, ".format(item)
        return "[{}]".format(res[:-2].strip())

    @property
    def size(self):
        return self._size

    def __len__(self):
        return self.size

    def is_empty(self):
        return self.size == 0

    def push(self, val):
        node = Node(val)
        if self._head is None:  # empty list
            self._head = self._tail = node
        else:
            node.prev = self._tail
            node.next = None
            self._tail.next = node
            self._tail = node
        self._size += 1

    def pop(self):
        return self.remove(self.size - 1)

    def unshift(self):
        return self.remove(0)

    def shift(self, val):
        node = Node(val=val)
        if self._tail is None:  # empty list
            self._head = self._tail = node
        else:
            node.prev = None
            node.next = self._head
            self._head.prev = node
            self._head = node
        self._size += 1

    def insert(self, pos, val):
        if (pos < 0 or pos > self.size):
            raise IndexError("Out of bounds.")
        if pos == 0:
            self.push(val)
        elif pos == self.size:
            self.shift(val)
        else:
            node = self._get_node_at(pos)
            pred = node.prev
            new_node = Node(val=val, prev=pred, next=node)
            node.prev = new_node
            pred.next = new_node
            self._size += 1

    def remove(self, pos):
        if (pos < 0 or pos >= self.size):
            raise IndexError("Out of bounds.")
        node = self._get_node_at(pos)
        pred = node.prev
        succ = node.next
        if pred is None:  # at head
            self._head = succ
        else:
            pred.next = succ
        if succ is None:  # at tail
            self._tail = pred
        else:
            succ.prev = pred
        self._size -= 1
        return node.val

    def __delitem__(self, pos):
        self.remove(pos)

    def get(self, pos):
        if (pos < 0 or pos >= self.size):
            raise IndexError("Out of bounds.")
        node = self._get_node_at(pos)
        return node.val

    def __getitem__(self, idx):
        return self.get(idx)

    def set(self, pos, val):
        if (pos < 0 or pos >= self.size):
            raise IndexError("Out of bounds.")
        node = self._get_node_at(pos)
        node.val = val

    def __setitem__(self, pos, val):
        self.set(pos, val)

    def _get_node_at(self, pos):
        """Get node from a certain position.

        Given n = size of linked list, the algorithmic runtime is O(n/2)=O(n).

        :param pos: index of desired node
        :type pos: int
        :returns: Node object
        """
        if pos < self.size / 2:
            cnt = pos
            node = self._head
            while cnt > 0:
                node = node.next
                cnt -= 1
        else:
            cnt = self.size - 1 - pos
            node = self._tail
            while cnt > 0:
                node = node.prev
                cnt -= 1
        return node

    def clone(self):
        return DoublyLinkedList(self)

    def __eq__(self, other):
        if self is other:
            return True
        elif self._size != other._size:
            return False
        else:
            this_head = self._head
            that_head = other._head
            while (this_head is not None and that_head is not None):
                if this_head.val != that_head.val:
                    return False
                this_head = this_head.next
                that_head = that_head.next
            return True

    def __ne__(self, other):
        return not (self == other)

    def __contains__(self, value):
        for item in self:
            if value == item:
                return True
        return False

    def __iter__(self):
        head = self._head
        while head is not None:
            yield head.val
            head = head.next

    def __add__(self, other):
        if self is other:  # have to clone list
            other = self.clone()
        self._tail.next = other._head
        other._head.prev = self._tail
        self._tail = other._tail

    def __reversed__(self):
        head = self._head
        reversed_list = DoublyLinkedList()
        while head is not None:
            reversed_list.shift(head.val)
            head = head.next
        return reversed_list

    def __nonzero__(self):
        return not self.is_empty()
