from player import Player
from graphics_pos import graphics_pos
from screen_reader import ScreenReader
from PIL import Image
from actions import Actions
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
    
    def auto_heal(self):
        print( self._is_attached, ' ', self.attach_target, ' ', self.auto_heal_enabled )
        if self._is_attached is True and self.attach_target is not '' and self.auto_heal_enabled is True:
            print('auto heal firing')
            if self.players[self.attach_target].get_hp() < 0.60:
                print('heal cast')
                Actions.press_and_release_key('e')
                
            if self.players[self.attach_target].get_hp() < 0.15:
                print('summoenr heal')
                Actions.press_and_release_key('d')
                
                
    def set_attach_target(self, pos_str):
        self.attach_target = pos_str
    
    def get_player(self, pos_str):
        return self.players[pos_str]
    
    def toggle_auto_heal(self):
        self.auto_heal_enabled = not self.auto_heal_enabled
        
    def update(self, screen_img):
        self.img = screen_img
        self.u_player_hp()
        self.u_yummi_attached()
        self.auto_heal()
        
        
    def test_update(self):
        im = Image.open("pics/yummi_not_attached.png")
        self.update(im)
    
    def u_yummi_attached(self):
        x = graphics_pos['center_hp_player_bar']['x']
        y = graphics_pos['center_hp_player_bar']['y']
        w = graphics_pos['center_hp_player_bar']['width']
        
        avg_red = 0
        avg_green = 0
        avg_blue = 0
        
        for i in range(x, x + w):
            avg_red += self.img.getpixel((i, y))[0]
            avg_green += self.img.getpixel((i, y))[1]
            avg_blue += self.img.getpixel((i, y))[2]
        
        avg_red = avg_red / w
        avg_green = avg_green / w
        avg_blue = avg_blue / w
        print((avg_blue / (avg_red+0.01)), '|', avg_blue, '|',  avg_green, '|', avg_red  )
        if avg_blue / (avg_red+0.01) > 3 and avg_blue > 150 and avg_green > 100 and avg_red < 50:
            self._is_attached = True
        else:
            self._is_attached = False
        
            
    def u_player_hp(self):
        for player in self.players.values():
            start_x = player.hp_bar_start_x
            y = graphics_pos['hp_bars_left']['y']
            width = graphics_pos['hp_bars_left']['x-width']
            
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
            player.print_hp()      
