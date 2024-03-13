import flet as ft


from pages.default import default
from pages.log import log
from pages.radical import radical
from pages.quadratic import quadratic
from pages.degrad import degrad
from pages.right_triangle import right_triangle
from pages.trigonometry import trigonometry
from pages.circle import circle
from pages.utils.memory import mload, mwrite
from pages.utils.config import cload
from pages.conv_gen import conv_gen
from pages.settings import settings

from pages.converters.weight import weight
from pages.converters.length import length
from pages.converters.square import square
from pages.converters.volume import volume
from pages.converters.temperature import temperature

BUTTON_SIZE = 70
SIZE = 87

CONVERTERS = [weight, length, square, volume, temperature]

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
        
        page.drawer.open = False
        
        page.drawer.update()
        page.appbar.update()
        
        page.controls.clear()
        
        l, s = 'error', 20
        
        FUNCTIONS = [default, radical, log, quadratic, degrad, right_triangle, trigonometry, circle]
        FUNCTIONS_INDEXES = [0, 7]
        
        if page.drawer.selected_index in list(range(FUNCTIONS_INDEXES[0], FUNCTIONS_INDEXES[1] + 1)):
            l, s = FUNCTIONS[page.drawer.selected_index](page)
        
        CONVERTERS_INDEXES = [FUNCTIONS_INDEXES[1] + 1, 12]
        
        if page.drawer.selected_index in list(range(CONVERTERS_INDEXES[0], CONVERTERS_INDEXES[1] + 1)):
            l, s = conv_gen(page, CONVERTERS[page.drawer.selected_index - CONVERTERS_INDEXES[0]])
        
        SETTINGS_INDEX = CONVERTERS_INDEXES[1] + 1
        if page.drawer.selected_index == SETTINGS_INDEX:
            l, s = settings(page)
            page.scroll = ft.ScrollMode.AUTO
        else:
            page.scroll = None

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
    
    def get_image_with_thememode(x: str):
        c = cload()
        if c['theme']['mode'] == 'light':
            return x
        else:
            x = x.replace('.png', '')
            return x + '_w.png'
    
    def Destination(label: str, icon: str, selected_icon: str = None):
        if selected_icon:
            return ft.NavigationDrawerDestination(
                    label=label,
                    icon_content=ft.Image(src=get_image_with_thememode(f'icons/{icon}.png'), width=25, height=25),
                    selected_icon_content=ft.Image(src=get_image_with_thememode(f'icons/{selected_icon}.png'), width=25, height=25)
                )
        else:
            return ft.NavigationDrawerDestination(
                    label=label,
                    icon_content=ft.Image(src=get_image_with_thememode(f'icons/{icon}.png'), width=25, height=25)
                )
    
    page.drawer = ft.NavigationDrawer(
        controls=[
            ft.Container(height=12),
            
            DividerText('Калькуляторы', False),
            
            ft.NavigationDrawerDestination(
                label="Обычный",
                icon=ft.icons.CALCULATE_OUTLINED,
                selected_icon=ft.icons.CALCULATE,
            ),
            
            DividerText('Алгебра'),
            
            Destination('Корень', 'radical'),
            Destination('Логарифм', 'log'),
            Destination('Квадратное уравнение', 'quadratic'),
            
            DividerText('Геометрия'),
            
            Destination('Конвертер углов', 'angle_outlined', 'angle'),
            Destination('Прямоугольный треугольник', 'right_triangle_outlined', 'right_triangle'),
            Destination('Тригонометрия', 'angle_outlined', 'angle'),
            Destination('Окружность', 'circle_outlined', 'circle'),
            
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
                icon_content=ft.Image(src=get_image_with_thememode(image), width=25, height=25),
                selected_icon_content=ft.Image(src=get_image_with_thememode(sel_image), width=25, height=25)
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
