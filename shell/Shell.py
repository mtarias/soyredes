from CPU import CPU
from Command import Command

class Shell():
    """ Provee funcionalidades de consola
    """   
    # Comandos ejecutables
    from commands import HelpCommand, LoadCommand
    commands = {'exit': Command('exit',
                                CPU.CC_EXIT, 
                                help_text='Termina la simulacion.', 
                                usage_text='exit'),
                'load': LoadCommand(),
                'help': HelpCommand(),
                'top': Command('top',
                                CPU.CC_TOP,
                                min_args=0,
                                max_args=0,
                                help_text='Muestra los procesos en ejecucion',
                                usage_text='top'),
                'calls': Command('calls',
                                CPU.CC_CALL_HISTORY,
                                min_args=0,
                                max_args=0,
                                help_text='Muestra el historial de llamadas',
                                usage_text='calls'),
                'msgs': Command('msgs',
                                CPU.CC_MSG_HISTORY,
                                min_args=0,
                                max_args=0,
                                help_text='Muestra el historial de mensajes',
                                usage_text='msgs'),
                'make_call': Command('make_call',
                                     CPU.CC_MAKE_CALL,
                                     min_args=3,
                                     max_args=3,
                                     help_text='Realiza una llamada.',
                                     usage_text='call inicio duracion numero'),
                'receive_call': Command('receive_call',
                                        CPU.CC_RECEIVE_CALL,
                                        min_args=3,
                                        max_args=3,
                                        help_text='Recibe una llamada.',
                                        usage_text='call inicio duracion numero'),
                'send_msg': Command('send_msg',
                                    CPU.CC_SEND_MSG,
                                    min_args=3,
                                    max_args=3,
                                    help_text='Envia un mensaje.',
                                    usage_text='send_msg inicio numero texto'),
                'receive_msg': Command('receive_msg',
                                       CPU.CC_RECEIVE_MSG,
                                       min_args=3,
                                       max_args=3,
                                       help_text='Recibe un mensaje.',
                                       usage_text='receive_msg inicio numero texto'),
                'add_contact': Command('add_contact',
                                       CPU.CC_ADD_CONTACT,
                                       min_args=3,
                                       max_args=3,
                                       help_text='Agrega un contacto a la agenda.',
                                       usage_text='add_contact inicio contacto numero'),
                'random_process': Command('random_process',
                                       CPU.CC_RANDOM,
                                       min_args=2,
                                       max_args=2,
                                       help_text='Proceso misc.',
                                       usage_text='random_process inicio duracion'),
                'send_location': Command('send_location',
                                       CPU.CC_SEND_LOCATION,
                                       min_args=1,
                                       max_args=1,
                                       help_text='Envia la posicion.',
                                       usage_text='send_location inicio'),
                'watch_location': Command('watch_location',
                                       CPU.CC_WATCH_LOCATION,
                                       min_args=2,
                                       max_args=2,
                                       help_text='Ve la ubicacion actual.',
                                       usage_text='watch_location inicio duracion'),   
                'play_game': Command('play_game',
                                       CPU.CC_PLAY_GAME,
                                       min_args=2,
                                       max_args=2,
                                       help_text='Juega un juego.',
                                       usage_text='play_game inicio duracion'), 
                'play_music': Command('play_music',
                                       CPU.CC_PLAY_MUSIC,
                                       min_args=2,
                                       max_args=2,
                                       help_text='Escucha musica.',
                                       usage_text='play_music inicio duracion'),             
                'start': Command('start',
                                 CPU.CC_START_PROCESS,
                                 min_args=3,
                                 max_args=3,
                                 help_text='Inicia un proceso.',
                                 usage_text='start nombre inicio duracion'),
                 'simulate': Command('simulate',
                                 CPU.CC_SIMULATE,
                                 min_args=0,
                                 max_args=1,
                                 help_text='Empieza la simulacion.',
                                 usage_text='simulate velocidad'),
                }
    
    def __init__(self, conn):
        """ Inicia el proceso con un objecto de conexion
            del pipe entre la CPU y la consola
        """
        self.conn = conn
        print 'Bienvenido a la simulacion del SO'
        print 'Escribe \'help\' para mostrar la ayuda.'
    
    def send_command(self, code, args=None):
        """ Envia un comando al proceso principal
            Este consta de una tupla con el codigo
            como primer elemento y una tupla con
            argumentos como segundo elemento.
        """ 
        self.conn.send((code, args))
    
    def print_command_error(self, command):
        """ Imprime un mensaje de error para un comando.
        """
        print 'Argumentos invalidos para %s. ' % command.name,
        if command.min_args is not None:
            print 'Argumentos minimos: %i. ' % command.min_args,
        if command.max_args is not None:
            print 'Argumentos maximos: %i. ' % command.max_args,
        print
        print 'uso:\t%s' % command.usage_text
    
    def run(self):
        while True:
            input_str = raw_input()
            parts = input_str.split()
            
            if len(parts) > 0:
                # Ver si el comando existe
                if parts[0] not in self.commands:
                    print 'No se encontro el comando %s.' % parts[0]
                    continue
                
                command = self.commands[parts[0]]
                # Ver que el numero de argumentos sea el correcto
                if command.min_args is not None and len(parts) - 1 < command.min_args:
                    self.print_command_error(command)
                elif command.max_args is not None and len(parts) - 1 > command.max_args:
                    self.print_command_error(command)
                else:
                    cc, args = command.run(*parts[1:])
                    #print repr(cc) + '\t' + repr(args)
                    if cc > -1:
                        if cc == 1001:
                            for c in args:
                                self.send_command(c[0].code, c[1])
                        else:
                            self.send_command(cc, args)
                    
                    # Ver si tenemos que salir
                    if cc == CPU.CC_EXIT:
                        print 'Saliendo...'
                        break
        
