import math 

class IntervalsTree:
    def __init__(self, array):
        self.tree = self.__build(array)
    
    def __str__(self):
        return "%s" % self.tree
    
    def __convert_index_to_tree(self, n):
        return len(self.tree)/2 + n
    
    def __convert_index_to_array(self, n):
        return n - len(self.tree)/2
    
    def get_sum(self):
        return self.tree[1]
    
    def get_element(self, array_index):
        tree_index = self.__convert_index_to_tree(array_index)
        return self.tree[tree_index]
    
    def is_leaf(self, index):
        return index >= len(self.tree)/2
    
    def left_child(self, i):
        return 2 * i
    
    def right_child(self, i):
        return 2 * i + 1
        
    def parent(self, i):
        return i/2
        
    def swap(self, i, j):
        tree_i = self.__convert_index_to_tree(i)
        tree_j = self.__convert_index_to_tree(j)
        temp = self.tree[tree_i]
        self.__update(tree_i, self.tree[tree_j])
        self.__update(tree_j, temp)
    
    def update(self, array_index, by):
        tree_i = self.__convert_index_to_tree()
        self.__update(tree_i, by)
    
    def __build(self, banners):
        
        # Pad to power of two and add leaves with our banners to it
        size = len(banners)
        padsize = int(math.pow(2,math.ceil(math.log(size,2))))
        tree = [0]*padsize + banners + [0]*(padsize - size)
    
        # Fill up whole tree
        for i in range(padsize - 1, 0, -1):
            tree[i] = tree[self.left_child(i)] + tree[self.right_child(i)]
        return tree
    
    def __update(self, tree_index, by):
        self.tree[tree_index] = by
        while tree_index != 1:
            parent_index = self.parent(tree_index)
            self.tree[parent_index] = self.tree[self.left_child(parent_index)] + self.tree[self.right_child(parent_index)]
            tree_index = parent_index
    
    def find_interval(self, value):
        current_index = 1
        while not self.is_leaf(current_index):
            if value >= self.tree[self.left_child(current_index)]:
                value -= self.tree[self.left_child(current_index)]
                current_index = self.right_child(current_index)
            else:
                current_index = self.left_child(current_index)
        return self.__convert_index_to_array(current_index)
        
