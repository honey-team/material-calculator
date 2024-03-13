import flet as ft

from pages.utils.number import Number, get_up
from pages.utils.memory import mload, mwrite

def radical(page: ft.Page):
    def on_change(*_):
        m = mload()
        m['pages']['radical']['n'] = n.value
        m['pages']['radical']['a'] = a.value
        mwrite(m)

        try:
            num = Number(a.value)
            _pow = 1 / Number(n.value)
            num = num ** _pow
        except ZeroDivisionError:
            num = None
            
        txt.value = TXT.format(n=get_up(Number(n.value)), a=Number(a.value), r=Number(num) if num else '?')
        page.update()
    
    m = mload()
    
    TXT = '{n}√{a} = {r}'
    
    
    n = ft.TextField(value=m['pages']['radical']['n'], label='n', input_filter=ft.InputFilter(allow=True, regex_string=r"[0-9.-]", replacement_string=""), on_change=on_change)
    a = ft.TextField(value=m['pages']['radical']['a'], label='a', input_filter=ft.InputFilter(allow=True, regex_string=r"[0-9.-]", replacement_string=""), on_change=on_change)
    
    try:
        num = Number(a.value)
        _pow = 1 / Number(n.value)
        num = num ** _pow
    except ZeroDivisionError:
        num = None
    
    txt = ft.Text(TXT.format(n=get_up(Number(n.value)), a=Number(a.value), r=Number(num) if num else '?'), size=25)
    
    
    page.update()
    
    page.add(txt, ft.Container(height=40), n, a)
    
    return 'Корень', 20