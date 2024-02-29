import flet as ft

from pages.utils.number import Number
from pages.utils.memory import mload, mwrite

def radical(page: ft.Page):
    def on_change(*_):
        m = mload()
        m['pages']['radical']['n'] = n.value
        m['pages']['radical']['a'] = a.value
        mwrite(m)

        num = Number(a.value)
        _pow = 1 / Number(n.value)
        num = num ** _pow
        txt.value = f'ⁿ√a = {num}'
        page.update()
    
    m = mload()
    
    txt = ft.Text('ⁿ√a = 0', size=25)
    n = ft.TextField(value=m['pages']['radical']['n'], label='n', input_filter=ft.InputFilter(allow=True, regex_string=r"[0-9.-]", replacement_string=""), on_change=on_change)
    a = ft.TextField(value=m['pages']['radical']['a'], label='a', input_filter=ft.InputFilter(allow=True, regex_string=r"[0-9.-]", replacement_string=""), on_change=on_change)
    
    num = Number(a.value)
    _pow = 1 / Number(n.value)
    num = num ** _pow
    txt.value = f'ⁿ√a = {num}'
    page.update()
    
    page.add(txt, ft.Container(height=40), n, a)
    
    return 'Корень', 20