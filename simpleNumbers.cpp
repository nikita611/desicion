#include <iostream>
#include <vector>
using namespace std;
 
int main()
{
	int n;
	cin >> n;
	
	vector<int> v;
	v.push_back(2);
	int cur;
	bool isSimple;

	for (int i = 3; i < n; i++)
	{
		isSimple = true;
		for (int j = 0; j < v.size(); j++)
		{
			if (i % v[j] == 0)
			{
				isSimple = false;
				break;
			}
		}
		if (isSimple)
			v.push_back(i);
	}

	for (int i = 0; i < v.size(); i++)
		cout << v[i] << endl;

    return 0;
}