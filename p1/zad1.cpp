#include <iostream>
#include <fstream>
#include <sstream>
#include <list>
#include <tuple>
#include <chrono>

using namespace std;

char* rjust(char* str, int64_t length, char* character) {
	int i;
	int64_t just_len = length - strlen(str);

	char* result = (char*)malloc(length + 1);
	for (i = 0; i < just_len; i++) result[i] = character[0];
	for (; i < length + 1; i++) result[i] = str[i - just_len];
	return result;
}

struct data_s {
	char** strings;
	int64_t* lengths;
	char** characters;
	int64_t size;
};

char* str_to_char(string str) {
	char* chr_p = new char[str.size() + 1];
	std::copy(str.begin(), str.end(), chr_p);
	chr_p[str.size()] = '\0';
	return chr_p;
}

data_s load_data() {
	string line;
	fstream fs;

	fs.open("data.csv", ios::in);
	getline(fs, line);
	int64_t datasize = stoi(line);

	char** strings = (char**)malloc(sizeof(char*) * datasize);
	int64_t* lengths = (int64_t*)malloc(sizeof(int64_t) * datasize);
	char** characters = (char**)malloc(sizeof(char*) * datasize);

	int64_t i = 0;
	while (getline(fs, line)) {
		string str = line.substr(0, line.find(','));
		strings[i] = str_to_char(str);

		string num = line.substr(line.find(',') + 1, line.rfind(',') - line.find(',') - 1);
		lengths[i] = stoi(num);

		string character = line.substr(line.rfind(',') + 1, line.length() - line.rfind(',') - 1);
		characters[i] = str_to_char(character);

		i++;
	}

	fs.close();

	data_s data;
	data.strings = strings;
	data.lengths = lengths;
	data.characters = characters;
	data.size = datasize;
	return data;
}

void test1() {
	data_s data = load_data();
	char** strings = data.strings;
	int64_t* lengths = data.lengths;
	char** characters = data.characters;
	int64_t size = data.size;

	ofstream result_file("resut_cpp.txt");
	for (int64_t i = 0; i < size; i++) {
		result_file << rjust(strings[i], lengths[i], characters[i]) << endl;
	}
	result_file.close();
}

void test2() {
	data_s data = load_data();
	char** strings = data.strings;
	int64_t* lengths = data.lengths;
	char** characters = data.characters;
	int size = data.size;
	int n = 7000;
	int i, j;
	chrono::time_point<std::chrono::steady_clock> start, end;

	start = chrono::steady_clock::now();
	for (j = 0; j < n; j++) {
		for (i = 0; i < size; i++) {
			rjust(strings[i], lengths[i], characters[i]);
		}
	}
	end = chrono::steady_clock::now();
	chrono::duration<double> func_time = end - start;

	start = chrono::steady_clock::now();
	for (j = 0; j < n; j++) {
		for (i = 0; i < size; i++) {
		}
	}
	end = chrono::steady_clock::now();
	std::chrono::duration<double> loop_time = end - start;

	std::chrono::duration<double> final_time = func_time - loop_time;

	ofstream result_file("performace_resut_cpp.txt");
	result_file << "Datasize: " << size << ", number of loops: " << n << endl;
	result_file << "Loop with function time: " << func_time.count() << endl;
	result_file << "Loop without function time: " << loop_time.count() << endl;
	result_file << "Final time: " << final_time.count() << endl;
	result_file.close();
}

int main(int argc, char** argv) {
	if (argc >= 2) {
		if (std::string(argv[1]) == "test1") {
			test1();
		}
		else if (std::string(argv[1]) == "test2") {
			test2();
		}
	}
}