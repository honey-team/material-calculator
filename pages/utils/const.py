import flet as ft


def get_color_with_thememode(page: ft.Page):
    match page.theme_mode:
        case ft.ThemeMode.LIGHT:
            return "black"
        case ft.ThemeMode.DARK:
            return "white"


def stroke_paint(page):
    return ft.Paint(color=get_color_with_thememode(page), stroke_width=2, style=ft.PaintingStyle.STROKE)


INPUT_FILTER = ft.InputFilter(allow=True, regex_string=r"[0-9.]", replacement_string="")
