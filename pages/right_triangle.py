import flet as ft
import flet.canvas as cv
from typing import Literal
from pages.utils.memory import mload, mwrite
from pages.utils.number import Number
from pages.utils.const import stroke_paint, INPUT_FILTER

FOCUSED_INPUT = None


def right_triangle(page: ft.Page) -> tuple[str, int]:
    # a |
    # b _
    # c \
        
    def update_canvas():
        cv_a = float(Number(a.value))
        cv_b = float(Number(b.value))
        
        if cv_b:
            k = (end_x - start_x) / cv_b
        elif cv_a:
            k = (end_y - start_y) / cv_a
        else:
            k = 0
        
        if cv_a * k > (end_y - start_y):
            k = (end_y - start_y) / cv_a
        cp.shapes = [
            cv.Line(start_x, start_y, start_x, start_y + (cv_a * k), stroke_paint(page)), # a
            cv.Line(start_x, start_y + (cv_a * k), start_x + (cv_b * k), start_y + (cv_a * k), stroke_paint(page)), # b
            cv.Line(start_x, start_y, start_x + (cv_b * k), start_y + (cv_a * k), stroke_paint(page)) # c
        ]
        cp.update()
        
    def change_abc(e):
        if e.control in [a, b]:
            ia, ib = Number(a.value), Number(b.value)
            
            ic = (ia**2 + ib**2)**0.5
            
            c.value = ic.get(3)
        
        elif e.control == c:
            if FOCUSED_INPUT == a:
                i, ia = Number(c.value), Number(a.value)
                if i.get() and i.get() >= ia.get():
                    ib = (i**2 - ia**2)**0.5
                    b.value = ib.get(3)
            elif FOCUSED_INPUT == b:
                i, ib = Number(c.value), Number(b.value)
                if i.get() and i.get() >= ib.get():
                    ia = (i**2 - ib**2)**0.5
                    a.value = ia.get(3)
            
        update_canvas()
        page.update()
        m = mload()
        m['pages']['right_triangle']['a'] = a.value
        m['pages']['right_triangle']['b'] = b.value
        m['pages']['right_triangle']['c'] = c.value
        mwrite(m)
        
    def on_focus(e):
        global FOCUSED_INPUT
        
        if e.control == c:
            FOCUSED_INPUT.disabled = True
        else:
            FOCUSED_INPUT = e.control
            a.disabled = False
            b.disabled = False
        page.update()
    
    m = mload()
    a = ft.TextField(label='a (катет слева)', value=m['pages']['right_triangle']['a'], on_change=change_abc, on_focus=on_focus, input_filter=INPUT_FILTER)
    
    b = ft.TextField(label='b (катет снизу)', value=m['pages']['right_triangle']['b'], on_change=change_abc, on_focus=on_focus, input_filter=INPUT_FILTER)
    
    c = ft.TextField(label='c (гипотенуза)', value=m['pages']['right_triangle']['c'], on_change=change_abc, on_focus=on_focus, input_filter=INPUT_FILTER)
    
    
    cv_a = float(a.value)
    cv_b = float(b.value)
    
    start_x, end_x = 30, 300
    start_y, end_y = 0, 220
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
            cv.Line(start_x, start_y, start_x, start_y + (cv_a * k), stroke_paint(page)), # a
            cv.Line(start_x, start_y + (cv_a * k), start_x + (cv_b * k), start_y + (cv_a * k), stroke_paint(page)), # b
            cv.Line(start_x, start_y, start_x + (cv_b * k), start_y + (cv_a * k), stroke_paint(page)) # c
        ]
    )
    page.add(a, b, c, cp)
    
    return 'Прямоугольный треугольник', 17
