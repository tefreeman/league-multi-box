import time
from game_loop import GameLoop
from utility import UtilityFuncs
from actions import Actions
from graphics_pos import graphics_pos
from game_state import GameState

def flee_back(gs, changes, gameState, l):
    print(time.time() - GameLoop.old_time)
    
    if time.time() - GameLoop.old_time < 11.5:
        Actions.press_and_release_key('e')
    if time.time() - GameLoop.old_time > 12 and time.time() - GameLoop.old_time < 18:
        Actions.press_and_release_key('b')
    
    elif time.time() - GameLoop.old_time > 20:
        if gs['players'][gs['attach_target']]['alive']:
            target = gs['attach_target']
            msg = ''
            if target == 'top':
                msg = 'f1'
            if target == 'jg':
                msg = 'f2'
            if target == 'mid':
                msg = 'f3'
            if target == 'adc':
                msg = 'f4'
            Actions.switch_champions(msg)
            gameState.set_attach_target(target)     
            return 'play'
        
def init_nexus_pos(gs, changes, gameState, l):
        if UtilityFuncs.dom_color(gameState.img.getpixel(graphics_pos['minimap']['top_nexus'])) == 'b':
            gameState.nexus_pos = graphics_pos['minimap']['top_nexus']
            return 'play'
        elif UtilityFuncs.dom_color(gameState.img.getpixel(graphics_pos['minimap']['bottom_nexus'])) == 'b':
             gameState.nexus_pos = graphics_pos['minimap']['bottom_nexus']
             return 'play'
        else:
            return False

    
def auto_heal(gs, changes, gameState, l):
    #print( self._is_attached, ' ', self.attach_target, ' ', self.auto_heal_enabled )
    if gs['is_attached'] is True and gs['attach_target'] is not '' and gs['auto_heal_enabled'] is True:
        print('auto heal firing')
        if gs['players'][gs['attach_target']]['hp'] < 0.60:
            Actions.press_and_release_key('e')
            
        if gs['players'][gs['attach_target']]['hp'] < 0.18:
            Actions.press_and_release_key('d')


def level_up(gs, changes, gameState, l):
    if gs['can_learn_spell'] is True:
        Actions.press_and_release_key('ctrl+r')
        time.sleep(0.01)
        Actions.press_and_release_key('ctrl+e')
        time.sleep(0.01)  
        Actions.press_and_release_key('ctrl+w')
        time.sleep(0.01)
        Actions.press_and_release_key('ctrl+q')   

def listen_attached_player_death(gs, changes, gameState, l):
    if gs['attach_target'] is not '':
        p_alive = gs['players'][gs['attach_target']]['alive']
        p_changes_alive = changes['players'][gs['attach_target']]['alive']
        if gs['is_attached'] is False and p_alive is False and changes['is_attached'] is True and p_changes_alive is True:
            Actions.move_click(gameState.nexus_pos)
            GameLoop.old_time = time.time()
            return 'flee'
    
def listen_player_attach_changes(gs, changes, gameState, l):
    if changes['attach_target'] is True:
        return 'play'
