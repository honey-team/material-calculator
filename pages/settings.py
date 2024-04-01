import json

import flet as ft

from pages.utils.config import cload, cwrite
from pages.utils.const import S, get_image_with_thememode
from pages.utils.memory import mwrite


def settings(page: ft.Page):
    config = cload()

    def _change_page_theme():
        config = cload()
        page.theme = ft.Theme(config["theme"]["bgcolor"])
        page.update()

    def _change_config_theme(bgcolor: str):
        config = cload()
        config["theme"]["bgcolor"] = bgcolor
        cwrite(config)

        _change_page_theme()

    def change_theme_blue(*_):
        _change_config_theme("blue")

    def change_theme_red(*_):
        _change_config_theme("red")

    def change_theme_green(*_):
        _change_config_theme("green")

    def change_theme_amber(*_):
        _change_config_theme("amber")

    def change_theme_purple(*_):
        _change_config_theme("purple")

    def change_theme_mode(*_):
        config = cload()
        if theme_mode.value:
            page.theme_mode = ft.ThemeMode.DARK
            config["theme"]["mode"] = "dark"
            theme_mode.label = "Тёмная тема"
        else:
            page.theme_mode = ft.ThemeMode.LIGHT
            config["theme"]["mode"] = "light"
            theme_mode.label = "Светлая тема"
        cwrite(config)

        for i in page.drawer.controls:
            if isinstance(i, ft.NavigationDrawerDestination):
                if config["theme"]["mode"] == "light":
                    if i.selected_icon_content:
                        if "_w" in i.selected_icon_content.src:
                            i.selected_icon_content.src = i.selected_icon_content.src.replace("_w", "")
                    if i.icon_content:
                        if "_w" in i.icon_content.src:
                            i.icon_content.src = i.icon_content.src.replace("_w", "")
                else:
                    if i.selected_icon_content:
                        if not "_w" in i.selected_icon_content.src:
                            x = i.selected_icon_content.src.replace(".png", "")
                            i.selected_icon_content.src = x + "_w.png"
                    if i.icon_content:
                        if not "_w" in i.icon_content.src:
                            x = i.icon_content.src.replace(".png", "")
                            i.icon_content.src = x + "_w.png"
 
        def minimize(*_):
            page.window_minimized = True
            page.update()

        page.appbar.actions=[
                ft.WindowDragArea(ft.IconButton(content=ft.Image(src=get_image_with_thememode('icons/minimize.png'), width=25, height=25), on_click=minimize)),
                ft.WindowDragArea(ft.IconButton(ft.icons.CLOSE, on_click=lambda *_: page.window_close(), icon_color=ft.colors.WHITE if page.theme_mode == ft.ThemeMode.DARK else ft.colors.BLACK)),
                ft.WindowDragArea(ft.Container(width=5))
            ]

        page.update()

    def reset_memory(*_):
        with open("default_memory.json", "r", encoding="utf-8") as MemoryFile:
            rawJson = MemoryFile.read()
        m = json.loads(rawJson)
        mwrite(m)

    def reset_config(*_):
        with open("default_config.json", "r", encoding="utf-8") as ConfigFile:
            rawJson = ConfigFile.read()
        c = json.loads(rawJson)
        cwrite(c)
        _change_page_theme()
        theme_mode.value = False
        change_theme_mode()

    def reset_all(*_):
        reset_memory()
        reset_config()
    
    def change_digits_in_result(e):
        c = cload()
        c['equations']['digits_in_result'] = e.control.value
        cwrite(c)

    space = ft.Container(height=10)
    space2 = ft.Container(height=20)

    ctm = config["theme"]["mode"]
    theme_mode = ft.Switch(
        label=S("Светлая тема") if ctm == "light" else S("Тёмная тема"), value=ctm == "dark", on_change=change_theme_mode
    )

    page.add(
        ft.ListView(
            [
                ft.Text(S(config["name"]), size=35),
                ft.Text(S(config["version"]), size=20),
                space2,
                ft.Text(S("Темы"), size=25, weight=ft.FontWeight.W_600),
                space2,
                theme_mode,
                ft.Row(
                    [
                        ft.ElevatedButton(
                            style=ft.ButtonStyle(bgcolor=ft.colors.BLUE_300, shape=ft.CircleBorder(), padding=33),
                            on_click=change_theme_blue,
                        ),
                        ft.ElevatedButton(
                            style=ft.ButtonStyle(bgcolor=ft.colors.RED_300, shape=ft.CircleBorder(), padding=33),
                            on_click=change_theme_red,
                        ),
                        ft.ElevatedButton(
                            style=ft.ButtonStyle(bgcolor=ft.colors.GREEN_300, shape=ft.CircleBorder(), padding=33),
                            on_click=change_theme_green,
                        ),
                        ft.ElevatedButton(
                            style=ft.ButtonStyle(bgcolor=ft.colors.AMBER_300, shape=ft.CircleBorder(), padding=33),
                            on_click=change_theme_amber,
                        ),
                    ]
                ),
                ft.Row(
                    [
                        ft.ElevatedButton(
                            style=ft.ButtonStyle(bgcolor=ft.colors.PURPLE_300, shape=ft.CircleBorder(), padding=33),
                            on_click=change_theme_purple,
                        )
                    ]
                ),
                space2,
                ft.Text(S('Уравнения'), size=25, weight=ft.FontWeight.W_600),
                space2,
                ft.Checkbox(label=S('Число в ответе'), value=config['equations']['digits_in_result'], on_change=change_digits_in_result),
                space2,
                ft.Text(S("Сброс"), size=25, weight=ft.FontWeight.W_600),
                space2,
                ft.FilledTonalButton(S("Сбросить память"), on_click=reset_memory),
                space,
                ft.FilledTonalButton(S("Сбросить настройки"), on_click=reset_config),
                space,
                ft.FilledTonalButton(S("Сбросить всё"), on_click=reset_all),
            ]
        )
    )

    return 20
