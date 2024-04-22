import flet as ft
from sympy import parse_expr
from sympy import simplify as simp
from sympy.parsing.sympy_parser import implicit_multiplication_application, standard_transformations

from pages.utils.number import check_for_reg


def simplify(page: ft.Page):
    def simpl(formula):
        transformations = standard_transformations + (implicit_multiplication_application,)

        def map_operations(formula_str):
            return formula_str.replace("^", "**").replace("=", "-")

        f = parse_expr(map_operations(formula), transformations=transformations)
        return simp(f)

    def simplb(*_):
        r.value = check_for_reg(str(simpl(a.value)))
        page.update()

    a = ft.TextField(label="Уравнение", border_color='primary,0.5')
    s = ft.FloatingActionButton(icon=ft.icons.CALCULATE, on_click=simplb)
    r = ft.Text("")

    page.add(a, s, ft.SelectionArea(content=r))

    return 20
