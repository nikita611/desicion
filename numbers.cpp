#include <iostream>
#include <vector>
using namespace std;

vector<int> numbers(int N)
{
	int n = N;
	vector <int> Vector;
	int var;
	int j = capacity(N);

    for(int i = 0; i < j;i++)
    {
		var = n;
		while (var > 10)
			var /= 10;
		Vector.push_back(var);

		n -= var * pow(10, capacity(n) - 1);
    }

	return Vector;
}

int main()
{
	
	return 0;
}