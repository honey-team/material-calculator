import flet as ft

from pages.circle import circle
from pages.conv_gen import conv_gen
from pages.converters.length import length
from pages.converters.square import square
from pages.converters.temperature import temperature
from pages.converters.volume import volume
from pages.converters.weight import weight
from pages.default import default
from pages.degrad import degrad
from pages.equations import equations
from pages.log import log
from pages.quadratic import quadratic
from pages.radical import radical
from pages.right_triangle import right_triangle
from pages.settings import settings
from pages.simplify import simplify
from pages.trigonometry import trigonometry
from pages.utils.config import cload
from pages.utils.const import get_image_with_thememode
from pages.utils.memory import mload, mwrite

FUNCTIONS = [default, radical, log, quadratic, equations, simplify, degrad, right_triangle, trigonometry, circle]
CONVERTERS = [weight, length, square, volume, temperature]


def app(page: ft.Page):
    config = cload()

    page.window_height, page.window_width = 582, 348
    page.window_resizable, page.window_maximizable = False, False
    page.window_title_bar_hidden = True
    page.window_title_bar_buttons_hidden = True
    page.title = config["name"]

    # theme
    page.theme = ft.Theme(config["theme"]["bgcolor"])
    page.theme_mode = ft.ThemeMode.LIGHT if config["theme"]["mode"] == "light" else ft.ThemeMode.DARK

    def open_drawer(*_):
        page.drawer.open = True
        page.drawer.update()
    
    def minimize(*_):
        page.window_minimized = True
        page.update()

    page.appbar = ft.AppBar(
            leading=ft.WindowDragArea(ft.IconButton(ft.icons.MENU_ROUNDED, on_click=open_drawer)),
            title=ft.WindowDragArea(ft.Text("Обычный", max_lines=1)),
            actions=[
                ft.WindowDragArea(ft.IconButton(content=ft.Image(src=get_image_with_thememode('icons/minimize.png'), width=25, height=25), on_click=minimize)),
                ft.WindowDragArea(ft.IconButton(ft.icons.CLOSE, on_click=lambda *_: page.window_close(), icon_color=ft.colors.WHITE if page.theme_mode == ft.ThemeMode.DARK else ft.colors.BLACK)),
                ft.WindowDragArea(ft.Container(width=5))
            ]
        )

    def DividerText(label: str, with_divider: bool = True) -> ft.Text:
        div_text = ft.Row([ft.Container(width=20), ft.Text(label, size=17, weight=ft.FontWeight.W_600)])
        space = ft.Container(height=10)
        if with_divider:
            return ft.Column(
                spacing=0,
                controls=[
                    space,
                    ft.Divider(thickness=2),
                    space,
                    div_text,
                    space,
                ],
            )
        return ft.Column(spacing=0, controls=[div_text, space])

    def Destination(label: str, icon: str, selected_icon: str = None, image: bool = True):
        if image:
            if selected_icon:
                return ft.NavigationDrawerDestination(
                    label=label,
                    icon_content=ft.Image(src=get_image_with_thememode(f"icons/{icon}.png"), width=25, height=25),
                    selected_icon_content=ft.Image(
                        src=get_image_with_thememode(f"icons/{selected_icon}.png"), width=25, height=25
                    ),
                )
            else:
                return ft.NavigationDrawerDestination(
                    label=label,
                    icon_content=ft.Image(src=get_image_with_thememode(f"icons/{icon}.png"), width=25, height=25),
                )
        else:
            if selected_icon:
                return ft.NavigationDrawerDestination(label=label, icon=icon, selected_icon=selected_icon)
            else:
                return ft.NavigationDrawerDestination(label=label, icon=icon)

    m = mload()

    def change_page(*_):
        controls = page.drawer.controls
        only_destinations = []

        for i in controls:
            if isinstance(i, ft.NavigationDrawerDestination):
                only_destinations.append(i)

        page.drawer.open = False
        page.on_keyboard_event = None

        page.update()

        page.controls.clear()
        s = 20

        FUNCTIONS_INDEXES = [0, len(FUNCTIONS) - 1]

        if page.drawer.selected_index in list(range(FUNCTIONS_INDEXES[0], FUNCTIONS_INDEXES[1] + 1)):
            s = FUNCTIONS[page.drawer.selected_index](page)

        CONVERTERS_INDEXES = [FUNCTIONS_INDEXES[1] + 1, FUNCTIONS_INDEXES[1] + len(CONVERTERS)]

        if page.drawer.selected_index in list(range(CONVERTERS_INDEXES[0], CONVERTERS_INDEXES[1] + 1)):
            s = conv_gen(page, CONVERTERS[page.drawer.selected_index - CONVERTERS_INDEXES[0]])

        SETTINGS_INDEX = CONVERTERS_INDEXES[1] + 1
        if page.drawer.selected_index == SETTINGS_INDEX:
            s = settings(page)
            page.scroll = ft.ScrollMode.AUTO
        else:
            page.scroll = None

        page.appbar.title.value = only_destinations[page.drawer.selected_index].label
        page.appbar.title.size = s

        page.update()

        m = mload()
        m["page"] = page.drawer.selected_index
        mwrite(m)

    page.drawer = ft.NavigationDrawer(
        controls=[
            ft.Container(height=12),
            DividerText("Калькуляторы", False),
            ###
            Destination("Обычный", ft.icons.CALCULATE_OUTLINED, ft.icons.CALCULATE, image=False),
            ###
            DividerText("Алгебра"),
            ###
            Destination("Корень", "radical"),
            Destination("Логарифм", "log"),
            Destination("Квадратное уравнение", "quadratic"),
            Destination("Уравнение", "x"),
            Destination("Упростить (beta)", "a"),
            ###
            DividerText("Геометрия"),
            ###
            Destination("Конвертер углов", "angle_outlined", "angle"),
            Destination("Прямоугольный треугольник", "right_triangle_outlined", "right_triangle"),
            Destination("Тригонометрия", "angle_outlined", "angle"),
            Destination("Окружность", "circle_outlined", "circle"),
            DividerText("Конвертеры"),
        ],
        on_change=change_page,
        selected_index=m["page"],
    )

    for i in CONVERTERS:
        info = i()
        page.drawer.controls.append(Destination(info["name"], info["image"], info["sel_image"]))

    page.drawer.controls.append(ft.Container(height=50))
    page.drawer.controls.append(Destination("Настройки", ft.icons.SETTINGS_OUTLINED, ft.icons.SETTINGS, image=False))
    page.drawer.controls.append(ft.Container(height=25))

    change_page()
    page.update()


if __name__ == "__main__":
    ft.app(target=app, assets_dir="assets")
