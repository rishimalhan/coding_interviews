#include <cmath>
#include <cstdio>
#include <vector>
#include <iostream>
#include <algorithm>
#include <unordered_map>
using namespace std;


int main() {
    /* Enter your code here. Read input from STDIN. Print output to STDOUT */   
    int no_ips;
    std::vector<int> int_vec;
    std::cin >> no_ips;
    int val;
    for (int i=0; i<no_ips; ++i)
    {
        std::cin >> val;
        int_vec.push_back(val);
    }
    int no_queries;
    std::cin >> no_queries;
    int query;
    // Check for repeated queries and store the data
    std::unordered_map<int, std::string> str_map;
    std::unordered_map<int, int> id_map;
    std::string resp;
    int index;
    std::vector<int>::iterator lower_val;
    std::vector<int>::iterator upper_val;
    for (int i=0; i<no_queries; ++i)
    {
        std::cin >> query;
        // If this query has occurred previosly use that value
        if (str_map.count(query)>0)
        {
            std::cout<< str_map.find(query)->second << " " << id_map.find(query)->second << "\n";
            continue;
        }

        lower_val = std::lower_bound(int_vec.begin(),int_vec.end(),query);
        index = lower_val - int_vec.begin() + 1;

        if (*lower_val==query) // lower bound returns the same value if present
        {
            resp = "Yes";
            std::cout<< resp << " " << index << "\n";
            str_map.emplace(query,resp);
            id_map.emplace(query,index);
        }
        else
        {
            resp = "No";
            std::cout<< resp << " " << index << "\n";
            str_map.emplace(query,resp);
            id_map.emplace(query,index);
        }
        
    }
    return 0;
}