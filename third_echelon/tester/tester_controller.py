import subprocess
from backend_tester import *

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


time_diff = time_unoptimized-time_optimized
percent_increase = (time_diff/time_unoptimized)*100
    
print(f"Unoptimized execution time : {time_unoptimized} sec")
print(f"optimized execution time : {time_optimized} sec")
print(f"Time_difference : {time_diff} sec")
print(f"Percent_decrease : {percent_increase}")

print("\n\n-------------------------------------------------------------------------------------\n\n")


memory_diff = memory_unoptimized-memory_optimized
percent_increase = (memory_diff/memory_unoptimized)*100


print(f"unoptimized memory usage : {memory_unoptimized} kB")
print(f"optimized memory usage : {memory_optimized} kB")
print(f"memory_difference : {memory_diff} kB")
print(f"Percent_decrease : {percent_increase}")

