class Node:
    def __init__(self,data=None,next_node=None):
        self.data=data
        self.next_node=next_node
    
class Data:
    def __init__(self,key,value):
        self.key = key
        self.value=value

class Hashtable:
    def __init__(self,table_size):
        self.table_size=table_size
        self.hash_table = [None]*table_size
    
    def custom_hash(self,key):
        #A good hashtable is one that produced minimum collision
        #This custom hash function returns a same value of hashed_key for a particular key
        hash_value =0
        for i in key:
            hash_value += ord(i)
            #MODULO OPERATOR MAKES SURE THAT THE TABLE SIZE IS NOT EXCEDED
            hash_value = ( hash_value * ord(i))% self.table_size #trying to make unique hashvalues
        return hash_value

    def add_key_value(self,key,value):
        hashed_key = self.custom_hash(key)
        if self.hash_table[hashed_key] == None:
            self.hash_table[hashed_key]=Node(Data(key,value),None)
        #if ther is something otherthan none ie. collission has occured 
        else:
            node=self.hash_table[hashed_key]
            while node.next_node:
                node =node.next_node
            node.next_node = Node(Data(key,value),None)

    def get_value(self,key):
        hashed_key=self.custom_hash(key)
        if self.hash_table[hashed_key] is not None:
            node=self.hash_table[hashed_key]
            if node.next_node is None:
                #if it is the only node
                return node.data.value
            else:
                #checks if the node has data in its next node
                #traversal for searching
                while node.next_node:
                    if key == node.data.key:
                        return node.data.value
                node=node.next_node

                if key == node.data.key:
                    return node.data.value
        return None

    
    def print_table(self):
        print("{")
        for i, val in enumerate(self.hash_table):
            if val is not None:
                llist_string = ""
                node = val
                if node.next_node:
                    while node.next_node:
                        llist_string += (
                            str(node.data.key) + " : " + str(node.data.value) + " --> "
                        )
                        node = node.next_node
                    llist_string += (
                        str(node.data.key) + " : " + str(node.data.value) + " --> None"
                    )
                    print(f"    [{i}] {llist_string}")
                else:
                    print(f"    [{i}] {val.data.key} : {val.data.value}")
            else:
                print(f"    [{i}] {val}")
        print("}")

# ht =Hashtable(4)
# ht.add_key_value("anisha","first")
# ht.add_key_value("anis","shruti")
# ht.add_key_value("anisha","last")
# ht.print_table()

