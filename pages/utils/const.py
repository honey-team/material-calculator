import flet as ft
from pages.utils.config import cload
from typing import Protocol

def get_color_with_thememode(page: ft.Page):
    match page.theme_mode:
        case ft.ThemeMode.LIGHT:
            return "black"
        case ft.ThemeMode.DARK:
            return "white"

OPACITY = 0.75

def get_bgcolor_for_window_with_thememode(page: ft.Page):
    match page.theme_mode:
        case ft.ThemeMode.LIGHT:
            return f'white,{OPACITY}'
        case ft.ThemeMode.DARK:
            return f'black,{OPACITY}'

def get_bgcolor_for_control_with_thememode(bgcolor: str, opacity: float = OPACITY):
    return f'{bgcolor},{opacity}'

def get_image_with_thememode(x: str):
        c = cload()
        if c["theme"]["mode"] == "light":
            return x
        else:
            x = x.replace(".png", "")
            return x + "_w.png"


def stroke_paint(page):
    return ft.Paint(color=get_color_with_thememode(page), stroke_width=2, style=ft.PaintingStyle.STROKE)


INPUT_FILTER = ft.InputFilter(allow=True, regex_string=r"[0-9.]", replacement_string="")


class SupportsStr(Protocol):
    def __str__(self) -> str: ...

# 1st april
def S(x: SupportsStr) -> str:
    # x = str(x)
    # res = ''
    # for i in x:
    #     if not i in [' ', '(', ')', '.', ',', '-', '+', '*', '/', '√']:
    #         res += '?'
    #     else:
    #         res += i
    # return res
    return str(x)
