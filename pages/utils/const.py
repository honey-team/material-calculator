import flet as ft
from pages.utils.config import cload


def get_color_with_thememode(page: ft.Page):
    match page.theme_mode:
        case ft.ThemeMode.LIGHT:
            return "black"
        case ft.ThemeMode.DARK:
            return "white"

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
