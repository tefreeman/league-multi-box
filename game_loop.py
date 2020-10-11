from utility import UtilityFuncs
from actions import Actions

class GameLoop:
    commands = []
    old_gs = None
    
    def __init__(self):
        pass
    
    @staticmethod
    def add_command(func):
        GameLoop.commands.append(func)
        
    @staticmethod
    def run_commands(gs):
        if GameLoop.old_gs is not None:
            changes = UtilityFuncs.get_dict_differences(gs, GameLoop.old_gs)
            for command in GameLoop.commands:
                command(gs, changes)
        
        GameLoop.old_gs = gs
        
    
    
