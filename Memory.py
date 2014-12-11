# -*- coding: utf-8 -*-
import pickle
import os
import shutil

class Memory:
    @staticmethod
    def set_up():
        if os.path.exists('pcb/'):
            shutil.rmtree('pcb/')
        os.mkdir('pcb')
        try:
            os.remove('msg_history.txt')
            os.remove('call_history.txt')
        except:
            pass

    @staticmethod
    def saveProcess(process):
        name = 'pcb/PCB%i.txt' % process.pid
        file = open(name, 'wb')
        pickle.dump(process, file)
        file.close()
        
    @staticmethod
    def loadProcess(pid):
        name = 'pcb/PCB%i.txt' % pid
        if os.path.exists(name):
            file = open(name, 'rb')
            process = pickle.load(file)
            return process
            
        return None
        
    @staticmethod
    def removeProcess(pid):
        name = 'pcb/PCB%i.txt' % pid
        try:
            os.remove(name)
            return True
        except:
            return False

    # Historial de mensajes.
    @staticmethod
    def writeMsgHistory(msgType, date, number, message):
        filename = 'msg_history.txt'
        io = open(filename, 'a')
        io.write('[%s] %s %s %s\n' % (date.strftime('%d/%m/%Y %H:%M:%S'), 'Rec' if msgType == 4 else 'Env', number, message.replace(' ', ':|:')))
        io.close()

    @staticmethod
    def readMsgHistory():
        filename = 'msg_history.txt'
        msgs = []
        for line in open(filename):
            date = line[:line.find(']')]
            parts = line[line.find(']') + 1:].split()
            msgs.append(
                (date.replace('[', '').replace(']', ''),
                 parts[0],
                 parts[1],
                 parts[2].replace(':|:', ' '))
            )
        print 'Fecha'.ljust(20), 'Tipo'.ljust(5), 'Numero'.ljust(15), 'Mensaje'.ljust(50)
        for m in msgs:
            print str(m[0]).ljust(20), str(m[1]).ljust(5), str(m[2]).ljust(15), m[3]

    # Historial de llamadas.
    @staticmethod
    def writeCallHistory(callType, date, number, callDuration):
        filename = 'call_history.txt'
        io = open(filename, 'a')
        io.write('[%s] %s %s %s\n' % (date.strftime('%d/%m/%Y %H:%M:%S'), 'Rec' if callType == 2 else 'Env', number, callDuration))
        io.close()

    @staticmethod
    def readCallHistory():
        filename = 'call_history.txt'
        calls = []
        for line in open(filename):
            date = line[:line.find(']')]
            parts = line[line.find(']') + 1:].split()
            calls.append(
                (date.replace('[', '').replace(']', ''),
                 parts[0],
                 parts[1],
                 parts[2])
            )
        print 'Fecha'.ljust(20), 'Tipo'.ljust(5), 'Numero'.ljust(15), 'Duracion'.ljust(10)
        for c in calls:
            print str(c[0]).ljust(20), str(c[1]).ljust(5), str(c[2]).ljust(15), str(c[3]).ljust(20)

    # Función que cuenta cuántos elementos tiene el archivo.
    @staticmethod
    def countFileItem (fileName):
        io = open(fileName, 'r')
        count = io.readlines().count('\n')
        io.close()
        return count
