#include <iostream>
#include <vector>
#include <sstream>
#include <string>
// #include <bits/stdc++.h> 



// Trying character pointer
// int main(int argc, char** argv)
// {
// 	char *c;
//     std::cout<< "Enter values" << std::endl;
//     std::cin >> c;
//     std::cout<< "Character is: " << c << std::endl;
// 	return 0;
// }





// STD vector for storing a list. Bascially dictionary type thing
// int main(int argc, char** argv)
// {
// 	std::vector<std::string> eng_digits;
// 	eng_digits.push_back("one");
// 	eng_digits.push_back("two");
// 	eng_digits.push_back("three");

// 	for (int i=0; i<eng_digits.size(); ++i)
// 		std::cout<< eng_digits[i] << std::endl;
// 	return 0;
// }






// Usage of pointers
// int main(int argc, char** argv)
// {
// 	int a[] = {50,40,12};
// 	int *p = a;
	
// 	std::cout<< p[1] << std::endl;
// 	return 0;
// }






// Usage of arrays
// int main(int argc, char** argv)
// {
// 	int a[4];
// 	for (int i=0; i<4; ++i)
// 		std::cin >> a[i];
// 	std::cout<< a[0] << std::endl;
// 	std::cout<< a[1] << std::endl;
// 	std::cout<< a[2] << std::endl;
// 	return 0;
// }







// Usage of parsing a command line or string
// int main(int argc, char** argv)
// {
// 	std::string ip;
// 	std::cin >> ip;
// 	std::string line;
// 	std::stringstream ip_str(ip);
// 	while (std::getline(ip_str,line,','))
// 		std::cout<< line << std::endl;
// 	return 0;
// }






// Advanced usage of parsing command line or string
// int main(int argc, char** argv)
// {
// 	/* Enter your code here. Read input from STDIN. Print output to STDOUT */  
//     // Read Value of n and q
//     int n,q;
//     std::cin >> n >> q;
//     std::vector<std::vector<int>> matrix;
//     matrix.resize(n);

//     // Fill the matrix till n lines
//     int ip;
//     for (int i=0; i<n; ++i)
//     {
//         std::cin >> ip;
//         while(std::cin)
//         {
//             matrix[i].push_back(ip);
//             std::cin >> ip;
//             if (std::cin.get()=='\n')
//             {
//                 matrix[i].push_back(ip);
//                 break;
//             }
//         }
//     }
//     return 0;
// }







// Parsing using stringstream with comma separated string
// int main(int argc, char** argv)
// {
// 	std::stringstream op_str("5,4");
// 	int curr_no;
// 	char ch;
// 	while(op_str>>curr_no)
// 	{
// 		std::cout<< curr_no << std::endl;
// 		op_str >> ch;
// 	}
// 	return 0;
// }







// Classes and constructors
// Operator Overloading
// class Box{
//     public:
//     int l,b,h;
//     Box()
//     {
//         l=0; b=0; h=0;
//     }

//     Box(int length, int breadth, int height)
//     {
//         l = length;
//         b = breadth;
//         h = height;
//     }

//     // Copy constructor
//     Box(const Box &ip_box)
//     {
//         this->l = ip_box.l;
//         this->b = ip_box.b;
//         this->h = ip_box.h;
//     }

//     int getLength()
//     {
//         return this->l;
//     }

//     int getBreadth()
//     {
//         return this->l;
//     }

//     int getHeight()
//     {
//         return this->l;
//     }

//     long long CalculateVolume()
//     {
//         return l*b*h;
//     }

//     bool operator < (const Box &B)
//     {
//         if ( (this->l < B.l) || (this->b < B.b && this->l==B.l) || (this->h < B.h && this->b==B.b && this->l==B.l) )
//             return true;
//         else {
//             return false;
//         }

//     }

//     friend std::ostream& operator << (std::ostream &os, const Box &out_box)
// 	{
// 		os << out_box.l << " " << out_box.b << " " << out_box.h << std::endl;
// 		return os;
// 	}
// };


// int main(int argc, char** argv)
// {
// 	Box a;
// 	a.l = -1;
// 	a.b = 1;
// 	a.h = 1;
// 	Box b;
// 	// std::cout<< b.l << std::endl;
// 	if(a < b)
// 		std::cout<< "Fuck" << std::endl;

// 	std::cout<< a;
// 	return 0;
// };





//
// int main(int argc, char** argv)
// {
// 	return 0;
// }



// template <typename T>
// class Foo {
//     T tVar;
//     public:
//     	Foo(){}
//         Foo(T t): tVar(t) {}
// };

// class FooDerived: public Foo<std::string>{};

// int main() {
//     FooDerived d;
//     return 0;
// }


// int main()
// {
//  // 	int a = 2<<3;
// 	// std::cout<< a << std::endl;
	
// 	// std::cout<< (int) 8.8 << std::endl;
// 	std::map<char,int> fuck;
// 	fuck['1'] = 1;
// 	std::cout<< fuck['1'] << std::endl;
// 	return 0;
// }






// // Arrays
// int main(int argc, char** argv)
// {
// 	// One dimensional array
// 	int a[5] = {1,2,3,4,5};
// 	for(int i=0; i<5; ++i)
// 		std::cout<<	a[i] << ",";
// 	std::cout<< std::endl;

// 	// Multi-dimensional array
// 	int b[5][2] = {1,2,3,4,5, 6,7,8,9,10}; // Fills the matrix row wise
// 	for (int i=0; i<5; ++i)
// 		for (int j=0; j<2; ++j)
// 			std::cout<< b[i][j] << ",";
// 	std::cout<< std::endl;
// 	return 0;
// }







// // Class inheritance
// // A public class becomes public, protected, private depending on the cast
// // A protected class becomes protected, protected, private depending on cast
// // A private class becomes private, private, private  depending on the cast
// class A
// {
// public:
// 	int class_var = 1;
// };

// class B : protected A
// {
// public:
// 	int class_var2 = 2;
// };

// int main(int argc, char** argv)
// {
// 	A a;
// 	std::cout<< a.class_var << std::endl;

// 	B b;
// 	// std::cout<< b.class_var << std::endl;
// 	std::cout<< b.class_var2 << std::endl;
// 	return 0;
// }






// // Virtual functions
// // Primarily used for polymorphism.
// // Inherited class can use the same function name but a different function definition
// class area
// {
// public:
// 	int compute_area(int a, int b)
// 	{
// 		return a*b;
// 	}
// };

// class modf_area : public area
// {
// public:
// 	int compute_area(int a, int b)
// 	{
// 		return 2*a*b;
// 	}
// };

// int main(int argc, char** argv)
// {
// 	area A;
// 	std::cout<< A.compute_area(5,10) << std::endl;

// 	modf_area B;
// 	std::cout<< B.compute_area(5,10) << std::endl;	
// 	return 0;
// }







// // Strings and char pointers
// int main(int argc, char** argv)
// {
// 	std::string my_str = "hello";
// 	int i=0;
// 	while(my_str[i])
// 	{
// 		std::cout<< my_str[i] << std::endl;
// 		++i;
// 	}
// 	// char ch[] = my_str;
// 	// ch = &my_str;
// 	return 0;
// }





// #include <queue>
// // C++ priority queue
// int main(int argc, char** argv)
// {
// 	std::priority_queue <std::pair<int,int>> q;
// 	q.push(std::make_pair(10,1));
// 	q.push(std::make_pair(20,2));
// 	q.push(std::make_pair(5,3));

// 	std::pair<int, int> top_elmnt = q.top(); 
// 	std::cout<< top_elmnt.second << std::endl;
// 	q.pop();
// 	top_elmnt = q.top();
// 	std::cout<< top_elmnt.second << std::endl;
// 	q.pop();
// 	return 0;
// }





// #include <map>
// struct node
// {
// 	int data;
// 	node* parent;
// };

// int main(int argc, char** argv)
// {
// 	node* root = new node;
// 	root->data = 15;
// 	root->parent = NULL;
// 	std::map<int,node*> ord_map;
// 	ord_map[0] = root;
// 	return 0;
// }






#include <set>
int main(int argc, char** argv)
{
	std::string str1 = "Hello";
	std::set<char> s;
	s.insert(str1[0]);
	if (s.count('S'))
		std::cout<< "Hello" << std::endl;
	return 0;
}






// // C++ pointers
// int* p =  new int;
// *p = 2;
// std::cout<< *p << std::endl;
// p[0] = 3;
// p[1] = 4;
// std::cout<< *(p+1) << std::endl;






// int getTriangleArea(vector<int> x, vector<int> y) {
//     // Computing area of triangle using semi-perimeter method
//     // Length of three sides are: a,b,c
//     double a,b,c;
//     a = pow( pow(x[0]-x[1],2) + pow(y[0]-y[1],2), 0.5);
//     b = pow( pow(x[1]-x[2],2) + pow(y[1]-y[2],2), 0.5);
//     c = pow( pow(x[2]-x[0],2) + pow(y[2]-y[0],2), 0.5);
//     double s = (a + b + c)/2;

//     return (long int) round(pow( s*(s-a)*(s-b)*(s-c) ,0.5));
// }



