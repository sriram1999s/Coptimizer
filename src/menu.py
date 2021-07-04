''' takes in flags from the UI '''
class Menu:
    def __init__(self):
        self.FLAG_UNROLL = True
        self.FLAG_COMPILE_INIT = True
        self.FLAG_INLINE = True
        self.FLAG_IF_TO_SWITCH = True
        self.FLAG_TAIL_RECURSION = True
        self.FLAG_JAMMING = True

    def set(self, flags):
        self.FLAG_UNROLL = flags["FLAG_UNROLL"]
        self.FLAG_COMPILE_INIT = flags["FLAG_COMPILE_INIT"]
        self.FLAG_INLINE = flags["FLAG_INLINE"]
        self.FLAG_IF_TO_SWITCH = flags["FLAG_IF_TO_SWITCH"]
        self.FLAG_TAIL_RECURSION = flags["FLAG_TAIL_RECURSION"]
        self.FLAG_JAMMING = flags["FLAG_JAMMING"]

''' instantiation '''
menu = Menu()
