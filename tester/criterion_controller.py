import subprocess
import functools
from tqdm import tqdm
import statistics

from backend_tester import *

def compile():
    subprocess.call(["touch profile.txt"], shell = True)

    ''' compiling unoptimized file '''
    with open("../tester/profile_temp.c","w") as f:
        f.write(profile(sys.argv[1]))
    subprocess.call(["gcc ../tester/profile_temp.c -o unop.out"], shell = True)

    ''' compiling optimized file '''
    with open("../tester/profile_temp.c","w") as f:
        f.write(profile(sys.argv[2]))
    subprocess.call(["gcc ../tester/profile_temp.c -o op.out"], shell = True)

def read_profile():
    with open("../tester/profile.txt","r") as prof:
        string = prof.read().split('\n')
        memory = float(string[0])
        time = float(string[1])
        return memory, time

def warmup():
    print("warming up .....")
    total_time_unop = 0
    total_time_op = 0
    total_mem_unop = 0
    total_mem_op = 0
    for run in range(3):
        subprocess.call(["./unop.out < inp.txt > unop_output.txt"], shell = True)
        mem, time = read_profile()
        total_mem_unop += mem
        total_time_unop += time

        subprocess.call(["./op.out < inp.txt > unop_output.txt"], shell = True)
        mem, time = read_profile()
        total_mem_op += mem
        total_time_op += time

    print(f"After warmup...\n\n\tAverage memory usage for unoptimized code : {total_mem_unop/3} KB\n")
    print(f"\tAverage time usage for unoptimized code : {total_time_unop/3} s\n")
    print(f"\tAverage memory usage for optimized code : {total_mem_op/3} KB\n")
    print(f"\tAverage time usage for optimized code : {total_time_op/3} s\n")

    precedent = (max(total_time_unop, total_time_op))/3
    return precedent

def execute(runs):
    # print("executing...")
    total_time_unop = 0
    total_time_op = 0
    total_mem_unop = 0
    total_mem_op = 0

    max_time_unop = 0
    max_time_op = 0
    max_mem_unop = 0
    max_mem_op = 0

    min_time_unop = 100000000
    min_time_op = 100000000
    min_mem_unop = 100000000
    min_mem_op = 100000000

    list_time_unop = []
    list_mem_unop = []
    list_time_op = []
    list_mem_op = []

    for run in tqdm(range(runs), desc = "Executing..."):
        subprocess.call(["./unop.out < inp.txt > unop_output.txt"], shell = True)
        mem, time = read_profile()
        total_mem_unop += mem
        total_time_unop += time
        if time > max_time_unop:
            max_time_unop = time
        elif time < min_time_unop:
            min_time_unop = time

        if mem > max_mem_unop:
            max_mem_unop = mem
        elif mem < min_mem_unop:
            min_mem_unop = mem

        list_time_unop.append(time)
        list_mem_unop.append(mem)

        subprocess.call(["./op.out < inp.txt > unop_output.txt"], shell = True)
        mem, time = read_profile()
        total_mem_op += mem
        total_time_op += time
        if time > max_time_op:
            max_time_op = time
        elif time < min_time_op:
            min_time_op = time

        if mem > max_mem_op:
            max_mem_op = mem
        elif mem < min_mem_op:
            min_mem_op = mem

        list_time_op.append(time)
        list_mem_op.append(mem)


    print(f"After execution...\n\n\tMemory usage for unoptimized code => Average : {total_mem_unop/runs} KB, Max : {max_mem_unop} KB, Min : {min_mem_unop} KB, Std Dev : {statistics.stdev(list_mem_unop)} KB\n")
    print(f"\tRun time for unoptimized code => Average : {total_time_unop/runs} KB, Max : {max_time_unop} s, Min : {min_time_unop} s, Std Dev : {statistics.stdev(list_time_unop)} s\n")
    print(f"\tMemory usage for optimized code => Average : {total_mem_op/runs} KB, Max : {max_mem_op} KB, Min : {min_mem_op} KB, Std Dev : {statistics.stdev(list_mem_op)} KB\n")
    print(f"\tRun time for optimized code => Average : {total_time_op/runs} KB, Max : {max_time_op} s, Min : {min_time_op} s, Std Dev : {statistics.stdev(list_time_op)} s\n")

def validate():
    PYTHON_FACTOR = 5
    precedent = warmup()
    # deciding no of runs
    runs = 0
    if(precedent < 1.00):
        runs = 1000
    elif(precedent < 5):
        runs = 200
    elif(precedent < 10):
        runs = 100
    else:
        runs = 10
    print(f"Trying {runs} runs. Estimated completion time : {runs * precedent * PYTHON_FACTOR} s. Do you wish to continue?[Y/n]")
    choice = input().lower()
    if(choice == "y" or choice == ''):
        execute(runs)
    else:
        print("Do you wish to enter number of runs?[Y/n]")
        choice = input().lower()
        if(choice == "y" or choice == ''):
            print("Enter number of runs :")
            runs = int(input())
            execute(runs)
        return

compile()
validate()
