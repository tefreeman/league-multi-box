from utility import UtilityFuncs
from actions import Actions

class GameLoop:
    MAX_OLD_GS = 3
    old_time = 0
    state = ''
    commands = {
        'init': []
    }
    
    listeners = {}
    
    old_gs = []
    
    def __init__(self):
        pass
    
    
    @staticmethod
    def add_listener(func, state: str):
        if state not in GameLoop.listeners:
            GameLoop.listeners[state]= []
        
        GameLoop.listeners[state].append(func)
    
    @staticmethod
    def add_command(func, state: str):
        if state not in GameLoop.commands:
            GameLoop.commands[state]= []
            
        if state not in GameLoop.listeners:
            GameLoop.listeners[state]= []
                   
        GameLoop.commands[state].append(func)

    @staticmethod
    def run_commands(GameState):
        print(len(GameLoop.old_gs))
        #print(GameLoop.state)
        gs = GameState.to_dict()
        if len(GameLoop.state) > 0:
            if len(GameLoop.old_gs) > 0:
                changes = UtilityFuncs.get_dict_differences(gs, GameLoop.old_gs)
                l = len(GameLoop.commands[GameLoop.state])
                for i in range(0, l):
                    command = GameLoop.commands[GameLoop.state][i]
                    result = command(gs, changes, GameState, l)
                    
                    if isinstance(result, str) is True:
                        GameLoop.state = result
                        break
                
                l = len(GameLoop.listeners[GameLoop.state])     
                for i in range(0, l):
                    listener = GameLoop.listeners[GameLoop.state][i]
                    result = listener(gs, changes, GameState, l)
                    
                    if isinstance(result, str) is True:
                        GameLoop.state = result
                        break
        else:
            if GameState.game_started is True:
                GameLoop.state = 'init'
        if len(GameLoop.old_gs) > GameLoop.MAX_OLD_GS:
            GameLoop.old_gs.pop(0)
        GameLoop.old_gs.append(gs)
        
    
    
