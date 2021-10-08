class Cache:
    def __init__(self):
        self.for_loops = {}
        self.for_count = 1

    def validate(self, sub_tree):
        print("in Cache.validate :", sub_tree)
        self.for_loops["for" + str(self.for_count)] = sub_tree
        self.for_count += 1

    def restructure_for(self):

        to_remove_keys = []
        for key1 in self.for_loops:
            for key2 in self.for_loops:
                if self.for_loops[key1] in self.for_loops[key2][2]:
                        to_remove_keys.append(key1)
                        break
        for key in to_remove_keys:
            del self.for_loops[key]
            
cache = Cache()
