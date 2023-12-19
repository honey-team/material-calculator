import flet as ft
import flet.canvas as cv
from typing import Literal
from pages.utils.memory import load, write

FOCUSED_INPUT = None

class Number:
    def __init__(self, num: str) -> None:
        if ',' in num or '.' in num:
            num = num.replace(',', '.')
            self.num = float(num) if num else 0
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


def triangle(page: ft.Page):
    # a |
    # b _
    # c \
        
    def update_canvas():
        cv_a = float(Number(a.value))
        cv_b = float(Number(b.value))
        
        start_x, end_x = 10, 300
        start_y, end_y = 0, 350
        
        if cv_b:
            k = (end_x - start_x) / cv_b
        elif cv_a:
            k = (end_y - start_y) / cv_a
        else:
            k = 0
        
        if cv_a * k > (end_y - start_y):
            k = (end_y - start_y) / cv_a
        cp.shapes = [
            cv.Line(start_x, start_y, start_x, start_y + (cv_a * k)), # a
            cv.Line(start_x, start_y + (cv_a * k), start_x + (cv_b * k), start_y + (cv_a * k)), # b
            cv.Line(start_x, start_y, start_x + (cv_b * k), start_y + (cv_a * k)) # c
        ]
        cp.update()
        
    def change_abc(e):
        if e.control in [a, b]:
            ia, ib = Number(a.value), Number(b.value)
            
            ic = (ia**2 + ib**2)**0.5
            
            c.value = ic.get(3)
        
        elif e.control == c:
            i, ia = Number(c.value), Number(a.value)
            if i.get() and i.get() >= ia.get():
                ib = (i**2 - ia**2)**0.5
                b.value = ib.get(3)
            
        update_canvas()
        page.update()
        m = load()
        m['pages']['triangle']['a'] = a.value
        m['pages']['triangle']['b'] = b.value
        m['pages']['triangle']['c'] = c.value
        write(m)
        
    def on_focus(e):
        global FOCUSED_INPUT
        FOCUSED_INPUT = e.control
        
        if FOCUSED_INPUT == c:
            b.disabled = True
        else:
            b.disabled = False
        page.update()
    
    m = load()
    a = ft.TextField(label='a', value=m['pages']['triangle']['a'], on_change=change_abc, on_focus=on_focus, input_filter=ft.InputFilter(allow=True, regex_string=r"[0-9,.]", replacement_string=""))
    
    b = ft.TextField(label='b', value=m['pages']['triangle']['b'], on_change=change_abc, on_focus=on_focus, input_filter=ft.InputFilter(allow=True, regex_string=r"[0-9,.]", replacement_string=""))
    
    c = ft.TextField(label='c', value=m['pages']['triangle']['c'], on_change=change_abc, on_focus=on_focus, input_filter=ft.InputFilter(allow=True, regex_string=r"[0-9,.]", replacement_string=""))
    
    
    cv_a = float(a.value)
    cv_b = float(b.value)
    
    start_x, end_x = 10, 300
    start_y, end_y = 0, 350
    k = (end_x - start_x) / cv_b
    
    if cv_a * k > (end_y - start_y):
        k = (end_y - start_y) / cv_a
    
    
    def on_keyboard(e: ft.KeyboardEvent):
        def change_input(x: Literal[-1, 1]):
            if x == 1:
                l = [a, b, c]
            else:
                l = [c, b, a]
            index = l.index(FOCUSED_INPUT) + 1
            
            if index > 2:
                return
            else:
                l[index].focus()
        
        match e.key:
            case 'A': a.focus()
            case 'B': b.focus()
            case 'C': c.focus()
            case 'Arrow Down': change_input(1)
            case 'Arrow Up': change_input(-1)
        
        page.update()


    page.on_keyboard_event = on_keyboard
    page.update()
        
    
    cp = cv.Canvas(
        [
            cv.Line(start_x, start_y, start_x, start_y + (cv_a * k)), # a
            cv.Line(start_x, start_y + (cv_a * k), start_x + (cv_b * k), start_y + (cv_a * k)), # b
            cv.Line(start_x, start_y, start_x + (cv_b * k), start_y + (cv_a * k)) # c
        ]
    )
    page.add(a, b, c, cp)
