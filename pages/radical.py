import flet as ft

from pages.utils.const import S
from pages.utils.memory import mload, mwrite
from pages.utils.number import Number, get_up


def radical(page: ft.Page):
    def on_change(*_):
        m = mload()
        m["pages"]["radical"]["n"] = n.value
        m["pages"]["radical"]["a"] = a.value
        mwrite(m)

        try:
            num = Number(a.value)
            _pow = 1 / Number(n.value)
            num = num**_pow
        except ZeroDivisionError:
            num = None

        txt.value = TXT.format(n=S(get_up(Number(n.value))), a=S(Number(a.value)), r=S(Number(num)) if num else "?")
        page.update()

    m = mload()

    TXT = "{n}√{a} = {r}"

    n = ft.TextField(
        value=m["pages"]["radical"]["n"],
        label=S("n"),
        input_filter=ft.InputFilter(allow=True, regex_string=r"[0-9.-]", replacement_string=""),
        on_change=on_change,
    )
    a = ft.TextField(
        value=m["pages"]["radical"]["a"],
        label=S("a"),
        input_filter=ft.InputFilter(allow=True, regex_string=r"[0-9.-]", replacement_string=""),
        on_change=on_change,
    )

    try:
        num = Number(a.value)
        _pow = 1 / Number(n.value)
        num = num**_pow
    except ZeroDivisionError:
        num = None

    txt = ft.Text('', size=25)
    on_change()

    page.add(txt, ft.Container(height=40), n, a)

    return 20
