from array_seq import Array_seq

class Dynamic_Array_Seq(Array_seq):
    def __init__(self, r = 2): # O(1)
        super().__init__()
        self.size = 0
        self.r = r
        self._compute_bounds()
        self._resize(0)

    def __len__(self): return self.size # O(1)

    def __iter__(self): # O(n)
        for i in range(len(self)): yield self.A[i]

    def build(self, X): # O(n)
        for a in X: self.insert_last(a)

    def _compute_bounds(self): # O(1)
        self.upper = len(self.A)
        self.lower = len(self.A) // (self.r * self.r)
# len(self.A) = 8, r = 2
#   upper = 8   (array is full when size reaches this)
#   lower = 8 // 4 = 2  (array is too empty when size drops below this)
# keeps array between 25% and 100% full

    def _resize(self, n): # O(1) amortized, O(n) worst case
        if (self.lower < n < self.upper): return
        m = max(n, 1) * self.r
        A = [None] * m
        self._copy_forward(0, self.size, A, 0)
        self.A = A
        self._compute_bounds()
# self.A: [a, b, _, _]   size=2, insert triggers resize (n=3, upper=4? no)
#   actually: resize when n >= upper or n <= lower
#   m = n * r  (allocate r times the needed space)
#   copy old elements into new bigger/smaller array
# self.A: [a, b, _, _, _, _]   new array with room to grow

    def insert_last(self, x): # O(1) amortized
        self._resize(self.size + 1)
        self.A[self.size] = x
        self.size += 1
# self.A: [a, b, c, _, _]   size=3, insert_last(x)
#          resize if needed (size+1 still within bounds? skip)
#          A[3] = x
#          size = 4
# self.A: [a, b, c, x, _]   size=4

    def delete_last(self): # O(1) amortized
        self.A[self.size - 1] = None
        self.size -= 1
        self._resize(self.size)
# self.A: [a, b, c, _, _, _]   size=3, delete_last()
#          A[2] = None
#          size = 2
#          resize if too empty (size <= lower? shrink array)
# self.A: [a, b, _, _]   size=2

    def insert_at(self, i, x): # O(n)
        self.insert_last(None)
        self._copy_backward(i, self.size - (i + 1), self.A, i + 1)
        self.A[i] = x
# self.A: [a, b, c, d, _]   size=4, insert_at(1, x)
#          insert_last(None) -> [a, b, c, d, None]  size=5
#          copy_backward(1, 3, A, 2): shift [b, c, d] right by 1
#          [a, b, b, c, d]
#          A[1] = x
# self.A: [a, x, b, c, d]   size=5

    def delete_at(self, i): # O(n)
        x = self.A[i]
        self._copy_forward(i + 1, self.size - (i + 1), self.A, i)
        self.delete_last()
        return x
# self.A: [a, b, c, d, _]   size=4, delete_at(1)
#          x = b (saved)
#          copy_forward(2, 2, A, 1): shift [c, d] left by 1
#          [a, c, d, d, _]
#          delete_last() -> [a, c, d, _, _]  size=3
# self.A: [a, c, d, _, _]   returns b

    # O(n)
    def insert_first(self, x): self.insert_at(0, x)
    def delete_first(self): return self.delete_at(0)
