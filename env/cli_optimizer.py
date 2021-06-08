from collections import defaultdict
import fire
import json
import subprocess

'''help menu'''
def help():
    print("\nWelcome to the command line Coptimizer....(bhenki)\n")
    print("Usage sf ------> python3 cli_optimzer.py sf [FLAGS]")
    print("Usage ox ------> python3 cli_optimzer.py ox [PATH]")
    print("sf [options] ----> setflags in from this pool [UNROLL,COMPILE_INIT,INLINE,IF_TO_SWITCH,TAIL_RECURSION,JAMMING]")
    print("ox [PATH] -----> optimize file in given path and create output.c file in same path")

'''to set flags'''
def sf(*args):
    flags = {}
    for key in ["FLAG_UNROLL","FLAG_COMPILE_INIT","FLAG_INLINE","FLAG_IF_TO_SWITCH","FLAG_TAIL_RECURSION","FLAG_JAMMING"]:
        flags[key] = False

    for op in args:
        flags["FLAG_"+op] = True

    json_obj = json.dumps(flags)

    with open("flags.json","w") as f:
        f.write(json_obj)


'''optimize'''

def ox(path):
    subprocess.call([f"python3 ../src/controller.py {path}"],shell=True)
    subprocess.call(["indent -linux temp.c -o output.c"],shell=True)
    subprocess.call(["rm temp.c"],shell=True)
    subprocess.call(["rm ../src/parser.out ../src/parsetab.py temp.c;rm -r ../src/__pycache__;"],shell=True)



if(__name__ == '__main__'):
    fire.Fire()
