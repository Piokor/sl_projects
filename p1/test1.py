from zad1_utils import load_data, rjust_my, save_result
from dataset_generator import generate_dataset
import filecmp
import subprocess

generate_dataset(1000)
# load generated data
data = load_data()

result_standard = []
result_my = []

# perform python function tests
for x in data:
    result_standard.append(x[0].rjust(x[1], x[2]))
    result_my.append(rjust_my(x[0], x[1], x[2]))

# save python results
save_result(result_standard, "result_standard.txt")
save_result(result_my, "result_my.txt")

# perform c++ function tests and save results
c_proc = subprocess.Popen("rjust_cpp.exe test1")
c_proc.wait()

result_my = filecmp.cmp("result_standard.txt", "result_my.txt")
print("My python implementation correction test result: " + "Passed" if result_my else "Failed")

result_cpp = filecmp.cmp("result_standard.txt", "resut_cpp.txt")
print("My c++ implementation correction test result: " + "Passed" if result_cpp else "Failed")
