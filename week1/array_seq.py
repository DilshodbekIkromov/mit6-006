class Array_seq: 
    def __init__(self):
        self.A = []
        self.size = 0
    # O ( 1 )
    def __len__(self):
        return self.size
    # O ( n )
    def __iter__(self):
        yield from self.A
    # O ( n )
    def build(self, X): 
        self.A = [ a for a in X]
        self.size = len(self.A)
    # O ( 1 )
    def get_at(self, i):
        return self.A[i]
    # O ( 1 )
    def set_at(self, i , x):
        self.A[i] = x
    # O ( n ) 
    def _copy_forward(self, i , n , A, j):
        for k in range(n):
            A[j+k] = self.A[i+k]
    # O ( n ) : copy n elements from self.A[i..i+n-1] into A[j..j+n-1] front to back
    def _copy_backward(self, i , n, A, j):
        for k in range(n-1, -1, -1):
            A[j+k] = self.A[i+k]
    # O ( n )
    def insert_at(self, i , x):
        n = len(self.A)
        A = [None] * (n+1)
        self._copy_forward(0,i,A,0) # copies elements before the insertion point (self.A[0..i-1]) into A[0..i-1]
        A[i]=x
        self._copy_forward(i, n-i, A, i+1) # copies elements from the insertion point onward (self.A[i..n-1]) into A[i+1..n], shifted right by one
        self.build(A)
# self.A:  [a, b, c, d, e]     insert x at i=2
#           ^^^                 1st copy_forward: copy [a, b]
#               ^^^^^^^^^       2nd copy_forward: copy [c, d, e] shifted right
# A:       [a, b, x, c, d, e]

    # O ( n )
    def delete_at(self,i):
        n = len(self.A)
        A = [None] * (n-1)
        self._copy_forward(0,i,A,0) # copies elements before the deletion point (self.A[0..i-1]) into A[0..i-1]
        x = self.A[i] # save the deleted element
        self._copy_forward(i+1, n - i - 1, A, i) # copies elements after the deletion point (self.A[i+1..n-1]) into A[i..n-2], shifted left by one
        self.build(A)
        return x
# self.A:  [a, b, c, d, e]     delete at i=2
#           ^^^                 1st copy_forward: copy [a, b]
#               ^                x = c (saved)
#                ^^^^^^^^^      2nd copy_forward: copy [d, e] shifted left
# A:       [a, b, d, e]

    # all are O ( n )
    def insert_first(self,x):
        self.insert_at(0,x)
    def delete_first(self): 
        return self.delete_at(0)
    def insert_last(self, x):
        return self.insert_at(len(self), x)
    def delete_last(self):
        return self.delete_at(len(self) - 1)
    



    



    
    















