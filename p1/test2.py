import subprocess
import time
from zad1_utils import load_data, rjust_my, save_result
from dataset_generator import generate_dataset

data = load_data()
n = 5000
results = f'datasize - {len(data)}\nnumber of loops - {n}\n'

start = time.time()
for _ in range(n):
    for x in data:
        rjust_my(x[0], x[1], x[2])
end = time.time()
my_time = end - start

start = time.time()
for _ in range(n):
    for x in data:
        x[0].rjust(x[1], x[2])
end = time.time()
python_time = end - start

start = time.time()
for _ in range(n):
    for x in data:
        pass
end = time.time()
loop_time = end - start

results += f'empty loop time: {loop_time}s\n'
results += f'my implementation time: {my_time} ({my_time - loop_time}s without loop time)\n'
results += f'python implementation time: {python_time} ({python_time - loop_time}s without loop time)\n'
save_result([results], "performance_result_py.txt")