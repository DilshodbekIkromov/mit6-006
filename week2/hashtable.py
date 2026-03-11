from ..week1.linkedlist import Linked_List_Seq
from random import randint

# Hash table using chaining (each slot holds a linked list to handle collisions).
# Supports the full Set interface: find, insert, delete, find_min/max, find_next/prev.
# Uses universal hashing h(k) = ((a*k) mod p) mod m for expected O(1) lookups.
# Table auto-resizes (grow/shrink) to keep load factor ~= 100/r (default r=200 means ~50% full).
class Hash_Table_Set:
    def __init__(self, r = 200): # O(1)
        self.chain_set = Linked_List_Seq  # each bucket is a linked list storing colliding items
        self.A = []                       # array of buckets (chains), length m
        self.size = 0                     # number of items stored across all chains
        self.r = r                        # resize ratio parameter: target load = n/m ≈ 100/r
                                          # r=200 -> load ≈ 0.5, r=100 -> load ≈ 1.0
        self.p = 2**31 - 1               # large Mersenne prime for universal hash family
        self.a = randint(1, self.p - 1)  # random multiplier in [1, p-1], chosen once at init
        self._compute_bounds()
        self._resize(0)                  # allocate initial bucket array

    def __len__(self): return self.size # O(1)

    def __iter__(self): # O(n)
        # iterate over every bucket, yielding each item from each chain
        for X in self.A:
            yield from X

    def build(self, X): # O(n) expected
        # insert each item from iterable X one by one (triggers resizes as needed)
        for x in X: self.insert(x)

    def _hash(self, k, m): # O(1)
        # universal hash: maps key k into bucket index [0, m)
        # h(k) = ((a * k) mod p) mod m
        # gives O(1) expected chain length when a is random
        return ((self.a * k) % self.p) % m

    def _compute_bounds(self): # O(1)
        # upper: max n before we must grow (= current number of buckets m)
        # lower: min n before we must shrink (keeps load from getting too sparse)
        # invariant maintained: lower < n < upper, so load factor stays near 100/r
        self.upper = len(self.A)
        self.lower = len(self.A) * 100*100 // (self.r*self.r)

    def _resize(self, n): # O(n)
        # only resize if n is outside [lower, upper) — avoids resizing on every operation
        if (self.lower >= n) or (n >= self.upper):
            f = self.r // 100
            if self.r % 100: f += 1
            # f = ceil(r / 100): multiplier so that m = n * f buckets
            # e.g. r=200 -> f=2, so m=2n buckets for ~50% load
            m = max(n, 1) * f
            A = [self.chain_set() for _ in range(m)]  # allocate m empty chains
            for x in self:                             # rehash all existing items into new array
                h = self._hash(x.key, m)
                A[h].insert(x)
            self.A = A
            self._compute_bounds()  # update bounds for the new table size

    def find(self, k): # O(1) expected
        # hash to the right bucket, then linear search within that chain
        h = self._hash(k, len(self.A))
        return self.A[h].find(k)

    def insert(self, x): # O(1) amortized expected
        # grow table if needed, then insert x into the appropriate chain
        self._resize(self.size + 1)
        h = self._hash(x.key, len(self.A))
        added = self.A[h].insert(x)  # returns True if new item, False if key already existed
        if added: self.size += 1
        return added

    def delete(self, k): # O(1) amortized expected
        assert len(self) > 0
        h = self._hash(k, len(self.A))
        x = self.A[h].delete(k)  # remove item with key k from its chain
        self.size -= 1
        self._resize(self.size)  # shrink table if it became too sparse
        return x

    def find_min(self): # O(n)
        # hash tables have no ordering, so must scan all items
        out = None
        for x in self:
            if (out is None) or (x.key < out.key):
                out = x
        return out

    def find_max(self): # O(n)
        out = None
        for x in self:
            if (out is None) or (x.key > out.key):
                out = x
        return out

    def find_next(self, k): # O(n)
        # find the item with the smallest key strictly greater than k
        out = None
        for x in self:
            if x.key > k:
                if (out is None) or (x.key < out.key):
                    out = x
        return out

    def find_prev(self, k): # O(n)
        # find the item with the largest key strictly less than k
        out = None
        for x in self:
            if x.key < k:
                if (out is None) or (x.key > out.key):
                    out = x
        return out

    def iter_order(self): # O(n^2)
        # yields all items in ascending key order by repeatedly calling find_next
        # O(n^2) because each find_next is O(n) and we call it n times
        x = self.find_min()
        while x:
            yield x
            x = self.find_next(x.key)
