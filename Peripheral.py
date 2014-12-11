class Peripheral(object):  
    def __init__(self, name):
        self.name = name
        self.listener = None
        self.blocker = None

    def set_listener(self, listener):
        self.listener = listener

    def block(self, process):
        self.blocker = process

    def free(self):
        self.blocker = None
        self.listener.free_peripheral(self)
 
    def is_free(self, process):
        return (self.blocker is None or self.blocker == process)
		
# Perifericos
screen = Peripheral("Screen")
headphones = Peripheral("Headphones")
microphone = Peripheral("Microphone")
gps = Peripheral("GPS")
rec_info = Peripheral("Rec_Info")
send_info = Peripheral("Send_Info")

peripherals = [screen,
               headphones,
               microphone,
               gps,
               rec_info,
               send_info]
               
peripheral_dict = dict((peripheral.name, peripheral) for peripheral in peripherals)
