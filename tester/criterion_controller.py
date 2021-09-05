import subprocess
import functools
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

    print(f"After warmup...\n\nAverage memory usage for unoptimized code : {total_mem_unop/3} KB\n")
    print(f"Average time usage for unoptimized code : {total_time_unop/3} s\n")
    print(f"Average memory usage for optimized code : {total_mem_op/3} KB\n")
    print(f"Average time usage for optimized code : {total_time_op/3} s\n")

    precedent = (max(total_time_unop, total_time_op))/3
    return precedent

def execute(runs):
    print("executing...")
    total_time_unop = 0
    total_time_op = 0
    total_mem_unop = 0
    total_mem_op = 0
    for run in range(runs):
        subprocess.call(["./unop.out < inp.txt > unop_output.txt"], shell = True)
        mem, time = read_profile()
        total_mem_unop += mem
        total_time_unop += time

        subprocess.call(["./op.out < inp.txt > unop_output.txt"], shell = True)
        mem, time = read_profile()
        total_mem_op += mem
        total_time_op += time

    print(f"After execution...\n\nAverage memory usage for unoptimized code : {total_mem_unop/runs} KB\n")
    print(f"Average time usage for unoptimized code : {total_time_unop/runs} s\n")
    print(f"Average memory usage for optimized code : {total_mem_op/runs} KB\n")
    print(f"Average time usage for optimized code : {total_time_op/runs} s\n")

def validate():
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
    print(f"Trying {runs} runs. Estimated completion time : {runs * precedent}. Do you wish to continue?[Y/n]")
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
