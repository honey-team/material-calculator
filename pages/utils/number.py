import math
from typing import TypeVar

from pages.utils.const import S

def _format_end(x: str) -> str:
    if '.' in x:
        bc, ac = x.split('.', 1)
        if ac.endswith('0'):
            while ac.endswith('0'):
                ac = ac[:-1]
        x = f'{bc}.{ac}'
        if x.endswith('.'):
            x = x[:-1]
    return x

def format_str(x: str) -> str:
    if '10**' in x:
        x2, pow10 = x.split('**', 1)
        pow10 = pow10.replace('0', '⁰')
        pow10 = pow10.replace('1', '¹')
        pow10 = pow10.replace('2', '²')
        pow10 = pow10.replace('3', '³')
        pow10 = pow10.replace('4', '⁴')
        pow10 = pow10.replace('5', '⁵')
        pow10 = pow10.replace('6', '⁶')
        pow10 = pow10.replace('7', '⁷')
        pow10 = pow10.replace('8', '⁸')
        pow10 = pow10.replace('9', '⁹')
        pow10 = pow10.replace('-', '⁻')

        x3, other = list(map(lambda x: x.replace(' ', ''), x2.split('*', 1)))
        return f'{_format_end('%.5f' % float(x3))} * {other}{pow10}'
    return _format_end('%.5f' % float(x))

def get_num(x: str) -> int | float:
    if '10**' in x:
        x, pow10 = x.split('**', 1)
        x = x.replace('10**', '')
        return float(eval(x)) * (10 ** int(pow10))
    return float(x)

def format_point(x: str) -> str:
    if '.' in x:
        start, end = x.split('.', 1)
        res_end = list(end)[::-1]
        
        for i in ''.join(list(end)[::-1]):
            if i == '0':
                res_end = res_end[1:]
                continue
            else:
                break
        
        if len(res_end) == 0:
            return start
        return start + '.' + ''.join(res_end[::-1])
    else:
        return x

class Number:
    def __init__(self, num: str) -> None:
        num = str(num)
        self.num: str = '0'
        if num:
            if 'e' in num:
                x, pow10 = num.split('e', 1)
                if pow10.startswith('+'): pow10 = pow10[1:]
                
                if pow10.startswith('0') or pow10.startswith('-0'):
                    while pow10.startswith('0') or pow10.startswith('-0'):
                        pow10 = pow10.replace('0', '', 1)
                
                self.num = f'{x} * 10**{pow10}'
            else:
                if num == '-':
                    self.num = '0'
                else:
                    self.num = format_point(num)
    
    def __str__(self) -> int:
        return self.get(5)
    
    def __int__(self) -> int:
        if self.num.endswith('.0'):
            return int(get_num(self.num))
        return math.floor(get_num(self.num))
    
    def __float__(self) -> float:
        return float(get_num(self.num))
    
    def get(self, digits_after_comma: int = 0) -> str:
        if digits_after_comma <= 0:
            return format_str(self.num)
        s = f'%.{digits_after_comma}f' % float(self.num)
        return format_str(format_point(s))
    
    def __repr__(self) -> str:
        return str(self)

    def __add__(self, other: 'int | float | Number'):
        if isinstance(other, Number):
            return Number(str(float(self) + float(other)))
        return Number(format_str(str(float(self) + other)))
    
    def __radd__(self, other: 'int | float | Number'):
        if isinstance(other, Number):
            return Number(str(float(other) + float(self)))
        return Number(format_str(str(other + float(self))))
    
    def __sub__(self, other: 'int | float | Number'):
        if isinstance(other, Number):
            return Number(str(float(self) - float(other)))
        return Number(format_str(str(float(self) - other)))
    
    def __rsub__(self, other: 'int | float | Number'):
        if isinstance(other, Number):
            return Number(str(float(other) - float(self)))
        return Number(format_str(str(other - float(self))))

    def __mul__(self, other: 'int | float | Number'):
        if isinstance(other, Number):
            return Number(str(float(self) * float(other)))
        return Number(format_str(str(float(self) * other)))
    
    def __rmul__(self, other: 'int | float | Number'):
        if isinstance(other, Number):
            return Number(str(float(other) * float(self)))
        return Number(format_str(str(other * float(self))))

    def __truediv__(self, other: 'int | float | Number'):
        if isinstance(other, Number):
            return Number(str(float(self) / float(other)))
        return Number(format_str(str(float(self) / other)))
    
    def __rtruediv__(self, other: 'int | float | Number'):
        if isinstance(other, Number):
            return Number(str(float(other) / float(self)))
        return Number(format_str(str(other / float(self))))
    
    def __pow__(self, other: 'int | float | Number'):
        if isinstance(other, Number):
            return Number(str(float(self) ** float(other)))
        return Number(format_str(str(float(self) ** other)))

    def __rpow__(self, other: 'int | float | Number'):
        if isinstance(other, Number):
            return Number(str(float(other) ** float(self)))
        return Number(format_str(str(other ** float(self))))
    
    def __eq__(self, __value: 'Number | int | float') -> bool:
        if isinstance(__value, Number):
            return float(self) == float(__value)
        return float(self) == __value
    
    def __ne__(self, __value: 'Number | int | float') -> bool:
        if isinstance(__value, Number):
            return float(self) != float(__value)
        return float(self) != __value
    
    def __lt__(self, __value: 'Number | int | float') -> bool:
        if isinstance(__value, Number):
            return float(self) < float(__value)
        return float(self) < __value
    
    def __gt__(self, __value: 'Number | int | float') -> bool:
        if isinstance(__value, Number):
            return float(self) > float(__value)
        return float(self) > __value
    
    def __le__(self, __value: 'Number | int | float') -> bool:
        if isinstance(__value, Number):
            return float(self) <= float(__value)
        return float(self) <= __value
    
    def __ge__(self, __value: 'Number | int | float') -> bool:
        if isinstance(__value, Number):
            return float(self) >= float(__value)
        return float(self) >= __value
    
    def __abs__(self) -> int:
        return abs(self.num)


def get_low(a: Number):
    a = a.get(5)
    replace_chars = {
        '0': '₀',
        '1': '₁',
        '2': '₂',
        '3': '₃',
        '4': '₄',
        '5': '₅',
        '6': '₆',
        '7': '₇',
        '8': '₈',
        '9': '₉',
        '-': '₋'
    }
    
    for key, value in replace_chars.items():
        a = a.replace(key, value) 
    
    return a

def get_up(a: Number | str):
    if isinstance(a, Number):
        a = a.get(5)
    replace_chars = {
        '0': '⁰',
        '1': '¹',
        '2': '²',
        '3': '³',
        '4': '⁴',
        '5': '⁵',
        '6': '⁶',
        '7': '⁷',
        '8': '⁸',
        '9': '⁹',
        '-': '⁻',
        'a': 'ᵃ',
        'b': 'ᵇ',
        'c': 'ᶜ',
        'd': 'ᵈ',
        'e': 'ᵉ',
        'f': 'ᶠ',
        'g': 'ᵍ',
        'h': 'ʰ',
        'i': 'ⁱ',
        'j': 'ʲ',
        'k': 'ᵏ',
        'l': 'ˡ',
        'm': 'ᵐ',
        'n': 'ⁿ',
        'o': 'ᵒ',
        'p': 'ᵖ',
        'r': 'ʳ',
        's': 'ˢ',
        't': 'ᵗ',
        'u': 'ᵘ',
        'v': 'ᵛ',
        'w': 'ʷ',
        'x': 'ˣ',
        'y': 'ʸ',
        'z': 'ᶻ'
    }
    
    for key, value in replace_chars.items():
        a = a.replace(key, value) 
    
    return a

# Fix equations answers

REG: dict[str, str] = {
    '{x}': '{x}'
}
REP = {
    'sqrt': '√',
    'I': 'i',
    '**': '^',
}

from re import compile, findall

N = TypeVar('N', bound=str)
E = TypeVar('E', bound=str)

def to_standard_form(num_str: str) -> tuple[N, E]:
    num = float(num_str.replace(',', ''))
    exp = 0
    while num >= 10:
        num /= 10
        exp += 1
    while num < 1:
        num *= 10
        exp -= 1

    return f'{num:.3f}', str(exp)


def check_for_reg(x: str) -> str:
    res = x
    for R, RN in REG.items():
        mt = findall(compile(R.format(x='[\d\.\d]+')), res)
        mt = [str(i) for i in mt]
        xs = [findall(compile('[\d\.\d]+'), i)[0] for i in mt]
        
        for i, m in enumerate(mt):
            res = res.replace(m, RN.format(x=xs[i]))
    for k, v in REP.items():
        res = res.replace(k, v)
        
    mt = findall(compile('[\w\^\.]+\^[\w\^\.]+'), res)
    mt = [str(i) for i in mt]
    for i in mt:
        first, second = i.split('^', 1)
        res = res.replace(i, f'{first}{get_up(second)}')
        
    mt = findall(compile('[\w√]+\*[a-zA-z]'), res)
    mt = [str(i) for i in mt]
    for i in mt:
        x, y = i.split('*', 1)
        n = i
        if not y.isdigit() and not '.' in y:
            n = x + y
        res = res.replace(i, n)
        
    # round
    try:
        mt = findall('[\w\.]', res)
        mt = [str(i) for i in mt]
        for i in mt:
            if i.isdigit() and float(i) != int(i):
                res = res.replace(i, str(round(float(i), 5)))
                
        if not res:
            res = '0'
        
        res = res.replace('(', '').replace(')', '').replace(' ', '')

        res = f'{float(res.replace(',', '')):,}'

        if len(res) > 12:
            first, second = to_standard_form(res)
            return f'{_format_end(first)} * 10{get_up(second)}'
        R = _format_end(res.replace(',', ''))
        return S(f'{float(R):,}' if float(R) != int(R.replace('.', '')) else f'{int(R):,}')
    except ValueError:
        return S(res.replace(',', ''))
