import flet as ft

def amf(page: ft.Page) -> tuple[str, int]:
    txt = ft.Text('AMF page')
    page.add(txt)
    
    return 'Сокращенное умножение', 20
