from math import cos, pi, sin

import flet as ft
import flet.canvas as cv

from pages.utils.const import INPUT_FILTER, S, stroke_paint
from pages.utils.memory import mload, mwrite
from pages.utils.number import Number


def degrad(page: ft.Page):
    def update_memory(*_):
        m = mload()
        m["pages"]["degrad"]["d"] = Number(d.value).get(5)
        m["pages"]["degrad"]["r"] = Number(r.value).get(5)
        mwrite(m)

    def change_d(*_):
        if Number(d.value) > 360:
            d.value = "360"
        r.value = pi / 180 * Number(d.value)
        update_canvas()
        page.update()
        update_memory()

    def change_r(*_):
        d.value = Number(r.value) * 180 / pi
        if Number(d.value) > 360:
            d.value = "360"
            r.value = Number(str(2 * pi))
        update_canvas()
        page.update()
        update_memory()

    def update_canvas(*_):
        R = Number(r.value)
        cp.shapes = [
            cv.Line(140, 140, 280, 140, stroke_paint(page)),
            cv.Line(140, 140, 140 + cos(R) * r1, 140 - sin(R) * r1, stroke_paint(page)),
            cv.Arc(
                140 - r2,
                140 - r2,
                2 * r2,
                2 * r2,
                start_angle=pi / 180 * (360 - (R * 180 / pi)),
                sweep_angle=R,
                paint=stroke_paint(page),
            ),
        ]

    m = mload()
    d = ft.TextField(value=m["pages"]["degrad"]["d"], label=S("Градусы"), input_filter=INPUT_FILTER, on_change=change_d)
    r = ft.TextField(value=m["pages"]["degrad"]["r"], label=S("Радианы"), input_filter=INPUT_FILTER, on_change=change_r)

    R = Number(r.value)
    r1 = 140
    r2 = 40

    cp = cv.Canvas(
        [
            cv.Line(140, 140, 280, 140, stroke_paint(page)),
            cv.Line(140, 140, 140 + cos(R) * r1, 140 - sin(R) * r1, stroke_paint(page)),
            cv.Arc(
                140 - r2,
                140 - r2,
                2 * r2,
                2 * r2,
                start_angle=pi / 180 * (360 - (R * 180 / pi)),
                sweep_angle=R,
                paint=stroke_paint(page),
            ),
        ]
    )

    page.add(d, r, cp)
    return 20
