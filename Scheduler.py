import Queue
from Memory import Memory
from Peripheral import Peripheral, peripherals

class Scheduler:
    def __init__(self):
        self.queue = []
        # Guarda el ultimo proceso cargado
        self.last_process = None
        self.waiting = dict((peripheral, []) for peripheral in peripherals)
        for peripheral in peripherals:
            peripheral.set_listener(self)

    def add(self, process):
        """ Agrega un proceso a la lista waiting
        """
        # Guardar en ram la informacion del proceso
        Memory.saveProcess(process)
        # Agregar a la cola priorizada (solo la prioridad y el pid)
        self.queue.append(process)
        self.last_process = process
      
    def dispose(self, process):
        """ Quita un proceso
        """
        Memory.removeProcess(process.pid)
        self.queue.remove(process)
        if self.last_process == process:
            self.last_process = None
        
    def getNext(self):
        """ Devuelve el proximo proceso a ejecutar
        """ 
        process = None
        while process is None and len(self.queue) > 0:
            process = self.queue[0]
            if not self.check_peripherals(process):
                self.queue.remove(process)
                process = None
        
        self.last_process = process
        return self.last_process

    def check_peripherals(self, process):
        result = True
        for peripheral, use_type in process.peripherals:
            if not peripheral.is_free(process):
                self.waiting[peripheral].append(process)
                result = False
        return result
                
    def free_peripheral(self, peripheral):
        for process in self.waiting[peripheral]:
            self.queue.append(process)
        self.waiting[peripheral] = []

    def top(self, curr_process):
        print 'Procesos en ejecucion:'
        process_list = []
        if (curr_process != None):
            process_list.append(curr_process)

        for process in self.queue:
            if curr_process is None or process.pid != curr_process.pid:
                process_list.append(Memory.loadProcess(process.pid))
                    

        if len(process_list) == 0:
            print 'Ninguno'
        else:
            print 'pid'.rjust(5), 'name'.ljust(15), 'start_time'.rjust(15), 'pending_time'.rjust(15), 'execution_time'.rjust(15)
            for p in process_list:
                print repr(p.pid).rjust(5), repr(p.name).ljust(15), repr(p.start_time).rjust(15), repr(p.pending_time).rjust(15), repr(p.execution_time).rjust(15)
            
