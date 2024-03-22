import flet as ft
from sympy import parse_expr, solve
from sympy.parsing.sympy_parser import implicit_multiplication_application, standard_transformations

from pages.utils.memory import mload, mwrite
from pages.utils.number import Number, check_for_reg, get_low


def equations(page: ft.Page):
    def update_memory(*_):
        m = mload()
        m["pages"]["equations"]["a"] = a.value
        try:
            m["pages"]["equations"]["x"] = solve_equation(a.value)
        except SyntaxError:
            pass
        mwrite(m)

    def solve_equation(formula):
        transformations = standard_transformations + (implicit_multiplication_application,)

        def map_operations(formula_str):
            return formula_str.replace("^", "**").replace("=", "-")

        f = parse_expr(map_operations(formula), transformations=transformations)
        return [check_for_reg(str(i)) for i in solve(f)]

    def get_answer(x: list[str]) -> str:
        res = ""
        for i, v in enumerate(x):
            res += f"x{get_low(Number(i+1))} = {v}\n"
        return res

    def solve_ev(*_):
        r.value = get_answer(solve_equation(a.value))
        page.update()
        update_memory()

    m = mload()
    a = ft.TextField(value=m["pages"]["equations"]["a"], label="Уравнение", on_change=update_memory)
    s = ft.FloatingActionButton(icon=ft.icons.CALCULATE, on_click=solve_ev)
    r = ft.Text(value=get_answer(m["pages"]["equations"]["x"]), size=20)

    page.add(a, s, ft.Text("Корни", size=20), ft.SelectionArea(content=r))

    return 20
