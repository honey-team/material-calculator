from typing import Callable, Literal, TypeAlias
import flet as ft

from pages.utils.config import cload
from pages.utils.const import SupportsStr
from pages.utils.memory import mload, mwrite
from pages.utils.number import check_for_reg

BUTTON_SIZE = 70
SIZE = 87

OPERATION: TypeAlias = Literal['+', '-', '*', '/', '**']

def default(page: ft.Page):
    def generate_button(text: str, click: Callable[..., None], size: int = 20):
        return ft.FilledTonalButton(
            content=ft.Text(text, size=size),
            height=BUTTON_SIZE,
            width=BUTTON_SIZE, 
            on_click=click
        )
    
    def generate_0_button(text: str, click: Callable[..., None], size: int = 20):
        return ft.FilledTonalButton(
            content=ft.Text(text, size=size),
            height=BUTTON_SIZE,
            width=BUTTON_SIZE * 2 + 10,
            on_click=click
        )

    def get_color() -> str:
        colors = {
            "light": {
                "blue": "#39709c",
                "red": "#754349",
                "green": "#3f6b4f",
                "amber": "#8c7e3a",
                "purple": "#613e76",
            },
            "dark": {
                "blue": "#65aee9",
                "red": "#da8087",
                "green": "#85c796",
                "amber": "#f0d369",
                "purple": "#b576d0"
            }
        }

        c = cload()
        return colors[c["theme"]["mode"]][c["theme"]["bgcolor"]]

    def memory(query: SupportsStr):
        query = query.replace(',', '')
        m = mload()
        m["pages"]["default"]["query"] = query
        mwrite(m)
    
    def get_value() -> str:
        m = mload()
        return m["pages"]["default"]["query"]
    
    def add_sym(sym: str):
        unhighlight_operation_button()
        if get_value():
            if check_that_query_endswith_operation():
                query.value = check_for_reg(sym)
                memory(get_value() + sym)
            else:
                v = get_value()
                op: OPERATION
                if '+' in v:
                    op = '+'
                elif '-' in v:
                    op = '-'
                elif '/' in v:
                    op = '/'
                elif '**' in v:
                    op = '**'
                elif '*' in v:
                    op = '*'
                else:
                    r = get_value() + sym
                    memory(r)
                    query.value = check_for_reg(r)
                    page.update()
                    return
                query.value = check_for_reg(get_value().split(op, 1)[1] + sym)
                memory(get_value() + sym)
        else:
            r = sym
            memory(r)
            query.value = check_for_reg(r)
        page.update()
        
    def highlight_operation_button(op: OPERATION):
        btn: ft.FilledTonalButton
        match op:
            case '+': btn = btn_sum
            case '-': btn = btn_sub
            case '*': btn = btn_mul
            case '/': btn = btn_div
            case '**': btn = btn_pow
        
        dark = page.theme_mode == ft.ThemeMode.DARK
        btn.bgcolor = 'white' if dark else 'black'
        btn.color = 'black' if dark else 'white'
        btn.update()
    
    def unhighlight_operation_button():
        for i in [btn_sum, btn_sub, btn_mul, btn_div, btn_pow]:
            if i.bgcolor != 'secondaryContainer':
                i.bgcolor = 'secondaryContainer'
                i.color = 'onSecondaryContainer'
        page.update()
    
    def check_that_query_endswith_operation() -> bool:
        if (v := get_value()):
            return v[-1] in ['+', '-', '*', '/']
        return False
     
    def operation(op: OPERATION):
        if check_that_query_endswith_operation():
            unhighlight_operation_button()
            r = get_value()[:-1] + op
        else:
            r = get_value() + op
        highlight_operation_button(op)
        memory(r)
    
    def fun_ac(*_):
        unhighlight_operation_button()
        memory('')
        query.value = '0'
        page.update()
    
    def fun_pm(*_):
        if not check_that_query_endswith_operation():
            v = get_value()
            if v.startswith('-'):
                r = v[1:]
            else:
                r = f'-{v}'
            memory(r)
            query.value = check_for_reg(r)
            page.update()
    
    def fun_rem(*_):
        r = get_value()[:-1]
        memory(r)
        query.value = check_for_reg(r)
        page.update()
    
    def eq() -> str:
        try:
            if check_that_query_endswith_operation():
                return check_for_reg(query.value)
            v = get_value()
            if '+' in v or '-' in v or '*' in v or '/' in v:
                r = str(eval(v))
                
                if r and '.' in r:
                    r = str(round(float(r), 5))
                
                memory(r)
                return check_for_reg(r)
            return check_for_reg(query.value)
        except NameError:
            return check_for_reg(get_value())

    def fun_pow(*_):
        query.value = eq()
        page.update()
        operation('**')
    
    def fun_div(*_):
        query.value = eq()
        page.update()
        operation('/')
    
    def fun_7(*_):
        add_sym('7')
    
    def fun_8(*_):
        add_sym('8')
    
    def fun_9(*_):
        add_sym('9')
    
    def fun_mul(*_):
        query.value = eq()
        page.update()
        operation('*')
    
    def fun_4(*_):
        add_sym('4')
    
    def fun_5(*_):
        add_sym('5')
    
    def fun_6(*_):
        add_sym('6')
    
    def fun_sum(*_):
        query.value = eq()
        page.update()
        operation('+')
    
    def fun_1(*_):
        add_sym('1')
    
    def fun_2(*_):
        add_sym('2')
    
    def fun_3(*_):
        add_sym('3')
    
    def fun_sub(*_):
        query.value = eq()
        page.update()
        operation('-')
    
    def fun_0(*_):
        add_sym('0')

    def fun_po(*_):
        add_sym('.')
    
    def fun_eq(*_):
        r = eq()
        memory(r)
        query.value = check_for_reg(r)
        page.update()
    
    if check_that_query_endswith_operation():
        memory(get_value()[:-1])
    else:
        memory(get_value())
    
    query = ft.Text(
        check_for_reg(eq()),
        size=BUTTON_SIZE - 23,
        text_align=ft.TextAlign.RIGHT,
        color=get_color(),
        width=SIZE * 4,
        font_family="sf pro text",
    )
    
    btn_ac = generate_button("AC", fun_ac, size=17)
    btn_pm = generate_button("±", fun_pm)
    btn_pow = generate_button("^", fun_pow)
    btn_div = generate_button("÷", fun_div)

    btn_7 = generate_button("7", fun_7)
    btn_8 = generate_button("8", fun_8)
    btn_9 = generate_button("9", fun_9)
    btn_mul = generate_button("×", fun_mul)

    btn_4 = generate_button("4", fun_4)
    btn_5 = generate_button("5", fun_5)
    btn_6 = generate_button("6", fun_6)
    btn_sum = generate_button("+", fun_sum)

    btn_1 = generate_button("1", fun_1)
    btn_2 = generate_button("2", fun_2)
    btn_3 = generate_button("3", fun_3)
    btn_sub = generate_button("-", fun_sub)

    btn_0 = generate_0_button("0", fun_0)
    btn_po = generate_button(".", fun_po)
    btn_eq = generate_button("=", fun_eq)
    
    def on_keyboard(e: ft.KeyboardEvent):
        match e.key:
            case "Delete":
                fun_ac()
            case "Backspace":
                fun_rem()
            case "^":
                fun_pow()
            case "/" | "Numpad Divide":
                fun_div()
            case "1" | "Numpad 1":
                fun_1()
            case "2" | "Numpad 2":
                fun_2()
            case "3" | "Numpad 3":
                fun_3()
            case "*" | "Numpad Multiply":
                fun_mul()
            case "4" | "Numpad 4":
                fun_4()
            case "5" | "Numpad 5":
                fun_5()
            case "6" | "Numpad 6":
                fun_6()
            case "+" | "Numpad Add":
                fun_sum()
            case "7" | "Numpad 7":
                fun_7()
            case "8" | "Numpad 8":
                fun_8()
            case "9" | "Numpad 9":
                fun_9()
            case "-" | "Numpad Subtract":
                fun_sub()
            case "0" | "Numpad 0":
                fun_0()
            case "." | "Numpad Decimal":
                fun_po()
            case "=" | "Enter":
                fun_eq()

    page.on_keyboard_event = on_keyboard
    page.update()
    
    page.add(
        query,
        ft.Row([btn_ac, btn_pm, btn_pow, btn_div]),
        ft.Row([btn_7, btn_8, btn_9, btn_mul]),
        ft.Row([btn_4, btn_5, btn_6, btn_sum]),
        ft.Row([btn_1, btn_2, btn_3, btn_sub]),
        ft.Row([btn_0, btn_po, btn_eq]),
    )

    return 20
