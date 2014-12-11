import multiprocessing
from Process import *
from Scheduler import Scheduler
import time
import Queue
from Memory import Memory
from Peripheral import Peripheral, peripherals

## Esta es la CPU
class CPU(multiprocessing.Process):
    # Codigos de comando para comunicar la consola con el proceso
    # Principal
    CC_EXIT = 100
    CC_MAKE_CALL = 200
    CC_RECEIVE_CALL = 210
    CC_SEND_MSG = 250
    CC_RECEIVE_MSG = 260
    CC_ADD_CONTACT = 300
    CC_START_PROCESS = 400
    CC_TOP = 500
    CC_CALL_HISTORY = 600
    CC_MSG_HISTORY = 700
    CC_RANDOM = 800
    CC_SEND_LOCATION = 900
    CC_WATCH_LOCATION = 1000
    CC_PLAY_GAME = 1100
    CC_PLAY_MUSIC = 1200
    
    CC_SIMULATE = 5000
    
    # Step de simulacion en ms
    TIME_STEP = 1000
    QUANTUM = 2
    
    def __init__(self, conn):
        super(CPU, self).__init__()
        self.conn = conn
        self.pid_count = 0
        self.count = 0
        Memory.set_up()
        self.scheduler = Scheduler()
        self.current_process = None

    def run(self):
        new_queue = Queue.Queue()
        
        speed = 1
        
        curr_time = 0
        run = True
        
        started = False
        
        while run:
            # Recibir comandos desde la consola
            while self.conn.poll():
                cc, args = self.conn.recv()
                new_process = None
                
                if cc == self.CC_EXIT:
                    run = False
                    break
                elif cc == self.CC_MAKE_CALL:
                    new_process = CallProcess(self.pid_count + 1, 1, 'make_call', *args)
                elif cc == self.CC_RECEIVE_CALL:
                    new_process = CallProcess(self.pid_count + 1, 2, 'receive_call', *args)
                elif cc == self.CC_SEND_MSG:
                    new_process = MessageProcess(self.pid_count + 1, 3, 'send_msg', *args)
                elif cc == self.CC_RECEIVE_MSG:
                    new_process = MessageProcess(self.pid_count + 1, 4, 'receive_msg', *args)
                elif cc == self.CC_ADD_CONTACT:
                    new_process = AddContactProcess(self.pid_count + 1, 5, 'add_contact', *args)
                elif cc == self.CC_RANDOM:
                    new_process = RandomProcess(self.pid_count + 1, 6, 'random_process', *args)
                elif cc == self.CC_SEND_LOCATION:
                    new_process = SendLocationProcess(self.pid_count + 1, 7, 'send_location', *args)
                elif cc == self.CC_WATCH_LOCATION:
                    new_process = WatchLocationProcess(self.pid_count + 1, 8, 'watch_location', *args)
                elif cc == self.CC_PLAY_GAME:
                    new_process = PlayGameProcess(self.pid_count + 1, 9, 'play_game', *args)
                elif cc == self.CC_PLAY_MUSIC:
                    new_process = PlayMusicProcess(self.pid_count + 1, 10, 'play_music', *args)
                elif cc == self.CC_START_PROCESS:
                    new_process = Process(self.pid_count + 1, 6 , *args)
                elif cc == self.CC_TOP:
                    self.scheduler.top(self.current_process)
                elif cc == self.CC_CALL_HISTORY:
                    Memory.readCallHistory()
                elif cc == self.CC_MSG_HISTORY:
                    Memory.readMsgHistory()
                elif cc == self.CC_SIMULATE:
                    started = True
                    speed = float(args[0]) if len(args) == 1 else 1
                    print 'Empezando simulacion'

                # Se agregan procesos a New
                if new_process is not None:
                    self.pid_count += 1
                    new_queue.put((new_process.start_time, new_process))

            if started:
                # Se agregan procesos de la cola New a la Cola Ready
                i = 0
                n = new_queue.qsize()
                while i < n:
                    process = new_queue.get()[1]
                    if (process.start_time*1000 == curr_time):
                        print 'Agendando Proceso %s numero %s en el tiempo %s' % (process.name,process.pid, curr_time)
                        self.scheduler.add(process)
                    else:
                        new_queue.put((process.start_time, process))
                    i+=1

                if self.current_process is not None:
                    if self.current_process.pending_time <= 0:
                        # Liberar perifericos bloqueados
                        self.current_process.free_peripherals()
                        # Eliminar el proceso del scheduler
                        self.scheduler.dispose(self.current_process)
                        self.current_process = None

                    # El scheduler devuelve el proceso que debe estar actualmente
                    # Si es tiempo de cambiar el proceso y ya hay uno usandose, se cambia
                    elif self.count == self.QUANTUM:
                        self.count = 0
                        #El proceso retirado va al final de la fila
                        self.scheduler.dispose(self.current_process)
                        self.scheduler.add(self.current_process)
                        self.current_process = self.scheduler.getNext()

                # Si la CPU no fue usada anteriormente, vemos si hay otro proceso esperando
                if self.current_process is None:
                    self.current_process = self.scheduler.getNext()

                # Si no, solo aumenta e contador de tiempo
                if self.count == self.QUANTUM:
                    self.count = 0

                if self.current_process is not None:
                    # ejecutar el proceso por la cantidad de tiempo concedida
                    self.current_process.run(self.TIME_STEP, curr_time)

                self.count +=1
                curr_time += self.TIME_STEP
                
            time.sleep(self.TIME_STEP / (1000 * speed))

