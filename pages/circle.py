from math import cos, pi, sin

import flet as ft
import flet.canvas as cv

from pages.utils.const import INPUT_FILTER, S, stroke_paint
from pages.utils.memory import mload, mwrite
from pages.utils.number import Number


def circle(page: ft.Page):
    def update_memory(*_):
        m = mload()
        m["pages"]["circle"]["r"] = str(Number(r.value))
        m["pages"]["circle"]["c"] = str(Number(C.value))
        m["pages"]["circle"]["a"] = str(Number(a.value))
        m["pages"]["circle"]["at"] = at.value
        m["pages"]["circle"]["l"] = str(Number(l.value))
        mwrite(m)

    def update_canvas(*_):
        match at.value:
            case "d":
                R = pi / 180 * Number(a.value)
            case "r":
                R = Number(a.value)
        cp.shapes = [
            cv.Circle(150, 85, 85, stroke_paint(page)),
            cv.Line(150, 85, 150 + cos(pi / 180 * -120) * 85, 85 + sin(pi / 180 * -120) * 85, stroke_paint(page)),
            cv.Line(
                150,
                85,
                150 + cos(pi / 180 * (-120 + R * 180 / pi)) * 85,
                85 + sin(pi / 180 * (-120 + R * 180 / pi)) * 85,
                stroke_paint(page),
            ),
            cv.Text(150 + cos(pi / 180 * -120) * 85, 105 + sin(pi / 180 * -120) * 85, "r", ft.TextStyle(size=20)),
        ]
        page.update()

    def change_r(*_):
        C.value = 2 * pi * Number(r.value)

        match at.value:
            case "d":
                R = pi / 180 * Number(a.value)
            case "r":
                R = Number(a.value)
        l.value = R * Number(r.value)

        page.update()
        update_memory()

    def change_C(*_):
        r.value = Number(C.value) / 2 / pi
        page.update()
        update_memory()

    def change_a(*_):
        match at.value:
            case "d":
                R = pi / 180 * Number(a.value)
            case "r":
                R = Number(a.value)
        l.value = R * Number(r.value)
        update_canvas()
        update_memory()

    def change_at(*_):
        match at.value:
            case "d":
                a.value = Number(a.value) * 180 / pi
            case "r":
                a.value = Number(a.value) * pi / 180
        page.update()
        change_a()

    def change_l(*_):
        R = Number(l.value) / Number(r.value)
        match at.value:
            case "d":
                a.value = R * 180 / pi
            case "r":
                a.value = R
        update_canvas()
        update_memory()

    m = mload()
    r = ft.TextField(value=m["pages"]["circle"]["r"], label=S("радиус"), on_change=change_r, input_filter=INPUT_FILTER)
    C = ft.TextField(value=m["pages"]["circle"]["c"], label=S("длина"), on_change=change_C, input_filter=INPUT_FILTER)
    a = ft.TextField(
        value=m["pages"]["circle"]["a"],
        label=S("центральный угол"),
        width=182,
        on_change=change_a,
        input_filter=INPUT_FILTER,
    )
    at = ft.Dropdown(
        value=m["pages"]["circle"]["at"],
        width=120,
        options=[ft.dropdown.Option("d", S("градусов")), ft.dropdown.Option("r", S("радиан"))],
        on_change=change_at,
    )
    l = ft.TextField(value=m["pages"]["circle"]["l"], label=S("длина дуги"), on_change=change_l, input_filter=INPUT_FILTER)

    match at.value:
        case "d":
            R = pi / 180 * Number(a.value)
        case "r":
            R = Number(a.value)

    cp = cv.Canvas(
        [
            cv.Circle(150, 85, 85, stroke_paint(page)),
            cv.Line(150, 85, 150 + cos(pi / 180 * -120) * 85, 85 + sin(pi / 180 * -120) * 85, stroke_paint(page)),
            cv.Line(
                150,
                85,
                150 + cos(pi / 180 * (-120 + R * 180 / pi)) * 85,
                85 + sin(pi / 180 * (-120 + R * 180 / pi)) * 85,
                stroke_paint(page),
            ),
            cv.Text(150 + cos(pi / 180 * -120) * 85, 105 + sin(pi / 180 * -120) * 85, "r", ft.TextStyle(size=20)),
        ]
    )

    page.add(r, C, ft.Row([a, at]), l, cp)

    return 20
