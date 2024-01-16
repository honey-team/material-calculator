import flet as ft
import json


from pages.utils.memory import mwrite
from pages.utils.config import cload, cwrite

def settings(page: ft.Page):
    config = cload()
    
    def _change_page_theme():
        config = cload()
        page.theme = ft.Theme(config['theme']['bgcolor'])
        page.update()
    
    def _change_config_theme(bgcolor: str):
        config = cload()
        config['theme']['bgcolor'] = bgcolor
        cwrite(config)
        
        _change_page_theme()
    
    def change_theme_blue(*_): _change_config_theme('blue')
    def change_theme_red(*_): _change_config_theme('red')
    def change_theme_green(*_): _change_config_theme('green')
    def change_theme_amber(*_): _change_config_theme('amber')
    def change_theme_purple(*_): _change_config_theme('purple')
    
    def change_theme_mode(*_):
        config = cload()
        if theme_mode.value:
            page.theme_mode = ft.ThemeMode.DARK
            config['theme']['mode'] = 'dark'
            theme_mode.label = 'Тёмная тема'
        else:
            page.theme_mode = ft.ThemeMode.LIGHT
            config['theme']['mode'] = 'light'
            theme_mode.label = 'Светлая тема'
        cwrite(config)
        
        for i in page.drawer.controls:
            if isinstance(i, ft.NavigationDrawerDestination):
                if i.selected_icon_content:
                    if '_w' in i.selected_icon_content.src:
                        i.selected_icon_content.src = i.selected_icon_content.src.replace('_w', '')
                    else:
                        x = i.selected_icon_content.src.replace('.png', '')
                        i.selected_icon_content.src = x + '_w.png'
                if i.icon_content:
                    if '_w' in i.icon_content.src:
                        i.icon_content.src = i.icon_content.src.replace('_w', '')
                    else:
                        x = i.icon_content.src.replace('.png', '')
                        i.icon_content.src = x + '_w.png'
        
        page.update()
    
    def reset_memory(*_):
        with open('default_memory.json', 'r', encoding='utf-8') as MemoryFile:
            rawJson = MemoryFile.read()
        m = json.loads(rawJson)
        mwrite(m)
    
    def reset_config(*_):
        with open('default_config.json', 'r', encoding='utf-8') as ConfigFile:
            rawJson = ConfigFile.read()
        c = json.loads(rawJson)
        cwrite(c)
        _change_page_theme()
        theme_mode.value = False
        change_theme_mode()
    
    def reset_all(*_):
        reset_memory()
        reset_config()
    
    space = ft.Container(height=10)
    space2 = ft.Container(height=20)
    
    ctm = config['theme']['mode']
    theme_mode = ft.Switch(label='Светлая тема' if ctm == 'light' else 'Тёмная тема', value=ctm == 'dark', on_change=change_theme_mode)

    page.add(ft.ListView([
        ft.Text(config['name'], size=35),
        ft.Text(config['version'], size=20),
        
        space2, ft.Text('Темы', size=25, weight=ft.FontWeight.W_600), space2,
        theme_mode,
        ft.Row([
            ft.ElevatedButton(style=ft.ButtonStyle(bgcolor=ft.colors.BLUE_300, shape=ft.CircleBorder(), padding=33), on_click=change_theme_blue),
            ft.ElevatedButton(style=ft.ButtonStyle(bgcolor=ft.colors.RED_300, shape=ft.CircleBorder(), padding=33), on_click=change_theme_red),
            ft.ElevatedButton(style=ft.ButtonStyle(bgcolor=ft.colors.GREEN_300, shape=ft.CircleBorder(), padding=33), on_click=change_theme_green),
            ft.ElevatedButton(style=ft.ButtonStyle(bgcolor=ft.colors.AMBER_300, shape=ft.CircleBorder(), padding=33), on_click=change_theme_amber)
        ]),
        ft.Row([
            ft.ElevatedButton(style=ft.ButtonStyle(bgcolor=ft.colors.PURPLE_300, shape=ft.CircleBorder(), padding=33), on_click=change_theme_purple)
        ]),
        
        space2, ft.Text('Сброс', size=25, weight=ft.FontWeight.W_600), space2,
        ft.FilledTonalButton('Сбросить память', on_click=reset_memory), space,
        ft.FilledTonalButton('Сбросить настройки', on_click=reset_config), space,
        ft.FilledTonalButton('Сбросить всё', on_click=reset_all)
    ]))
    
    return 'Настройки', 20