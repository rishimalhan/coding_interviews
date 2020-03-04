// Find indices of array such that a+b=c+d

#include <iostream>
#include <vector>
#include <map>
#include <algorithm>
#include <set>

bool isUnique(std::vector<int> v)
{
    std::set<int> s(v.begin(), v.end());
	return s.size() == v.size();
}

std::vector<std::vector<int>> find_indices(int* ptr, int no_elements)
{
	std::vector<std::vector<int>> indices;

	std::map<int,std::vector<int>> ab_sums; // Stores the sums for ij elements as a map
	std::vector<int> ij_index;
	std::vector<int> temp;

	// First iterate through the  determine the 
	for (int i=0; i<no_elements-1; ++i)
	{
		for (int j=i+1; j<no_elements; ++j)
		{
			int sum = ptr[i] + ptr[i+1];

			if (ab_sums.count(sum))
			{
				auto iterator = ab_sums.find(sum);
				ij_index = iterator->second;
				ij_index.push_back(i); ij_index.push_back(j);	
				ij_index.clear();
			}
			else
			{
				ij_index.push_back(i); ij_index.push_back(j);
				ab_sums.emplace( sum, ij_index );	
				ij_index.clear();
			}
		}	
	}
	ij_index.clear();

	for (int k=0; k<no_elements-1; ++k)
	{
		for (int l=k+1; l<no_elements; ++l)
		{
			int sum = ptr[k] + ptr[l];
			if (ab_sums.count(sum)) // If this sum is there, then add i,j, k and l to list
			{
				auto iterator = ab_sums.find(sum);
				std::vector<int> ij_index = iterator->second;
				for (int j=0; j<ij_index.size(); j+=2)
				{
					temp.push_back(ij_index[j]); //i
					temp.push_back(ij_index[j+1]); //j
					temp.push_back(k);
					temp.push_back(l);

					if (isUnique(temp))
						indices.push_back(temp);
					temp.clear();
				}
			}
		}
	}

	return indices;
};

void print_vec(std::vector<std::vector<int>> &ip_vec)
{
	for(int i=0; i<ip_vec.size(); ++i)
	{
		std::cout<< "Indices: ";
		for (int j=0; j<ip_vec[i].size(); j+=4)
		{
			std::cout<< ip_vec[i][j]+1 << " , " << ip_vec[i][j+1]+1 << " , " << ip_vec[i][j+2]+1 << " , " << ip_vec[i][j+3]+1 <<"\t";
		}
		std::cout<< std::endl;
	}
}

int main(int argc, char** argv)
{
	// Create a sample array
	int ip_arr[7] = {1,5,4,6,3,3,4};
	std::vector<std::vector<int>> indices = find_indices(ip_arr, (sizeof(ip_arr)/sizeof(*ip_arr)));
	print_vec(indices);
	return 0;
}