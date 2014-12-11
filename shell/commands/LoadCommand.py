from shell.Command import Command

class LoadCommand(Command):
    def __init__(self):
        super(LoadCommand, self).__init__('load',
                                          min_args=1,
                                          max_args=1,
                                          help_text='Carga un archivo con comandos a ejecutar, la ruta puede ser relativa o absoluta.',
                                          usage_text='load ruta')
                                  
    def run(self, *args):
        procList = []
        command_list = []
        io = open(args[0])
        
        for line in io:
            procList.append(line[:-1].split(';'))

        for process in procList:
            command = self.addToNew(process)
            command_list.append(command)
    	
        return 1001, command_list
    	    
    def addToNew(self, string_process):
        from shell import Shell
        kind = int(string_process[2])
        command = None
        
        if(kind == 1):
            command = (Shell.commands['make_call'], (string_process[1],string_process[5], string_process[4]))
        elif(kind == 2):
            command = (Shell.commands['receive_call'], (string_process[1],string_process[5],string_process[4]))
        elif(kind == 3):
            command = (Shell.commands['send_msg'], (string_process[1],string_process[4],string_process[5]))
        elif(kind == 4):
            command = (Shell.commands['receive_msg'], (string_process[1],string_process[4],string_process[5]))   
        elif(kind == 5):
            command = (Shell.commands['add_contact'], (string_process[1],string_process[4],string_process[5]))
        elif(kind == 6):
             command = (Shell.commands['random_process'], (string_process[1], string_process[4]))
        elif(kind == 7):
            command = (Shell.commands['send_location'], (string_process[1]))
        elif(kind == 8):
            command = (Shell.commands['watch_location'], (string_process[1], string_process[4]))
        elif(kind == 9):
            command = (Shell.commands['play_game'], (string_process[1], string_process[4]))
        elif(kind == 10):
            command = (Shell.commands['play_music'], (string_process[1], string_process[4]))
           
        return command
    
