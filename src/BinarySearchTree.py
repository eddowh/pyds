# -*- coding: utf-8 -*-


class Node(object):

    def __init__(self, key, value, parent, left=None, right=None):
        self.key = key
        self.value = value
        self.parent = parent
        self.left = left
        self.right = right

    def __str__(self):
        return "<{}, {}>".format(self.key, self.value)

    def get_key(self):
        return self.key

    def get_value(self):
        return self.value

    def get_parent(self):
        return self.parent

    def get_left(self):
        return self.left

    def get_right(self):
        return self.right

    def set_value(self, value):
        self.value = value

    def set_parent(self, parent):
        self.parent = parent

    def set_left(self, left):
        self.left = left

    def set_right(self, right):
        self.right = right

    def is_leaf(self):
        return (self.left is None and self.right is None)

    def __eq__(self, other):
        if self is other:
            return True
        elif other is None:
            return False
        else:
            return (
                self.key == other.key and
                self.value == other.key and
                self.parent == other.parent and
                self.left == other.left and
                self.right == other.right
            )


class BinarySearchTree(object):
    _root = None
    _curr = None
    _size = 0

    def __init__(self, lst=None):
        if lst is None:
            pass
        elif (type(lst) in {BinarySearchTree, list}):
            for item in lst:
                self.insert(item)

    def __str__(self):
        return BinarySearchTree._print_root(self._root)

    def clear(self):
        self = BinarySearchTree()
        assert self.is_empty()

    @property
    def size(self):
        return self._size

    def __len__(self):
        return self.size

    def is_empty(self):
        return self.size == 0

    def get(self, key):
        try:
            node = self._find(key)
        except KeyError:
            # TODO
            raise
        else:
            return node.get_value()

    def set(self, key, value):
        try:
            node = self._find(key)
        except KeyError:
            # TODO
            raise
        else:
            node.set_value(value)

    def insert(self, key, value):
        """If the key already exists, update with the new value."""
        # base case for when there is no elements
        if self._root is None:
            self._root = Node(key, value, parent=None)
        else:
            node = self._root
            while True:
                # the idea is to keep navigating until we reach
                # a child node that is NULL, and so we set that
                # "null child" as a new node with the key and value
                # specified
                if key < node.get_key():
                    if node.get_left() is None:
                        new_leaf = Node(key, value, parent=node)
                        node.set_left(new_leaf)
                        break
                    else:
                        node = node.get_left()
                elif key > node.get_key():
                    if node.get_right() is None:
                        new_leaf = Node(key, value, parent=node)
                        node.set_right(new_leaf)
                        break
                    else:
                        node = node.get_right()
                else:  # key is equal, set value
                    node.set_value(value)
                    break
        # update size counter
        self._size += 1

    def remove(self, key):
        try:
            node = self._find(key)
        except KeyError:
            # TODO
            pass
        else:
            lc = node.get_left()
            rc = node.get_right()
            p = node.get_parent()
            # leaf node (no children)
            if lc is None and rc is None:
                if p.get_left() is node:
                    p.set_left(None)
                elif p.get_right() is node:
                    p.set_right(None)
            # node has one children
            elif lc is None and rc is not None:
                rc.set_parent(p)
                p.set_right(rc)
            elif lc is not None and rc is None:
                lc.set_parent(p)
                p.set_left(lc)
            # node has two children
            elif lc is not None and rc is not None:
                min_node = self._pop_min_node(rc)
                node.set_key(min_node.get_key())
                node.set_value(min_node.get_value())
            # update size counter
            self._size -= 1

    def __iter__(self):
        """Iterate the elements of the tree from smallest to biggest."""
        self._curr = None
        return self

    def __next__(self):
        if self._curr is None:
            self._curr = self._find_min()
            return self._curr
        elif self._curr.get_right() is not None:  # get leftmost leaf
            self._curr = BinarySearchTree._find_min_node(
                self._curr.get_right()
            )
            return self._curr
        else:
            while self._curr.get_parent() is not None:
                # the next biggest element is only when
                # you travel to a parent from a left node
                if self._curr.get_parent().get_left() is self._curr:
                    self._curr = self._curr.get_parent()
                    return self._curr
                else:
                    self._curr = self._curr.get_parent()
            # by now we cannot find any bigger elements
            # which means we have reached the end of the iterator
            # so we stop returning
            raise StopIteration

    def __nonzero__(self):
        return not self.is_empty()

    @staticmethod
    def _pop_min_node(node):
        """Recursive implementation for removing the minimum node.

        Returns the removed node (previous minimum).
        """
        if node.get_left() is None:
            if node.get_right() is not None:
                node.get_right().set_parent(node.get_parent())
            return node.get_right()
        return node.set_left(
            BinarySearchTree._pop_min_node(node.get_left())
        )

    @staticmethod
    def _print_root(root):
        # TODO
        return ""

    @staticmethod
    def _find_min_node(node):
        min_node = node
        while min_node.get_left() is not None:
            min_node = min_node.get_left()
        return min_node

    def _find_min(self):
        """Find the node with the minimum key in the tree.

        Useful for finding the beginning of the iterator.
        """
        return self._find_min_node(self._root)

    def _find(self, key):
        """Internal find function that returns the node with the key."""
        node = self._root
        while node is not None:
            if node.get_key() == key:
                return node
            elif node.get_key() < key:
                node = node.get_left()
            else:
                node = node.get_right()
        # not found
        raise KeyError
