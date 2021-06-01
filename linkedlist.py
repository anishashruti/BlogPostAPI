class Node:
    def __init__(self,data=None,next_node=None):
        self.data = data
        self.next_node = next_node

class LinkedList:
    
    def __init__(self):
        self.head = None
        self.tail = None
    
    def to_list(self):
        l = []
        if self.head is None:
            return l

        node = self.head
        while node:
            l.append(node.data)
            node = node.next_node
        return l

    def print_ll(self):
        ll_string = ""
        node = self.head
        if node is None:
            print(None)
        while node:
            ll_string += f" {str(node.data)} ->"
            node = node.next_node

        ll_string += " None"
        print(ll_string)

    def insert_front(self,data):
        if self.head is None:
            self.head=Node(data,None)
            self.tail=self.head
            return
        new_Node = Node(data,self.head)
        self.head=new_Node
    
    def insert_end(self,data):
        #to check if the linked list if empty
        if self.head is None:
            self.insert_front(data)
            return
        #if we keep track of the lastnode then we dont need any traversal
            # if self.tail is None:
            # perform traversal till we reach the end
            #     node = self.head
            #     while node.next_node:
            #         node = node.next_node
            #     node.next_node= Node(data,None)
            #     self.tail=node.next_node
        self.tail.next_node=Node(data,None)
        self.tail=self.tail.next_node
        
    def get_user_by_id(self, user_id):
        node = self.head
        while node:
            if node.data["id"] is int(user_id):
                return node.data
            node = node.next_node
        return None

# ll = LinkedList()

# ll.insert_front('Piriya')
# ll.insert_front('Anisha')
# ll.insert_front('Deeps')
# ll.insert_front('Paal')
# ll.insert_front('Mama')

# ll.insert_end('Ammmeh')

# ll.print_ll()