import math
from Memory import Memory
import datetime
import Peripheral

PERIPHERAL_USE = 10
PERIPHERAL_BLOCK = 20

class Process(object):
    def __init__(self, pid, proc_type, name, start_time, execution_time, peripherals=[]):
        self.pid = int(pid)
        self.name = name
        self.start_time = int(start_time)
        self.proc_type = int(proc_type)
        self.execution_time = int(execution_time) * 1000
        self.pending_time = int(execution_time) * 1000       
        self.started = False
        self.peripherals = peripherals
        
    def run(self, lapse, time):
        if self.start_time is None:
            self.start_time = time
        self.pending_time -= lapse
        if self.pending_time < 0:
            self.pending_time = 0
        
        if not self.started:
            for peripheral, use_type in self.peripherals:
                if use_type == PERIPHERAL_BLOCK:
                    print '\tBloqueando %s ' % peripheral.name
                    peripheral.block(self)
            self.started = True
        
        # print 'Proceso %s numero %i esta en ejecucion y le quedan %i ms' % (self.name, self.pid,self.pending_time)
        ## print 'Proceso %i le queda %d en el tiempo %i \n' % (self.pid, self.pending_time, time)
        
    def free_peripherals(self):
        for peripheral, use_type in self.peripherals:
            if use_type == PERIPHERAL_BLOCK:
                print '\tLiberando %s ' % peripheral.name
                peripheral.free()
            
    def __getstate__(self):
        return {'pid': self.pid,
                'name': self.name,
                'start_time': self.start_time,
                'proc_type': self.proc_type,
                'execution_time': self.execution_time,
                'pending_time': self.pending_time,
                'started': self.started,
                'peripherals': [(p[0].name, p[1]) for p in self.peripherals]}
                
    def __setstate__(self, state):
        self.pid = state['pid']
        self.name = state['name']
        self.start_time = state['start_time']
        self.proc_type = state['proc_type']
        self.execution_time = state['execution_time']
        self.pending_time = state['pending_time']    
        self.started = state['started']
        self.peripherals = []
        for name, use_type in state['peripherals']:
            self.peripherals.append((Peripheral.peripheral_dict[name], use_type))

class CallProcess(Process):
    def __init__(self, pid, proc_type, name, start_time, execution_time, number):
        start_time = int(start_time)
        self.number = number
        self.date = datetime.datetime.now()
        peripherals = [(Peripheral.screen, PERIPHERAL_USE), 
                       (Peripheral.headphones, PERIPHERAL_BLOCK),
                       (Peripheral.microphone, PERIPHERAL_BLOCK),
                       (Peripheral.send_info, PERIPHERAL_USE),
                       (Peripheral.rec_info, PERIPHERAL_USE)]
        super(CallProcess, self).__init__(pid, proc_type, name, start_time, execution_time, peripherals)
        
    def run(self, lapse, time):
        if not self.started:
            Memory.writeCallHistory(self.proc_type, self.date, self.number, self.execution_time)
        super(CallProcess, self).run(lapse, time)  
        
    def __getstate__(self):
        state = super(CallProcess, self).__getstate__()
        state.update({'number': self.number,
                      'date': self.date})
        return state
        
    def __setstate__(self, state):
        self.number = state['number']
        self.date = state['date']
        super(CallProcess, self).__setstate__(state)

class MessageProcess(Process):
    def __init__(self, pid, proc_type, name, start_time, number, text):
        start_time = int(start_time) if start_time is not None else None
        self.number = number
        self.text = text
        execution_time =  int(math.ceil(float(20 * len(self.text)) / 1000))
        self.date = datetime.datetime.now()
        peripherals = [(Peripheral.headphones, PERIPHERAL_USE),
                       (Peripheral.send_info, PERIPHERAL_USE),
                       (Peripheral.rec_info, PERIPHERAL_USE)]
        super(MessageProcess, self).__init__(pid, proc_type, name, start_time, execution_time, peripherals)
    
    def run(self, lapse, time):
        if not self.started:
            Memory.writeMsgHistory(self.proc_type, self.date, self.number, self.text)
        super(MessageProcess, self).run(lapse, time)  
        
    def __getstate__(self):
        state = super(MessageProcess, self).__getstate__()
        state.update({'number': self.number,
                      'text': self.text,
                      'date': self.date})
        return state
        
    def __setstate__(self, state):
        self.number = state['number']
        self.text = state['text']
        self.date = state['date']
        super(MessageProcess, self).__setstate__(state)
        
class AddContactProcess(Process):
    def __init__(self, pid, proc_type, name, start_time, contact, number):
        start_time = int(start_time) if start_time is not None else None
        self.number = number
        self.contact = contact
        #Asumimos que cuando agregamos un contacto,s e demora 2 segundos
        execution_time =  2 * 1000;
        peripherals = [(Peripheral.screen, PERIPHERAL_USE)]
        super(AddContactProcess, self).__init__(pid, proc_type, name, start_time, execution_time, peripherals)
        
    def __getstate__(self):
        state = super(AddContactProcess, self).__getstate__()
        state.update({'number': self.number,
                      'contact': self.contact})
        return state
        
    def __setstate__(self, state):
        self.number = state['number']
        self.contact = state['contact']
        super(AddContactProcess, self).__setstate__(state)
        
class RandomProcess(Process):
    def __init__(self, pid, proc_type, name, start_time, execution_time):
        peripherals = [(Peripheral.screen, PERIPHERAL_USE),
                       (Peripheral.headphones, PERIPHERAL_USE),
                       (Peripheral.microphone, PERIPHERAL_USE),
                       (Peripheral.gps, PERIPHERAL_USE),
                       (Peripheral.send_info, PERIPHERAL_USE),
                       (Peripheral.rec_info, PERIPHERAL_USE)]
        super(RandomProcess, self).__init__(pid, proc_type, name, start_time, execution_time, peripherals)
        
class SendLocationProcess(Process):
    def __init__(self, pid, proc_type, name, start_time):
        peripherals = [(Peripheral.gps, PERIPHERAL_USE),
                       (Peripheral.send_info, PERIPHERAL_USE)]
        execution_time =  2 * 1000;
        super(SendLocationProcess, self).__init__(pid, proc_type, name, start_time, execution_time, peripherals)
        
class WatchLocationProcess(Process):
    def __init__(self, pid, proc_type, name, start_time, execution_time):
        peripherals = [(Peripheral.screen, PERIPHERAL_USE),
                       (Peripheral.gps, PERIPHERAL_USE)]
        super(WatchLocationProcess, self).__init__(pid, proc_type, name, start_time, execution_time, peripherals)
        
class PlayGameProcess(Process):
    def __init__(self, pid, proc_type, name, start_time, execution_time):
        peripherals = [(Peripheral.screen, PERIPHERAL_USE),
                       (Peripheral.headphones, PERIPHERAL_USE),
                       (Peripheral.gps, PERIPHERAL_USE),
                       (Peripheral.send_info, PERIPHERAL_USE),
                       (Peripheral.rec_info, PERIPHERAL_USE)]
        super(PlayGameProcess, self).__init__(pid, proc_type, name, start_time, execution_time, peripherals)
        
class PlayMusicProcess(Process):
    def __init__(self, pid, proc_type, name, start_time, execution_time):
        peripherals = [(Peripheral.screen, PERIPHERAL_USE),
                       (Peripheral.headphones, PERIPHERAL_USE)]
        super(PlayMusicProcess, self).__init__(pid, proc_type, name, start_time, execution_time, peripherals)  
        
