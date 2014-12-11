# -*- coding: utf-8 -*-

class Command(object):
    """ Representa un comando que puede ejecutarse en la consola.
    """
    
    def __init__(self, name, code=-1, min_args=0, max_args=0, help_text='', usage_text=''):
        self.name = name
        self.code = code
        self.min_args = min_args
        self.max_args = max_args
        self.help_text = help_text
        self.usage_text = usage_text
        
    def run(self, *args):
        """ Ejecuta el comando, devuelve el codigo a enviar al proceso principal.
            En las clases hijas, puede realizar otras funciones.
        """
        return self.code, args
