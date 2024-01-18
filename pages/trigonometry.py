import flet as ft

def trigonometry(page: ft.Page):
    def change_dd(*_): ...
    deg = ft.TextField(label='Градусы', width=143)
    tdeg = ft.Dropdown(options=[
        ft.dropdown.Option('deg', 'градусы'),
        ft.dropdown.Option('rad', 'радианы')
    ], width=160)
    
    res_deg = ft.TextField(label='Результат')
    
    page.add(
        ft.Row([deg, tdeg]),
        ft.Dropdown(options=[
            ft.dropdown.Option('cos', 'Конинус (cos)'),
            ft.dropdown.Option('sin', 'Синус (sin)'),
            ft.dropdown.Option('tg', 'Тангенс (tg)'),
            ft.dropdown.Option('ctg', 'Котангенс (ctg)')
        ], on_change=change_dd),
        res_deg
    )
    
    return 'Тригонометрия (dev)', 20
