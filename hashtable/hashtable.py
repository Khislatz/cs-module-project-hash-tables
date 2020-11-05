class HashTableEntry:
    """
    Linked List hash table key/value pair
    """
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None

    def __eq__(self, other):
        if isinstance(other, HashTableEntry):
            return self.key == other.key
        return False

    def __repr__(self):
        return f'HashTableEntry({self.key}, {self.value})'                    


class Node: 
    def __init__(self, value):
        self.value = value
        self.next = None
        
    def __repr__(self):
        return str(self.value)

class LinkedList: # Hash class 
    def __init__(self):
        self.head = None
    
    def __repr__(self):
        currStr = ""
        curr = self.head
        while curr is not None:
            currStr +=f'{str(curr.value)} -> '
            curr = curr.next
        return currStr

    # Runtime: O(1) 
    def insert_at_head(self, node):
        node.next = self.head
        self.head = node 

    # Runtime complexity: O(n) because we have 2 functions where one has a runtime O(n) and the other one O(1)
    # O(n) + O(1) = O(n)
    def insert_at_head_or_overwrite(self, node):
        existingNode = self.find(node.value)
        if existingNode is not None:
            existingNode.value = node.value
            return False
        else:
            self.insert_at_head(node)            
            return True

    # Runtime complexity: O(n), where n is the number of nodes        
    # Space complexity: O(1) because the space requirements do not change based on the input 
    def delete(self, value):
        curr  = self.head

        # Case 1 is when we want to delete the first value (head):
        # if curr is the value, which the head now, is the value we want to delete
        if curr.value == value:
            # we want to move the head to the next value 
            self.head = curr.next
            # returning the node that we just deleted 
            return curr 
        # Case 2 is when we want to delete the middle value (in between head and tail):
        prev = curr 
        curr = curr.next 

        while curr is not None:
            # if the current pointer is the value we want to delete, we point the previous value to the one after
            # its next value (we skip the one in between)
            if curr.value == value:
                prev.next = curr.next
                curr.next = None 
                return curr
            else:
                prev = curr
                curr.next
        return None          



    # Runtime: O(n), where n is the number of nodes. Because the worst case is that we need to
    # traverse the entirely of this list     
    def find(self, value):   
        curr = self.head
        while curr is not None:
            if curr.value == value: 
                # then we found the node we were looking for, so we return the node  
                return curr 
            # otherwise     
            curr = curr.next
        return None



# Hash table can't have fewer than this many slots
MIN_CAPACITY = 8


class HashTable:
    """
    A hash table that with `capacity` buckets
    that accepts string keys

    Implement this.
    """

    def __init__(self, capacity):
        # Your code here
        self.capacity = MIN_CAPACITY
        self.num_elements = 0
        self.hash_table = [None] * self.capacity


    def get_num_slots(self):
        """
        Return the length of the list you're using to hold the hash
        table data. (Not the number of items stored in the hash table,
        but the number of slots in the main list.)

        One of the tests relies on this.

        Implement this.
        """
        # Your code here
        return len(self.hash_table) 


    def get_load_factor(self):
        """
        Return the load factor for this hash table.
        
        We will manually keep track of number of elements using put and delete functions  
        A hash table consists of slots. Some slots have a linked list of elements; some are empty.
        The number of elements depends on the number of Hash Table Entries we have in our hash table 

        For example, if we have 3 slots: 2 are not empty and one is empty. 1 non-empty slot has a linked list of 2
        elements and the other non-empty slot has 3 linked list elements. 

        So the load factor equals: number of total elements (2+3) / total number of slots 3(both empty and non-empty)  
        """
        # Your code here
        return self.num_elements / self.get_num_slots() 
 
    def fnv1(self, key):
        """
        FNV-1 Hash, 64-bit

        Implement this, and/or DJB2.
        """

        # Your code here
        pass

    def djb2(self, key):
        """
        DJB2 hash, 32-bit
        Implement this, and/or FNV-1.
        """
        # Your code here
        enc = key.encode()
        hsh = 5381
        for char in enc:
            hsh = ((hsh << 5) + hsh) + char
        
        return hsh & 0xFFFFFFFF


    def hash_index(self, key):
        """
        Take an arbitrary key and return a valid integer index
        between within the hash_table capacity of the hash table.
        """
        #return self.fnv1(key) % self.capacity
        return self.djb2(key) % self.get_num_slots() # self.djb2(key) % len(self.hash_table) 

    def put(self, key, value):
        """
        Store the value with the given key.

        Hash collisions should be handled with Linked List Chaining.

        Implement this.
        """
        # Calculate index of the key
        index = self.hash_index(key)
        # If the index is not empty meaning that there is already a linked list in that slot
        if self.hash_table[index] != None:
            # We need to add to that linked list
            linked_list = self.hash_table[index]
            # Since there might something exist in the linked list, we either add at head or overwrite   
            # Since we don't know if we added the new value at head or overwritten the old one, 
            # we need to know whether we should increase the number of elements or not (num_elements)
            did_add_new_node = linked_list.insert_at_head_or_overwrite(Node(HashTableEntry(key, value)))
            if did_add_new_node:
                self.num_elements += 1
        # If the slot is empty (there is no existing linked list) we need to create one 
        else:                
            linked_list = LinkedList()
            linked_list.insert_at_head(Node(HashTableEntry(key, value)))
            self.hash_table[index] = linked_list
            self.num_elements += 1

        # if self.get_load_factor() > 0.7:
        #     self.resize(self.get_num_slots() * 2)

    def delete(self, key):
        """
        Remove the value stored with the given key.

        Print a warning if the key is not found.

        Implement this.
        """
        # Your code here
        # Compute hash
        
        index = self.hash_index(key)
        if self.hash_table[index] != None:
            linked_list = self.hash_table[index]
            did_delete_node = linked_list.delete(HashTableEntry(key, None))
            if did_delete_node != None:
                self.num_elements -=1
                if self.get_load_factor() < 0.2:
                    self.resize(self.get_num_slots() /2) 
        else:
            print('Warning: node is not found')                 

    def get(self, key):
        """
        Retrieve the value stored with the given key.

        Returns None if the key is not found.

        Implement this.
        """
        # Your code here
        # Compute hash
        index = self.hash_index(key)
        # Go to first node in list in hash_table
        node = self.hash_table[index]
        if node != None:
            linked_list = self.hash_table[index]
            node = linked_list.find(HashTableEntry(key, None))
            if node !=None:
                return node.value.value
        return None                

    def resize(self, new_capacity):
        """
        Changes the capacity of the hash table and
        rehashes all key/value pairs.

        Implement this.
        """
        # Your code here
        old_table = self.hash_table
        self.hash_table = [None] * int(new_capacity)
        # Resetting the number of elements
        self.num_elements = 0

        for element in old_table:
            if element == None:
                continue
            curr_node = element.head
            while curr_node != None:
                temp = curr_node.next
                curr_node.next = None
                index = self.hash_index(curr_node.value.key)

                if self.hash_table[index] != None:
                    self.hash_table[index].insert_at_head(curr_node)
                else:
                    linked_list = LinkedList()
                    linked_list.insert_at_head(curr_node)
                    self.hash_table[index] = linked_list

                curr_node = temp
                self.num_elements +=1                       

if __name__ == "__main__":
    ht = HashTable(8)

    ht.put("line_1", "'Twas brillig, and the slithy toves")
    ht.put("line_2", "Did gyre and gimble in the wabe:")
    ht.put("line_3", "All mimsy were the borogoves,")
    ht.put("line_4", "And the mome raths outgrabe.")
    ht.put("line_5", '"Beware the Jabberwock, my son!')
    ht.put("line_6", "The jaws that bite, the claws that catch!")
    ht.put("line_7", "Beware the Jubjub bird, and shun")
    ht.put("line_8", 'The frumious Bandersnatch!"')
    ht.put("line_9", "He took his vorpal sword in hand;")
    ht.put("line_10", "Long time the manxome foe he sought--")
    ht.put("line_11", "So rested he by the Tumtum tree")
    ht.put("line_12", "And stood awhile in thought.")

    print("")

    # Test storing beyond capacity
    for i in range(1, 13):
        print(ht.get(f"line_{i}"))

    # Test resizing
    # old_capacity = ht.get_num_slots()
    # ht.resize(ht.capacity * 2)
    # new_capacity = ht.get_num_slots()

    # print(f"\nResized from {old_capacity} to {new_capacity}.\n")

    # Test if data intact after resizing
    for i in range(1, 13):
        print(ht.get(f"line_{i}"))

    print("")
