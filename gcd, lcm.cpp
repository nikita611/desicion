#include <iostream>
using namespace std;

int gcd(int a, int b)
{
	while (a != b)
	{
		if (a < b)
			b -= a;
		if (b < a)
			a -= b;
	}
	return a;

}

int lcm(int a, int b)
{
	return a * b / gcd(a, b);
}

int main()
{
	
	return 0;
}