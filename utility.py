from typing import Dict, Set

class UtilityFuncs:
    
    @staticmethod
    def fuzzy_color_match(input_c, output_c, max_color_dif = 5, min_color_diff = -5):
        if (input_c[0] - output_c[0]) > max_color_dif or (input_c[0] - output_c[0]) < min_color_diff:
            return False
        if (input_c[1] - output_c[1]) > max_color_dif or (input_c[1] - output_c[1]) < min_color_diff:
            return False
        if (input_c[2] - output_c[2]) > max_color_dif or (input_c[2] - output_c[2]) < min_color_diff:
            return False
    
        return True
    
    @staticmethod
    def dom_color(rgb):
        if rgb[0] > rgb[1] and rgb[0] > rgb[2]:
            return 'r'
        elif rgb[1] > rgb[0] and rgb[1] > rgb[2]:
            return 'g'
        elif rgb[2] > rgb[0] and rgb[2] > rgb[1]:
            return 'b'
        else:
            return 's'
        
    
    @staticmethod
    def get_dict_differences(d, o):
        diff = {}
        keys: Set = UtilityFuncs.dict_keys_to_set(d)
        
        for key in keys:
            v1 = UtilityFuncs._read_dict(d, key)
            v2 = UtilityFuncs._read_dict(o, key)
            
            if v1 == v2:
                UtilityFuncs._build_dict(diff, key, False)
            else:
                UtilityFuncs._build_dict(diff, key, True)
        return diff
   
    @staticmethod
    def dict_keys_to_set(d: Dict):
        keys = set()
        UtilityFuncs._inner_dict_keys_to_set(d, keys, "")
        return keys
      
    
    @staticmethod
    def _inner_dict_keys_to_set(d: Dict, keys: Set, i: str = ""):
        for k, v in d.items():
            n = i
            if isinstance(v, dict):
                if len(i) > 0:
                    n += "." + k
                else:
                    n += k
                UtilityFuncs._inner_dict_keys_to_set(v, keys, n)
            else:
                if len(n) > 0:
                    n += "." + k
                else:
                    n += k
                keys.add(n)
    
    @staticmethod
    def _read_dict(d: Dict, k: str):
        k_arr = k.split('.')
        r = d
        for key in k_arr:
            r = r[key]
        return r
    
    @staticmethod
    def _build_dict(d: Dict, k: str, v):
        k_arr = k.split('.')
        r = d
        for i in range(0, len(k_arr)):
            key = k_arr[i]
            if i == len(k_arr) - 1:
                r[key] = v
            else:
                if key not in d:
                    r[key] = {}
                r = r[key]
