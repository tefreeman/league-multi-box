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
        self.nexus_pos = None
        self._is_attached = False
        self.attach_target = ''
        self.auto_heal_enabled = False
        self.game_started = False
        self._is_moving = False
        self._can_learn_spell = False
        self._pos = None
    def to_dict(self):
        return {
            'players': {
                'top': self.players['top'].to_dict(),
                'jg': self.players['jg'].to_dict(),
                'mid': self.players['mid'].to_dict(),
                'adc':self.players['adc'].to_dict(),
            },
            'is_attached': self._is_attached,
            'attach_target': self.attach_target,
            'auto_heal_enabled': self.auto_heal_enabled,
            'is_moving': self._is_moving,
            'can_learn_spell': self._can_learn_spell
        }
            
    def set_attach_target(self, pos_str):
        self.attach_target = pos_str
        self.set_is_moving(True)
    
    def get_player(self, pos_str):
        return self.players[pos_str]
    
    def toggle_auto_heal(self):
        self.auto_heal_enabled = not self.auto_heal_enabled
        
    def update(self, screen_img):
        self.img = screen_img
        self.u_players_hp()
        self.u_yummi_attached()
        self.u_is_moving()
        self.u_can_learn_spell()
        self.u_player_pos()
        
        print(self._pos)
        GameLoop.run_commands(self)
        
    
    def u_can_learn_spell(self):
        if UtilityFuncs.fuzzy_color_match(self.img.getpixel((809,977)), (155, 116, 57)) is True:
            self._can_learn_spell = True
        elif UtilityFuncs.fuzzy_color_match(self.img.getpixel((858,977)), (155, 116, 57)) is True:
            self._can_learn_spell = True
        elif UtilityFuncs.fuzzy_color_match(self.img.getpixel((908,977)), (155, 116, 57)) is True:
            self._can_learn_spell = True
        elif UtilityFuncs.fuzzy_color_match(self.img.getpixel((957,977)), (155, 116, 57)) is True:
           self._can_learn_spell = True   
        else:
           self._can_learn_spell = False
           
    def test_update(self):
        im = Image.open("C:/Users/Trevor/Documents/pics/yummi_not_attached.png")
        self.update(im)
    
    def u_is_moving(self):
        if self._is_moving is True:
            if self.players[self.attach_target].is_alive() is False:
                self._is_moving is False
            
            if self._is_attached is True:
                 self._is_moving is False
            
    def set_is_moving(self, val):
        self._is_moving = val

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
            # set game to start
            self.game_started = True
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
    
    def u_player_pos(self):
        box_size = (81,46)
        minimap_ul = (13,780)
        minimap_lr = (298,1065)
        x = minimap_ul[0] + 10
        y = minimap_ul[1]
        x_values = []
        y_values = []
        white_pixel_loc = None
        wpl_flag = False
        while x < minimap_lr[0]:
            for j in range(y, minimap_lr[1]):
                if self.img.getpixel((x, j))[0] == 255 and self.img.getpixel((x, j))[1]  == 255 and  self.img.getpixel((x, j))[2] == 255:
                    wpl_flag = True
                    white_pixel_loc = (x, j)
                    x_values.append(x)
                    y_values.append(j)
                    break
            if wpl_flag is True:
                break
            x += box_size[0] - 10 
        
        
        n = white_pixel_loc[0]
        m = white_pixel_loc[0]
        
        while True: 
            x_pos_flag = False
            x_neg_flag = False
            
            if self.img.getpixel((n, white_pixel_loc[1]))[0] == 255 and self.img.getpixel((n, white_pixel_loc[1]))[1] == 255 and self.img.getpixel((n, white_pixel_loc[1]))[2] == 255:
                x_values.append(n)
                x_pos_flag = True
            
            if self.img.getpixel((n, white_pixel_loc[1]-1))[0] == 255 and self.img.getpixel((n, white_pixel_loc[1]-1))[1] == 255 and self.img.getpixel((n, white_pixel_loc[1]-1))[2] == 255:
                x_values.append(n)
                x_pos_flag = True
                
            if self.img.getpixel((m, white_pixel_loc[1]))[0] == 255 and self.img.getpixel((m, white_pixel_loc[1]))[1] == 255 and self.img.getpixel((m, white_pixel_loc[1]))[2] == 255:
                x_values.append(m)
                x_neg_flag = True
            
            if self.img.getpixel((m, white_pixel_loc[1]-1))[0] == 255 and self.img.getpixel((m, white_pixel_loc[1]-1))[1] == 255 and self.img.getpixel((m, white_pixel_loc[1]-1))[2] == 255:
                x_values.append(m)
                x_neg_flag = True
                
            if x_pos_flag is False and x_neg_flag is False:
                break
            
            n += 1
            m -= 1
        
        x_values.sort()
        
        L = x_values[0]
        R = x_values[len(x_values) - 1]
        
        d = white_pixel_loc[1]

        
        while True:
            y_left_flag = False
            y_right_flag =False

            if self.img.getpixel((L, d))[0] == 255 and self.img.getpixel((L, d))[1] == 255 and self.img.getpixel((L, d))[2] == 255:
                y_values.append(d)
                y_left_flag = True
            
            if self.img.getpixel((R, d))[0] == 255 and self.img.getpixel((R, d))[1] == 255 and self.img.getpixel((R, d))[2] == 255:
                y_values.append(d)
                y_right_flag = True
                
            if y_left_flag is False and y_right_flag is False: 
                break
            
            d -= 1

        y_values.sort()
        
        bx = box_size[0] / 2
        by = box_size[1] / 2
        xl = len(x_values) - 1
        yl = len(y_values) - 1
        if white_pixel_loc[0] < minimap_ul[0] + box_size[0]:
            # use right side
            if white_pixel_loc[1] < minimap_ul[1] + box_size[1]:
                #use lower right
                self._pos =  (x_values[xl]- bx, y_values[yl] -by)
            else:
                #use upper right
                self._pos = (x_values[xl]- bx, y_values[0]+ by)
        else:
            #use left side
            if white_pixel_loc[1] < minimap_ul[1] + box_size[1]:
                #use lower left
                self._pos = (x_values[0] + bx, y_values[yl] -by)
            else:
                #use upper left
                self._pos = (x_values[0] + bx, y_values[0] + by)
            
        


    def _find_center(self, point):
        pass     
        
