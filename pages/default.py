import flet as ft

from pages.utils.config import cload
from pages.utils.memory import mload, mwrite

BUTTON_SIZE = 70
SIZE = 87


def default(page: ft.Page) -> tuple[str, int]:
    def gen_button(text: str, click):
        return ft.FilledTonalButton(text, height=BUTTON_SIZE, width=BUTTON_SIZE, on_click=click)

    def get_color() -> str:
        colors = {
            "light": {
                "blue": "#39709c",  #
                "red": "#754349",
                "green": "#3f6b4f",
                "amber": "#8c7e3a",
                "purple": "#613e76",
            },
            "dark": {"blue": "#65aee9", "red": "#da8087", "green": "#85c796", "amber": "#f0d369", "purple": "#b576d0"},
        }

        c = cload()
        return colors[c["theme"]["mode"]][c["theme"]["bgcolor"]]

    def memory():
        m = mload()

        if m["page"] == 0:
            query = str(text.value)
            m["pages"]["default"]["query"] = query
            mwrite(m)

    def add_sym_to_txt(sym: str):
        if text.value != "Ошибка":
            text.value += sym
            page.update()
        memory()

    def reset_txt():
        text.value = "0"
        page.update()

    def fun_ac(e=None):
        reset_txt()
        memory()

    def fun_backspace():
        if len(text.value) != 1:
            text.value = text.value[:-1]
        else:
            text.value = "0"
        page.update()
        memory()

    def fun_plus_minus(e=None):
        if text.value != "0" and text.value != "Ошибка":
            if text.value.startswith("-"):
                text.value = text.value.removeprefix("-")
            else:
                text.value = "-" + text.value
        memory()

    def fun_degree(e=None):
        if text.value != "0" and text.value != "Ошибка":
            add_sym_to_txt("**")
        memory()

    def fun_div(e=None):
        if text.value != "0" and text.value != "Ошибка":
            add_sym_to_txt("/")
        memory()

    def fun_1(e=None):
        if text.value != "0":
            add_sym_to_txt("1")
        else:
            text.value = "1"
            page.update()
        memory()

    def fun_2(e=None):
        if text.value != "0":
            add_sym_to_txt("2")
        else:
            text.value = "2"
            page.update()
        memory()

    def fun_3(e=None):
        if text.value != "0":
            add_sym_to_txt("3")
        else:
            text.value = "3"
            page.update()
        memory()

    def fun_mul(e=None):
        if text.value != "0" and text.value != "Ошибка":
            add_sym_to_txt("*")
        memory()

    def fun_4(e=None):
        if text.value != "0":
            add_sym_to_txt("4")
        else:
            text.value = "4"
            page.update()
        memory()

    def fun_5(e=None):
        if text.value != "0":
            add_sym_to_txt("5")
        else:
            text.value = "5"
            page.update()
        memory()

    def fun_6(e=None):
        if text.value != "0":
            add_sym_to_txt("6")
        else:
            text.value = "6"
            page.update()
        memory()

    def fun_sum(e=None):
        if text.value != "0" and text.value != "Ошибка":
            add_sym_to_txt("+")
        memory()

    def fun_7(e=None):
        if text.value != "0":
            add_sym_to_txt("7")
        else:
            text.value = "7"
            page.update()
        memory()

    def fun_8(e=None):
        if text.value != "0":
            add_sym_to_txt("8")
        else:
            text.value = "8"
            page.update()
        memory()

    def fun_9(e=None):
        if text.value != "0":
            add_sym_to_txt("9")
        else:
            text.value = "9"
            page.update()
        memory()

    def fun_sub(e=None):
        if text.value != "0" and text.value != "Ошибка":
            add_sym_to_txt("-")
        memory()

    def fun_0(e=None):
        if text.value != "0":
            add_sym_to_txt("0")
        memory()

    def fun_point(e=None):
        if text.value != "0" and text.value != "Ошибка":
            add_sym_to_txt(".")
        memory()

    def _format_int(x: str) -> int | float:
        res = float(x)

        if int(res) == res:
            res = str(int(res))

        return res

    def fun_equal(e=None):
        if text.value != "Ошибка":
            try:
                text.value = _format_int(str("%.5f" % float(eval(text.value))))
                page.update()
            except ZeroDivisionError:
                text.value = "Ошибка"
                page.update()
        memory()

    text = ft.Text(
        "0",
        size=BUTTON_SIZE - 23,
        text_align=ft.TextAlign.RIGHT,
        color=get_color(),
        width=SIZE * 4,
        font_family="sf pro text",
    )

    button_ac = gen_button("AC", fun_ac)
    button_plus_minus = gen_button("±", fun_plus_minus)
    button_degree = gen_button("^", fun_degree)
    button_div = gen_button("÷", fun_div)

    button_7 = gen_button("7", fun_7)
    button_8 = gen_button("8", fun_8)
    button_9 = gen_button("9", fun_9)
    button_mul = gen_button("×", fun_mul)

    button_4 = gen_button("4", fun_4)
    button_5 = gen_button("5", fun_5)
    button_6 = gen_button("6", fun_6)
    button_sum = gen_button("+", fun_sum)

    button_1 = gen_button("1", fun_1)
    button_2 = gen_button("2", fun_2)
    button_3 = gen_button("3", fun_3)
    button_sub = gen_button("-", fun_sub)

    button_0 = ft.FilledTonalButton("0", height=BUTTON_SIZE, width=BUTTON_SIZE * 2 + 10, on_click=fun_0)
    button_point = gen_button(".", fun_point)
    button_equal = gen_button("=", fun_equal)

    def on_keyboard(e: ft.KeyboardEvent):
        match e.key:
            case "Delete":
                fun_ac()
            case "Backspace":
                fun_backspace()
            case "^":
                fun_degree()
            case "/" | "Numpad Divide":
                fun_div()
            case "1" | "Numpad 1":
                fun_1()
            case "2" | "Numpad 2":
                fun_2()
            case "3" | "Numpad 3":
                fun_3()
            case "*" | "Numpad Multiply":
                fun_mul()
            case "4" | "Numpad 4":
                fun_4()
            case "5" | "Numpad 5":
                fun_5()
            case "6" | "Numpad 6":
                fun_6()
            case "+" | "Numpad Add":
                fun_sum()
            case "7" | "Numpad 7":
                fun_7()
            case "8" | "Numpad 8":
                fun_8()
            case "9" | "Numpad 9":
                fun_9()
            case "-" | "Numpad Subtract":
                fun_sub()
            case "0" | "Numpad 0":
                fun_0()
            case "." | "Numpad Decimal":
                fun_point()
            case "=" | "Enter":
                fun_equal()

    page.on_keyboard_event = on_keyboard
    page.update()

    m = mload()
    text.value = m["pages"]["default"]["query"]

    page.add(
        text,
        ft.Row([button_ac, button_plus_minus, button_degree, button_div]),
        ft.Row([button_7, button_8, button_9, button_mul]),
        ft.Row([button_4, button_5, button_6, button_sum]),
        ft.Row([button_1, button_2, button_3, button_sub]),
        ft.Row([button_0, button_point, button_equal]),
    )

    return 20
