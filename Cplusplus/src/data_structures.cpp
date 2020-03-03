#include <iostream>
// #include <list>

// // Lists. Check methods in geeks for geeks
// void print_list(std::list <int> ip_list)
// {
// 	std::list <int> :: iterator it;
// 	for(it=ip_list.begin(); it!=ip_list.end();++it)
// 	{
// 		std::cout<< *it << "\t";
// 	}
// 	std::cout<< std::endl;
// }
// int main(int argc, char** argv)
// {
// 	/* Defined as list <data type> similar to vectors.
// 	Operations like push_back and push_front are less expensive compared to vectors
// 	*/
// 	std::list <int> a;
// 	a.push_back(0);
// 	a.push_back(1);
// 	a.push_back(2);	
// 	print_list(a);
// 	return 0;
// }








// // Linked lists
// // dot operator is used to access values of struct or members and -> is used to access them using pointers.
// struct node
// {
// 	int data;
// 	node *next;
// };

// class SinglyLinkedList
// {
// public:
// 	node* head;
// 	node* tail;
// public:
// 	SinglyLinkedList()
// 	{
// 		head = NULL;
// 		tail = NULL;
// 	};

// 	void addNode(int _data)
// 	{
// 		node* temp = new node; // If new node not present, memory is not allocated and it will throw an error when we try to store value for this new node.
// 		temp->data = _data;
// 		temp->next = NULL;
// 		if (!head)
// 		{
// 			// std::cout<< "head is null" << std::endl;
// 			head = temp;
// 			tail = temp;
// 		}
// 		else
// 		{
// 			// std::cout<< "head is not null" << std::endl;
// 			tail->next = temp;
// 			tail = temp;
// 		}
// 	};

// 	void printList()
// 	{
// 		node* temp = this->head;
// 		while(temp)
// 		{
// 			std::cout<< "Data is: " << temp->data << std::endl;
// 			temp = temp->next;
// 		}

// 	};
// };

// int main(int argc, char** argv)
// {
// 	SinglyLinkedList llist;
// 	for (size_t i=0; i<100; ++i)
// 		llist.addNode(i);
	
// 	llist.printList();
// 	return 0;
// }










// // Breadth first search and Depth First Search
// // API for graph
// #include <vector>
// #include <queue>
// #include <stack>
// class Graph
// {
// public:
// 	std::vector<std::vector<int>> graph;

// public:
// 	Graph(){}
// 	void addEdge(int parent, int child)
// 	{
// 		if (parent >= graph.size())
// 		{
// 			graph.resize(parent+1);
// 			graph[parent].push_back(child);
// 		}
// 		else
// 			graph[parent].push_back(child);
// 	};

// 	void printGraph()
// 	{
// 		for (int i=0; i < graph.size(); ++i)
// 		{
// 			std::cout<< i << ": ";
// 			for (int j=0; j < graph[i].size(); ++j)
// 			{
// 				if (j==graph[i].size()-1)
// 					std::cout<< graph[i][j] << std::endl;
// 				else
// 					std::cout<< graph[i][j] << " , ";
// 			}				
// 		}
// 	}
// };


// class Searches
// {
// private:
// public:
// 	Searches(){};

// 	void BFS(std::vector<std::vector<int>> graph, int strt_node)
// 	{
		// std::vector<bool> isVisited;
		// for (int i=0; i < graph.size(); ++i)
		// {
		// 	for (int j=0; j < graph[i].size(); ++j)
		// 	{
		// 		if (graph[i][j]>=isVisited.size())
		// 		{
		// 			isVisited.resize(graph[i][j]+1);
		// 			isVisited[graph[i][j]] = false;
		// 		}
		// 		else
		// 			isVisited[graph[i][j]] = false;
		// 	}
		// }

// 		std::queue<int> q;
// 		q.push(strt_node);
// 		isVisited[strt_node] = true;
// 		while(!q.empty())
// 		{
// 			int curr_node = q.front();
// 			q.pop();
// 			std::cout<< curr_node << std::endl;
// 			std::vector<int> neighbrs = graph[curr_node];
// 			for (int i=0; i<neighbrs.size();++i)
// 			{
// 				if (!isVisited[neighbrs[i]])
// 				{
// 					q.push(neighbrs[i]);
// 					isVisited[neighbrs[i]] = true;
// 				}
// 			}
// 		}
// 	};

// 	void DFS_util(std::vector<std::vector<int>> graph,std::vector<bool> isVisited,std::stack<int> s)
// 	{
// 		int curr_node = s.top();
// 		s.pop();
// 		std::cout<< curr_node << std::endl;
// 		std::vector<int> neighbrs = graph[curr_node];
// 		for (int i=0; i<neighbrs.size();++i)
// 		{
// 			if (!isVisited[neighbrs[i]])
// 			{
// 				s.push(neighbrs[i]);
// 				isVisited[neighbrs[i]] = true;
// 				DFS_util(graph,isVisited,s);	
// 			}
// 		}

// 	};
// 	void DFS(std::vector<std::vector<int>> graph,int strt_node)
// 	{
// 		std::vector<bool> isVisited;
// 		for (int i=0; i < graph.size(); ++i)
// 		{
// 			for (int j=0; j < graph[i].size(); ++j)
// 			{
// 				if (graph[i][j]>=isVisited.size())
// 				{
// 					isVisited.resize(graph[i][j]+1);
// 					isVisited[graph[i][j]] = false;
// 				}
// 				else
// 					isVisited[graph[i][j]] = false;
// 			}
// 		}
// 		std::stack<int> s;
// 		s.push(strt_node);
// 		isVisited[strt_node] = true;
// 		DFS_util(graph,isVisited,s);	
// 	};
// };


// int main(int argc, char** argv)
// {
// 	Graph g;
// 	g.addEdge(0, 1);
// 	g.addEdge(0, 2);
// 	g.addEdge(1, 2); 
// 	g.addEdge(2, 0); 
// 	g.addEdge(2, 3); 
// 	g.addEdge(3, 3);
// 	// g.printGraph();

// 	Searches traverser;

// 	// Run BFS
// 	traverser.BFS(g.graph,2);
// 	traverser.DFS(g.graph,2);
// 	return 0;
// }










// Binary trees
#include <queue>
struct binary_tree
{
	int data;
	binary_tree* left;
	binary_tree* right;
	binary_tree* parent;
};

class tree
{
private:
	binary_tree* root_node;
	std::vector<bool> isVisited;
	int no_nodes;
public:
	tree() {root_node = NULL;};

	binary_tree* create_node(int _data)
	{
		binary_tree* node = new binary_tree;
		node->data = _data;
		node->parent = NULL;
		node->left = NULL;
		node->right = NULL;
		return node;
	};
	void addConnection(binary_tree* node, binary_tree* parent, binary_tree* left_child, binary_tree* right_child)
	{
		if (!root_node)
			root_node = node;
		node->left = left_child;
		node->right = right_child;
		node->parent = parent;

	};
	void init_visited()
	{
		no_nodes = 0;		
		std::queue<binary_tree*> q;
		q.push(root_node);
		no_nodes+=1;
		while(!q.empty())
		{
			binary_tree* temp = q.front(); q.pop();
			if (temp->left)
			{
				q.push(temp->left);
				no_nodes+=1;
			}
		
			if (temp->right)
			{
				q.push(temp->right);
				no_nodes+=1;
			}
			
		}
		std::cout<< "Number of nodes: " << no_nodes << std::endl;
		isVisited.resize(no_nodes);
		for (int i=0; i < no_nodes; ++i)
			isVisited[i] = false;
	};
	void printLevelOrder()
	{
		std::queue<binary_tree*> q;

		q.push(root_node);
		while(!q.empty())
		{
			binary_tree* temp = q.front(); q.pop();
			if (!temp->left && !temp->right)
			{
				std::cout<< "Leaf Node: " << temp->data << std::endl;
				continue;
			}

			std::cout<< "Parent: " << temp->data << " Children: ";
			if (temp->left)
			{
				std::cout<< "Left: " << temp->left->data << " ";
				q.push(temp->left);
			}
		
			if (temp->right)
			{
				std::cout<< "Right: " << temp->right->data << " ";
				q.push(temp->right);
			}
			std::cout<< std::endl;
		};
	};


	void preorder_util(binary_tree* node)
	{
		if (!isVisited[node->data-1])
		{
			// print the current node
			std::cout<< node->data << std::endl;
			isVisited[node->data-1] = true;
		}

		if (node->left!=NULL)
			preorder_util(node->left);
		if (node->right!=NULL)
			preorder_util(node->right);
	}
	void preorder() // nlr version of DFS
	{
		init_visited();
		preorder_util(root_node);	
	};

	void inorder_util(binary_tree *node) //lnr
	{
		if (node->left!=NULL)
			inorder_util(node->left);
		if (!isVisited[node->data-1])
		{
			std::cout<< node->data << std::endl;
			isVisited[node->data-1] = true;
		}
		if (node->right!=NULL)
			inorder_util(node->right);
	};
	void inorder()
	{
		init_visited();
		inorder_util(root_node);
	};

	void postorder_util(binary_tree* node)
	{
		if (node->left!=NULL)
			postorder_util(node->left);
		if (node->right!=NULL)
			postorder_util(node->right);
		if (!isVisited[node->data-1])
		{
			std::cout<< node->data << std::endl;
			isVisited[node->data-1] = true;
		}	
	};
	void postorder()
	{
		init_visited();
		postorder_util(root_node);
	};
};


int main(int argc, char** argv)
{

	// Option-1
	// binary_tree node1;
	// binary_tree node2;
	// binary_tree node3;
	// node1.data = 1;
	// node2.data = 2;
	// node3.data = 3;

	// node1.left = &node2;
	// node1.right = &node3;
	// node1.parent = &node1;

	// std::cout<< node1.left->data << std::endl;
	// std::cout<< node1.right->data << std::endl;
	// std::cout<< node1.parent->data << std::endl;


	// Option-2. Creating memory in the heap. We can keep creating pointers to different nodes and then write a function to add edge
	// which basically adds connection pointing the parent to the child.
	tree bin_tree;
	binary_tree* node1 = bin_tree.create_node(1);
	binary_tree* node2 = bin_tree.create_node(2);
	binary_tree* node3 = bin_tree.create_node(3);
	binary_tree* node4 = bin_tree.create_node(4);
	binary_tree* node5 = bin_tree.create_node(5);
	// binary_tree* node6 = bin_tree.create_node(6);
	
	// Some Tree-1
	// bin_tree.addConnection(node1, NULL, node2, node3);
	// bin_tree.addConnection(node2, node1, node4, NULL);
	// bin_tree.addConnection(node3, node1, node5, node6);


	// Tree 2 and some traversals
	bin_tree.addConnection(node1,NULL,node2,node3);
	bin_tree.addConnection(node2,node1,node4,node5);
	bin_tree.printLevelOrder();
	std::cout<< "Preorder" << std::endl;
	bin_tree.preorder();
	std::cout<< std::endl<< std::endl;
	std::cout<< "Inorder" << std::endl;
	bin_tree.inorder();
	std::cout<< std::endl<< std::endl;
	std::cout<< "Postorder" << std::endl;
	bin_tree.postorder();


	// Tree -3
	
	return 0;
}




