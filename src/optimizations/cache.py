from regenerator import solve
import re
from collections import defaultdict

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

    def dependancy_present(self, for_str, for_count):
        pat = "for\(.*?\)\{"*(for_count)
        print("\n\nfor_str, pat :", for_str, pat)

        if (re.search(pat, for_str)):
            return False
        return True

    def find_frequency_index(self):
        for loop in self.for_loops.copy():
            for_str = "".join(solve(0, len(self.for_loops[loop]), self.for_loops[loop]))

            count = len(re.findall("for", for_str))
            curr = self.for_loops[loop]
            # pattern to find the inner most for loop's body
            if(self.dependancy_present(for_str, count)):
                continue

            pat = "for.*?"*(count-1)
            pat += "for.*?\{(.*?)\}"
            m = re.search(pat, for_str)
            inner_body = m.group(1)
            # find all "last" indices of data structures
            pat_data_structs = "([_a-zA-Z][_a-zA-Z0-9]*?)(?:\[(.*?)\])+"
            data_structs = re.findall(pat_data_structs, inner_body)
            # finding frequency of "last" indices
            ix_dict = defaultdict(lambda:0)
            for data in data_structs:
                _, ix = data
                ix_dict[ix] += 1
            # finding all for conditions
            for_cndts_pat = "for\(.*?\)"
            for_cndts = re.findall(for_cndts_pat, for_str)
            # sorting indices based on frequency
            temp_list = sorted(ix_dict.items(), key = lambda x:x[1])

            #generating new for_order
            new_for_order = ""
            for tup_ix in temp_list:
                for candidate_for_ix in range(len(for_cndts)):
                    candidate_for = for_cndts[candidate_for_ix]
                    pat = tup_ix[0] + ".*?="
                    if(re.search(pat, candidate_for)):
                        new_for_order += "{" + candidate_for
                        for_cndts[candidate_for_ix] = None
                        break

            print("for_cndts after: ",for_cndts)

            for remaining_candidate in for_cndts:
                if(remaining_candidate!=None):
                    new_for_order = remaining_candidate + new_for_order

            #attaching body
            new_for_order = new_for_order + "{" + inner_body + ("}"*count)
            self.for_loops[loop].pop()
            self.for_loops[loop].pop()
            self.for_loops[loop][0] = new_for_order





# TODO
# 1) reflect the changes in the original subtree
cache = Cache()
