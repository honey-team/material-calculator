import math
from typing import Literal

import flet as ft

from pages.utils.const import S
from pages.utils.memory import mload, mwrite
from pages.utils.number import Number


def trigonometry(page: ft.Page):
    LAST_NUMBERED: Literal[1, 2] = 1

    def mem():
        m = mload()
        m["pages"]["trigonometry"]["a"] = deg.value
        m["pages"]["trigonometry"]["at"] = tdeg.value
        m["pages"]["trigonometry"]["f"] = fun.value
        m["pages"]["trigonometry"]["r"] = res_deg.value

    def change_1(*_):
        global LAST_NUMBERED
        LAST_NUMBERED = 1
        a = Number(deg.value)

        if tdeg.value == "deg":
            rad = math.pi / 180 * a
        else:
            rad = a

        def ctg(x: float):
            return 1 / math.tan(x)

        def do_f(function, *args):
            return str(Number(function(*args)))

        match fun.value:
            case "cos":
                res_deg.value = do_f(math.cos, float(rad))
            case "sin":
                res_deg.value = do_f(math.sin, float(rad))
            case "tg":
                res_deg.value = do_f(math.tan, float(rad))
            case "ctg":
                res_deg.value = do_f(ctg, float(rad))

        page.update()

    def change_2(*_):
        global LAST_NUMBERED
        LAST_NUMBERED = 2
        a = Number(res_deg.value)
        rad = Number("0")

        try:
            match fun.value:
                case "cos":
                    rad = Number(math.acos(float(a)))
                case "sin":
                    rad = Number(math.asin(float(a)))
                case "tg":
                    rad = Number(math.atan(float(a)))
                case "ctg":
                    rad = Number(math.atan(float(1 / a)))
        except ValueError:
            ...

        if tdeg.value == "deg":
            deg.value = str(rad * 180 / math.pi)
        else:
            deg.value = str(rad)
        page.update()

    def change_dd(*_):
        global LAST_NUMBERED
        match LAST_NUMBERED:
            case 1:
                change_1()
            case 2:
                change_2()

    m = mload()

    deg = ft.TextField(
        width=143,
        value=m["pages"]["trigonometry"]["a"],
        on_change=change_1,
        input_filter=ft.InputFilter(allow=True, regex_string=r"[0-9.-]", replacement_string=""),
    )
    tdeg = ft.Dropdown(
        options=[ft.dropdown.Option("deg", S("градусы")), ft.dropdown.Option("rad", S("радианы"))],
        value=m["pages"]["trigonometry"]["at"],
        width=160,
        on_change=change_dd,
    )

    fun = ft.Dropdown(
        options=[
            ft.dropdown.Option("cos", S("Конинус (cos)")),
            ft.dropdown.Option("sin", S("Синус (sin)")),
            ft.dropdown.Option("tg", S("Тангенс (tg)")),
            ft.dropdown.Option("ctg", S("Котангенс (ctg)")),
        ],
        value=m["pages"]["trigonometry"]["f"],
        on_change=change_dd,
    )

    res_deg = ft.TextField(
        value=m["pages"]["trigonometry"]["r"],
        on_change=change_2,
        input_filter=ft.InputFilter(allow=True, regex_string=r"[0-9.-]", replacement_string=""),
    )

    page.add(ft.Row([deg, tdeg]), fun, res_deg)

    return 20
