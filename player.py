from enum import Enum
from graphics_pos import graphics_pos


class Player:
    def __init__(self, lane_str: str):
        self._lane = lane_str
        self.hp_bar_start_x = graphics_pos['player_bars_left']['x-lanes'][lane_str] 
        self._hp = 1
        self._mana = 1
        self._cd_reduction = 1
        self._pos = None
        
        
        self._alive = True
    
    def to_dict(self):
        return {
            'lane': self._lane,
            'hp': self._hp,
            'mana': self._mana,
            'cd': self._cd_reduction,
            'alive': self._alive
        }
        
    def get_lane(self):
        return self._lane
    
    def set_lane(self, lane_str: str):
        self._lane = lane_str
    
    def set_pos(self, x, y):
        self._pos = (x,y)
        
    def get_pos(self):
        return self._pos
    
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