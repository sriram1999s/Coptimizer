import random
import subprocess
import time

def gen_normal_program(start,end,max_length):
    input_list  = []
    for _ in range(max_length):
        input_list+=[random.randint(start,end)]
    return input_list


def runTestCases(program1_location,program2_location,num):
    assert type(program1_location) == str
    assert type(program2_location) == str
    input = gen_normal_program(100000,10000000,num)
    for i in range(len(input)):
        input_str = str(input[i])+"\n"
        proc = subprocess.Popen(program2_location, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        try:
            outs, errs = proc.communicate(input = input_str.encode('utf-8'), timeout=25)
        except TimeoutExpired:
            proc.kill()
            outs, errs = proc.communicate()
        #print(input_str)
        optimized_out = outs.decode('utf-8').split('\n')
        proc = subprocess.Popen(program1_location, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        try:
            outs, errs = proc.communicate(input = input_str.encode('utf-8'), timeout=25)
        except TimeoutExpired:
            proc.kill()
            outs, errs = proc.communicate()
        actual_out =  outs.decode('utf-8').split('\n')

        if(actual_out[0] == optimized_out[0]):
            print(f"passed! program2: {optimized_out[1]} ms",end=' ')
            print(f"passed! program1: {actual_out[1]} ms",end=' ')
            time_diff = (float(actual_out[1]) - float(optimized_out[1]))
            print("time_diff: " + "{:.8f}".format(time_diff), "ms",end=' ')
            percent = (time_diff/float(actual_out[1]))*100
            print("percent_increase :"+"{:.2f}".format(percent) + '%')
        else:
            print(f"failed! i/p: {input_str} , o/p2 : {optimized_out} , o/p1 : {actual_out}")

runTestCases("./inp","./out", 100)
