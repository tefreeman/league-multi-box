from player import Player
from graphics_pos import graphics_pos
from screen_reader import ScreenReader
from PIL import Image
from actions import Actions
from utility import UtilityFuncs
from game_loop import GameLoop

class GameState:
    def __init__(self):

        self.img = None
        self.players = {
            'top': Player('top'),
            'jg': Player('jg'),
            'mid': Player('mid'),
            'adc': Player('adc')
        }
        
        self._is_attached = False
        self.attach_target = ''
        self.auto_heal_enabled = False
    
    def to_dict(self):
        return {
            'img': self.img,
            'players': {
                'top': self.players['top'].to_dict(),
                'jg': self.players['jg'].to_dict(),
                'mid': self.players['mid'].to_dict(),
                'adc':self.players['adc'].to_dict(),
            },
            'is_attached': self._is_attached,
            'attach_target': self.attach_target,
            'auto_heal_enabled': self.auto_heal_enabled
        }
    
   
                
    
    def u_yummi_retreat(self):
        if UtilityFuncs.dom_color(self.img.getpixel(graphics_pos['minimap']['top_nexus'])) == 'b':
            if self._is_attached is False and self.players[self.attach_target].is_alive() is False:
                Actions.move_click(graphics_pos['minimap']['top_nexus'])
        elif UtilityFuncs.dom_color(self.img.getpixel(graphics_pos['minimap']['bottom_nexus'])) == 'b':
             if self._is_attached is False and self.players[self.attach_target].is_alive() is False:
                Actions.move_click(graphics_pos['minimap']['top_nexus'])
    
            
    def set_attach_target(self, pos_str):
        self.attach_target = pos_str
    
    def get_player(self, pos_str):
        return self.players[pos_str]
    
    def toggle_auto_heal(self):
        self.auto_heal_enabled = not self.auto_heal_enabled
        
    def update(self, screen_img):
        self.img = screen_img
        self.u_players_hp()
        self.u_yummi_attached()
        GameLoop.run_commands(self.to_dict())
        
        
    def test_update(self):
        im = Image.open("C:/Users/Trevor/Documents/pics/yummi_not_attached.png")
        self.update(im)
    
    def u_yummi_attached(self):
        #print(self.img.getpixel((900, 357)))
        #print(self.img.getpixel((891, 355)))
        
        connected = False
        connected_2 = False
        for i in range(330, 420):
            if UtilityFuncs.fuzzy_color_match(self.img.getpixel((900, i)), (115, 109, 247)):
                connected = True
            if UtilityFuncs.fuzzy_color_match(self.img.getpixel((891, i)), (239, 203, 99)):
                connected_2 = True
        
        if connected and connected_2:
            self._is_attached = True
        else:
            self._is_attached = False
            
            
    def u_players_hp(self):
        for player in self.players.values():
            start_x = player.hp_bar_start_x
            y = graphics_pos['player_bars_left']['hp-y']
            width = graphics_pos['player_bars_left']['x-width']
            
            black_pixel_count = 0
            red_pixel_count = 0
            
            for i in range(start_x, start_x + width):
                if self.img.getpixel((i, y))[0] < 25 and self.img.getpixel((i, y))[1] < 25  and self.img.getpixel((i, y))[2] < 25:
                    black_pixel_count += 1
                if self.img.getpixel((i, y))[0] > 120 and self.img.getpixel((i, y))[1] < 20  and self.img.getpixel((i, y))[2] < 20:
                    red_pixel_count += 1
                
            hp = (width - black_pixel_count) / width
            
            if red_pixel_count > 1:
                player.set_alive(False)
                hp = 0
            
            player.set_hp(hp) 
    
    def u_player_mana(self):
        pass
