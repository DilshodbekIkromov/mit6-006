from ..week1.array_seq import Array_seq 
class Sorted_Array_Set:
    def __init__(self):
        self.A = Array_seq()
    def __len__(self):
        return len(self.A)
    def __iter__(self):
        yield from self.A 
    def iter_order(self):
        yield from self

    def build(self, X): 
        self.A.build(X)
        self._sort()
    def _sort(self):
        pass
    def _binary_search(self, k, i , j):
        if i >= j:
            return i 
        m = (i + j)// 2
        x = self.A.get_at(m)
        if x.key > k: 
            return self._binary_search(k,i,m-1)
        if x.key < k: 
            return self._binary_search(k, m+1, j)
        return m 
    def find_min(self):
        if len(self) > 0:
            return self.A.get_at(0)
        else: 
            return None
    def find_max(self):
        if len(self)>0:
            return self.A.get_at(len(self)-1)
        else: 
            return None 
    def find(self, k):
        if len(self) == 0:
            return None
        i = self._binary_search(k, 0, len(self) - 1)
        x = self.A.get_at(i)
        if x.key == k:
            return x 
        else: 
            return None 
    def find_next(self, k):
        if len(self) == 0:
            return None
        i = self._binary_search(k, 0, len(self) - 1)
        x =self.A.get_at(i)
        if x.key > k: 
            return x 
        if i > 0: 
            return self.A.get_at(i-1)
        else: 
            return None 
    def find_prev(self, k):
        if len(self) == 0:
            return None
        i = self._binary_search(k,0, len(self) - 1)
        x = self.A.get(i)
        if x.key < k:
            return x 
        if i > 0:
            return self.A.get_at(i)
        else: 
            return None
    def insert(self,x): 
        if len(self.A) == 0:
            self.A.insert_first(x)
        else:
            i = self._binary_search(x.key, 0, len(self.A) - 1)
            k = self.A.get_at(i).key
            if k == x.key:
                self.A.set_at(i,x)
                return False
            if k > x.key:
                self.A.insert_at(i,x)
            else: 
                self.A.insert_at(i + 1, x)
        return True
    def delete(self, k):
        i = self._binary_search(k, 0, len(self.A) - 1)
        assert self.A.get_at(i).key == k
        return self.A.delete_at(i)


    
