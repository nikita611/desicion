#include <iostream>
#include <vector>
using namespace std;

int checksum(vector<int> vec)
{
	const int seed = 113;
    const unsigned long long limit = 10000007;


    unsigned long long sum = 0;
    for (int i = 0; i < vec.size(); i++)
    {
        sum = (sum + vec[i]) * 113;
            sum %= limit;
    }

    return sum;
}

int main()
{
	return 0;
}