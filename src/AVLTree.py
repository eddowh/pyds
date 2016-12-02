# -*- coding: utf-8 -*-

from .BinarySearchTree import Node, BinarySearchTree


class AVLNode(Node):

    def __init__(self, key, value, parent, left=None, right=None):
        super(AVLNode, self).__init__(key, value, parent, left, right)
        self._height = 0

    def get_height(self):
        return self._height

    def set_height(self, h):
        self._height = h

    @staticmethod
    def cast_from_node(node):
        """'Casts' a Node and all its children to AVLNodes.

        Assigns the proper height for the node at each depth.
        """
        avlnode = AVLNode._naive_cast_from_node(node)
        depth = avlnode.get_max_depth()
        AVLNode._adjust_heights_recur(avlnode, depth + 1)
        return avlnode

    @staticmethod
    def _adjust_heights_recur(avlnode, height):
        """Assigns/fixes the heights of AVLNodes.

        Used in conjunction with AVLNode._naive_cast_from_node
        to produce a proper AVLNode with the correct heights.
        """
        if avlnode is None:
            pass  # do nothing
        else:
            height -= 1
            avlnode.set_height(height)
            AVLNode._adjust_heights_recur(avlnode.get_left(), height)
            AVLNode._adjust_heights_recur(avlnode.get_right(), height)

    @staticmethod
    def _naive_cast_from_node(node):
        """'Casts' a Node and all its children to AVLNodes.

        Does not assign heights for the nodes.
        """
        if node is not None and type(node) != Node:
            raise TypeError("Must cast of type {}".format(type(node)))
        elif node is None:
            return node
        else:
            p = AVLNode(
                key=node.get_key(),
                value=node.get_value(),
                parent=None
            )
            if node.get_left() is None:
                q = None
            else:
                q = AVLNode._naive_cast_from_node(node.get_left())
                q.set_parent(p)
            if node.get_right() is None:
                r = None
            else:
                r = AVLNode._naive_cast_from_node(node.get_right())
                r.set_parent(p)
            p.set_left(q)
            p.set_right(r)
            return p


class AVLTree(BinarySearchTree):

    def insert(self, key, value):
        super(AVLTree, self).insert(key, value)
        # find the newly inserted node
        p = self._find(key)
        while True:
            p = AVLTree.balance_node(p)
            if p.get_parent() is None:  # reaches the root
                break
            p = p.get_parent()
        self._root = p

    def remove(self, key):
        try:
            # tbr = to be removed
            tbr = self._find(key)
        except KeyError:
            raise
        else:
            # TODO
            pass

    @staticmethod
    def get_node_height(node):
        return 0 if node is None else node.get_height()

    @staticmethod
    def get_node_bfactor(node):
        return (
            AVLTree.get_node_height(node.get_right()) -
            AVLTree.get_node_height(node.get_left())
        )

    @staticmethod
    def fix_node_height(node):
        hl = AVLTree.get_node_height(node.get_left())
        hr = AVLTree.get_node_height(node.get_right())
        node.set_height(hl + 1 if hl > hr else hr + 1)

    @staticmethod
    def rotate_node_left(q):
        p = q.get_right()

        # detach p's left and make it q's right
        # p_lst = p's left subtree
        p_lst = p.get_left()
        q.set_right(p_lst)
        if p_lst is not None:
            p_lst.set_parent(q)

        # make q's parent's child p instead
        # q_p = q's parent
        q_p = q.get_parent()
        p.set_parent(q_p)
        if q_p is not None:
            if q_p.get_left() is q:
                q_p.set_left(p)
            elif q_p.get_right() is q:
                q_p.set_right(p)

        # finally make q's parent p
        p.set_left(q)
        q.set_parent(p)

        # fix the heights
        AVLTree.fix_node_height(p)
        AVLTree.fix_node_height(q)

        return p

    @staticmethod
    def rotate_node_right(p):
        q = p.get_left()

        # detach q's right and make it p's left
        # q_rst = q's right subtree
        q_rst = q.get_right()
        p.set_left(q_rst)
        if q_rst is not None:
            q_rst.set_parent(p)

        # make's p's parent's child q instead
        # p_p = p's parent
        p_p = p.get_parent()
        q.set_parent(p_p)
        if p_p is not None:
            if p_p.get_left() is p:
                p_p.set_left(q)
            elif p_p.get_right() is p:
                p_p.set_right(q)

        # finally you can make p's parent q
        q.set_right(p)
        p.set_parent(q)

        # fix the heights
        AVLTree.fix_node_height(p)
        AVLTree.fix_node_height(q)

        return q

    @staticmethod
    def balance_node(node):
        """Balances node to satisfy AVL height specifications.

        Assumes that the height can only be off by one (2 or -2).
        Hence, only useful to balance from bottom to top.
        """
        AVLTree.fix_node_height(node)
        if AVLTree.get_node_bfactor(node) == 2:
            # right subtree's left subtree is higher
            if AVLTree.get_node_bfactor(node.get_right() < 0):
                node.set_right(AVLTree.rotate_node_right(node.get_right()))
            return AVLTree.rotate_node_left(node)
        elif AVLTree.get_node_bfactor(node) == -2:
            # left subtree's right subtree is higher
            if AVLTree.get_node_bfactor(node.get_left() > 0):
                node.set_left(AVLTree.rotate_node_left(node.get_left()))
            return AVLTree.rotate_node_right(node)
        else:  # satisfies AVL height requirements
            return node

    @staticmethod
    def _pop_min_node(node):
        """Recursive implementation for removing the minimum node.

        Returns the removed node (previous minimum), and balances
        each node on the way up.

        TODO: needs a more reusable implementation that reuses code
        inherited from BinarySearchTree.
        """
        if node.get_left() is None:
            if node.get_right() is not None:
                node.get_right().set_parent(node.get_parent())
            return node.get_right()
        p = node.set_left(
            BinarySearchTree._pop_min_node(node.get_left())
        )
        return AVLTree.balance(p)

    @staticmethod
    def from_bst(bst):
        # self._root = AVLNode.cast_from_node(bst._root)
        pass
