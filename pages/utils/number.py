import math

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
        return _format_end(x2 + pow10)
    return _format_end(x)

def get_num(x: str) -> int | float:
    if '10**' in x:
        x, pow10 = x.split('**', 1)
        x = x.replace('10**', '')
        return float(eval(x)) * (10 ** int(pow10))
    return float(x)

class Number:
    def __init__(self, num: str) -> None:
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
                    self.num = num
    
    def __str__(self) -> int:
        return format_str(self.num)
    
    def __int__(self) -> int:
        if self.num.endswith('.0'):
            return int(get_num(self.num))
        return math.floor(get_num(self.num))
    
    def __float__(self) -> float:
        return float(get_num(self.num))
    
    def get(self, digits_after_comma: int = 0) -> str:
        if digits_after_comma <= 0:
            return format_str(self.num)
        s = f'%.{digits_after_comma}f' % self.num
        return s
    
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
    
    def __abs__(self) -> int:
        return abs(self.num)
