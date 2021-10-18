from regenerator import solve
import re

class Cache:
    def __init__(self):
        self.for_loops = {}
        self.for_count = 1

    def validate(self, sub_tree):
        print("in Cache.validate :", sub_tree)
        self.for_loops["for" + str(self.for_count)] = sub_tree
        self.for_count += 1

    def retain_outer_loop(self):
        """keeps only the outer most loop in the for loops dictionary so that cache optimziations is no called on each sub for loop"""
        to_remove_keys = set()
        for key1 in self.for_loops:
            for key2 in self.for_loops:
                if(key1 != key2):
                    # print("sadasdasd ",self.for_loops[key1],"\n||\n",self.for_loops[key2][2])


                    def repl(x):
                        # print("grps ",x.group(1))
                        return '\\' + str(x.group(1))

                    pat = "".join(solve(0, len(self.for_loops[key1]),self.for_loops[key1]))
                    pat = re.sub("([+*.?^{}()\[\]])", repl , pat)

                    text = "".join(solve(0, len(self.for_loops[key2]),self.for_loops[key2]))
                    if(re.search(pat, text)):
                        to_remove_keys.add(key1)
                        
        for key in to_remove_keys:
            del self.for_loops[key]


            
# TODO
# 1) frequency of loop variables
# 2) swap for loops accordingly
cache = Cache()
