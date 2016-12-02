# -*- coding: utf-8 -*-

import unittest

from src.BinarySearchTree import BinarySearchTree, Node
from src.AVLTree import AVLTree, AVLNode


class AVLNodeTest(unittest.TestCase):

    def test_cast_from_node(self):
        n_1 = Node(1, '', parent=None, left=None, right=None)
        n_3 = Node(3, '', parent=None, left=None, right=None)
        n_5 = Node(5, '', parent=None, left=None, right=None)
        n_7 = Node(7, '', parent=None, left=None, right=None)
        n_2 = Node(2, '', parent=None, left=n_1, right=n_3)
        n_1.set_parent(n_2)
        n_3.set_parent(n_2)
        n_6 = Node(6, '', parent=None, left=n_5, right=n_7)
        n_5.set_parent(n_6)
        n_7.set_parent(n_6)
        n_4 = Node(4, '', parent=None, left=n_2, right=n_6)
        n_2.set_parent(n_4)
        n_6.set_parent(n_4)

        p = AVLNode.cast_from_node(n_4)  # root

        # root node: 4
        self.assertEqual(p.key, 4)
        self.assertIsNone(p.parent)
        self.assertEqual(p.left.key, 2)
        self.assertEqual(p.right.key, 6)
        self.assertEqual(p.get_height(), 3)

        # left of root node: 2
        self.assertEqual(p.left.key, 2)
        self.assertEqual(p.left.parent.key, 4)
        self.assertEqual(p.left.left.key, 1)
        self.assertEqual(p.left.right.key, 3)
        self.assertEqual(p.left.get_height(), 2)

        # left of left of root node: 1
        self.assertEqual(p.left.left.key, 1)
        self.assertEqual(p.left.left.parent.key, 2)
        self.assertIsNone(p.left.left.left)
        self.assertIsNone(p.left.left.right)
        self.assertEqual(p.left.left.get_height(), 1)

        # right of left of root node: 3
        self.assertEqual(p.left.right.key, 3)
        self.assertEqual(p.left.right.parent.key, 2)
        self.assertIsNone(p.left.right.left)
        self.assertIsNone(p.left.right.right)
        self.assertEqual(p.left.right.get_height(), 1)

        # right of root node: 6
        self.assertEqual(p.right.key, 6)
        self.assertEqual(p.right.parent.key, 4)
        self.assertEqual(p.right.left.key, 5)
        self.assertEqual(p.right.right.key, 7)
        self.assertEqual(p.right.get_height(), 2)

        # left of right of root node: 5
        self.assertEqual(p.right.left.key, 5)
        self.assertEqual(p.right.left.parent.key, 6)
        self.assertIsNone(p.right.left.left)
        self.assertIsNone(p.right.left.right)
        self.assertEqual(p.right.left.get_height(), 1)

        # right of right of root node: 7
        self.assertEqual(p.right.right.key, 7)
        self.assertEqual(p.right.right.parent.key, 6)
        self.assertIsNone(p.right.right.left)
        self.assertIsNone(p.right.right.right)
        self.assertEqual(p.right.right.get_height(), 1)


class AVLTreeTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_insert(self):
        pass

    def test_remove(self):
        pass

    def test_balance_node(self):
        pass

    def test_rotate_node_left_at_root(self):
        bst = BinarySearchTree([
            (6, ''),
            (4, ''), (8, ''),
            (7, ''), (10, ''),
            (9, ''), (11, ''),
        ])
        q = AVLNode.cast_from_node(bst._root)
        self.assertEqual(q.key, 6)
        q = AVLTree.rotate_node_left(q)
        self.assertEqual(q.key, 8)

    def test_rotate_node_right_at_root(self):
        bst = BinarySearchTree([
            (6, ''),
            (4, ''), (7, ''),
            (2, ''), (5, ''),
            (1, ''), (3, ''),
        ])
        q = AVLNode.cast_from_node(bst._root)
        self.assertEqual(q.key, 6)
        q = AVLTree.rotate_node_right(q)
        self.assertEqual(q.key, 4)

    def test_rotate_node_left_at_nonroot(self):
        pass

    def test_rotate_node_right_at_nonroot(self):
        pass
