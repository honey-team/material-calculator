import flet as ft

from pages.default import default
from pages.triangle import triangle
BUTTON_SIZE = 70
SIZE = 87

def app(page: ft.Page):
    page.window_height = SIZE * 6 + 60
    page.window_width = SIZE * 4
    page.window_resizable = False
    page.window_maximizable = False
    page.title = 'Material Calculator'
    
    def open_drawer(*_):
        page.drawer.open = True
        page.drawer.update()
    
    page.appbar = ft.AppBar(
        leading=ft.IconButton(ft.icons.MENU_ROUNDED, on_click=open_drawer)
    )
    
    def change_page(*_):
        page.controls.clear()
        match page.drawer.selected_index:
            case 0:
                default(page)
            case 1:
                triangle(page)
        page.update()
    
    page.drawer = ft.NavigationDrawer(
        controls=[
            ft.Container(height=12),
            ft.NavigationDrawerDestination(
                label="Обычный",
                icon=ft.icons.CALCULATE_OUTLINED,
                selected_icon=ft.icons.CALCULATE,
            ),
            ft.Divider(thickness=2),
            ft.NavigationDrawerDestination(
                label="Треугольник",
                icon_content=ft.Image(src='icons/triangle_outlined.png', width=25, height=25),
                selected_icon_content=ft.Image(src='icons/triangle.png', width=25, height=25)
            ),
            ft.NavigationDrawerDestination(
                icon_content=ft.Icon(ft.icons.PHONE_OUTLINED),
                label="Item 3",
                selected_icon=ft.icons.PHONE,
            ),
        ],
        on_change=change_page
    )

    default(page)
    page.update()

if __name__ == '__main__':
    ft.app(target=app, assets_dir="assets")
