import flet as ft
import flet.canvas as cv
from math import cos, sin, pi

from pages.utils.number import Number
from pages.utils.colors import stroke_paint

def circle(page: ft.Page):
    def update_canvas(*_):
        match at.value:
            case 'd':
                R = pi / 180 * Number(a.value)
            case 'r':
                R = Number(a.value)
        cp.shapes = [
            cv.Circle(150,85,85, stroke_paint(page)),
            cv.Line(150,85,150 + cos(pi/180*-120)*85, 85 + sin(pi/180*-120)*85, stroke_paint(page)),
            cv.Line(150,85,150 + cos(pi/180*(-120 + R * 180 / pi)) * 85, 85 + sin(pi/180*(-120 + R * 180 / pi))*85, stroke_paint(page)),
            cv.Text(150 + cos(pi/180*-120)*85, 105 + sin(pi/180*-120)*85, 'r', ft.TextStyle(size=20))
        ]
        page.update()
    
    def change_r(*_):
        C.value = 2 * pi * Number(r.value)
        
        match at.value:
            case 'd':
                R = pi / 180 * Number(a.value)
            case 'r':
                R = Number(a.value)
        l.value = R * Number(r.value)
        
        page.update()
    
    def change_C(*_):
        r.value = Number(C.value) / 2 / pi
        page.update()
        
    def change_a(*_):
        match at.value:
            case 'd':
                R = pi / 180 * Number(a.value)
            case 'r':
                R = Number(a.value)
        l.value = R * Number(r.value)
        update_canvas()
    
    def change_l(*_):
        R = Number(l.value) / Number(r.value)
        match at.value:
            case 'd':
                a.value = R * 180 / pi
            case 'r':
                a.value = R
        update_canvas()

    r = ft.TextField(label='радиус', on_change=change_r)
    C = ft.TextField(label='длина', on_change=change_C)
    a = ft.TextField(label='центральный угол', value='0', width=182, on_change=change_a)
    at = ft.Dropdown(width=120, options=[
        ft.dropdown.Option('d', 'градусов'),
        ft.dropdown.Option('r', 'радиан')
    ], value='d', on_change=change_a
    )
    l = ft.TextField(label='длина дуги', on_change=change_l)
    
    match at.value:
            case 'd':
                R = pi / 180 * Number(a.value)
            case 'r':
                R = Number(a.value)
    
    cp = cv.Canvas(
        [
            cv.Circle(150,85,85, stroke_paint(page)),
            cv.Line(150,85,150 + cos(pi/180*-120)*85, 85 + sin(pi/180*-120)*85, stroke_paint(page)),
            cv.Line(150,85,150 + cos(pi/180*(-120 + R * 180 / pi)) * 85, 85 + sin(pi/180*(-120 + R * 180 / pi))*85, stroke_paint(page)),
            cv.Text(150 + cos(pi/180*-120)*85, 105 + sin(pi/180*-120)*85, 'r', ft.TextStyle(size=20))
        ]
    )
    
    page.add(r,C,ft.Row([a, at]),l, cp)
    
    return 'Окружность', 14
