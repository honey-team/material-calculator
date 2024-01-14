from pages.utils.number import Number

def volume():
    def a(x: Number, a_t: int, b_t: int):
        pows = [-9, -6, -3, 0, 9, 18]
        
        p = Number(str(pows[a_t] - pows[b_t]))
        
        res = (10**p) * x
        return res
            
    return {
        'name': 'Объём',
        'size': 20,
        'image': 'icons/volume.png',
        'sel_image': 'icons/volume.png',
        'types': [
            'кубический миллиметр',
            'кубический сантиметр',
            'кубический дециметр',
            'кубический метр',
            'кубический километр',
            'кубический мегаметр'
            ],
        'function': a,
        'mem_name': 'volume'
    }