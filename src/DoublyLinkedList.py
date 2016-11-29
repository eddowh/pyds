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
        """Construct a new linked list.

        This can either clone an existing linked list, or
        create a new linked list from a Python list.
        """
        if lst is None:
            pass
        elif (type(lst) in {DoublyLinkedList, list}):
            for item in lst:
                self.push(item)

    def clear(self):
        """Empty the list."""
        self = DoublyLinkedList()
        assert self.is_empty()

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
        """Append an item to the end of the list."""
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
        """Remove and return the last item from the list."""
        return self.remove(self.size - 1)

    def unshift(self):
        """Remove and return the first item from the list."""
        return self.remove(0)

    def shift(self, val):
        """Append an item to the front of the list."""
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
        """Insert an item at a certain position in the list."""
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
        """Remove and return an item at a certain position from the list."""
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
        """Return an item at a certain position in the list."""
        if (pos < 0 or pos >= self.size):
            raise IndexError("Out of bounds.")
        node = self._get_node_at(pos)
        return node.val

    def __getitem__(self, key):
        if isinstance(key, int):
            return self.get(key)
        elif isinstance(key, slice):
            start, stop, step = key.indices(len(self))
            # create new list
            res = DoublyLinkedList()
            # "jump" to starting index
            head = self._get_node_at(start)
            res.push(head.val)
            start += step
            cond = (start < stop) if step > 0 else (start > stop)
            while cond:
                for _ in range(abs(step)):
                    head = head.next if step > 0 else head.prev
                res.push(head.val)
                start += step
                cond = (start < stop) if step > 0 else (start > stop)
            return res
        else:
            raise TypeError('Index must be int or slice')

    def set(self, pos, val):
        """Set a new value for an item at a certain position in the list."""
        if (pos < 0 or pos >= self.size):
            raise IndexError("Out of bounds.")
        node = self._get_node_at(pos)
        node.val = val

    def __setitem__(self, key, value):
        if isinstance(key, int):
            return self.get(key, value)
        elif isinstance(key, slice):
            start, stop, step = key.indices(len(self))
            # TODO
            pass
        else:
            raise TypeError('Index must be int or slice')

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
        """Copy the object.

        Calls the constructor with this list as the parameter.
        """
        return DoublyLinkedList(self)

    def __eq__(self, other):
        """Check whether all values in the two lists are equal."""
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
        """Check whether an item is in the list."""
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
        """Returns a new list by appending another list to the end."""
        if not isinstance(other, DoublyLinkedList):
            raise TypeError
        res = self.clone()
        other = other.clone()
        res._tail.next = other._head
        other._head.prev = res._tail
        res._tail = other._tail
        return res

    def __mul__(self, n):
        """Returns a new list by appending the same list n times."""
        if not isinstance(n, int):
            raise TypeError
        if n < 1:
            return DoublyLinkedList()
        res = self.clone()
        for _ in range(n - 1):
            res += self
        return res

    def reverse(self):
        """Sort the items of the list in place.

        Given n = size of linked list, the algorithmic runtime is O(n/2)=O(n).
        """
        cnt = 0
        head = self._head
        tail = self._tail
        while cnt < self.size / 2:
            head.val, tail.val = tail.val, head.val
            head = head.next
            tail = tail.prev
            cnt += 1

    def __reversed__(self):
        reversed_list = self.clone()
        reversed_list.reverse()
        return reversed_list

    def __nonzero__(self):
        return not self.is_empty()

if __name__ == '__main__':
    x = DoublyLinkedList([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    print(x)
    y = [1, 2, 3, 4, 5]
    print(y[1:2])
    y[1:4:2] = [99, 100]
    print(y)
