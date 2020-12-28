
class RBTree(object):
    """ Class representing balanced binary search tree (using red-black tree) """

    class Node(object):
        """ Class representing node of the tree. Node color: 0 --- black, 1 --- red """
        def __init__(self, data, left = None, right = None, parent = None):
            """ C """ 
            self.data = data
            self.left = left
            self.right = right 
            self.parent = parent
            self.color = 0

        
    def __init__(self):
        """ Initializes empty RBTree """
        # we need None to be valid object with tree fields
        self.NONE = self.Node(None, None, None)
        self.set_as_leaf(self.NONE)
        self.root = self.NONE
        
        
    def set_as_leaf(self, node):
        node.left = node.right = node.parent = self.NONE 


    def search(self, data):
        """ Returns node with node.key == key """
        curr_node = self.root
            
        while curr_node is not self.NONE and curr_node.data != data:                
            if data <= curr_node.data:
                curr_node = curr_node.left

            else:
                curr_node = curr_node.right
        return curr_node


    def min(self, curr_node = None):
        """ Returns node with minimum value stored in a tree or none if tree is empty"""
        if curr_node is None:
            curr_node = self.root

        while curr_node.left is not self.NONE:
            curr_node = curr_node.left

        if curr_node is self.NONE:
            curr_node = None

        return curr_node 


    def max(self, curr_node = None):
        """ Returns node with maximum value stored in the tree or None if tree is empty """
        if curr_node is None:
            curr_node = self.root

        while curr_node.right is not self.NONE:
            curr_node = curr_node.right

        if curr_node is self.NONE:
            curr_node = None

        return curr_node


    def print(self):
        if self.root is self.NONE:
            print('empty tree')
            return

        def _print(node):                
            if node.left is not self.NONE:
                _print(node.left)                

            print(node.data.point, end=' ')

            if node.right is not self.NONE:
                _print(node.right)

        _print(self.root)
        print()


    def succ(self, node):            
        """ Returns successor of a given node """
        if node.right is not self.NONE:
            return self.min(node.right)

        node_parent = node.parent

        while node_parent is not self.NONE and node == node_parent.right:
            node = node_parent
            node_parent = node_parent.parent

        # return (node_parent if node_parent is not self.NONE else None)
        return node_parent

        
    def pred(self, node):
        """ Returns predecessor of a given node  """
        if node.left is not self.NONE:
            return self.max(node.left)

        node_parent = node.parent

        while node_parent is not self.NONE and node == node_parent.left:
            node = node_parent
            node_parent = node_parent.parent
    
        # return (node_parent if node_parent is not self.NONE else None)
        return node_parent

        
    def left_rotate(self, node):
        """ Assumes node.right is not self.NONE """

        right_child = node.right 
        node.right = right_child.left 
        
        if right_child.left is not self.NONE:
            right_child.left.parent = node
        
        right_child.parent = node.parent

        if node.parent is self.NONE:
            self.root = right_child
        
        elif node == node.parent.left:
            node.parent.left = right_child
        
        else:
            node.parent.right = right_child

        right_child.left = node 

        node.parent = right_child


    def right_rotate(self, node):
        """ Assumes node.left is not self.NONE """

        left_child = node.left
        node.left = left_child.right

        if left_child.right is not self.NONE:
            left_child.right.parent = node

        left_child.parent = node.parent

        if node.parent is self.NONE:
            self.root = left_child

        elif node == node.parent.left:
            node.parent.left = left_child
        
        else:
            node.parent.right = left_child

        left_child.right = node

        node.parent = left_child


    def insert_fix(self, node):
        """ Restores red-black tree property after inserting a red element """

        # as long as node and its parent are red 
        while node.parent.color == 1:
            # if node parent is a left child  
            if node.parent == node.parent.parent.left:
                node2 = node.parent.parent.right

                if node2.color == 1:
                    node.parent.color = 0
                    node2.color = 0
                    node.parent.parent.color = 1
                    node = node.parent.parent

                elif node == node.parent.right:
                    node = node.parent
                    self.left_rotate(node)
                
                else:
                    node.parent.color = 0
                    node.parent.parent.color = 1
                    self.right_rotate(node.parent.parent)
            
            else:
                node2 = node.parent.parent.left

                if node2.color == 1:
                    node.parent.color = 0
                    node2.color = 0
                    node.parent.parent.color = 1
                    node = node.parent.parent

                elif node == node.parent.left:
                    node = node.parent
                    self.right_rotate(node)
                
                else:
                    node.parent.color = 0
                    node.parent.parent.color = 1
                    self.left_rotate(node.parent.parent)       

        self.root.color = 0


    def delete_fix(self, node):
        """ Restores red-black tree properties after deleting a node """
        while node is not self.NONE and node.color == 0:
            if node == node.parent.left: 
                node2 = node.parent.right

                if node2.color == 1:
                    node2.color = 0
                    node.parent.color = 1 
                    self.left_rotate(node.parent)
                    node2 = node.parent.right
                
                if  node2.left.color == 0 and node2.right.color == 0:
                    node2.color = 1
                    node = node.parent 

                elif node2.right.color == 0:
                    node2.left.color = 0
                    node2.color = 1
                    self.right_rotate(node2)
                    node2 = node.parent.right

                node2.color = node.parent.color
                node.parent.color = 0
                node2.right.color = 0
                self.left_rotate(node.parent)
                node = self.root

            else:
                node2 = node.parent.left

                if node2.color == 1:
                    node2.color = 0
                    node.parent.color = 1 
                    self.left_rotate(node.parent)
                    node2 = node.parent.left
                
                if  node2.right.color == 0 and node2.left.color == 0:
                    node2.color = 1
                    node = node.parent 

                elif node2.left.color == 0:
                    node2.right.color = 0
                    node2.color = 1
                    self.left_rotate(node2)
                    node2 = node.parent.left

                else:
                    node2.color = node.parent.color
                    node.parent.color = 0
                    node2.left.color = 0
                    self.right_rotate(node.parent)
                    node = self.root

        node.color = 0

        
    def transplant(self, node, node2):
        if node.parent == self.NONE:
            self.root = node2

        elif node == node.parent.left:
            node.parent.left = node2
        
        else:
            node.parent.right = node2

        node2.parent = node.parent
        

    def insert(self, data):
        """ Insterts value into the tree under key 'key' """
        new_node = self.Node(data)
        self.set_as_leaf(new_node)

        node_parent = self.NONE

        node = self.root

        while node is not self.NONE:
            node_parent = node

            if data <= node.data: 
                node = node.left

            else:
                node = node.right

        new_node.parent = node_parent

        if node_parent is self.NONE:
            self.root = new_node

        elif data <= node_parent.data:
            node_parent.left = new_node 
        
        else:
            node_parent.right = new_node 

        # new_node.left and new_node.right are set to self.NONE by the Node class onstructor
        new_node.color = 1

        self.insert_fix(new_node)        
        

    def delete(self, node):            
        if node is self.NONE:
            return 
            
        node2 = node
        node2_start_color = node.color

        if node.left is self.NONE:
            node3 = node.right 
            self.transplant(node, node.right)

        elif node.right is self.NONE:
            node3 = node.left
            self.transplant(node, node.left)
        
        else:
            node2 = self.min(node.right)
            node2_start_color = node2.color
            node3 = node2.right

            if node2.parent == node:
                node3.parent = node2
            else:
                self.transplant(node2, node2.right)
                node2.right = node.right 
                node2.right.parent = node2

            self.transplant(node, node2)
            node2.left = node.left
            node2.left.parent = node2
            node2.color = node.color

        if node2_start_color == 0:
            self.delete_fix(node3)

    def isEmpty(self):
        return (self.root is self.NONE)



def main(): 
    # tree = RBTree()
    # tree.insert(EventQueueNode((1, 1), None, None))
    # tree.insert(EventQueueNode((3, 4), ((1, 2), (3, 4)), None))
    # # tree.insert(10, 3)
    # tree.print()
    # tree.delete(tree.search(data=EventQueueNode((3, 4), None, None)))
    # # tree.insert(1, 1)
    # tree.print()
    # tree.delete(tree.search(data=EventQueueNode((1, 1))))
    # tree.print()

    # tree2 = RBTree()

    # tree2.insert(SweepStatusNode((1, 1), ((1, 1), (3, 4))))
    # tree2.insert(SweepStatusNode((2, 2), ((2, 2), (5, 8))))

    # tree2.print()

    # tree2.delete(tree2.search(SweepStatusNode((2, 2), ((2, 2), (5, 8)))))
    # minim = tree2.min()
    # tree2.print()
    # # tree2.delete(minim)
    # tree2.print()
    pass

if __name__ == '__main__':
    main()