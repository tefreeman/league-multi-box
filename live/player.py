from enum import Enum
from graphics_pos import graphics_pos


class Player:
    def __init__(self, pos_str: str):
        self.pos = pos_str
        self.hp_bar_start_x = graphics_pos['hp_bars_left']['x-lanes'][pos_str]
        
        self._hp = 1
        self._alive = True
        
    def set_hp(self, new_hp):
        self._hp = new_hp
        if self._hp > 0:
            self.set_alive(True)
            
    def get_hp(self):
        return self._hp
    
    def set_alive(self, state):
        self._alive = state
    
    def is_alive(self):
        return self._alive
    
    def print_hp(self):
        print(self.pos + ' hp: ' , self._hp)