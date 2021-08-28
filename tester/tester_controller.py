import subprocess
import functools
from backend_tester import *
from concurrent.futures import ThreadPoolExecutor, as_completed


def test_results():

    with open("../tester/profile_temp.c","w") as f:
        f.write(profile(sys.argv[1]))

    subprocess.call(["gcc ../tester/profile_temp.c"], shell = True)
    subprocess.call(["./a.out < inp.txt > unop_output.txt"], shell = True)

    with open("../tester/profile.txt","r") as prof:
        string = prof.read().split('\n')
        memory_unoptimized = float(string[0])
        time_unoptimized = float(string[1])

    with open("../tester/profile_temp.c","w") as f:
        f.write(profile(sys.argv[2]))

    subprocess.call(["gcc ../tester/profile_temp.c"], shell = True)
    subprocess.call(["./a.out < inp.txt > op_output.txt"],shell=True)

    with open("../tester/profile.txt","r") as prof:
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



def parallel_shit():
    processes = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        for i in range(10):
            processes.append(executor.submit(test_results))

    return processes


def normal_shit():
    processes = []
    for i in range(10):
        processes.append(test_results())
    return processes

processes = normal_shit()
##print(processes)
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


json_out = "{";
json_out += "\"unop_time\" : \"" + str(time_unoptimized) + " sec\","
json_out += "\"op_time\" : \"" + str(time_optimized) + " sec\","
json_out += "\"time_diff\" : \"" + str(time_diff) + " sec\","
json_out += "\"p_dec_t\" : \"" + str(percent_increase) + " %\","
# print(f"Unoptimized execution time : {time_unoptimized} sec")
# print(f"optimized execution time : {time_optimized} sec")
# print(f"Time_difference : {time_diff} sec")
# print(f"Percent_decrease : {percent_increase}")
#
# print("\n\n-------------------------------------------------------------------------------------\n\n")


# Memory stuff

memory_diff = memory_unoptimized-memory_optimized
percent_increase = (memory_diff/memory_unoptimized)*100


json_out += "\"unop_mem\" : \"" + str(memory_unoptimized) + " kB\","
json_out += "\"op_mem\" : \"" + str(memory_optimized) + " kB\","
json_out += "\"mem_diff\" : \"" + str(memory_diff) + " kB\","
json_out += "\"p_dec_m\" : \"" + str(percent_increase) + " %\""
json_out += "}";
# print(f"unoptimized memory usage : {memory_unoptimized} kB")
# print(f"optimized memory usage : {memory_optimized} kB")
# print(f"memory_difference : {memory_diff} kB")
# print(f"Percent_decrease : {percent_increase}")

print(json_out)
subprocess.call(["rm -r __pycache__"],shell=True)
