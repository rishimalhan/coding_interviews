// Given an array and an integer K, find the maximum for each and every contiguous subarray of size k.

#include <iostream>
#include <deque> 
#include <limits>
using namespace std;

void printKMax(int arr[], int n, int k){
    if (n==0)
        return;
    int index = 0;
    int max_val;
    std::deque<int> sld_win; // Create a sliding window
    max_val = -std::numeric_limits<int>::max();
    while(index!=n){
        if (sld_win.size()==k){
            std::cout<< max_val << " ";
            // Before popping the back value, check if max value is the same
            if (arr[sld_win.back()]==max_val){
                sld_win.pop_back();
                max_val = -std::numeric_limits<int>::max();
                for (int i=0; i<k-1; ++i){
                    if (max_val<arr[sld_win.at(i)]){
                        max_val = arr[sld_win.at(i)];
                    }
                }
            }
            else
                sld_win.pop_back();
            sld_win.push_front(index);
        }
        else{
            sld_win.push_front(index);
        }

        if (max_val<arr[index]){
            max_val = arr[index];
        }
        index ++;
    }  
    std::cout<< max_val << "\n";
}

int main(){
  
	int t;
	cin >> t;
	while(t>0) {
		int n,k;
    	cin >> n >> k;
    	int i;
    	int arr[n];
    	for(i=0;i<n;i++)
      		cin >> arr[i];
    	printKMax(arr, n, k);
    	t--;
  	}
  	return 0;
}