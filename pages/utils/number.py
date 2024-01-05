class Number:
    def __init__(self, num: str) -> None:
        if ',' in num or '.' in num:
            num = num.replace(',', '.')
            self.num = float(num) if num else 0
        else:
            if num == '-':
                self.num = 0
            else:
                self.num = int(num) if num else 0
    
    def get(self, digits_after_comma: int = -1) -> int | float | str:
        if digits_after_comma == -1:
            return self.num
        else:
            s = f'%.{digits_after_comma}f' % self.num
            return s.replace('.', ',')
    
    def __int__(self) -> int:
        if isinstance(self.num, int):
            return self.get()
        return round(self.get())
    
    def __float__(self) -> float:
        if isinstance(self.num, float):
            return self.get()
        return float(self.get())

    def __str__(self) -> int:
        if isinstance(self.num, float):
            s = str(self.num)
            num = s.replace('.', ',')
            return num
        return str(self.num)
    
    def __repr__(self) -> str:
        return str(self)

    def __add__(self, other: 'int | float | Number'):
        if isinstance(other, Number):
            return Number(str(float(self) + float(other)))
        return Number(str(self.get() + other))
    
    def __radd__(self, other: 'int | float | Number'):
        if isinstance(other, Number):
            return Number(str(float(other) + float(self)))
        return Number(str(other + self.get()))
    
    def __sub__(self, other: 'int | float | Number'):
        if isinstance(other, Number):
            return Number(str(float(self) - float(other)))
        return Number(str(self.get() - other))
    
    def __rsub__(self, other: 'int | float | Number'):
        if isinstance(other, Number):
            return Number(str(float(other) - float(self)))
        return Number(str(other - self.get()))

    def __mul__(self, other: 'int | float | Number'):
        if isinstance(other, Number):
            return Number(str(float(self) * float(other)))
        return Number(str(self.get() * other))
    
    def __rmul__(self, other: 'int | float | Number'):
        if isinstance(other, Number):
            return Number(str(float(other) * float(self)))
        return Number(str(other * self.get()))

    def __truediv__(self, other: 'int | float | Number'):
        if isinstance(other, Number):
            return Number(str(float(self) / float(other)))
        return Number(str(self.get() / other))
    
    def __rtruediv__(self, other: 'int | float | Number'):
        if isinstance(other, Number):
            return Number(str(float(other) / float(self)))
        return Number(str(other / self.get()))
    
    def __pow__(self, other: 'int | float | Number'):
        if isinstance(other, Number):
            return Number(str(float(self) ** float(other)))
        return Number(str(self.get() ** other))

    def __rpow__(self, other: 'int | float | Number'):
        if isinstance(other, Number):
            return Number(str(float(other) ** float(self)))
        return Number(str(other ** self.get()))
    
    def __abs__(self) -> int:
        return abs(self.num)
