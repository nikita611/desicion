#include <iostream>
#include <vector>
#include <cmath>
using namespace std;

int capacity(int numb)
{
	int i = 0;
	while (numb != 0)
	{
		numb /= 10;
		++i;
	}
	
	return i;
}

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