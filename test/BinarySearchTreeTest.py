# -*- coding: utf-8 -*-

import unittest

from src.BinarySearchTree import BinarySearchTree


class BinarySearchTreeTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_insert_empty(self):
        bst = BinarySearchTree()
        bst.insert(5, 'e')
        self.assertEqual(bst.size, 1)
        self.assertEqual(bst._root.get_key(), 5)
        self.assertEqual(bst._root.get_value(), 'e')
        self.assertTrue(bst._root.is_leaf())

    def test_insert_left_to_root(self):
        bst = BinarySearchTree()
        bst.insert(5, 'e')
        bst.insert(3, 'c')
        self.assertEqual(bst.size, 2)
        self.assertEqual(bst._root.get_key(), 5)
        self.assertEqual(bst._root.get_value(), 'e')
        self.assertIsNone(bst._root.get_right())
        self.assertIsNotNone(bst._root.get_left())
        self.assertFalse(bst._root.is_leaf())
        self.assertTrue(bst._root.get_left().is_leaf())

    def test_insert_right_to_root(self):
        bst = BinarySearchTree()
        bst.insert(5, 'e')
        bst.insert(7, 'g')
        self.assertEqual(bst.size, 2)
        self.assertEqual(bst._root.get_key(), 5)
        self.assertEqual(bst._root.get_value(), 'e')
        self.assertIsNone(bst._root.get_left())
        self.assertIsNotNone(bst._root.get_right())
        self.assertFalse(bst._root.is_leaf())
        self.assertTrue(bst._root.get_right().is_leaf())

    def test_insert_update(self):
        bst = BinarySearchTree()
        bst.insert(5, 'e')
        self.assertEqual(bst._root.get_value(), 'e')
        bst.insert(5, 'f')
        self.assertEqual(bst._root.get_value(), 'f')

    def test_get(self):
        bst = BinarySearchTree()
        bst.insert(5, 'e')
        self.assertEqual(bst.get(5), 'e')
        bst.insert(5, 'f')
        self.assertEqual(bst.get(5), 'f')
        with self.assertRaises(KeyError):
            bst.get(0)

    def test_set(self):
        bst = BinarySearchTree()
        bst.insert(5, 'e')
        self.assertEqual(bst.get(5), 'e')
        bst.set(5, 'f')
        self.assertEqual(bst.get(5), 'f')
        with self.assertRaises(KeyError):
            bst.set(1, 'a')

    def test_iterator(self):
        bst = BinarySearchTree()
        lst = [4, 3, 1, 2, 6, 5, 7]
        for el in lst:
            bst.insert(el, '')
        self.assertEqual(bst.size, 7)
        self.assertListEqual([el.get_key() for el in bst], sorted(lst))


if __name__ == '__main__':
    unittest.main()
