# -*- coding: utf-8 -*-

from pyprimes import next_prime

# constants
SEPARATE_CHAINING = 0
LINEAR_PROBING = 1
QUADRATIC_PROBING = 2
DOUBLE_HASHING = 3


class HashMethodException(Exception):
    pass


class HashTable(object):

    def __init__(self, method=LINEAR_PROBING, load_factor_threshold=0.50):
        self._size = 0
        self._capacity = 11
        self._load_factor_threshold = load_factor_threshold

        # hashing method - separate chaining or open addressing
        if method not in (0, 1, 2, 3):
            raise HashMethodException(
                "Must use separate chaining or open addressing:\n"
                "0 = separate chaining\n"
                "1 = linear probing\n"
                "2 = quadratic probing\n"
                "3 = double hashing\n"
            )
        else:
            self._method = method

        self._table = [
            # list of lists if separate chaining
            [] if method == SEPARATE_CHAINING else None
            for _ in range(self._capacity)
        ]

    @property
    def size(self):
        return self._size

    @property
    def load_factor(self):
        return float(self.size) / self._capacity

    def __contains__(self, k):
        i = self._internal_hash(k)

        if self._method == SEPARATE_CHAINING:
            found = False
            for n, el in enumerate(self._table[i]):
                if el == k:
                    found = True
                    break
            return found

        else:
            return self._table[i] is not None

    def _internal_hash(self, k):
        """TODO"""
        i = self._hash(k)

        # separate chaining doesn't use open addressing
        if self._method == SEPARATE_CHAINING:
            return i

        # probing
        cnt = 1
        while True:
            if self._method == LINEAR_PROBING:
                j = i + cnt
            elif self._method == QUADRATIC_PROBING:
                j = i + cnt ** 2
            elif self._method == DOUBLE_HASHING:
                j = i + cnt * self._hash_2(k)
            j = j % self._capacity

            if self._table[j] is None:
                break
            else:
                cnt += 1

        return j

    def _hash(self, k):
        """Main hash function."""
        # TODO
        raise NotImplemented

    def _hash_2(self, k):
        """Hash function used __only__ for double hashing."""
        # TODO
        raise NotImplemented

    def insert(self, k):
        i = self._internal_hash(k)

        if self._method == SEPARATE_CHAINING:
            # search through the list and see if it exists
            # so it can be incremeented, otherwise create new
            found = False
            for n, el in enumerate(self._table[i]):
                if el == k:
                    found = True
                    break
            if not found:
                self._table[i].append([k, 0])
                self._size += 1

        # open addressing
        else:
            if self._table[i] is None:
                self._table[i] = k
                self._size += 1

        # resize if load factor is above 0.50
        if self.load_factor >= self._load_factor_threshold:
            self._resize()

    def remove(self, k):
        i = self._internal_hash(k)

        if self._method == SEPARATE_CHAINING:
            found = False
            for n, el in enumerate(self._table[i]):
                if el == k:
                    found = True
                    self._table[i].pop(n)
                    break
                if not found:
                    raise KeyError("key={} not found.".format(k))

        else:  # open addressing
            if self._table[i] is None:
                raise KeyError("key={} not found.".format(k))
            else:
                self._table[i] = None

        self._size -= 1

    def _resize(self):
        old_capacity = self._capacity
        self._capacity = next_prime(old_capacity * 2)

        if self._method == SEPARATE_CHAINING:
            rehashed = []
            for i, el in enumerate(self._table):
                if len(el) > 0:
                    rehashed.extend(el)
                    self._table[i] = []
            for j in range(self._capacity - old_capacity):
                rehashed.append([])
        else:
            rehashed = []
            for i, el in enumerate(self._table):
                if el is not None:
                    rehashed.append(el)
                    self._table[i] = None
            for j in range(self._capacity - old_capacity):
                rehashed.append(None)

        # now that everything is resized, rehash again
        for el in rehashed:
            self.insert(el)
