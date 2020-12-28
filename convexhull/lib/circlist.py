""" K. Kafara """


from typing import Any


class CircList(object):
    
    class Node(object):
        def __init__(self, data: Any = None, prev = None, next = None): 
            self.next = None
            self.prev = None
            self.data = data            
    
    def __init__(self):
        self.sentinel = self.Node()
    
    
    def append(self, data: Any) -> None: 
        raise NotImplementedError

        
    def print(self):
        raise NotImplementedError
    
    
    
    
def main():
    circ_list = CircList()
    
    for i in range(10):
        circ_list.append(i)
        

    print("exec print")
    circ_list.print()
    
        
if __name__ == "__main__":
    main()
    