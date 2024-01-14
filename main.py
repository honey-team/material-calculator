import flet as ft


from pages.default import default
from pages.quadratic import quadratic
from pages.amf import amf
from pages.right_triangle import right_triangle
from pages.utils.memory import mload, mwrite
from pages.utils.config import cload
from pages.conv_gen import conv_gen
from pages.settings import settings

from pages.converters.weight import weight
from pages.converters.length import length
from pages.converters.square import square
from pages.converters.volume import volume

BUTTON_SIZE = 70
SIZE = 87

CONVERTERS = [weight, length, square, volume]

def app(page: ft.Page):
    config = cload()

    page.window_height = SIZE * 6 + 60
    page.window_width = SIZE * 4
    page.window_resizable = False
    page.window_maximizable = False
    page.title = config['name']
    page.theme = ft.Theme(config['theme']['bgcolor'])
    page.theme_mode = ft.ThemeMode.LIGHT if config['theme']['mode'] == 'light' else ft.ThemeMode.DARK
    
    def open_drawer(*_):
        page.drawer.open = True
        page.drawer.update()
    
    page.appbar = ft.AppBar(
        leading=ft.IconButton(ft.icons.MENU_ROUNDED, on_click=open_drawer),
        title=ft.Text('Обычный', max_lines=1)
    )
    
    def change_page(*_):
        controls = page.drawer.controls
        only_destinations = []
        
        for i in controls:
            if isinstance(i, ft.NavigationDrawerDestination):
                only_destinations.append(i)
        
        page.appbar.title.value = only_destinations[page.drawer.selected_index].label
        
        page.drawer.open = False
        
        page.drawer.update()
        page.appbar.update()
        
        page.controls.clear()
        match page.drawer.selected_index:
            case 0:
                page.scroll = None
                l, s = default(page)
            case 1:
                page.scroll = None
                l, s = quadratic(page)
            case 2:
                page.scroll = None
                l, s = amf(page)
            case 3:
                page.scroll = None
                l, s = right_triangle(page)
            case 4:
                page.scroll = None
                l, s = conv_gen(page, weight)
            case 5:
                page.scroll = None
                l, s = conv_gen(page, length)
            case 6:
                page.scroll = None
                l, s = conv_gen(page, square)
            case 7:
                page.scroll = None
                l, s = conv_gen(page, volume)
            case 8:
                page.scroll = ft.ScrollMode.AUTO
                l, s = settings(page)
        page.appbar.title.value = l        
        page.appbar.title.size = s        
        
        page.update()
        
        m = mload()
        m['page'] = page.drawer.selected_index
        mwrite(m)
    
    m = mload()
    
    def DividerText(label: str, with_divider: bool = True) -> ft.Text:
        div_text = ft.Row([
            ft.Container(width=20),
            ft.Text(label, size=17, weight=ft.FontWeight.W_600)
        ])
        space = ft.Container(height=10)
        if with_divider:
            return ft.Column(spacing=0, controls=[
                space,
                ft.Divider(thickness=2),
                space,
                div_text,
                space,
            ])
        return ft.Column(spacing=0, controls=[
            div_text,
            space
        ])
    
    page.drawer = ft.NavigationDrawer(
        controls=[
            ft.Container(height=12),
            DividerText('Калькуляторы', False),
            ft.NavigationDrawerDestination(
                label="Обычный",
                icon=ft.icons.CALCULATE_OUTLINED,
                selected_icon=ft.icons.CALCULATE,
            ),
            
            DividerText('Уравнения'),
            ft.NavigationDrawerDestination(
                label="Квадратное уравнение",
                icon_content=ft.Image(src='icons/quadratic.png', width=25, height=25)
            ),
            
            DividerText('Алгебра'),
            ft.NavigationDrawerDestination(
                label="Сокращенное уравнение (DEV)",
                icon_content=ft.Image(src='icons/amf.png', width=25, height=25)
            ),
            
            DividerText('Геометрия'),
            ft.NavigationDrawerDestination(
                label="Прямоугольный треугольник",
                icon_content=ft.Image(src='icons/right_triangle_outlined.png', width=25, height=25),
                selected_icon_content=ft.Image(src='icons/right_triangle.png', width=25, height=25)
            ),
            DividerText('Конвертеры'),
        ],
        on_change=change_page,
        selected_index=m['page']
    )
    page.update()
    
    for i in CONVERTERS:
        info = i()
        name, image, sel_image = info['name'], info['image'], info['sel_image']
        
        page.drawer.controls.append(
            ft.NavigationDrawerDestination(
                label=name,
                icon_content=ft.Image(src=image, width=25, height=25),
                selected_icon_content=ft.Image(src=sel_image, width=25, height=25)
            )
        )
    page.drawer.controls.append(ft.Container(height=50))
    page.drawer.controls.append(
        ft.NavigationDrawerDestination(
                label='Настройки',
                icon=ft.icons.SETTINGS_OUTLINED,
                selected_icon=ft.icons.SETTINGS
            )
    )
    page.drawer.controls.append(ft.Container(height=25))

    change_page()
    page.update()

if __name__ == '__main__':
    ft.app(target=app, assets_dir="assets")
