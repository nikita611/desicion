#include <iostream>
#include <vector>
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

template<typename T>
vector<T> parseStringToNumber(string str)
{
	bool b;
	if (typeid(T).name == "int")
		b = true;
	if (typeid(T).name == "double" || typeid(T).name == "float")
		b = false;

    vector<T> vec;
    for (int beg = 0, end = 0; end != str.size() ; end++)
    {
        if (str[end] == ' ')
        {
			if(b)
				vec.push_back( atoi(str.substr(beg, end - beg).c_str()) );
			else vec.push_back( atof(str.substr(beg, end - beg).c_str()) );
            beg = ++end;
        }

        if (end == str.size() - 1)
        {
			if(b)
				vec.push_back( atoi(str.substr(beg, end - beg + 1).c_str()) );
			else vec.push_back( atof(str.substr(beg, end - beg + 1).c_str()) );
            break;
        }
        
    }
    
    return vec;
    
}
int main()
{
	
	return 0;
}