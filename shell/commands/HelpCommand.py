from shell.Command import Command

class HelpCommand(Command):
    def __init__(self):
        super(HelpCommand, self).__init__('help',
                                          min_args=0,
                                          max_args=1,
                                          help_text='Muestra ayuda acerca de los comandos.',
                                          usage_text='help [nombre_proceso]')
                                  
    def run(self, *args):
        from shell import Shell
        if len(args) == 0:
            print 'Comandos disponibles:'
            for command_name in Shell.commands.keys():
                print command_name + '\n'
            print
        elif args[0] not in Shell.commands:
            print 'No se encontro el comando %s.' % args[0]
        else:
            command = Shell.commands[args[0]]
            print '%s:\t%s' % (command.name, command.help_text)
            print 'uso:\t%s' % command.usage_text
        return super(HelpCommand, self).run(args)
