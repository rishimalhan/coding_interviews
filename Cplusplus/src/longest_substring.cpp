#include <iostream>
#include <vector>

// Longest substring without repeating characters
int lengthOfLongestSubstring(string s) {
	int ptr = 0;
	int max_length = 0;
	std::vector<char> sub_str;
	while(ptr!=s.length())
	{
	    if (std::count(sub_str.begin(),sub_str.end(),s[ptr])==0)
	        sub_str.push_back(s[ptr]);
	    else
	    {
	        sub_str.erase(sub_str.begin(),++std::find(sub_str.begin(),sub_str.end(),s[ptr]));
	        sub_str.push_back(s[ptr]);
	    }
	    
	    if (max_length < (int) sub_str.size())
	        max_length = sub_str.size();
	    
	    ptr++;
	}
	return max_length;
}