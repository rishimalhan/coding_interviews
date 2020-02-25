import sys


# Simple class and object
# class student:
# 	def __init__(self,first_name,last_name):
# 		self.first_name = first_name
# 		self.last_name = last_name
# 		return

# 	def logger(self):
# 		print(self.first_name + self.last_name)

# # Main
# a = student("xyz","abc")
# a.logger()
# student.logger(a)





# LINKED lists
# Linked arrays or linked lists use pointer to next element and are not stored in contiguous locations in memory
# drawback is, to access an element, we have to go sequentially. A binary search cannot be conducted
# Not cache friendly

# # Creating a list of objects of specific class
# class node:
# 	child = None
# 	def __init__(self,data):
# 		self.x = data[0]
# 		self.y = data[1]
# 		self.z = data[2]
# 		return

# # Separate linked list class can also be used to create a head which is node object and then the same process.
# class linked_list:
# 	def __init__(self,parent):
# 		self.parent = parent


# data1 = [0,0,0]
# data2 = [0.5,0.5,0.5]
# data3 = [1,1,1]

# nodes1 = node(data1)
# nodes2 = node(data2)
# nodes3 = node(data3)

# nodes1.child = nodes2
# nodes2.child = nodes3

# print(nodes1.child)
# print(nodes2.child)
# print(nodes3.child)





# # Python LISTS
# # a = [1,2,3,4]
# # b = [[1,2,3],[4,5,6]] # Multi dimensional list

# # OR

# # Append(element)
# a = []
# a.append(1)
# a.append(2)
# a.append((3,4)) # This will append a tuple (3,4) to the list. Basically things get appended as it is
# a.append("string")
# print(a)
# print(a[2][0]) # tuple elements can be accessed like this.

# # Insert(pos,element)
# b = []
# b.insert(1,4)
# print(b[0])
# # print(b[1]) # This will print list index out of range

# b = [1,2,3,4]
# b.insert(1,5) # This will append element at 1 position so new list will be 1,5,2,3,4
# print(b) 

# # Extend([elements]) method appends multiple elements at the end
# a = [1,2]
# a.extend([3,4,5])
# print(a)

# # List elements are accessed using [index]. A negative index can be used to access elements from the end.
# # list.remove(element) removes the corresponding element from the list
# a = [1,2,3,4]
# b = a.pop()
# print(a)
# print(b)

# a = [1,2,3,4]
# b = a.pop(2)
# print(a)
# print(b)

# # Slicing operation can be performed on the list like a[3:8] to print elements from index 3 to 7
# a = [1,2,3,4,5,6]
# print(a[2:5])

# # reverse, sort, count, and copy are other useful methods









# from collections import defaultdict
# import queue

# # Breadth first search
# class Graph:
# 	def __init__(self):
# 		self.graph = defaultdict(list)
# 		return

# 	def addEdge(self,parent,child):
# 		self.graph[parent].append(child)
# 		return

# def BFS(graph,strt_node):
# 	print("Running BFS")
# 	isVisited = [False] * len(graph.graph) # Creating a list of specific size
# 	q = queue.LifoQueue() # LIFO
# 	q.put(strt_node)
# 	isVisited[strt_node] = True
# 	while(not q.empty()):
# 		curr_node = q.get()
# 		print("Current Node: {}". format(curr_node))
# 		neighbrs = graph.graph[curr_node]
# 		for i in neighbrs:
# 			if not isVisited[i]:
# 				q.put(i)
# 				isVisited[i] = True

# 	return



# if __name__ == '__main__':
# 	g = Graph()
	# g.addEdge(0, 1) 
	# g.addEdge(0, 2) 
	# g.addEdge(1, 2) 
	# g.addEdge(2, 0) 
	# g.addEdge(2, 3) 
	# g.addEdge(3, 3)
# 	BFS(g,2)