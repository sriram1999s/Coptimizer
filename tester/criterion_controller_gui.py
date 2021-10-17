import subprocess
import functools
from tqdm import tqdm
import statistics
import sys

sys.argv = ['criterion_controller_gui.py', 'testfile.c', 'output.c']
from backend_tester import *

ret_dict = {}
def compile():
    import json
    global ret_dict
    subprocess.run(["touch profile.txt"], shell = True)

    ''' compiling unoptimized file  :  # f.write(profile(sys.argv[1]))'''
    with open("../tester/profile_temp.c","w") as f:
        f.write(profile(sys.argv[1]))
    subprocess.run(["gcc ../tester/profile_temp.c -o unop.out"], shell = True)

    ''' compiling optimized file  :  # f.write(profile(sys.argv[2]))'''
    with open("../tester/profile_temp.c","w") as f:
        f.write(profile(sys.argv[2]))
    subprocess.run(["gcc ../tester/profile_temp.c -o op.out"], shell = True)
    precedent, suggested_runc, completion_time = warmup()
    
    ret_dict['suggested_runc'] = suggested_runc
    ret_dict['completion_time'] = completion_time
    
    return ret_dict

def read_profile():
    with open("../tester/profile.txt","r") as prof:
        string = prof.read().split('\n')
        memory = float(string[0])
        time = float(string[1])
        return memory, time

def warmup():
    global ret_dict
    PYTHON_FACTOR = 5
    print("warming up .....")
    total_time_unop = 0
    total_time_op = 0
    total_mem_unop = 0
    total_mem_op = 0
    for run in range(3):
        subprocess.run(["./unop.out < inp.txt > unop_output.txt"], shell = True)
        mem, time = read_profile()
        total_mem_unop += mem
        total_time_unop += time

        subprocess.run(["./op.out < inp.txt > unop_output.txt"], shell = True)
        mem, time = read_profile()
        total_mem_op += mem
        total_time_op += time

    ret_dict['avg_list'] = []
    ret_dict['avg_list'].append(f"Average memory usage for unoptimized code : {round(total_mem_unop/3, 2)} KB")
    ret_dict['avg_list'].append(f"Average time usage for unoptimized code : {round(total_time_unop/3, 6)} s")
    ret_dict['avg_list'].append(f"Average memory usage for optimized code : {round(total_mem_op/3, 2)} KB")
    ret_dict['avg_list'].append(f"Average time usage for optimized code : {round(total_time_op/3, 6)} s")

    precedent = (max(total_time_unop, total_time_op))/3
    runs = 0
    if(precedent < 1.00):
        runs = 1000
    elif(precedent < 5):
        runs = 200
    elif(precedent < 10):
        runs = 100
    else:
        runs = 10
    # print(f"Suggested No. of {runs} runs. Estimated completion time : {runs * precedent * PYTHON_FACTOR} s.")

    return precedent, runs, round(runs * precedent * PYTHON_FACTOR, 2)

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
        subprocess.run(["./unop.out < inp.txt > unop_output.txt"], shell = True)
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

        subprocess.run(["./op.out < inp.txt > op_output.txt"], shell = True)
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

    json_out = {}
    json_out['unop_time'] = f"{total_time_unop/runs} sec"
    json_out['unop_mem'] = f"{total_mem_unop/runs} kB"
    json_out['op_mem'] = f"{total_mem_op/runs} kB"
    json_out['op_time'] = f"{total_time_op/runs} sec"

    unop_mem = total_mem_unop/runs; op_mem = total_mem_op/runs
    memory_diff = unop_mem - op_mem
    percent_increase_m = (memory_diff / unop_mem) * 100

    unop_time = total_time_unop/runs; op_time = total_time_op/runs
    time_diff = unop_time - op_time
    percent_increase_t = (time_diff / unop_time) * 100

    json_out['p_dec_t'] = str(percent_increase_t) + ' %'
    json_out['p_dec_m'] = str(percent_increase_m) + ' %'
    json_out['time_diff'] = str(time_diff) + ' sec'
    json_out['mem_diff'] = str(memory_diff) + ' kB'

    return json_out

def validate(runs):
    # deciding no of runs
    return execute(runs)
    # returns json_out with avg. metrics

# compile()
# validate(1000)