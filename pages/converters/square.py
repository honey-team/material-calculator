from pages.utils.number import Number

def square():
    def a(x: Number, a_t: int, b_t: int):
        pows = [-6, -4, -2, 0, 6, 12]
        
        p = Number(str(pows[a_t] - pows[b_t]))
        
        res = (10**p) * x
        return res
            
    return {
        'name': 'Площадь',
        'size': 20,
        'image': 'icons/square_outlined.png',
        'sel_image': 'icons/square.png',
        'types': [
            'квадратный миллиметр',
            'квадратный сантиметр',
            'квадратный дециметр',
            'квадратный метр',
            'квадратный километр',
            'квадратный мегаметр'
            ],
        'function': a,
        'mem_name': 'square'
    }