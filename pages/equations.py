import flet as ft
from sympy import N, parse_expr, solve
from sympy.parsing.sympy_parser import implicit_multiplication_application, standard_transformations

from pyperclip import copy as pc_copy

from pages.utils.config import cload
from pages.utils.memory import mload, mwrite
from pages.utils.number import Number, check_for_reg, get_low


def equations(page: ft.Page):
    def update_memory(*_):
        m = mload()
        m["pages"]["equations"]["a"] = a.value
        mwrite(m)

    def solve_equation(formula: str, format_answer: bool = True):
        transformations = standard_transformations + (implicit_multiplication_application,)

        def map_operations(formula_str):
            first, second = formula_str.replace('^', '**').split('=', 1)
            second = second.replace('+', '-')
            
            return f'{first}-{second}'

        f = parse_expr(map_operations(formula), transformations=transformations)
        
        res = []
        
        for i in solve(f):
            if isinstance(i, dict):
                res.append(i)
            else:
                if format_answer:
                    res.append(check_for_reg(str(i)))
                else:
                    res.append(i)
        return res

    def get_answer(x: list[str]) -> str:
        res = ""
        for i, v in enumerate(x):
            if isinstance(v, dict):
                for k, v2 in v.items():
                    res += f'{k}{get_low(Number(i+1))} = {v2}\n'
            else:
                res += f"x{get_low(Number(i+1))} = {v}\n"
        return res

    def solve_ev(*_):
        c = cload()
        if c['equations']['digits_in_result']:
            digits = solve_equation(a.value, False)
            digits = [check_for_reg(str(N(i, 6))) for i in digits]
            r.value = get_answer(digits)
        else:
            r.value = get_answer(solve_equation(a.value))
            row.height = get_height_of_row()
        page.update()
    
    def get_height_of_row() -> int:
        HEIGHT_OF_LINE = 20
        LINE_SPACING = 10
        FIELD_HEIGHT = 70
        
        I = 0
        for i in r.value.splitlines():
            if len(i) > 31:
                I += (len(i) - 31) // 31 + 1
        
        lines = len(r.value.splitlines()) + I
        width = FIELD_HEIGHT + HEIGHT_OF_LINE * (lines + 1) + LINE_SPACING * (lines + 2)
        
        return 445 - width

    m = mload()
    a = ft.TextField(value=m["pages"]["equations"]["a"], label="Уравнение", on_change=update_memory)
    r = ft.Text(value='', size=20)
    solve_ev()
    
    def copy_all(*_):
        pc_copy(r.value)
    
    s = ft.FloatingActionButton(icon=ft.icons.CALCULATE, on_click=solve_ev)
    c = ft.FloatingActionButton(icon=ft.icons.COPY, on_click=copy_all)
    
    row = ft.Row([s, c], vertical_alignment=ft.CrossAxisAlignment.END, alignment=ft.MainAxisAlignment.END, height=get_height_of_row())

    page.add(a, ft.Text("Корни", size=20), ft.SelectionArea(content=r), row)

    return 20
