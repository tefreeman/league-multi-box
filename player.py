from enum import Enum
from graphics_pos import graphics_pos


class Player:
    def __init__(self, lane_str: str):
        self._lane = lane_str
        self.hp_bar_start_x = graphics_pos['hp_bars_left']['x-lanes'][lane_str]
        
        self._hp = 1
        self._mana = 1
        self._cd_reduction = 1
        
        self._alive = True
    
    def get_lane(self):
        return self._lane
    
    def set_lane(self, lane_str: str):
        self._lane = lane_str
    
    def set_mana(self, val):
        self._mana = val
    
    def get_mana(self):
        return self._mana
    
    def set_hp(self, val):
        self._hp = val
        if self._hp > 0:
            self.set_alive(True)
            
    def get_hp(self):
        return self._hp
    
    def set_alive(self, state):
        self._alive = state
    
    def is_alive(self):
        return self._alive
    
    def print_hp(self):
        print(self._lane + ' hp: ' , self._hp)