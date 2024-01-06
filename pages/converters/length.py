from pages.utils.number import Number

def length():
    def a(x: Number, a_t: int, b_t: int):
        pows = [-3, -2, None, -1, 0, 3, None, 6]

        def to_m(x: Number, one_xtm: Number) -> Number:
            return x * one_xtm
        
        match a_t:
            case 2: # дюйм
                m = to_m(x, Number('0,0254'))
                
                match b_t:
                    case 2: return x
                    case 6: return m / 1852
                    case _:
                        p = Number(str(pows[4] - pows[b_t]))
                        
                        return (10**p) * m
            case 6: # морская миля
                m = to_m(x, Number('1852'))
                
                match b_t:
                    case 2: return m / 0.0254
                    case 6: return x
                    case _:
                        p = Number(str(pows[4] - pows[b_t]))
                        
                        return (10**p) * m
            case _:
                match b_t:
                    case 2:
                        m = to_m(x, str(10**pows[a_t]))
                        return m / 0.0254
                    case 6:
                        m = to_m(x, str(10**pows[a_t]))
                        return m / 1852
                    case _:
                        p = Number(str(pows[a_t] - pows[b_t]))

                        return (10**p) * x
            
    return {
        'name': 'Длина',
        'size': 20,
        'image': 'icons/weight_outlined.png',
        'sel_image': 'icons/weight.png',
        'types': [
            'миллиметр',
            'сантиметр',
            'дюйм',
            'дециметр',
            'метр',
            'километр',
            'морская миля',
            'мегаметр'
            ],
        'function': a,
        'mem_name': 'length'
    }