import subprocess
import functools
from backend_tester import *
from concurrent.futures import ThreadPoolExecutor, as_completed


def test_results():

    with open("profile_temp.c","w") as f:
        f.write(profile(sys.argv[1]))

    subprocess.call(["gcc","profile_temp.c"])
    subprocess.call(["./a.out < inp > unop_output"],shell=True)

    with open("profile","r") as prof:
        string = prof.read().split('\n')
        memory_unoptimized = float(string[0])
        time_unoptimized = float(string[1])

    with open("profile_temp.c","w") as f:
        f.write(profile(sys.argv[2]))

    subprocess.call(["gcc","profile_temp.c"])
    subprocess.call(["./a.out < inp > op_output"],shell=True)

    with open("profile","r") as prof:
        string = prof.read().split('\n')
        memory_optimized = float(string[0])
        time_optimized = float(string[1])


    # time_diff = time_unoptimized-time_optimized
    # percent_increase = (time_diff/time_unoptimized)*100

    return (time_optimized,time_unoptimized,memory_optimized,memory_unoptimized)


time_optimized = 0.0
time_unoptimized = 0.0
memory_optimized = 0.0
memory_unoptimized = 0.0



def parallel():
    processes = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        for i in range(10):
            processes.append(executor.submit(test_results))

    return processes


def normal():
    processes = []
    for i in range(10):
        processes.append(test_results())
    return processes

processes = normal()
#print(processes)
for task in processes:
    time_optimized += task[0]
    time_unoptimized += task[1]
    memory_optimized += task[2]
    memory_unoptimized += task[3]

time_optimized = time_optimized/10
time_unoptimized = time_unoptimized/10
memory_optimized = memory_optimized/10
memory_unoptimized = memory_unoptimized/10


# Time stuff

time_diff = time_unoptimized - time_optimized
percent_increase = (time_diff / time_unoptimized) * 100

print(f"Unoptimized execution time : {time_unoptimized} sec")
print(f"optimized execution time : {time_optimized} sec")
print(f"Time_difference : {time_diff} sec")
print(f"Percent_decrease : {percent_increase}")

print("\n\n-------------------------------------------------------------------------------------\n\n")


# Memory stuff

memory_diff = memory_unoptimized-memory_optimized
percent_increase = (memory_diff/memory_unoptimized)*100


print(f"unoptimized memory usage : {memory_unoptimized} kB")
print(f"optimized memory usage : {memory_optimized} kB")
print(f"memory_difference : {memory_diff} kB")
print(f"Percent_decrease : {percent_increase}")


subprocess.call(["rm -r __pycache__"],shell=True)
