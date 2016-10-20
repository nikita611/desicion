#include <iostream>
#include <string>
#include <vector>
#include <cstdlib>
using namespace std;

int main()
{
	string str;
	getline(cin, str);
	vector<int> vec;

	for (int beg = 0, end = 0; end != str.size() ; end++)
	{


		if (str[end] == ' ')
		{
			vec.push_back( atoi(str.substr(beg, end - beg).c_str()) );
			beg = ++end;
		}

		if (end == str.size() - 1)
		{
			vec.push_back( atoi(str.substr(beg, end - beg + 1).c_str()) );
			break;
		}
		
	}

	for (int i = 0; i < vec.size(); i++)
		cout << vec[i] << endl;

	system("pause");

	return 0;
}