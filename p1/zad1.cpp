#include <iostream>
#include <fstream>
#include <sstream>
#include <list>
#include <tuple>

using namespace std;

string rjust(string str, int64_t length, string character) {
	int64_t just_len = length - str.length();
	just_len = just_len > 0 ? just_len : 0;
	string result = string(just_len, character[0]) + str;
	return result;
}

list<tuple<string, int64_t, string>> load_data() {
	string line;
	fstream fs;
	list<tuple<string, int64_t, string>> result;

	fs.open("data.csv", ios::in);

	while (getline(fs, line)) {
		string str = line.substr(0, line.find(','));
		string num = line.substr(line.find(',') + 1, line.rfind(',') - line.find(',') - 1);
		string character = line.substr(line.rfind(',') + 1, line.length() - line.rfind(',') - 1);
		tuple<string, int64_t, string> tup(str, stoi(num), character);
		result.push_back(tup);
	}

	fs.close();

	return result;
}

int main() {
	list<tuple<string, int64_t, string>> data = load_data();
	ofstream result_file("result_cpp.txt");
	for (std::list<tuple<string, int64_t, string>>::iterator iter = data.begin(); iter != data.end(); iter++)
		result_file << rjust(get<0>(*iter), get<1>(*iter), get<2>(*iter)) << endl;
	result_file.close();
}