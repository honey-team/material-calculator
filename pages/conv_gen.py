from typing import Any, Callable, Literal

import flet as ft

from pages.utils.memory import mload, mwrite
from pages.utils.number import Number


def conv_gen(page: ft.Page, fun: Callable[..., dict[str, Any]]):
    info = fun()

    def on_change(*_):
        if at.value and bt.value:
            res: Number = info["function"](
                Number(x.value), info["types"].index(at.value), info["types"].index(bt.value)
            )
            r.value = str(res)
            page.update()
        m = mload()
        m["pages"]["converters"][info["mem_name"]]["a"] = x.value
        m["pages"]["converters"][info["mem_name"]]["at"] = info["types"].index(at.value) if at.value else 0
        m["pages"]["converters"][info["mem_name"]]["b"] = r.value
        m["pages"]["converters"][info["mem_name"]]["bt"] = info["types"].index(bt.value) if bt.value else 0
        mwrite(m)

    def get_type(x: Literal["a", "b"]) -> int:
        m = mload()
        match x:
            case "a":
                return x if (x := m["pages"]["converters"][info["mem_name"]]["at"]) else 0
            case "b":
                return x if (x := m["pages"]["converters"][info["mem_name"]]["bt"]) else 0

    m = mload()
    x = ft.TextField(
        value=m["pages"]["converters"][info["mem_name"]]["a"],
        on_change=on_change,
        input_filter=ft.InputFilter(allow=True, regex_string=r"[0-9,.-]", replacement_string=""),
    )
    r = ft.TextField(
        value=m["pages"]["converters"][info["mem_name"]]["b"],
        on_change=on_change,
        input_filter=ft.InputFilter(allow=True, regex_string=r"[0-9,.-]", replacement_string=""),
        read_only=True,
    )
    at = ft.Dropdown(
        options=[ft.dropdown.Option(i) for i in info["types"]], on_change=on_change, value=info["types"][get_type("a")]
    )
    bt = ft.Dropdown(
        options=[ft.dropdown.Option(i) for i in info["types"]], on_change=on_change, value=info["types"][get_type("b")]
    )
    page.add(x, at, ft.Divider(thickness=2), r, bt)

    return info["size"]
