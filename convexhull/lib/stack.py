class Stack:
    def __init__(self, size = 0):
        self.s = [] if size == 0 else [None] * size
        self.size = size
        self.itop = -1
    
    def push(self, item):
        if self.itop < self.size - 1:
            self.itop += 1
            self.s[self.itop] = item
        else:
            self.itop += 1
            self.size += 1
            self.s.append(item)
            
    def pop(self):
        if self.itop >= 0:
            self.itop -= 1

    def top(self):
        if self.itop >= 0:
            return self.s[self.itop]
        else:
            return None
    
    def sec(self):
        if self.itop > 0:
            return self.s[self.itop - 1]
        else:
            return None
        
    def is_empty(self):
        return not (self.itop >= 0)

    def getsize(self):
        return self.itop+1
    
    
    def __str__(self):
        return str(self.s[:self.itop+1])  