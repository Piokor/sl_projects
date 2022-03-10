from zad1 import load_data, rjust_my, save_result
from dataset_generator import generate_dataset
import filecmp
import subprocess

generate_dataset(1000)

data = load_data()

result_standard = []
result_my = []

for x in data:
    result_standard.append(x[0].rjust(x[1], x[2]))
    result_my.append(rjust_my(x[0], x[1], x[2]))
c_proc = subprocess.Popen("rjust_cpp.exe")
c_proc.wait()

save_result(result_standard, "result_standard.txt")
save_result(result_my, "result_my.txt")

print(filecmp.cmp("result_standard.txt", "result_my.txt"))
print(filecmp.cmp("result_standard.txt", "resut_cpp.txt"))