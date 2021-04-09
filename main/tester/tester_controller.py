import subprocess
from backend_tester import *

with open("profile_temp.c","w") as f:
    f.write(profile(sys.argv[1]))

subprocess.call(["gcc","profile_temp.c"])
subprocess.call(["./a.out < inp > unop_output"],shell=True)

with open("profile","r") as prof:
    time_unoptimized = float(prof.read())

with open("profile_temp.c","w") as f:
    f.write(profile(sys.argv[2]))
    
subprocess.call(["gcc","profile_temp.c"])
subprocess.call(["./a.out < inp > op_output"],shell=True)

with open("profile","r") as prof:
    time_optimized = float(prof.read())

time_diff = time_unoptimized-time_optimized
percent_increase = (time_diff/time_unoptimized)*100
    
print(f"Unoptimized execution time : {time_unoptimized}")
print(f"optimized execution time : {time_optimized}")
print(f"Time_difference : {time_diff}")
print(f"Percent_increase : {percent_increase}")

