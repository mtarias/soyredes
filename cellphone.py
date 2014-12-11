from Scheduler import Scheduler
from CPU import *
from shell import Shell
import multiprocessing
import time

if __name__ == "__main__":
    # Crear Pipe para conectar la consola con el SO
    parent_conn, child_conn = multiprocessing.Pipe()
    
    shell = Shell(parent_conn)
    cpu = CPU(child_conn)
    
    cpu.start()
    
    shell.run()
    
    cpu.join()
